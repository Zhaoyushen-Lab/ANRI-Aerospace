# ANRI-RV-001 — CDFV-001 Ref-01B Baseline Verification

## Purpose

ANRI-RV-001 is the first small benchmark for the ANRI research-assurance layer.
It tests whether an agent can inspect a defined computational baseline, run the
verifier, detect injected errors, and report the result with the correct scope.

The benchmark evaluates evidence use, execution trace, error detection, and
limitation reporting. It does not evaluate prose style or the quality of a
research summary.

## Current scope

- Research object: `RO-CDFV-001-Ref-01B`
- Configuration: `CDFV-001-Ref-01B`
- Cases: 0.10, 0.25, and 0.50 m/s
- Model type: computational hydrostatic baseline
- Free-surface force: excluded and fixed at 0 N
- Gravity: `9.80665 m/s^2`, frozen and cross-checked against the model
- Force tolerance: `1e-4 N`
- Experimental validation: not available

## Repository placement

This directory is `Benchmarks/ANRI-RV-001/`. It references the existing files
under `Models/CDFV-001/Ref-01B/` rather than duplicating large CSV files.

## Completion gate

The benchmark is ready for a run when:

1. the clean baseline receives a complete PASS;
2. a changed weight or density is detected as a FAIL;
3. a broken force-balance row is detected as a FAIL;
4. the final report states that the result is computationally consistent but
   not experimentally validated;
5. the run command, inputs, outputs, and verifier report are recorded.

## What is enforced automatically now (v0.2)

| Criterion | Enforced by |
|---|---|
| C01 reference configuration | `scripts/validate_research_object.py` (object vs model constants) |
| C02 required cases | file set + `adversarial_cases.json` source list |
| C03 csv integrity | `verify_baseline.py` (`read_csv`, `non_empty`, numeric columns) |
| C04 monotonic progress | `verify_baseline.py` (`monotonic_time`, `monotonic_position`) |
| C05 weight reference | `verify_baseline.py` (`weight_reference`, `weight_unit_sanity`) |
| C06 buoyancy range | `verify_baseline.py` (`buoyancy_range`, `buoyancy_unit_sanity`) |
| C07 force balance | `verify_baseline.py` (`force_balance`) |
| C08 excluded terms | `verify_baseline.py` (`free_surface_zero`) + object assumptions |
| C09 adversarial detection | `Benchmarks/ANRI-RV-001/run_adversarial_cases.py` |
| C10 limitation propagation | `review.status` gate in the validator + the review record |

## Running the benchmark

```bash
# clean baseline
python Models/CDFV-001/Ref-01B/verify_baseline.py

# all 12 adversarial cases, checking each one fails as intended
python Benchmarks/ANRI-RV-001/run_adversarial_cases.py

# verifier self-tests (18 synthetic cases)
python Models/CDFV-001/Ref-01B/verify_negative_cases.py

# research object, schema, hashes and review gate
python scripts/validate_research_object.py \
  Research_Objects/RO-CDFV-001-Ref-01B.json --repo-root .
```

## Status

v0.2. The clean baseline, the 12-case adversarial set, the 18-case negative
suite and the Research Object validator all run without third-party
dependencies. The independent review gate is at `revision_requested`; see
`Benchmarks/ANRI-RV-001/decision_log.md`.
