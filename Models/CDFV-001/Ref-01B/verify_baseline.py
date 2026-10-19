#!/usr/bin/env python3
r"""Verify the CDFV-001 Ref-01B computational baseline.

This verifier uses only the Python standard library.  It checks the result
files that are available and performs physics checks when the corresponding
columns can be identified.  Missing or unrecognised columns are reported as
PARTIAL rather than silently guessed.

Determinism contract (see the RO-CDFV-001-Ref-01B review report, findings F2
and F7):

* every path written into ``verification.json`` and ``verification_report.md``
  is repository-relative and POSIX-style, so both files are byte-identical on
  Windows and on Ubuntu;
* no wall-clock timestamp is written into the frozen artifacts.  Operational
  metadata (time, platform, interpreter) goes to a separate
  ``local_run_meta.json`` which is git-ignored and is never hashed by the
  Research Object.

Exit codes:

* 0 - every performed check passed;
* 1 - at least one check failed;
* 2 - the results directory or its data files could not be read.

Run from anywhere inside the repository, for example:

    py -3 .\Models\CDFV-001\Ref-01B\verify_baseline.py

By default the script verifies the ``results`` directory next to itself and
writes ``verification.json``, ``verification_report.md`` and
``local_run_meta.json`` into the directory it verified.  Another directory can
be given positionally or with ``--results-dir``.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import platform
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Sequence

# Reference configuration from P002 / CDFV-001 Ref-01B.
MASS_KG = 2.030
DIAMETER_M = 0.090
LENGTH_M = 0.323
WATER_DENSITY_KG_M3 = 1000.0
GRAVITY_M_S2 = 9.80665
FREE_SURFACE_FORCE_N = 0.0
FORCE_TOLERANCE_N = 1e-4

WEIGHT_N = MASS_KG * GRAVITY_M_S2
DISPLACED_VOLUME_M3 = math.pi * (DIAMETER_M / 2.0) ** 2 * LENGTH_M
FULL_BUOYANCY_N = WATER_DENSITY_KG_M3 * GRAVITY_M_S2 * DISPLACED_VOLUME_M3

CHECKS_VERSION = "0.2"
SUMMARY_FILE_NAME = "summary.csv"
META_FILE_NAME = "local_run_meta.json"

# A unit error is normally a factor of 1e-3 or larger; this tolerance only
# absorbs floating-point formatting noise when comparing the weight column.
UNIT_SANITY_REL_TOL = 1e-6

# Exact (normalised) matches are always allowed.  The substring fallback is
# only applied to aliases of at least this many characters, so that short
# aliases such as "t" or "z" cannot claim unrelated long headers like
# "net_hydrostatic_force_N".
MIN_FUZZY_ALIAS_LENGTH = 3


ALIASES: dict[str, tuple[str, ...]] = {
    "time": ("time_s", "time", "t_s", "t"),
    "position": (
        "z_center_m",
        "z_m",
        "z",
        "position_m",
        "vertical_position_m",
        "vertical_position",
        "height_m",
    ),
    "speed": ("velocity_m_s", "speed_mps", "velocity_mps", "v_mps", "speed", "velocity"),
    "acceleration": ("acceleration_m_s2", "acceleration_mps2", "acceleration"),
    "buoyancy": (
        "buoyancy_n",
        "buoyancy_force_n",
        "buoyancy",
        "hydrostatic_force_n",
    ),
    "weight": ("weight_n", "weight", "gravity_force_n", "gravity_n"),
    "constraint": (
        "constraint_force_n",
        "constraint_n",
        "actuator_force_n",
        "external_force_n",
    ),
    "free_surface": ("free_surface_force_n", "free_surface_n", "f_fs_n"),
}


def normalise_header(value: str) -> str:
    """Make a CSV header comparable across harmless spelling differences."""

    value = value.strip().lower().replace("μ", "u")
    return re.sub(r"[^a-z0-9]+", "_", value).strip("_")


def alias_keys(aliases: Sequence[str]) -> list[str]:
    return [key for key in (normalise_header(alias) for alias in aliases) if key]


def fuzzy_alias_keys(aliases: Sequence[str]) -> list[str]:
    """Alias keys eligible for the substring fallback."""

    return [key for key in alias_keys(aliases) if len(key) >= MIN_FUZZY_ALIAS_LENGTH]


def find_column(
    headers: Sequence[str], aliases: Sequence[str]
) -> tuple[str | None, str | None]:
    """Return ``(column, note)`` for one logical column.

    Only an exact normalised match is accepted silently.  The substring
    fallback exists for headers such as ``force_constraint_N``, but a fuzzy
    match is always returned with a note so the caller can report it as a
    failure: frozen baseline results must use their declared column names, and a
    guessed column is exactly the silent substitution this verifier must not
    perform.  Two or more fuzzy candidates are refused outright.
    """

    original = list(headers)
    normalised = {normalise_header(header): header for header in original}

    for key in alias_keys(aliases):
        if key in normalised:
            return normalised[key], None

    keys = fuzzy_alias_keys(aliases)
    candidates: list[str] = []
    for header in original:
        key = normalise_header(header)
        if any(alias_key in key or key in alias_key for alias_key in keys):
            candidates.append(header)

    if not candidates:
        return None, None
    if len(candidates) > 1:
        return None, (
            "ambiguous fuzzy header match; candidates="
            f"{sorted(candidates)}; use an exact declared column name"
        )
    return candidates[0], (
        f"fuzzy header match on '{candidates[0]}'; use an exact declared "
        "column name"
    )


def as_float(value: Any) -> float | None:
    if value is None:
        return None
    text = str(value).strip()
    if not text:
        return None
    try:
        number = float(text)
    except ValueError:
        return None
    return number if math.isfinite(number) else None


def check_result(label: str, status: str, detail: str) -> dict[str, str]:
    return {"label": label, "status": status, "detail": detail}


def monotonic_direction(values: list[float], tolerance: float = 1e-12) -> str | None:
    if len(values) < 2:
        return "constant"
    increasing = all(b >= a - tolerance for a, b in zip(values, values[1:]))
    decreasing = all(b <= a + tolerance for a, b in zip(values, values[1:]))
    if increasing:
        return "increasing"
    if decreasing:
        return "decreasing"
    return None


def load_rows(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        headers = [
            header.strip()
            for header in (reader.fieldnames or [])
            if header is not None
        ]
        rows = list(reader)
    return headers, rows


def repository_root(script_path: Path) -> Path:
    """Return the repository root, or the model directory when not in a repo."""

    current = script_path.resolve().parent
    for candidate in (current, *current.parents):
        if (candidate / ".git").exists():
            return candidate
    return current


def to_posix_relative(path: Path, repo_root: Path) -> str:
    """Return a repository-relative POSIX path, or a stable fallback.

    The result is written into verification.json, which is hash-registered, so it
    must not depend on where the tree happens to be checked out.  Two cases are
    therefore treated as "cannot express relatively, use a stable fallback":

    * the path is outside the repository root (``relative_to`` raises);
    * the computed relative path escapes the root with ``..``, which happens when
      the root could not be located -- for example in an exported tree that has no
      ``.git`` directory, where ``repository_root`` falls back to the model
      directory and the results directory then appears to sit above it.

    Returning the bare directory name keeps the recorded artifact byte-identical
    across machines, which is what the hash registry depends on.
    """

    resolved = path.resolve()
    try:
        relative = resolved.relative_to(repo_root.resolve())
    except ValueError:
        return resolved.name
    if any(part == ".." for part in relative.parts):
        return resolved.name
    return relative.as_posix()


def verify_data_file(
    path: Path, tolerance_n: float, mass_kg: float = 0.0
) -> dict[str, Any]:
    checks: list[dict[str, str]] = []
    try:
        headers, rows = load_rows(path)
    except Exception as exc:  # pragma: no cover - diagnostic path
        return {
            "file": path.name,
            "status": "FAIL",
            "rows": 0,
            "headers": [],
            "columns": {},
            "checks": [check_result("read_csv", "FAIL", str(exc))],
        }

    checks.append(
        check_result(
            "read_csv",
            "PASS" if headers else "FAIL",
            f"{len(headers)} columns, {len(rows)} data rows",
        )
    )

    columns: dict[str, str | None] = {}
    for name, aliases in ALIASES.items():
        column, note = find_column(headers, aliases)
        columns[name] = column
        if note is not None:
            # A fuzzy match is never accepted silently: frozen results must use
            # their declared column names, so a guess is reported as a failure.
            checks.append(
                check_result(
                    f"column_match_{name}",
                    "FAIL",
                    f"{note}; available headers: {headers}",
                )
            )

    duplicates = sorted({header for header in headers if headers.count(header) > 1})
    if duplicates:
        checks.append(
            check_result("duplicate_headers", "FAIL", f"duplicate headers: {duplicates}")
        )

    if not rows:
        checks.append(check_result("non_empty", "FAIL", "No data rows found"))
    else:
        checks.append(check_result("non_empty", "PASS", f"{len(rows)} rows"))

    numeric_values: dict[str, list[float]] = {}
    for logical_name in ALIASES:
        column = columns.get(logical_name)
        if column is None:
            # A required column that cannot be identified is a hard failure: the
            # corresponding physics check cannot be performed at all, and a
            # silent SKIP would let a damaged file look acceptable.
            checks.append(
                check_result(
                    f"column_{logical_name}",
                    "FAIL",
                    f"required column not recognised; available headers: {headers}",
                )
            )
            continue
        values = [as_float(row.get(column)) for row in rows]
        missing = sum(value is None for value in values)
        numeric_values[logical_name] = [value for value in values if value is not None]
        checks.append(
            check_result(
                f"numeric_{logical_name}",
                "PASS" if missing == 0 else "FAIL",
                f"column={column}; missing_or_non_numeric={missing}",
            )
        )

    for logical_name in ("time", "position", "speed"):
        values = numeric_values.get(logical_name)
        if values is None:
            continue
        direction = monotonic_direction(values)
        checks.append(
            check_result(
                f"monotonic_{logical_name}",
                "PASS" if direction is not None else "FAIL",
                direction or "non-monotonic",
            )
        )

    # Reference-value checks, performed only when matching columns exist.
    weights = numeric_values.get("weight")
    if weights:
        max_error = max(abs(value - WEIGHT_N) for value in weights)
        checks.append(
            check_result(
                "weight_reference",
                "PASS" if max_error <= tolerance_n else "FAIL",
                f"max_error={max_error:.9g} N; expected={WEIGHT_N:.9g} N",
            )
        )

    buoyancies = numeric_values.get("buoyancy")
    if buoyancies:
        lower = min(buoyancies)
        upper = max(buoyancies)
        in_range = lower >= -tolerance_n and upper <= FULL_BUOYANCY_N + tolerance_n
        checks.append(
            check_result(
                "buoyancy_range",
                "PASS" if in_range else "FAIL",
                f"range=[{lower:.9g}, {upper:.9g}] N; "
                f"expected=[0, {FULL_BUOYANCY_N:.9g}] N",
            )
        )

    free_surface = numeric_values.get("free_surface")
    if free_surface:
        max_error = max(abs(value - FREE_SURFACE_FORCE_N) for value in free_surface)
        checks.append(
            check_result(
                "free_surface_zero",
                "PASS" if max_error <= tolerance_n else "FAIL",
                f"max_error={max_error:.9g} N; expected={FREE_SURFACE_FORCE_N} N "
                "(excluded from the baseline)",
            )
        )

    accelerations = numeric_values.get("acceleration")
    if accelerations:
        # The original baseline prescribes constant velocity, so a == 0 was itself
        # an assertion.  Once accelerated cases exist that assertion is wrong in
        # general, so it is now reported rather than enforced: the check records
        # which motion type the case is, and only a constant-velocity case is held
        # to a == 0.
        max_acceleration = max(abs(value) for value in accelerations)
        is_constant_velocity = max_acceleration <= tolerance_n
        checks.append(
            check_result(
                "motion_type",
                "PASS",
                (
                    "constant velocity (a = 0), so the acceleration term vanishes"
                    if is_constant_velocity
                    else f"accelerated (max|a| = {max_acceleration:.9g} m/s^2), "
                    "so m*a must appear in the balance"
                ),
            )
        )

    buoyancy = numeric_values.get("buoyancy")
    weight = numeric_values.get("weight")
    constraint = numeric_values.get("constraint")
    acceleration = numeric_values.get("acceleration")
    if (
        buoyancy
        and weight
        and constraint
        and len(buoyancy) == len(weight) == len(constraint)
    ):
        # The balance is m*a = F_constraint + F_buoyancy - F_weight, so the residual
        # must carry the inertial term.  Checking c + b - w alone is correct only
        # while a == 0, which is exactly the assumption this repository used to
        # make; with an accelerated case the omitted term is m*a, i.e. 2.03 N at
        # a = 1 m/s^2, which is the same size as the load being studied.
        mass_kg = mass_kg if mass_kg else MASS_KG
        if acceleration and len(acceleration) == len(constraint):
            inertial = [mass_kg * a for a in acceleration]
        else:
            inertial = [0.0] * len(constraint)
        residuals = [
            c + b - w - i for c, b, w, i in zip(constraint, buoyancy, weight, inertial)
        ]
        max_residual = max(abs(value) for value in residuals)
        checks.append(
            check_result(
                "force_balance",
                "PASS" if max_residual <= tolerance_n else "FAIL",
                f"max_abs(constraint + buoyancy - weight - mass*acceleration)"
                f"={max_residual:.9g} N",
            )
        )
    else:
        checks.append(
            check_result(
                "force_balance",
                "SKIP",
                "Need recognised buoyancy, weight, and constraint columns "
                "of equal length",
            )
        )

    # Unit sanity: a column expressed in kN or mN instead of N is caught here
    # explicitly, in both directions.  The lower bound is guarded so that a
    # verifier run with a deliberately widened tolerance still makes sense.
    if buoyancies:
        upper = max(buoyancies)
        margin = min(0.5 * FULL_BUOYANCY_N, max(tolerance_n, 1e-9))
        tolerance_ratio = margin / FULL_BUOYANCY_N if FULL_BUOYANCY_N else 0.0
        ok = (
            upper <= FULL_BUOYANCY_N * (1.0 + tolerance_ratio)
            and upper >= FULL_BUOYANCY_N * (1.0 - tolerance_ratio)
        )
        checks.append(
            check_result(
                "buoyancy_unit_sanity",
                "PASS" if ok else "FAIL",
                f"max(buoyancy)={upper:.9g} N vs full_submergence="
                f"{FULL_BUOYANCY_N:.9g} N; a unit error (kN or mN written as N) "
                "changes this ratio by orders of magnitude",
            )
        )

    if weights:
        ratio = max(weights) / WEIGHT_N if WEIGHT_N else 0.0
        checks.append(
            check_result(
                "weight_unit_sanity",
                "PASS" if abs(ratio - 1.0) <= UNIT_SANITY_REL_TOL else "FAIL",
                f"max(weight)/reference_weight={ratio:.9g}; expected 1",
            )
        )

    failed = [item for item in checks if item["status"] == "FAIL"]
    skipped = [item for item in checks if item["status"] == "SKIP"]
    status = "FAIL" if failed else ("PARTIAL" if skipped else "PASS")
    return {
        "file": path.name,
        "status": status,
        "rows": len(rows),
        "headers": headers,
        "columns": columns,
        "checks": checks,
    }


def render_report(report: dict[str, Any]) -> str:
    lines = [
        "# Ref-01B Baseline Verification",
        "",
        f"- Overall status: **{report['overall_status']}**",
        f"- Verified results: `{report['results_directory']}`",
        f"- Checks version: `{report['checks_version']}`",
        "- Generated by: `Models/CDFV-001/Ref-01B/verify_baseline.py`",
        "",
        "## Reference configuration",
        "",
        f"- Mass: `{MASS_KG} kg`",
        f"- Cylinder: `{DIAMETER_M} m × {LENGTH_M} m`",
        f"- Water density: `{WATER_DENSITY_KG_M3} kg/m^3`",
        f"- Gravity: `{GRAVITY_M_S2} m/s^2`",
        f"- Weight: `{WEIGHT_N:.9g} N`",
        f"- Full-submerged buoyancy: `{FULL_BUOYANCY_N:.9g} N`",
        f"- Force-balance tolerance: `{report['tolerance_n']} N`",
        f"- Free-surface force: `{FREE_SURFACE_FORCE_N} N` (excluded by definition)",
        "",
        "## File checks",
        "",
        "| File | Rows | Status |",
        "|---|---:|---|",
    ]
    for item in report["files"]:
        lines.append(f"| `{item['file']}` | {item['rows']} | **{item['status']}** |")

    for item in report["files"]:
        lines.extend(["", f"## `{item['file']}`", ""])
        lines.append("| Check | Status | Detail |")
        lines.append("|---|---|---|")
        for check in item["checks"]:
            detail = check["detail"].replace("|", "\\|")
            lines.append(f"| {check['label']} | **{check['status']}** | {detail} |")
        lines.extend(
            [
                "",
                "Recognised columns:",
                "",
                "```json",
                json.dumps(item["columns"], indent=2),
                "```",
            ]
        )

    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "`PASS` means the available check passed. `FAIL` means a check failed "
            "or a required column could not be identified, so the file cannot be "
            "treated as verified. `SKIP` is only used for checks whose inputs are "
            "legitimately absent; it never hides a missing required column.",
            "",
            "This computational baseline excludes free-surface force, drag, and "
            "added mass. Passing these checks does not constitute experimental "
            "validation.",
            "",
            "This report is deterministic: it contains no timestamp and no "
            "machine-specific path. Operational metadata is written separately to "
            "`local_run_meta.json`, which is git-ignored and never hashed.",
            "",
        ]
    )
    return "\n".join(lines)


def write_text_lf(path: Path, text: str) -> None:
    """Write UTF-8 with LF terminators regardless of platform.

    ``Path.write_text`` emits CRLF on Windows, which would make the frozen
    verification artifacts differ between Windows and Ubuntu.
    """

    with path.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write(text)


def write_meta(path: Path, results_relative: str, data_files: Sequence[Path]) -> None:
    """Write non-frozen operational metadata (git-ignored, never hashed)."""

    payload = {
        "note": (
            "Local operational metadata. Not part of the frozen research record; "
            "git-ignored and never hashed by the Research Object."
        ),
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "python_version": sys.version.split()[0],
        "platform": platform.platform(),
        "verified_results": results_relative,
        "verified_files": [path.name for path in data_files],
    }
    write_text_lf(path, json.dumps(payload, indent=2) + "\n")


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "results_dir_positional",
        nargs="?",
        type=Path,
        default=None,
        help="Directory containing the Ref-01B CSV files (default: ./results).",
    )
    parser.add_argument(
        "--results-dir",
        type=Path,
        default=None,
        help="Directory containing the Ref-01B CSV files (default: ./results).",
    )
    parser.add_argument(
        "--tolerance-n",
        type=float,
        default=FORCE_TOLERANCE_N,
        help=f"Absolute force tolerance in newtons (default: {FORCE_TOLERANCE_N}).",
    )
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=None,
        help="Repository root used for relative paths (default: auto-detected).",
    )
    parser.add_argument(
        "--meta-out",
        type=Path,
        default=None,
        help=f"Path for local metadata (default: <results>/{META_FILE_NAME}).",
    )
    parser.add_argument(
        "--no-meta",
        action="store_true",
        help="Do not write local operational metadata at all.",
    )
    args = parser.parse_args(argv)

    if args.results_dir is not None and args.results_dir_positional is not None:
        parser.error(
            "give the results directory either positionally or with "
            "--results-dir, not both"
        )
    return args


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    script_path = Path(__file__).resolve()
    repo_root = (
        args.repo_root.resolve()
        if args.repo_root is not None
        else repository_root(script_path)
    )

    results_dir = (
        args.results_dir if args.results_dir is not None else args.results_dir_positional
    )
    if results_dir is None:
        results_dir = script_path.parent / "results"
    results_dir = results_dir.resolve()

    if not results_dir.is_dir():
        print(f"ERROR: results directory does not exist: {results_dir}", file=sys.stderr)
        return 2

    data_files = sorted(
        path
        for path in results_dir.glob("*.csv")
        if path.name.lower() != SUMMARY_FILE_NAME
    )
    if not data_files:
        print(f"ERROR: no data CSV files found in {results_dir}", file=sys.stderr)
        return 2

    files = [verify_data_file(path, args.tolerance_n) for path in data_files]
    statuses = {item["status"] for item in files}
    overall_status = (
        "FAIL" if "FAIL" in statuses else ("PARTIAL" if "PARTIAL" in statuses else "PASS")
    )

    report: dict[str, Any] = {
        "results_directory": to_posix_relative(results_dir, repo_root),
        "overall_status": overall_status,
        "checks_version": CHECKS_VERSION,
        "tolerance_n": args.tolerance_n,
        "reference": {
            "mass_kg": MASS_KG,
            "diameter_m": DIAMETER_M,
            "length_m": LENGTH_M,
            "water_density_kg_m3": WATER_DENSITY_KG_M3,
            "gravity_m_s2": GRAVITY_M_S2,
            "force_tolerance_n": FORCE_TOLERANCE_N,
            "free_surface_force_n": FREE_SURFACE_FORCE_N,
            "weight_n": WEIGHT_N,
            "displaced_volume_m3": DISPLACED_VOLUME_M3,
            "full_buoyancy_n": FULL_BUOYANCY_N,
        },
        "files": files,
    }

    json_path = results_dir / "verification.json"
    report_path = results_dir / "verification_report.md"
    write_text_lf(json_path, json.dumps(report, indent=2) + "\n")
    write_text_lf(report_path, render_report(report))

    if not args.no_meta:
        meta_path = (
            args.meta_out.resolve()
            if args.meta_out is not None
            else results_dir / META_FILE_NAME
        )
        write_meta(meta_path, report["results_directory"], data_files)

    print(f"Overall status: {overall_status}")
    for item in files:
        print(f"  {item['file']}: {item['status']} ({item['rows']} rows)")
    print(f"wrote {json_path}")
    print(f"wrote {report_path}")
    return 1 if overall_status == "FAIL" else 0


if __name__ == "__main__":
    raise SystemExit(main())
