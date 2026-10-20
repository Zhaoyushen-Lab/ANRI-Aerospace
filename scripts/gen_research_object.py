#!/usr/bin/env python3
"""Regenerate Research_Objects/RO-CDFV-001-Ref-01B.json and its run manifest.

This is the canonical way to refresh the hash-registered record.  Every SHA-256
in both files is computed from the bytes on disk, so the object and its manifest
cannot drift from the artifacts.

Run it when a frozen artifact legitimately changes, when the review record is
updated, or when a new artifact is added:

    py -3 scripts/gen_research_object.py \
      --git-commit "$(git rev-parse HEAD)" \
      --created-utc "2026-10-11T06:32:35Z" \
      --review-date 2026-10-11

Then run the validator and commit the two JSON files together with the change
that caused them to move.  The validator fails if you forget.

Note on the "self" placeholder: the object and its manifest record each other's
digest.  The object is written first, so it records the manifest's real digest;
the manifest declares the object with the literal "self", which is left in place
so the tool is idempotent.  The validator resolves the pair and accepts the
placeholder only on those two entries.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import re
import sys
from pathlib import Path
from typing import Any, Sequence

REPO = Path(__file__).resolve().parent.parent
MODEL = REPO / "Models" / "CDFV-001" / "Ref-01B" / "baseline_model.py"
VERIFIER = REPO / "Models" / "CDFV-001" / "Ref-01B" / "verify_baseline.py"

RO_REL = "Research_Objects/RO-CDFV-001-Ref-01B.json"
MANIFEST_REL = "Benchmarks/ANRI-RV-001/run_manifest.json"
REVIEW_REPORT = "Reviews/RO-CDFV-001-Ref-01B_Independent_Review_Report.md"

EXTERNAL_REVIEW_SHA256 = "ae6aa3b084060431a7558952743dd78eb5a4da9cd2fb0b73413861b0cf26e992"

ADVERSARIAL_CASES = [
    "A01_wrong_weight",
    "A02_broken_force_balance",
    "A03_wrong_weight_mid",
    "A04_broken_force_balance_high",
    "A05_time_not_monotonic",
    "A06_position_not_monotonic",
    "A07_missing_buoyancy_column",
    "A08_missing_weight_column",
    "A09_buoyancy_out_of_range",
    "A10_weight_wrong_unit_mN",
    "A11_buoyancy_wrong_unit_kN",
    "A12_free_surface_nonzero",
]


def write_lf(path: Path, text: str) -> None:
    """Write UTF-8 with LF terminators on every platform.

    ``Path.write_text`` translates "\\n" to the platform line separator, so on
    Windows it would silently emit CRLF and change every recorded SHA-256.
    """

    with path.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write(text)


def sha256(relative: str) -> str:
    path = REPO / relative
    if not path.is_file():
        raise SystemExit(f"missing artifact: {relative}")
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_module(path: Path, name: str) -> Any:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise SystemExit(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def build_artifact_list() -> list[tuple[str, str]]:
    """Return the frozen artifact set as (path, role) pairs.

    Deliberately excluded, with reasons:

    * ``scripts/validate_gate_selftest.py`` 閳?it mutates and validates a copy of
      this record. Hashing the test would make every edit to the test invalidate
      the record it tests, which is circular churn rather than evidence.
    * ``Reviews/DeepSeek_Harness_Repair_Prompt.md`` and the two review-prompt
      files 閳?author-facing instructions, not research evidence. The review
      *verdict* and the checklist are registered; the prompts are not.
    * ``.github/workflows/anri-validation.yml`` 閳?the gate definition. It is
      covered by branch protection and review, not by a self-referential digest.
    * ``scripts/collect_state.py`` and ``Research_Log/*`` 閳?measurement tooling
      and the research log. They observe and narrate the record; registering them
      would move the object's hash on every log entry, and the log is commentary
      rather than evidence. The research evidence itself (model, results,
      validators, schema, review verdict, run manifest) is registered below.

    Everything the claim depends on is listed below.
    """

    artifacts: list[tuple[str, str]] = [
        ("Research_Planning/CDFV-001_Reference_Configuration.md", "input"),
        ("Research_Planning/P003_Free_Surface_Loading.md", "input"),
        ("Research_Planning/P003_Stage1_Sourcing_Checklist.md", "input"),
        ("Research_Planning/P003_B1_Measurement_Spec.md", "input"),
        ("Research_Planning/P003_B1_Preregistration.md", "input"),
        ("Research_Planning/P004_Candidate_Comparison.md", "input"),
        ("Research_Planning/P002_Data_Availability_Check.md", "input"),
        ("Research_Planning/P004_Added_Mass_Screening.md", "input"),
        ("Research_Planning/P004_Added_Mass_Coefficient.md", "input"),
        ("Experiment_Requests/CLEANROOM-Replication_Task.md", "input"),
        ("Models/CDFV-001/Ref-01B/baseline_model.py", "model"),
        ("Models/CDFV-001/Ref-01B/verify_baseline.py", "model"),
        ("Models/CDFV-001/Ref-01B/verify_negative_cases.py", "model"),
        ("Models/CDFV-001/Ref-01B/README.md", "report"),
        ("Models/CDFV-001/Ref-01B/results/README.md", "report"),
        ("Models/CDFV-001/Ref-01B/results/Ref-01B-B-0p10mps.csv", "result"),
        ("Models/CDFV-001/Ref-01B/results/Ref-01B-B-0p25mps.csv", "result"),
        ("Models/CDFV-001/Ref-01B/results/Ref-01B-B-0p50mps.csv", "result"),
        # Accelerated cases, added for P004 (added mass). These make the inertial
        # term observable; the constant-speed cases have a == 0, where m*a vanishes
        # and the recorded constraint force cannot distinguish "added mass omitted"
        # from "added mass negligible".
        ("Models/CDFV-001/Ref-01B/results/Ref-01B-B-0p10mps-a0p10mps2.csv", "result"),
        ("Models/CDFV-001/Ref-01B/results/Ref-01B-B-0p10mps-a1p00mps2.csv", "result"),
        ("Models/CDFV-001/Ref-01B/results/Ref-01B-B-0p25mps-a0p10mps2.csv", "result"),
        ("Models/CDFV-001/Ref-01B/results/Ref-01B-B-0p25mps-a1p00mps2.csv", "result"),
        ("Models/CDFV-001/Ref-01B/results/Ref-01B-B-0p50mps-a0p10mps2.csv", "result"),
        ("Models/CDFV-001/Ref-01B/results/Ref-01B-B-0p50mps-a1p00mps2.csv", "result"),
        ("Models/CDFV-001/Ref-01B/results/summary.csv", "result"),
        ("Models/CDFV-001/Ref-01B/results/verification.json", "report"),
        ("Models/CDFV-001/Ref-01B/results/verification_report.md", "report"),
        ("scripts/validate_research_object.py", "model"),
        ("scripts/gen_research_object.py", "model"),
        ("schema/research_object.schema.json", "schema"),
        ("Benchmarks/ANRI-RV-001/make_adversarial_cases.py", "model"),
        ("Benchmarks/ANRI-RV-001/run_adversarial_cases.py", "model"),
        ("Benchmarks/ANRI-RV-001/make_blind_copy.py", "model"),
        ("Benchmarks/ANRI-RV-001/adversarial/adversarial_cases.json", "index"),
        ("Benchmarks/ANRI-RV-001/rubric.yaml", "input"),
        ("Benchmarks/ANRI-RV-001/task.md", "input"),
        ("Benchmarks/ANRI-RV-001/README.md", "report"),
        ("Benchmarks/ANRI-RV-001/adversarial/README.md", "report"),
        ("Benchmarks/ANRI-RV-001/decision_log.md", "review"),
        ("Research_Planning/Decision_Log.md", "review"),
        (MANIFEST_REL, "manifest"),
        (REVIEW_REPORT, "review"),
        ("Reviews/DeepSeek_Harness_Repair_Report.md", "review"),
        ("Reviews/RO-CDFV-001-Ref-01B_Review_Checklist.md", "review"),
    ]
    for case in ADVERSARIAL_CASES:
        base = f"Benchmarks/ANRI-RV-001/adversarial/{case}"
        artifacts.append((f"{base}/mutation.json", "index"))
        artifacts.append((f"{base}/results/verification.json", "report"))
        artifacts.append((f"{base}/results/verification_report.md", "report"))
    # The object lists itself. Its role must not be "manifest": that role means
    # "this is the run manifest to cross-check", and reusing it here would make
    # the object look like its own manifest. The maniest is linked explicitly
    # through run_manifest_ref instead.
    artifacts.append((RO_REL, "review"))
    return artifacts


def quantity(value: float, unit: str, source: str) -> dict[str, object]:
    return {"value": value, "unit": unit, "source": source}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--git-commit", required=True)
    parser.add_argument("--created-utc", required=True)
    parser.add_argument("--review-date", required=True)
    parser.add_argument(
        "--check-only",
        action="store_true",
        help="Recompute and compare without writing the two JSON files.",
    )
    args = parser.parse_args()
    if not re.fullmatch(r"[a-f0-9]{40}", args.git_commit):
        parser.error("--git-commit must be a 40-character lowercase hex digest")
    return args


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args()

    model = load_module(MODEL, "anri_baseline_model")
    verifier = load_module(VERIFIER, "anri_verify_baseline")
    cfg = model.Ref01BConfig()

    if not (
        cfg.gravity_m_s2 == verifier.GRAVITY_M_S2 == 9.80665
        and cfg.mass_kg == verifier.MASS_KG
        and cfg.water_density_kg_m3 == verifier.WATER_DENSITY_KG_M3
    ):
        raise SystemExit("model and verifier constants disagree; refusing to generate")

    artifacts = build_artifact_list()
    hashes = {path: sha256(path) for path, _ in artifacts}
    # The object cannot contain its own digest.
    hashes[RO_REL] = "self"

    reference_configuration = {
        "configuration_id": "CDFV-001-Ref-01B",
        "mass_kg": quantity(cfg.mass_kg, "kg", "P002 Table 1 (literature reference)"),
        "diameter_m": quantity(
            cfg.diameter_m, "m", "P002 Table 1 (literature reference)"
        ),
        "length_m": quantity(cfg.length_m, "m", "P002 Table 1 (literature reference)"),
        "water_density_kg_m3": quantity(
            cfg.water_density_kg_m3,
            "kg/m^3",
            "assumption A-FRESHWATER (fresh water, temperature not specified)",
        ),
        "gravity_m_s2": quantity(
            cfg.gravity_m_s2,
            "m/s^2",
            "assumption A-GRAVITY (standard gravity, frozen value)",
        ),
        "force_tolerance_n": quantity(
            verifier.FORCE_TOLERANCE_N, "N", "verifier acceptance tolerance (absolute)"
        ),
        "free_surface_force_n": quantity(
            0.0,
            "N",
            "assumption A-FREE-SURFACE-ZERO (term excluded from the baseline)",
        ),
    }

    research_object = {
        "schema_version": "0.2",
        "id": "RO-CDFV-001-Ref-01B",
        "type": "research_object",
        "version": "0.2.0",
        "status": "in_review",
        "title": "CDFV-001 Ref-01B computational hydrostatic benchmark",
        "purpose": (
            "Establish an internally reproducible vertical water-exit baseline "
            "before adding free-surface loading or experimental data."
        ),
        "scope": {
            "configuration_id": "CDFV-001-Ref-01B",
            "research_question": (
                "Is the prescribed-motion hydrostatic baseline internally "
                "computationally consistent under the stated assumptions?"
            ),
            "included": [
                "vertical prescribed water-exit motion",
                "gravity",
                "partially submerged buoyancy",
                "algebraic constraint force",
                "CSV integrity and force-balance verification",
                "adversarial error-detection benchmark",
            ],
            "excluded": [
                "free-surface loading",
                "drag",
                "added mass",
                "propulsion dynamics",
                "attitude coupling",
                "experimental validation",
            ],
        },
        "run_manifest_ref": MANIFEST_REL,
        "reference_configuration": reference_configuration,
        "claims": [
            {
                "id": "C-CDFV-001-BASELINE-CONSISTENT",
                "text": (
                    "Within the frozen reference configuration, the baseline "
                    "satisfies the algebraic identity constraint_force + buoyancy "
                    "- weight = 0 to within 1e-4 N for every emitted row of the "
                    "three prescribed-velocity cases. This is an internal "
                    "computational consistency statement about a model residual; "
                    "it is not experimental validation of free-surface loading "
                    "and not a physical validation of the model."
                ),
                "status": "supported",
                "evidence_refs": ["E-CDFV-001-CONFIG", "E-CDFV-001-RESULTS"],
                "validator_refs": ["V-ANRI-RV-001"],
                "limitation_refs": [
                    "L-NO-EXPERIMENT",
                    "L-EXCLUDED-PHYSICS",
                    "L-NEAR-NEUTRAL",
                ],
            }
        ],
        "evidence": [
            {
                "id": "E-CDFV-001-CONFIG",
                "type": "configuration",
                "source": "Research_Planning/CDFV-001_Reference_Configuration.md",
                "supports": ["C-CDFV-001-BASELINE-CONSISTENT"],
                "status": "mapped",
                "conditions": [
                    "mass=2.030 kg",
                    "diameter=0.090 m",
                    "length=0.323 m",
                    "water density=1000 kg/m^3",
                    "gravity=9.80665 m/s^2",
                    "force tolerance=1e-4 N",
                    "freshwater assumption",
                ],
                "values": {
                    field: {"value": value, "unit": unit}
                    for field, value, unit in (
                        ("mass_kg", cfg.mass_kg, "kg"),
                        ("diameter_m", cfg.diameter_m, "m"),
                        ("length_m", cfg.length_m, "m"),
                        ("water_density_kg_m3", cfg.water_density_kg_m3, "kg/m^3"),
                        ("gravity_m_s2", cfg.gravity_m_s2, "m/s^2"),
                        ("force_tolerance_n", verifier.FORCE_TOLERANCE_N, "N"),
                    )
                },
            },
            {
                "id": "E-CDFV-001-RESULTS",
                "type": "calculation",
                "source": "Models/CDFV-001/Ref-01B/results/verification_report.md",
                "supports": ["C-CDFV-001-BASELINE-CONSISTENT"],
                "status": "available",
                "conditions": [
                    "0.10 m/s",
                    "0.25 m/s",
                    "0.50 m/s",
                    "verifier checks version 0.2",
                ],
            },
            {
                "id": "E-ANRI-RV-001-ADVERSARIAL",
                "type": "calculation",
                "source": "Benchmarks/ANRI-RV-001/adversarial/adversarial_cases.json",
                "supports": ["C-CDFV-001-BASELINE-CONSISTENT"],
                "status": "available",
                "conditions": [
                    "12 adversarial cases",
                    "7 fault families",
                    "all three velocity cases mutated",
                    "each case must be rejected by its intended check",
                ],
            },
        ],
        "validators": [
            {
                "id": "V-ANRI-RV-001",
                "name": "ANRI-RV-001 Ref-01B baseline verifier",
                "command": "python Models/CDFV-001/Ref-01B/verify_baseline.py",
                "result_ref": "Models/CDFV-001/Ref-01B/results/verification.json",
                "report_ref": "Models/CDFV-001/Ref-01B/results/verification_report.md",
                "checks_version": "0.2",
            }
        ],
        "artifacts": [
            {"path": path, "role": role, "sha256": hashes[path]}
            for path, role in artifacts
        ],
        "assumptions": [
            {
                "id": "A-FRESHWATER",
                "text": "Water density is 1000 kg/m^3; temperature is not specified.",
                "status": "explicit",
                "value": cfg.water_density_kg_m3,
                "unit": "kg/m^3",
                "source": "modelling assumption, frozen in baseline_model.py",
            },
            {
                "id": "A-GRAVITY",
                "text": (
                    "Gravitational acceleration is the standard value 9.80665 "
                    "m/s^2. The model, the verifier and the reference "
                    "configuration all use this single value, and the validator "
                    "fails if they diverge."
                ),
                "status": "explicit",
                "value": cfg.gravity_m_s2,
                "unit": "m/s^2",
                "source": "standard gravity, frozen value (A-GRAVITY)",
            },
            {
                "id": "A-FREE-SURFACE-ZERO",
                "text": (
                    "Free-surface force is set to 0 N in the baseline and the "
                    "verifier checks that the column stays zero."
                ),
                "status": "explicit",
                "value": 0.0,
                "unit": "N",
                "source": "baseline model definition",
            },
            {
                "id": "A-PRESCRIBED-MOTION",
                "text": (
                    "Motion is prescribed with a = 0; propulsion dynamics are not "
                    "modelled and the constraint force is a model residual."
                ),
                "status": "explicit",
                "source": "baseline model definition",
            },
            {
                "id": "A-TOLERANCE",
                "text": (
                    "Force comparisons use an absolute tolerance of 1e-4 N, the "
                    "acceptance tolerance recorded in the reference configuration."
                ),
                "status": "explicit",
                "value": verifier.FORCE_TOLERANCE_N,
                "unit": "N",
                "source": "verifier acceptance tolerance",
            },
        ],
        "limitations": [
            {
                "id": "L-NO-EXPERIMENT",
                "text": "No laboratory or field measurement is included.",
                "status": "open",
            },
            {
                "id": "L-EXCLUDED-PHYSICS",
                "text": (
                    "Free-surface loading, drag, added mass, wave effects and "
                    "attitude coupling are outside this baseline."
                ),
                "status": "bounded",
            },
            {
                "id": "L-NEAR-NEUTRAL",
                "text": (
                    "The configuration is near-neutral: the fully submerged "
                    "constraint force is about 0.2436 N against a 19.9075 N "
                    "weight (about 1.2 %), so the reported residual is sensitive "
                    "to the frozen mass, density, gravity and diameter. No "
                    "uncertainty budget has been established."
                ),
                "status": "open",
            },
        ],
        "review": {
            "status": "revision_requested",
            "reviewer_refs": ["R-ANRI-REVIEW-001"],
            "decision_ref": "D-ANRI-RV-001-001",
            "reviews": [
                {
                    "review_id": "R-ANRI-REVIEW-001",
                    "reviewer": (
                        "DeepSeek Harness independent review session "
                        "(model-generated, read-only)"
                    ),
                    "independent": True,
                    "date": args.review_date,
                    "decision": "request_changes",
                    "report_path": REVIEW_REPORT,
                    "report_sha256": hashes[REVIEW_REPORT],
                    "scope": (
                        "Full read-only review of RO-CDFV-001-Ref-01B against "
                        "Reviews/RO-CDFV-001-Ref-01B_Review_Checklist.md: schema, "
                        "paths, hashes, claim support, reference configuration, "
                        "clean baseline, A01/A02, GitHub Actions, machine paths, "
                        "line endings, and the review gate."
                    ),
                    "blocking_findings": [
                        "F1 recorded SHA-256 values computed on CRLF working-tree bytes",
                        "F2 verification artifacts not hash-registered and non-deterministic",
                        "F3 run manifest digests wrong for the committed content",
                        "F4 run manifest displaced_volume_m3 contradicts the evidence",
                        "F6 validator did not apply the schema or check evidence paths",
                        "F9 no independent review gate record",
                    ],
                    "external_source_sha256": EXTERNAL_REVIEW_SHA256,
                    "external_note": (
                        "The verbatim original of this report lives outside the "
                        "repository (reviewer's desktop). The repository copy is "
                        "identical except that three machine-specific path strings "
                        "were replaced with repository-relative or <user-home> "
                        "forms; this external digest covers the original."
                    ),
                }
            ],
        },
        "provenance": {
            "repository": "https://github.com/Zhaoyushen-Lab/ANRI-Aerospace.git",
            "git_commit": args.git_commit,
            "created_utc": args.created_utc,
            "author": "ANRI-Aerospace",
            "branch": "feat/research-object-v0.1",
        },
    }

    # The manifest records every frozen artifact, and it also covers the Research
    # Object itself using the documented "self" placeholder: a file cannot contain
    # its own digest, so the object's entry borrows from the object's own record of
    # the manifest, which is concrete. The manifest does not list itself.
    manifest_artifacts = [
        {"path": path, "role": role, "sha256": hashes[path]}
        for path, role in artifacts
        if path not in (MANIFEST_REL, RO_REL)
    ]
    manifest_artifacts.append({"path": RO_REL, "role": "review", "sha256": "self"})

    manifest = {
        "schema_version": "0.2",
        "manifest_type": "research_run_manifest",
        "benchmark_id": "ANRI-RV-001",
        "run_id": "ANRI-RV-001-Ref-01B-clean-and-adversarial",
        "status": "completed",
        "created_utc": args.created_utc,
        "generated_from_commit": args.git_commit,
        "repository": {
            "name": "ANRI-Aerospace",
            "remote": "https://github.com/Zhaoyushen-Lab/ANRI-Aerospace.git",
            "branch": "feat/research-object-v0.1",
            "git_commit": args.git_commit,
        },
        "environment": {
            "os": "Windows",
            "shell": "PowerShell",
            "python": "3.13.14",
            "execution_mode": "local computational benchmark",
            "experimental_validation": False,
            "note": (
                "Host details are recorded here for provenance but are NOT part "
                "of any hashed artifact. Frozen results and reports contain no "
                "timestamp and no machine path."
            ),
        },
        "scope": {
            "configuration_id": "CDFV-001-Ref-01B",
            "benchmark_type": "P002 computational benchmark",
            "purpose": (
                "Verify internal consistency of the CDFV-001 vertical baseline "
                "model and test detection of controlled adversarial mutations."
            ),
            "model_scope": (
                "Quasi-static vertical force balance for a submerged reference "
                "configuration."
            ),
        },
        "reference_configuration": {
            "mass_kg": cfg.mass_kg,
            "diameter_m": cfg.diameter_m,
            "length_m": cfg.length_m,
            "weight_N": verifier.WEIGHT_N,
            "displaced_volume_m3": verifier.DISPLACED_VOLUME_M3,
            "full_buoyancy_N": verifier.FULL_BUOYANCY_N,
            "fluid": "freshwater",
            "fluid_density_kg_m3": cfg.water_density_kg_m3,
            "gravity_m_s2": cfg.gravity_m_s2,
            "force_tolerance_N": verifier.FORCE_TOLERANCE_N,
            "source": "Research_Planning/CDFV-001_Reference_Configuration.md",
        },
        "assumptions": {
            "free_surface_force_N": 0.0,
            "drag_included": False,
            "added_mass_included": False,
            "attitude_effects_included": False,
            "fluid_is_incompressible": True,
            "experimental_validation_completed": False,
            "interpretation": (
                "A PASS establishes computational and internal consistency for "
                "the stated baseline assumptions; it does not establish "
                "experimental validity or complete CDFV vehicle performance."
            ),
        },
        "commands": [
            {
                "purpose": "Verify clean baseline",
                "command": "py -3 ./Models/CDFV-001/Ref-01B/verify_baseline.py",
                "expected_status": "PASS",
            },
            {
                "purpose": "Run verifier negative-case suite",
                "command": "py -3 ./Models/CDFV-001/Ref-01B/verify_negative_cases.py",
                "expected_status": "PASS",
            },
            {
                "purpose": "Regenerate adversarial cases from the clean results",
                "command": (
                    "py -3 ./Benchmarks/ANRI-RV-001/make_adversarial_cases.py "
                    "--source ./Models/CDFV-001/Ref-01B/results "
                    "--dest ./Benchmarks/ANRI-RV-001/adversarial"
                ),
                "expected_status": "completed",
            },
            {
                "purpose": "Run every adversarial case and check it is rejected",
                "command": "py -3 ./Benchmarks/ANRI-RV-001/run_adversarial_cases.py",
                "expected_status": "PASS",
            },
            {
                "purpose": "Validate the Research Object, schema, hashes and gate",
                "command": (
                    "py -3 ./scripts/validate_research_object.py "
                    "./Research_Objects/RO-CDFV-001-Ref-01B.json --repo-root ."
                ),
                "expected_status": "PASS",
            },
            {
                "purpose": "Mutation-test the validator itself",
                "command": (
                    "py -3 ./scripts/validate_gate_selftest.py <scratch-dir>"
                ),
                "expected_status": "PASS",
            },
        ],
        "observed_results": {
            "clean_baseline": {
                "overall_status": "PASS",
                "checks_version": "0.2",
                "maximum_force_balance_residual_N": 3.552713678800501e-15,
                "cases": [
                    {
                        "file": "Models/CDFV-001/Ref-01B/results/Ref-01B-B-0p10mps.csv",
                        "velocity_m_s": 0.10,
                        "rows": 4846,
                        "status": "PASS",
                    },
                    {
                        "file": "Models/CDFV-001/Ref-01B/results/Ref-01B-B-0p25mps.csv",
                        "velocity_m_s": 0.25,
                        "rows": 1940,
                        "status": "PASS",
                    },
                    {
                        "file": "Models/CDFV-001/Ref-01B/results/Ref-01B-B-0p50mps.csv",
                        "velocity_m_s": 0.50,
                        "rows": 971,
                        "status": "PASS",
                    },
                ],
            },
            "verifier_negative_cases": {"case_count": 18, "status": "PASS"},
            "validator_gate_selftest": {"scenario_count": 13, "status": "PASS"},
            "adversarial": {
                "case_count": len(ADVERSARIAL_CASES),
                "status": "PASS",
                "cases": ADVERSARIAL_CASES,
            },
        },
        "artifacts": manifest_artifacts,
        "reproducibility": {
            "frozen_artifacts_are_deterministic": True,
            "frozen_artifacts_contain": "no timestamp, no machine path",
            "line_endings": "LF everywhere; .gitattributes sets * -text",
            "local_metadata": (
                "local_run_meta.json files are git-ignored and never hashed"
            ),
            "self_placeholder": (
                "The object and this manifest record each other's digest. The "
                "object records this manifest's real SHA-256; this manifest "
                "declares the object with the literal 'self', which the "
                "validator accepts only on these two entries."
            ),
            "note": (
                "Every other artifact above is byte-reproducible from the clean "
                "checkout; generating twice must not change any hash."
            ),
        },
        "next_action": (
            "Close the blocking findings of the independent review, then have an "
            "independent reviewer re-review and record a new review entry before "
            "the object may move to review.status = approved."
        ),
    }

    if args.check_only:
        problems: list[str] = []
        for relative, payload in ((RO_REL, research_object), (MANIFEST_REL, manifest)):
            existing = json.loads((REPO / relative).read_text(encoding="utf-8"))
            if existing != payload:
                problems.append(relative)
        if problems:
            print("check-only: FAIL, these files are out of date: " + ", ".join(problems))
            return 1
        print("check-only: PASS, both files are up to date")
        return 0

    # Resolve the manifest's own real digest for the object to record.  Because
    # the object lists the manifest with a real hash, write the manifest twice
    # only if the digest moves; in practice the manifest is deterministic once the
    # artifact set is fixed, so a single pass plus verification is enough.
    MANIFEST_PATH = REPO / MANIFEST_REL
    RO_PATH = REPO / RO_REL
    write_lf(MANIFEST_PATH, json.dumps(manifest, indent=2) + "\n")
    manifest_digest = sha256(MANIFEST_REL)

    for entry in research_object["artifacts"]:
        if entry["path"] == MANIFEST_REL:
            entry["sha256"] = manifest_digest
    write_lf(RO_PATH, json.dumps(research_object, indent=2) + "\n")

    if sha256(MANIFEST_REL) != manifest_digest:
        raise SystemExit("manifest digest changed during generation")

    print(f"wrote {RO_REL}")
    print(f"wrote {MANIFEST_REL}")
    print(f"manifest sha256: {manifest_digest}")
    print(f"artifacts hashed: {len(research_object['artifacts'])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
