# ANRI-RV-001 decision log

## Decision

**Decision ID:** D-ANRI-RV-001-001  
**Date:** YYYY-MM-DD  
**Status:** candidate / accepted / rejected

The CDFV-001 Ref-01B baseline is accepted as an internally consistent
computational benchmark under the stated assumptions.

## Evidence

- Verifier report: `Models/CDFV-001/Ref-01B/results/verification_report.md`
- Machine-readable report: `Models/CDFV-001/Ref-01B/results/verification.json`
- Benchmark rubric: `Benchmarks/ANRI-RV-001/rubric.yaml`
- Run manifest: `Benchmarks/ANRI-RV-001/run_manifest.json`

## Findings

- Clean cases: 0.10, 0.25, and 0.50 m/s.
- Internal force-balance residual: record the measured maximum here.
- Adversarial cases detected: record A01–A04 results here.

## Scope and limitations

- The model is hydrostatic and computational.
- Free-surface force is excluded and set to zero.
- Drag and added mass are excluded.
- No laboratory measurement has been performed.
- The result must not be described as experimental validation.

## Next action

Define the smallest free-surface loading sensitivity model and prepare a
laboratory request only after the computational benchmark remains reproducible
on a clean checkout.
