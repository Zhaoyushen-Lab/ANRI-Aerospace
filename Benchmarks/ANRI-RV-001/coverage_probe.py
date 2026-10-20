"""Measure which columns the verifier actually constrains.

The negative-case suite answers "does a known fault get caught". It cannot answer
"is there a wrong value that passes everything", because it only ever perturbs the
columns somebody thought of. This probe inverts the question: perturb EVERY column
of the clean baseline, one at a time, and record whether the verifier notices.

A column that survives perturbation is a blind spot - a value that can be wrong while
the gate stays green. That is the failure mode worth finding, and it is invisible to
any suite built from a list of anticipated faults.

Method
------
For each column, and for each perturbation kind, write a modified copy of the clean
0.25 m/s case, run verify_baseline.py against a directory containing only that file,
and record the exit code plus which checks failed.

Perturbation kinds
------------------
  row    one interior row scaled by (1 + delta)
  all    every row scaled by (1 + delta)

Columns holding identifiers are skipped.

Usage
-----
    py -3 .\\Benchmarks\\ANRI-RV-001\\coverage_probe.py
    py -3 .\\Benchmarks\\ANRI-RV-001\\coverage_probe.py --delta 0.01 --json out.json
"""

from __future__ import annotations

import argparse
import csv
import io
import json
import subprocess
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
VERIFIER = REPO / "Models/CDFV-001/Ref-01B/verify_baseline.py"
SOURCE = REPO / "Models/CDFV-001/Ref-01B/results/Ref-01B-B-0p25mps.csv"

# Columns that are labels rather than numbers.
SKIP = {"case_id"}

# Columns whose value each check is expected to constrain, for reporting only.
# Names must match the labels the verifier actually emits.
EXPECTED_GUARD = {
    "time_s": "monotonic_time",
    "z_center_m": "monotonic_position",
    "velocity_m_s": "monotonic_speed",
    "acceleration_m_s2": "motion_type",
    "buoyancy_N": "force_balance / buoyancy_range / buoyancy_unit_sanity",
    "weight_N": "force_balance / weight_reference / weight_unit_sanity",
    "constraint_force_N": "force_balance",
    "free_surface_force_N": "free_surface_zero",
}


