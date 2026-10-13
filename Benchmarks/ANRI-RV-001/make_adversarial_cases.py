#!/usr/bin/env python3
"""Create reproducible adversarial copies of clean Ref-01B CSV results.

The clean results directory is copied into per-case directories under
``Benchmarks/ANRI-RV-001/adversarial/``.  The source directory is never
modified.

Coverage (see the RO-CDFV-001-Ref-01B review report, findings F9 and F11):

* every clean velocity case (0.10, 0.25 and 0.50 m/s) is mutated, not only the
  first file;
* several column families are exercised: weight, buoyancy, constraint force,
  time, position, required columns, units and the excluded free-surface term;
* the same physical fault is injected into different cases, so a verifier that
  silently stopped checking one file cannot pass.

Each case records in ``mutation.json`` the exact SHA-256 of the file it
produced, the mutation kind and the check that must detect it.  The manifest
``adversarial_cases.json`` lists every case with the hash of its
``mutation.json`` so the frozen set is auditable.

All output uses LF line terminators on every platform, so the produced bytes
are identical on Windows and Ubuntu.

Example (run from the repository root):

    py -3 Benchmarks/ANRI-RV-001/make_adversarial_cases.py \
      --source Models/CDFV-001/Ref-01B/results \
      --dest Benchmarks/ANRI-RV-001/adversarial
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import shutil
from pathlib import Path
from typing import Any, Callable

MANIFEST_NAME = "adversarial_cases.json"
SUMMARY_FILE_NAME = "summary.csv"

Row = dict[str, str]
Mutation = Callable[[list[str], list[Row], str], str]


def write_text_lf(path: Path, text: str) -> None:
    """Write UTF-8 with LF terminators regardless of platform.

    ``Path.write_text`` would emit CRLF on Windows and change the recorded
    digest of every generated file.
    """

    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write(text)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_csv(path: Path) -> tuple[list[str], list[Row]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        fieldnames = [name for name in (reader.fieldnames or []) if name is not None]
        rows = [dict(row) for row in reader]
    return fieldnames, rows


def write_csv(path: Path, fieldnames: list[str], rows: list[Row]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def row_index_for_fraction(total: int, fraction: float) -> int:
    return min(total - 1, max(0, int(total * fraction)))


# --------------------------------------------------------------------------
# Mutation kinds
# --------------------------------------------------------------------------


def mutate_add_constant(column: str, delta: float, fraction: float = 0.0) -> Mutation:
    def apply(fieldnames: list[str], rows: list[Row], case_id: str) -> str:
        index = row_index_for_fraction(len(rows), fraction)
        original = float(rows[index][column])
        rows[index][column] = format(original + delta, ".17g")
        return (
            f"{column} row {index} ({case_id}): {original!r} -> "
            f"{rows[index][column]!r} (delta {delta:+g})"
        )

    return apply


def mutate_scale(column: str, factor: float) -> Mutation:
    def apply(fieldnames: list[str], rows: list[Row], case_id: str) -> str:
        for row in rows:
            row[column] = format(float(row[column]) * factor, ".17g")
        return (
            f"{column} multiplied by {factor:g} in all {len(rows)} rows "
            "(unit error, for example kN where N is expected)"
        )

    return apply


def mutate_swap(column: str, offset: int, fraction: float = 0.25) -> Mutation:
    def apply(fieldnames: list[str], rows: list[Row], case_id: str) -> str:
        index = row_index_for_fraction(len(rows), fraction)
        other = min(len(rows) - 1, index + offset)
        if other == index:
            raise SystemExit(f"{case_id}: cannot swap {column} at index {index}")
        rows[index][column], rows[other][column] = (
            rows[other][column],
            rows[index][column],
        )
        return f"{column} values swapped between rows {index} and {other}"

    return apply


def mutate_drop_column(column: str) -> Mutation:
    def apply(fieldnames: list[str], rows: list[Row], case_id: str) -> str:
        if column not in fieldnames:
            raise SystemExit(f"{case_id}: column {column!r} not found")
        fieldnames.remove(column)
        for row in rows:
            row.pop(column, None)
        return f"column {column!r} removed from the header and every row"

    return apply


CASES: list[dict[str, Any]] = [
    {
        "case_id": "A01_wrong_weight",
        "source_name": "Ref-01B-B-0p10mps.csv",
        "mutation": mutate_add_constant("weight_N", 0.1),
        "mutation_kind": "reference_value_changed",
        "expected_detection": "weight_reference",
        "expected_status": "FAIL",
        "description": (
            "A single weight_N value is increased by 0.1 N. The verifier must "
            "reject the case because the weight no longer matches m*g."
        ),
    },
    {
        "case_id": "A02_broken_force_balance",
        "source_name": "Ref-01B-B-0p10mps.csv",
        "mutation": mutate_add_constant("constraint_force_N", 1.0),
        "mutation_kind": "force_balance_broken",
        "expected_detection": "force_balance",
        "expected_status": "FAIL",
        "description": (
            "A single constraint_force_N value is increased by 1 N, breaking "
            "constraint + buoyancy - weight = 0."
        ),
    },
    {
        "case_id": "A03_wrong_weight_mid",
        "source_name": "Ref-01B-B-0p25mps.csv",
        "mutation": mutate_add_constant("weight_N", 0.05),
        "mutation_kind": "reference_value_changed",
        "expected_detection": "weight_reference",
        "expected_status": "FAIL",
        "description": (
            "The same reference-value fault as A01 but in the 0.25 m/s case, so "
            "a verifier that only inspects the first file cannot pass."
        ),
    },
    {
        "case_id": "A04_broken_force_balance_high",
        "source_name": "Ref-01B-B-0p50mps.csv",
        "mutation": mutate_add_constant("constraint_force_N", -0.5, fraction=0.5),
        "mutation_kind": "force_balance_broken",
        "expected_detection": "force_balance",
        "expected_status": "FAIL",
        "description": (
            "The force-balance fault appears in the 0.50 m/s case, in the middle "
            "of the file rather than in the first row."
        ),
    },
    {
        "case_id": "A05_time_not_monotonic",
        "source_name": "Ref-01B-B-0p10mps.csv",
        "mutation": mutate_swap("time_s", 1),
        "mutation_kind": "time_not_monotonic",
        "expected_detection": "monotonic_time",
        "expected_status": "FAIL",
        "description": (
            "Two adjacent time_s values are exchanged, so time is no longer "
            "monotonic while the force balance still holds."
        ),
    },
    {
        "case_id": "A06_position_not_monotonic",
        "source_name": "Ref-01B-B-0p25mps.csv",
        "mutation": mutate_swap("z_center_m", 1),
        "mutation_kind": "position_not_monotonic",
        "expected_detection": "monotonic_position",
        "expected_status": "FAIL",
        "description": (
            "Two adjacent z_center_m values are exchanged, so the vertical "
            "position is no longer monotonic."
        ),
    },
    {
        "case_id": "A07_missing_buoyancy_column",
        "source_name": "Ref-01B-B-0p50mps.csv",
        "mutation": mutate_drop_column("buoyancy_N"),
        "mutation_kind": "missing_column",
        "expected_detection": "column_match_buoyancy",
        "expected_status": "FAIL",
        "description": (
            "The buoyancy_N column is removed. The verifier must refuse the "
            "file: the leftover submerged_volume_m3 column matches the buoyancy "
            "alias fuzzily, and a fuzzy match is never accepted silently."
        ),
    },
    {
        "case_id": "A08_missing_weight_column",
        "source_name": "Ref-01B-B-0p10mps.csv",
        "mutation": mutate_drop_column("weight_N"),
        "mutation_kind": "missing_column",
        "expected_detection": "column_weight",
        "expected_status": "FAIL",
        "description": "The weight_N column is removed from the 0.10 m/s case.",
    },
    {
        "case_id": "A09_buoyancy_out_of_range",
        "source_name": "Ref-01B-B-0p50mps.csv",
        "mutation": mutate_add_constant("buoyancy_N", 1.0),
        "mutation_kind": "buoyancy_out_of_range",
        "expected_detection": "buoyancy_range",
        "expected_status": "FAIL",
        "description": (
            "One buoyancy_N value exceeds the fully submerged reference "
            "buoyancy, which is impossible for this geometry."
        ),
    },
    {
        "case_id": "A10_weight_wrong_unit_mN",
        "source_name": "Ref-01B-B-0p10mps.csv",
        "mutation": mutate_scale("weight_N", 1e-3),
        "mutation_kind": "unit_error",
        "expected_detection": "weight_reference",
        "expected_status": "FAIL",
        "description": (
            "The weight column is written in mN instead of N; every value is "
            "1000 times too small."
        ),
    },
    {
        "case_id": "A11_buoyancy_wrong_unit_kN",
        "source_name": "Ref-01B-B-0p25mps.csv",
        "mutation": mutate_scale("buoyancy_N", 1e-3),
        "mutation_kind": "unit_error",
        "expected_detection": "buoyancy_unit_sanity",
        "expected_status": "FAIL",
        "description": (
            "The buoyancy column is written in kN instead of N in the "
            "0.25 m/s case, so every value is 1000 times too small."
        ),
    },
    {
        "case_id": "A12_free_surface_nonzero",
        "source_name": "Ref-01B-B-0p50mps.csv",
        "mutation": mutate_add_constant("free_surface_force_N", 0.25, fraction=0.75),
        "mutation_kind": "excluded_term_present",
        "expected_detection": "free_surface_zero",
        "expected_status": "FAIL",
        "description": (
            "A non-zero free-surface force appears in a baseline that defines "
            "that term as exactly zero."
        ),
    },
]


def mutate_one(
    source_dir: Path,
    case_dir: Path,
    case: dict[str, Any],
) -> dict[str, Any]:
    case_id = case["case_id"]
    source_name = case["source_name"]
    source_file = source_dir / source_name
    if not source_file.is_file():
        raise SystemExit(f"Source file does not exist: {source_file}")

    result_dir = case_dir / "results"
    result_dir.mkdir(parents=True, exist_ok=True)
    # Copy every clean CSV over the case's copy. shutil.copyfile overwrites, so no
    # pre-deletion is needed. Deliberately NOT deleting other files here: this
    # generator produces only the case inputs (the CSVs and mutation.json). The
    # verifier outputs (verification.json / verification_report.md) live beside
    # them and are produced by verify_baseline.py, and they are hash-registered in
    # the Research Object. An earlier pre-deletion loop removed those files, so a
    # regeneration after a verified commit left the tree dirty and the CI drift
    # check failed on every run.
    for csv_file in sorted(source_dir.glob("*.csv")):
        if csv_file.name.lower() == SUMMARY_FILE_NAME:
            continue
        shutil.copyfile(csv_file, result_dir / csv_file.name)

    target = result_dir / source_name
    fieldnames, rows = read_csv(target)
    if not rows:
        raise SystemExit(f"{case_id}: no data rows found in {target}")
    detail = case["mutation"](fieldnames, rows, case_id)
    write_csv(target, fieldnames, rows)

    metadata = {
        "case_id": case_id,
        "mutation_kind": case["mutation_kind"],
        "source_file": f"Models/CDFV-001/Ref-01B/results/{source_name}",
        "mutated_file": (
            f"Benchmarks/ANRI-RV-001/adversarial/{case_id}/results/{source_name}"
        ),
        "mutated_file_sha256": sha256(target),
        "row_count": len(rows),
        "detail": detail,
        "expected_detection": case["expected_detection"],
        "expected_status": case["expected_status"],
        "description": case["description"],
        "clean_results_untouched": True,
    }
    write_text_lf(case_dir / "mutation.json", json.dumps(metadata, indent=2) + "\n")
    return metadata


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Create the ANRI-RV-001 adversarial case set from clean results."
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
    dest_dir.mkdir(parents=True, exist_ok=True)

    expected_case_dirs = {case["case_id"] for case in CASES}
    removed: list[str] = []
    for child in sorted(dest_dir.iterdir()):
        if child.is_dir() and child.name not in expected_case_dirs:
            shutil.rmtree(child)
            removed.append(child.name)

    entries: list[dict[str, Any]] = []
    for case in CASES:
        case_dir = dest_dir / case["case_id"]
        metadata = mutate_one(source_dir, case_dir, case)
        entries.append(
            {
                "case_id": case["case_id"],
                "source_file": metadata["source_file"],
                "mutated_file": metadata["mutated_file"],
                "mutated_file_sha256": metadata["mutated_file_sha256"],
                "mutation_kind": metadata["mutation_kind"],
                "expected_detection": metadata["expected_detection"],
                "expected_status": metadata["expected_status"],
                "mutation_json": (
                    f"Benchmarks/ANRI-RV-001/adversarial/{case['case_id']}"
                    "/mutation.json"
                ),
                "mutation_json_sha256": sha256(case_dir / "mutation.json"),
                "description": metadata["description"],
            }
        )
        print(f"wrote {case_dir} ({metadata['mutation_kind']})")

    manifest = {
        "benchmark_id": "ANRI-RV-001",
        "schema_version": "0.2",
        "generator": "Benchmarks/ANRI-RV-001/make_adversarial_cases.py",
        "clean_source": "Models/CDFV-001/Ref-01B/results",
        "case_count": len(entries),
        "removed_stale_case_dirs": removed,
        "cases": entries,
    }
    manifest_path = dest_dir / MANIFEST_NAME
    write_text_lf(manifest_path, json.dumps(manifest, indent=2) + "\n")
    print(f"wrote {manifest_path}")
    if removed:
        print(f"removed stale case directories: {removed}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
