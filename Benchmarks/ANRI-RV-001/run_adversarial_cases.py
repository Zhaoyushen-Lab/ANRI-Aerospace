#!/usr/bin/env python3
"""Run every ANRI-RV-001 adversarial case and check it fails as intended.

Reads ``adversarial/adversarial_cases.json`` (produced by
``make_adversarial_cases.py``), runs the baseline verifier on each case
directory, and fails if any case passes, if the wrong check fired, or if the
observed status does not match the declared expectation.

Run from the repository root:

    py -3 Benchmarks/ANRI-RV-001/run_adversarial_cases.py
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

BENCHMARK_DIR = Path(__file__).resolve().parent
REPO_ROOT = BENCHMARK_DIR.parent.parent
MANIFEST = BENCHMARK_DIR / "adversarial" / "adversarial_cases.json"
VERIFIER = REPO_ROOT / "Models" / "CDFV-001" / "Ref-01B" / "verify_baseline.py"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--manifest",
        type=Path,
        default=MANIFEST,
        help=f"Adversarial case manifest (default: {MANIFEST}).",
    )
    parser.add_argument(
        "--results-dir",
        type=Path,
        default=None,
        help="Verifier results directory (default: <repo-root>/Models/CDFV-001/Ref-01B/results).",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    manifest_path = args.manifest.resolve()
    if not manifest_path.is_file():
        print(
            f"ERROR: adversarial manifest not found: {manifest_path}\n"
            "Run make_adversarial_cases.py first.",
            file=sys.stderr,
        )
        return 2

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    cases = manifest.get("cases", [])
    if not cases:
        print(f"ERROR: manifest declares no cases: {manifest_path}", file=sys.stderr)
        return 2

    failures: list[str] = []
    print(f"ANRI-RV-001 adversarial cases: {len(cases)}")

    for case in cases:
        case_id = case["case_id"]
        mutation = BENCHMARK_DIR / "adversarial" / case_id / "mutation.json"
        if not mutation.is_file():
            failures.append(f"{case_id}: missing {mutation}")
            print(f"  FAIL {case_id}: missing mutation.json")
            continue

        metadata = json.loads(mutation.read_text(encoding="utf-8"))
        results_dir = mutation.parent / "results"
        command = [
            sys.executable,
            str(VERIFIER),
            "--results-dir",
            str(results_dir),
            "--repo-root",
            str(REPO_ROOT),
            "--no-meta",
        ]
        completed = subprocess.run(
            command, capture_output=True, text=True, check=False
        )
        exit_code = completed.returncode

        report_path = results_dir / "verification.json"
        if not report_path.is_file():
            failures.append(f"{case_id}: verifier wrote no report")
            print(f"  FAIL {case_id}: no verification.json")
            continue
        report = json.loads(report_path.read_text(encoding="utf-8"))

        failed_checks: list[str] = []
        statuses: set[str] = set()
        for file_report in report["files"]:
            for check in file_report["checks"]:
                statuses.add(check["status"])
                if check["status"] == "FAIL":
                    failed_checks.append(check["label"])

        problems: list[str] = []
        expected_check = case["expected_detection"]
        if expected_check not in failed_checks:
            problems.append(
                f"expected check {expected_check!r} did not fail "
                f"(observed: {sorted(set(failed_checks))})"
            )
        if report["overall_status"] != case["expected_status"]:
            problems.append(
                f"status {report['overall_status']!r} != expected "
                f"{case['expected_status']!r}"
            )
        if exit_code == 0:
            problems.append("verifier exited 0, so the case was accepted")
        if not case.get("expected_detection"):
            problems.append("manifest entry has no expected_detection")

        if problems:
            failures.append(f"{case_id}: " + "; ".join(problems))
            print(f"  FAIL {case_id}: {'; '.join(problems)}")
        else:
            print(
                f"  PASS {case_id}: status={report['overall_status']} "
                f"exit={exit_code} detected_by={expected_check} "
                f"(kind={metadata['mutation_kind']})"
            )

    if failures:
        print(f"adversarial suite: FAIL ({len(failures)} of {len(cases)} cases)")
        return 1

    print(f"adversarial suite: PASS ({len(cases)} cases)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
