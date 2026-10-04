#!/usr/bin/env python3
"""Create reproducible adversarial copies of clean Ref-01B CSV results.

The source results directory is copied into separate case directories. The
source directory is never changed.

Example (run from the repository root):

    py -3 Benchmarks/ANRI-RV-001/make_adversarial_cases.py \
      --source Models/CDFV-001/Ref-01B/results \
      --dest Benchmarks/ANRI-RV-001/adversarial
"""

from __future__ import annotations

import argparse
import csv
import json
import shutil
from pathlib import Path


def mutate_one(
    source_dir: Path,
    case_dir: Path,
    column: str,
    delta: float,
    case_id: str,
) -> None:
    result_dir = case_dir / "results"
    result_dir.mkdir(parents=True, exist_ok=True)

    csv_files = sorted(
        path for path in source_dir.glob("*.csv") if path.name.lower() != "summary.csv"
    )
    if not csv_files:
        raise SystemExit(f"No data CSV files found in {source_dir}")

    for source_file in source_dir.glob("*.csv"):
        shutil.copy2(source_file, result_dir / source_file.name)

    target = result_dir / csv_files[0].name
    with target.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        fieldnames = reader.fieldnames or []
        rows = list(reader)

    if column not in fieldnames:
        raise SystemExit(f"Column {column!r} not found in {target}")
    if not rows:
        raise SystemExit(f"No data rows found in {target}")

    row_index = 0
    original_value = float(rows[row_index][column])
    rows[row_index][column] = format(original_value + delta, ".17g")

    with target.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    metadata = {
        "case_id": case_id,
        "source_file": csv_files[0].name,
        "mutated_file": str(target),
        "row_index_zero_based": row_index,
        "column": column,
        "original_value": original_value,
        "delta": delta,
        "expected_detection": "FAIL",
        "clean_results_untouched": True,
    }
    (case_dir / "mutation.json").write_text(
        json.dumps(metadata, indent=2), encoding="utf-8"
    )


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Create A01 and A02 copies from clean Ref-01B CSV results."
    )
    parser.add_argument(
        "--source", type=Path, required=True, help="Clean Ref-01B results directory"
    )
    parser.add_argument(
        "--dest", type=Path, required=True, help="Adversarial output directory"
    )
    args = parser.parse_args()

    source_dir = args.source.resolve()
    dest_dir = args.dest.resolve()
    if not source_dir.is_dir():
        raise SystemExit(f"Source directory does not exist: {source_dir}")

    mutate_one(
        source_dir,
        dest_dir / "A01_wrong_weight",
        "weight_N",
        0.1,
        "A01_wrong_weight",
    )
    mutate_one(
        source_dir,
        dest_dir / "A02_broken_force_balance",
        "constraint_force_N",
        1.0,
        "A02_broken_force_balance",
    )
    print(f"wrote {dest_dir / 'A01_wrong_weight'}")
    print(f"wrote {dest_dir / 'A02_broken_force_balance'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
