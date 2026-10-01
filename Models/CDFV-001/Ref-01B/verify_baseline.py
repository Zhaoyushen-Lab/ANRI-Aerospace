#!/usr/bin/env python3
r"""Verify the CDFV-001 Ref-01B computational baseline.

This first version deliberately uses only the Python standard library.  It
checks the result files that are available and performs physics checks when
the corresponding columns can be identified.  Missing/unrecognised columns
are reported as PARTIAL rather than silently guessed.

Run from the repository root, for example:

    py -3 .\Models\CDFV-001\Ref-01B\verify_baseline.py

The script expects a ``results`` directory next to itself and writes
``verification.json`` and ``verification_report.md`` into that directory.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable


# Reference configuration from P002 / CDFV-001 Ref-01B.
MASS_KG = 2.030
DIAMETER_M = 0.090
LENGTH_M = 0.323
WATER_DENSITY_KG_M3 = 1000.0
GRAVITY_M_S2 = 9.80665

WEIGHT_N = MASS_KG * GRAVITY_M_S2
DISPLACED_VOLUME_M3 = math.pi * (DIAMETER_M / 2.0) ** 2 * LENGTH_M
FULL_BUOYANCY_N = WATER_DENSITY_KG_M3 * GRAVITY_M_S2 * DISPLACED_VOLUME_M3


ALIASES: dict[str, tuple[str, ...]] = {
    "time": ("time_s", "time", "t_s", "t"),
    "position": (
        "z_m",
        "z",
        "position_m",
        "vertical_position_m",
        "vertical_position",
        "height_m",
    ),
    "speed": ("speed_mps", "velocity_mps", "v_mps", "speed", "velocity"),
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
}


def normalise_header(value: str) -> str:
    """Make a CSV header comparable across harmless spelling differences."""

    value = value.strip().lower().replace("μ", "u")
    return re.sub(r"[^a-z0-9]+", "_", value).strip("_")


def find_column(headers: Iterable[str], aliases: Iterable[str]) -> str | None:
    """Return the original header matching one of the known aliases."""

    original = list(headers)
    normalised = {normalise_header(header): header for header in original}
    for alias in aliases:
        key = normalise_header(alias)
        if key in normalised:
            return normalised[key]

    # Conservative fallback for headers such as ``force_constraint_N``.
    for header in original:
        key = normalise_header(header)
        for alias in aliases:
            alias_key = normalise_header(alias)
            if alias_key and (alias_key in key or key in alias_key):
                return header
    return None


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
        headers = reader.fieldnames or []
        rows = list(reader)
    return headers, rows


def verify_data_file(path: Path, tolerance_n: float) -> dict[str, Any]:
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

    columns = {
        name: find_column(headers, aliases) for name, aliases in ALIASES.items()
    }

    if not rows:
        checks.append(check_result("non_empty", "FAIL", "No data rows found"))
    else:
        checks.append(check_result("non_empty", "PASS", f"{len(rows)} rows"))

    # Check numeric columns and, where available, their ordering.
    numeric_values: dict[str, list[float]] = {}
    for logical_name in ("time", "position", "speed", "buoyancy", "weight", "constraint"):
        column = columns[logical_name]
        if column is None:
            checks.append(
                check_result(
                    f"column_{logical_name}",
                    "SKIP",
                    f"No recognised column; available headers: {headers}",
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

    for logical_name in ("time", "position"):
        values = numeric_values.get(logical_name)
        if values is None:
            continue
        direction = monotonic_direction(values)
        checks.append(
            check_result(
                f"monotonic_{logical_name}",
                "PASS" if direction is not None else "FAIL",
                f"{direction or 'non-monotonic'}",
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
                f"range=[{lower:.9g}, {upper:.9g}] N; expected=[0, {FULL_BUOYANCY_N:.9g}] N",
            )
        )

    buoyancy = numeric_values.get("buoyancy")
    weight = numeric_values.get("weight")
    constraint = numeric_values.get("constraint")
    if buoyancy and weight and constraint and len(buoyancy) == len(weight) == len(constraint):
        residuals = [c + b - w for c, b, w in zip(constraint, buoyancy, weight)]
        max_residual = max(abs(value) for value in residuals)
        checks.append(
            check_result(
                "force_balance",
                "PASS" if max_residual <= tolerance_n else "FAIL",
                f"max_abs(constraint + buoyancy - weight)={max_residual:.9g} N",
            )
        )
    else:
        checks.append(
            check_result(
                "force_balance",
                "SKIP",
                "Need recognised buoyancy, weight, and constraint columns of equal length",
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
        f"- Generated (UTC): `{report['generated_utc']}`",
        f"- Overall status: **{report['overall_status']}**",
        f"- Results directory: `{report['results_directory']}`",
        "",
        "## Reference configuration",
        "",
        f"- Mass: `{MASS_KG} kg`",
        f"- Cylinder: `{DIAMETER_M} m × {LENGTH_M} m`",
        f"- Weight: `{WEIGHT_N:.9g} N`",
        f"- Full-submerged buoyancy: `{FULL_BUOYANCY_N:.9g} N`",
        f"- Force-balance tolerance: `{report['tolerance_n']} N`",
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
        lines.extend(["", "Recognised columns:", "", "```json", json.dumps(item["columns"], indent=2), "```"])

    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "`PASS` means the available check passed. `PARTIAL` means the file was readable but one or more checks could not be performed because the column was not recognised. `FAIL` requires investigation before treating the baseline as verified.",
            "",
            "This computational baseline excludes free-surface force, drag, and added mass. Passing these checks does not constitute experimental validation.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "results_dir",
        nargs="?",
        type=Path,
        default=Path(__file__).resolve().parent / "results",
        help="Directory containing the Ref-01B CSV files (default: ./results)",
    )
    parser.add_argument(
        "--tolerance-n",
        type=float,
        default=1e-4,
        help="Absolute force tolerance in newtons (default: 1e-4)",
    )
    args = parser.parse_args()
    results_dir = args.results_dir.resolve()

    if not results_dir.is_dir():
        print(f"ERROR: results directory does not exist: {results_dir}", file=sys.stderr)
        return 2

    data_files = sorted(
        path
        for path in results_dir.glob("*.csv")
        if path.name.lower() != "summary.csv"
    )
    if not data_files:
        print(f"ERROR: no data CSV files found in {results_dir}", file=sys.stderr)
        return 2

    files = [verify_data_file(path, args.tolerance_n) for path in data_files]
    statuses = {item["status"] for item in files}
    overall_status = "FAIL" if "FAIL" in statuses else ("PARTIAL" if "PARTIAL" in statuses else "PASS")
    report: dict[str, Any] = {
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "results_directory": str(results_dir),
        "overall_status": overall_status,
        "tolerance_n": args.tolerance_n,
        "reference": {
            "mass_kg": MASS_KG,
            "diameter_m": DIAMETER_M,
            "length_m": LENGTH_M,
            "water_density_kg_m3": WATER_DENSITY_KG_M3,
            "gravity_m_s2": GRAVITY_M_S2,
            "weight_n": WEIGHT_N,
            "displaced_volume_m3": DISPLACED_VOLUME_M3,
            "full_buoyancy_n": FULL_BUOYANCY_N,
        },
        "files": files,
    }

    json_path = results_dir / "verification.json"
    report_path = results_dir / "verification_report.md"
    json_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    report_path.write_text(render_report(report), encoding="utf-8")

    print(f"Overall status: {overall_status}")
    for item in files:
        print(f"  {item['file']}: {item['status']} ({item['rows']} rows)")
    print(f"wrote {json_path}")
    print(f"wrote {report_path}")
    return 1 if overall_status == "FAIL" else 0


if __name__ == "__main__":
    raise SystemExit(main())