def read_rows(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    reader = csv.DictReader(io.StringIO(path.read_text(encoding="utf-8")))
    assert reader.fieldnames is not None
    return list(reader.fieldnames), list(reader)


def write_rows(path: Path, fieldnames: list[str], rows: list[dict[str, str]]) -> None:
    buffer = io.StringIO(newline="")
    writer = csv.DictWriter(buffer, fieldnames=fieldnames, lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    path.write_bytes(buffer.getvalue().encode("utf-8"))


def run_verifier(results_dir: Path) -> tuple[int, list[str]]:
    proc = subprocess.run(
        [sys.executable, str(VERIFIER), "--results-dir", str(results_dir)],
        cwd=REPO,
        capture_output=True,
        encoding="utf-8",
        errors="replace",
    )
    failed: list[str] = []
    report = results_dir / "verification.json"
    if report.is_file():
        try:
            data = json.loads(report.read_text(encoding="utf-8"))
            for f in data.get("files", []):
                for c in f.get("checks", []):
                    if c.get("status") not in ("PASS", "SKIP"):
                        failed.append(f"{c.get('label')}:{c.get('status')}")
        except Exception:
            pass
    return proc.returncode, failed


def perturb(
    fieldnames: list[str],
    rows: list[dict[str, str]],
    column: str,
    delta: float,
    kind: str,
) -> list[dict[str, str]]:
    """Perturb one column ADDITIVELY, scaled to that column's own magnitude.

    A multiplicative perturbation is wrong here for two reasons this probe hit:

    * ``acceleration_m_s2`` and ``free_surface_force_N`` are identically zero in the
      constant-speed baseline, so scaling them by (1 + delta) changes nothing and the
      probe reports a blind spot that does not exist;
    * ``z_center_m`` crosses zero mid-run, so scaling the midpoint row by 1% also
      changes nothing.

    Using a fraction of the column's peak absolute value keeps every perturbation
    non-trivial regardless of sign or offset.
    """

    values = [float(r[column]) for r in rows]
    scale = max(abs(v) for v in values)
    if scale == 0.0:
        # A column that is identically zero can only be probed additively, and only
        # if the caller supplies an absolute step. Use the weight as the yardstick.
        scale = max(abs(float(r["weight_N"])) for r in rows) * 1e-3
    step = delta * scale

    out = [dict(r) for r in rows]
    targets = range(len(out)) if kind == "all" else [len(out) // 2]
    for i in targets:
        out[i][column] = repr(float(out[i][column]) + step)
    return out


def run_consistent_error_case(
    fieldnames: list[str], rows: list[dict[str, str]], factor: float, recompute: bool
) -> tuple[int, list[str]]:
    """Scale volume AND buoyancy together, as a wrong cross-section would.

    This is the "internally consistent wrongness" case: the derived columns and the
    force column agree with each other, so a consistency-only check would pass it.
    Whether the verifier notices therefore depends on something else - in practice on
    ``buoyancy_unit_sanity`` pinning max(buoyancy) to FULL_BUOYANCY_N.
    """

    out = [dict(r) for r in rows]
    for r in out:
        r["submerged_volume_m3"] = repr(float(r["submerged_volume_m3"]) * factor)
        r["buoyancy_N"] = repr(float(r["buoyancy_N"]) * factor)
        if recompute:
            r["constraint_force_N"] = repr(
                -float(r["buoyancy_N"]) + float(r["weight_N"])
            )
            r["constraint_force_abs_N"] = repr(abs(float(r["constraint_force_N"])))
            r["net_hydrostatic_force_N"] = repr(
                float(r["buoyancy_N"]) - float(r["weight_N"])
            )

    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp)
        write_rows(d / SOURCE.name, fieldnames, out)
        return run_verifier(d)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--delta", type=float, default=0.01)
    parser.add_argument("--json", type=Path, default=None)
    parser.add_argument(
        "--kinds", nargs="+", default=["row", "all"], choices=["row", "all"]
    )
    parser.add_argument(
        "--consistent",
        action="store_true",
        help=(
            "Also run the internally-consistent-wrongness case: scale submerged "
            "volume and buoyancy together, so they agree with each other but both "
            "disagree with the geometry. A consistency-only check would pass it."
        ),
    )
    args = parser.parse_args(argv)

    fieldnames, rows = read_rows(SOURCE)
    numeric = [c for c in fieldnames if c not in SKIP]
    print(f"source : {SOURCE.name}  rows={len(rows)}")
    print(f"delta  : {args.delta:+.3%}")
    print(f"columns: {len(numeric)}")
    print()

    results = []
    with tempfile.TemporaryDirectory() as tmp:
        tmpdir = Path(tmp)

        # Control: the unmodified file must pass, otherwise the probe is meaningless.
        control = tmpdir / "control"
        control.mkdir()
        write_rows(control / SOURCE.name, fieldnames, rows)
        code, failed = run_verifier(control)
        print(f"control (unmodified): exit={code} failed={failed}")
        if code != 0:
            print("ABORT: the clean file does not pass, so coverage cannot be measured")
            return 2
        print()

        header = f"{'column':<26} {'kind':<5} {'exit':>4}  {'caught':<7} checks"
        print(header)
        print("-" * len(header))

        for column in numeric:
            for kind in args.kinds:
                case_dir = tmpdir / f"{column}-{kind}"
                case_dir.mkdir()
                modified = perturb(fieldnames, rows, column, args.delta, kind)
                write_rows(case_dir / SOURCE.name, fieldnames, modified)
                code, failed = run_verifier(case_dir)
                caught = code != 0
                labels = ",".join(sorted({f.split(":")[0] for f in failed})) or "-"
                print(f"{column:<26} {kind:<5} {code:>4}  {'YES' if caught else 'NO ': <7} {labels}")
                results.append(
                    {
                        "column": column,
                        "kind": kind,
                        "exit": code,
                        "caught": caught,
                        "failed_checks": failed,
                        "expected_guard": EXPECTED_GUARD.get(column),
                    }
                )

    blind = [r for r in results if not r["caught"]]
    print()
    print(f"undetected perturbations: {len(blind)} of {len(results)}")
    for r in blind:
        exp = r["expected_guard"] or "(no check claims this column)"
        print(f"  BLIND SPOT  {r['column']:<24} {r['kind']:<5} expected guard: {exp}")

    if args.consistent:
        print()
        print("internally consistent wrongness (volume and buoyancy scaled together)")
        print(f"  {'factor':>8} {'constraint':<14} {'exit':>4}  {'verdict':<12} checks")
        for factor in (1.10, 1.001, 1.000001, 0.99, 0.999):
            for recompute in (False, True):
                code, failed = run_consistent_error_case(
                    fieldnames, rows, factor, recompute
                )
                labels = ",".join(sorted({f.split("=")[0] for f in failed})) or "-"
                tag = "recomputed" if recompute else "original"
                verdict = "caught" if code != 0 else "PASSES (bad)"
                print(
                    f"  {factor:>8.6f} {tag:<14} {code:>4}  {verdict:<12} {labels}"
                )

    if args.json is not None:
        args.json.write_bytes(
            json.dumps(
                {"delta": args.delta, "results": results}, indent=2, ensure_ascii=False
            ).encode("utf-8")
            + b"\n"
        )
        print(f"\nwrote {args.json}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
