#!/usr/bin/env python3
"""Negative-case regression tests for the Ref-01B baseline verifier.

These tests exercise the verifier's own failure behaviour.  They exist so that
header matching, the unit-sanity checks, the monotonicity checks and the
explicit-failure reporting cannot silently regress (see the
RO-CDFV-001-Ref-01B review report, findings F11 and F12).

Each case builds a small synthetic CSV in a temporary directory, runs the real
verifier without writing local metadata, and asserts:

* the expected checks fail;
* the overall status matches (FAIL or PARTIAL);
* the process exit code matches (1 for any failure, 0 otherwise);
* every check status is one of PASS / FAIL / SKIP.

Run from the repository root:

    py -3 Models/CDFV-001/Ref-01B/verify_negative_cases.py
"""

from __future__ import annotations

import csv
import importlib.util
import io
import sys
import tempfile
from contextlib import redirect_stdout
from pathlib import Path
from typing import Any

SCRIPT_PATH = Path(__file__).resolve()
VERIFIER_PATH = SCRIPT_PATH.parent / "verify_baseline.py"


def load_verifier() -> Any:
    spec = importlib.util.spec_from_file_location("anri_verify_baseline", VERIFIER_PATH)
    if spec is None or spec.loader is None:
        raise SystemExit(f"cannot load verifier from {VERIFIER_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


VERIFIER = load_verifier()

COLUMNS = [
    "case_id",
    "time_s",
    "z_center_m",
    "velocity_m_s",
    "acceleration_m_s2",
    "buoyancy_N",
    "weight_N",
    "free_surface_force_N",
    "constraint_force_N",
]


def make_row(
    *,
    time_s: float,
    z_center_m: float,
    buoyancy_n: float,
    weight_n: float,
    free_surface_n: float = 0.0,
    acceleration: float = 0.0,
    speed_header: str = "velocity_m_s",
    constraint_header: str = "constraint_force_N",
) -> dict[str, str]:
    constraint = -buoyancy_n + weight_n + acceleration
    return {
        "case_id": "synthetic",
        "time_s": repr(time_s),
        "z_center_m": repr(z_center_m),
        speed_header: "0.1",
        "acceleration_m_s2": repr(acceleration),
        "buoyancy_N": repr(buoyancy_n),
        "weight_N": repr(weight_n),
        "free_surface_force_N": repr(free_surface_n),
        constraint_header: repr(constraint),
    }


def default_rows() -> list[dict[str, str]]:
    weight = VERIFIER.WEIGHT_N
    full_buoyancy = VERIFIER.FULL_BUOYANCY_N
    return [
        make_row(time_s=0.000, z_center_m=-0.20, buoyancy_n=full_buoyancy, weight_n=weight),
        make_row(time_s=0.001, z_center_m=-0.10, buoyancy_n=full_buoyancy / 2, weight_n=weight),
        make_row(time_s=0.002, z_center_m=0.00, buoyancy_n=0.0, weight_n=weight),
    ]


def write_case(
    directory: Path,
    headers: list[str],
    rows: list[dict[str, str]],
    *,
    raw: bool = False,
) -> Path:
    """Write one synthetic case CSV.

    ``raw=True`` writes the header verbatim (used for structurally malformed
    headers such as duplicates, which ``csv.DictWriter`` cannot express).
    """

    path = directory / "Ref-01B-B-0p10mps.csv"
    if raw:
        lines = [",".join(headers)]
        for row in rows:
            lines.append(",".join(str(row.get(name, "")) for name in headers))
        path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        return path

    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=headers, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    return path


def run_verifier(directory: Path) -> tuple[int, dict[str, Any]]:
    buffer = io.StringIO()
    with redirect_stdout(buffer):
        exit_code = VERIFIER.main(
            ["--results-dir", str(directory), "--no-meta"]
        )
    report = VERIFIER.json.loads(
        (directory / "verification.json").read_text(encoding="utf-8")
    )
    return exit_code, report


class Case:
    def __init__(
        self,
        name: str,
        *,
        headers: list[str] | None = None,
        rows: list[dict[str, str]] | None = None,
        expected_failures: tuple[str, ...],
        expected_status: str,
        expected_exit: int = 1,
        raw: bool = False,
    ) -> None:
        self.name = name
        self.headers = list(headers if headers is not None else COLUMNS)
        self.rows = rows if rows is not None else default_rows()
        self.expected_failures = expected_failures
        self.expected_status = expected_status
        self.expected_exit = expected_exit
        self.raw = raw


def build_cases() -> list[Case]:
    weight = VERIFIER.WEIGHT_N
    full_buoyancy = VERIFIER.FULL_BUOYANCY_N
    cases: list[Case] = []

    # --- column matching ---------------------------------------------------
    alias_headers = [
        "case_id",
        "time_s",
        "z_center_m",
        "velocity_mps",
        "acceleration_m_s2",
        "buoyancy_N",
        "weight_N",
        "free_surface_force_N",
        "constraint_force_N",
    ]
    alias_rows = [
        make_row(
            time_s=index * 0.001,
            z_center_m=-0.2 + index * 0.1,
            buoyancy_n=VERIFIER.FULL_BUOYANCY_N / (index + 1),
            weight_n=VERIFIER.WEIGHT_N,
            speed_header="velocity_mps",
        )
        for index in range(3)
    ]
    cases.append(
        Case(
            "header_uses_velocity_mps_alias",
            headers=alias_headers,
            rows=alias_rows,
            expected_failures=(),
            expected_status="PASS",
            expected_exit=0,
        )
    )
    cases.append(
        Case(
            "header_uses_undeclared_fuzzy_name",
            headers=[
                "case_id",
                "time_s",
                "z_center_m",
                "velocity_m_s",
                "acceleration_m_s2",
                "buoyancy_N",
                "weight_N",
                "free_surface_force_N",
                "force_constraint_N",
            ],
            rows=[
                make_row(
                    time_s=index * 0.001,
                    z_center_m=-0.2 + index * 0.1,
                    buoyancy_n=VERIFIER.FULL_BUOYANCY_N / (index + 1),
                    weight_n=VERIFIER.WEIGHT_N,
                    constraint_header="force_constraint_N",
                )
                for index in range(3)
            ],
            expected_failures=("column_match_constraint",),
            expected_status="FAIL",
        )
    )

    # The real model emits both "constraint_force_N" and "constraint_force_abs_N".
    # The exact-match rule must select the signed column, never the absolute one.
    abs_headers = COLUMNS + ["constraint_force_abs_N"]
    abs_rows = default_rows()
    for row in abs_rows:
        row["constraint_force_abs_N"] = repr(abs(float(row["constraint_force_N"])))
    cases.append(
        Case(
            "abs_constraint_column_present",
            headers=abs_headers,
            rows=abs_rows,
            expected_failures=(),
            expected_status="PASS",
            expected_exit=0,
        )
    )

    # ... and a file that only offers the absolute column must not be accepted.
    only_abs_headers = [
        name for name in COLUMNS if name != "constraint_force_N"
    ] + ["constraint_force_abs_N"]
    only_abs_rows = []
    for row in default_rows():
        row = dict(row)
        row["constraint_force_abs_N"] = repr(abs(float(row.pop("constraint_force_N"))))
        only_abs_rows.append(row)
    cases.append(
        Case(
            "only_abs_constraint_column",
            headers=only_abs_headers,
            rows=only_abs_rows,
            expected_failures=("column_constraint",),
            expected_status="FAIL",
        )
    )

    cases.append(
        Case(
            "duplicate_header",
            headers=["case_id", "time_s", "weight_N", "weight_N"],
            rows=[
                {
                    "case_id": "synthetic",
                    "time_s": "0.0",
                    "weight_N": repr(VERIFIER.WEIGHT_N),
                }
            ],
            expected_failures=("duplicate_headers",),
            expected_status="FAIL",
            raw=True,
        )
    )

    # --- missing columns ---------------------------------------------------
    for dropped, check in (
        ("buoyancy_N", "column_buoyancy"),
        ("weight_N", "column_weight"),
        ("constraint_force_N", "column_constraint"),
    ):
        headers = [name for name in COLUMNS if name != dropped]
        rows = [
            {key: value for key, value in row.items() if key != dropped}
            for row in default_rows()
        ]
        cases.append(
            Case(
                f"missing_column_{dropped}",
                headers=headers,
                rows=rows,
                expected_failures=(check,),
                expected_status="FAIL",
                expected_exit=1,
            )
        )

    # --- numeric and reference failures -----------------------------------
    bad_numeric = default_rows()
    bad_numeric[1]["weight_N"] = "not-a-number"
    cases.append(
        Case(
            "non_numeric_weight",
            rows=bad_numeric,
            expected_failures=("numeric_weight",),
            expected_status="FAIL",
        )
    )

    wrong_weight = default_rows()
    wrong_weight[0]["weight_N"] = repr(weight * 1.001)
    cases.append(
        Case(
            "wrong_weight_reference",
            rows=wrong_weight,
            expected_failures=("weight_reference", "force_balance"),
            expected_status="FAIL",
        )
    )

    # --- monotonicity ------------------------------------------------------
    non_monotonic_time = default_rows()
    non_monotonic_time[0]["time_s"], non_monotonic_time[1]["time_s"] = (
        non_monotonic_time[1]["time_s"],
        non_monotonic_time[0]["time_s"],
    )
    cases.append(
        Case(
            "time_not_monotonic",
            rows=non_monotonic_time,
            expected_failures=("monotonic_time",),
            expected_status="FAIL",
        )
    )

    non_monotonic_position = default_rows()
    non_monotonic_position[1]["z_center_m"], non_monotonic_position[2]["z_center_m"] = (
        non_monotonic_position[2]["z_center_m"],
        non_monotonic_position[1]["z_center_m"],
    )
    cases.append(
        Case(
            "position_not_monotonic",
            rows=non_monotonic_position,
            expected_failures=("monotonic_position",),
            expected_status="FAIL",
        )
    )

    # --- units and ranges --------------------------------------------------
    milli_newton_weight = default_rows()
    for row in milli_newton_weight:
        row["weight_N"] = repr(weight * 1e-3)
    cases.append(
        Case(
            "weight_in_millinewton",
            rows=milli_newton_weight,
            expected_failures=(
                "weight_reference",
                "weight_unit_sanity",
                "force_balance",
            ),
            expected_status="FAIL",
        )
    )

    kilo_newton_buoyancy = default_rows()
    for row in kilo_newton_buoyancy:
        row["buoyancy_N"] = repr(float(row["buoyancy_N"]) * 1e-3)
    cases.append(
        Case(
            "buoyancy_in_kilonewton",
            rows=kilo_newton_buoyancy,
            expected_failures=("force_balance",),
            expected_status="FAIL",
        )
    )

    out_of_range = default_rows()
    out_of_range[0]["buoyancy_N"] = repr(full_buoyancy + 1.0)
    cases.append(
        Case(
            "buoyancy_above_full_submergence",
            rows=out_of_range,
            expected_failures=("buoyancy_range", "buoyancy_unit_sanity", "force_balance"),
            expected_status="FAIL",
        )
    )

    negative_buoyancy = default_rows()
    negative_buoyancy[0]["buoyancy_N"] = repr(-1.0)
    cases.append(
        Case(
            "buoyancy_negative",
            rows=negative_buoyancy,
            expected_failures=("buoyancy_range", "force_balance"),
            expected_status="FAIL",
        )
    )

    # --- excluded term and prescribed acceleration -------------------------
    nonzero_free_surface = default_rows()
    nonzero_free_surface[0]["free_surface_force_N"] = "0.25"
    cases.append(
        Case(
            "free_surface_nonzero",
            rows=nonzero_free_surface,
            expected_failures=("free_surface_zero",),
            expected_status="FAIL",
        )
    )

    # --- accelerated motion: balance must carry the inertial term -----------
    # A non-zero acceleration is no longer an error in itself: the verifier now
    # accepts accelerated cases and checks that m*a appears in the balance.  The
    # remaining failure mode is an accelerated file whose constraint force was
    # computed WITHOUT the inertial term, which is exactly what the old baseline
    # plus a copied acceleration column would look like.
    ignored_inertia = default_rows()
    for row in ignored_inertia:
        row["acceleration_m_s2"] = "1.0"
        # Deliberately omit mass*acceleration from the constraint force.
        row["constraint_force_N"] = repr(
            -float(row["buoyancy_N"]) + float(row["weight_N"])
        )
    cases.append(
        Case(
            "accelerated_without_inertial_term",
            rows=ignored_inertia,
            expected_failures=("force_balance",),
            expected_status="FAIL",
        )
    )

    return cases


def main() -> int:
    failures: list[str] = []
    cases = build_cases()
    print(f"ANRI-RV-001 verifier negative cases: {len(cases)}")

    with tempfile.TemporaryDirectory(prefix="anri-negative-cases-") as raw_tmp:
        tmp_root = Path(raw_tmp)
        for case in cases:
            directory = tmp_root / case.name
            directory.mkdir(parents=True, exist_ok=True)
            write_case(directory, case.headers, case.rows, raw=case.raw)
            exit_code, report = run_verifier(directory)

            observed_failures: list[str] = []
            statuses: set[str] = set()
            for file_report in report["files"]:
                for check in file_report["checks"]:
                    statuses.add(check["status"])
                    if check["status"] == "FAIL":
                        observed_failures.append(check["label"])

            problems: list[str] = []
            missing = sorted(set(case.expected_failures) - set(observed_failures))
            if missing:
                problems.append(f"expected failures not observed: {missing}")
            if report["overall_status"] != case.expected_status:
                problems.append(
                    f"overall_status={report['overall_status']!r}, "
                    f"expected {case.expected_status!r}"
                )
            if exit_code != case.expected_exit:
                problems.append(
                    f"exit code {exit_code}, expected {case.expected_exit}"
                )
            unknown = statuses - {"PASS", "FAIL", "SKIP"}
            if unknown:
                problems.append(f"unexpected check statuses: {sorted(unknown)}")

            if problems:
                failures.append(f"{case.name}: " + "; ".join(problems))
                print(f"  FAIL {case.name}: {'; '.join(problems)}")
            else:
                detail = ", ".join(observed_failures) or "no failures"
                print(
                    f"  PASS {case.name}: status={report['overall_status']} "
                    f"exit={exit_code} failures=[{detail}]"
                )

    if failures:
        print(f"negative-case suite: FAIL ({len(failures)} of {len(cases)} cases)")
        return 1

    print(f"negative-case suite: PASS ({len(cases)} cases)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
