# ANRI-RV-001 — CDFV-001 Ref-01B Baseline Verification

## Purpose

ANRI-RV-001 is the first small benchmark for the ANRI research-assurance layer.
It tests whether an agent can inspect a defined computational baseline, run the
verifier, detect injected errors, and report the result with the correct scope.

The benchmark evaluates evidence use, execution trace, error detection, and
limitation reporting. It does not evaluate prose style or the quality of a
research summary.

## Current scope

- Research object: CDFV-001
- Configuration: Ref-01B
- Cases: 0.10, 0.25, and 0.50 m/s
- Model type: computational hydrostatic baseline
- Free-surface force: excluded and fixed at 0 N
- Experimental validation: not available

## Expected repository placement

Copy this directory into the repository as:

```text
Benchmarks/ANRI-RV-001/
```

The benchmark should reference the existing files under
`Models/CDFV-001/Ref-01B/` rather than duplicating large CSV files.

## Two-day completion gate

The benchmark is ready for a first run when:

1. the clean baseline receives a complete PASS;
2. a changed weight or density is detected as a FAIL or WARNING;
3. a broken force-balance row is detected as a FAIL;
4. the final report states that the result is computationally consistent but
   not experimentally validated;
5. the run command, inputs, outputs, and verifier report are recorded.

In v0.1, the existing Python verifier directly covers most of C03–C07.
C01, C02, C08, and C10 are checked from the report and source files. That is
intentional: the first benchmark measures the whole research-assurance task,
not only one numerical script. Automatic enforcement can be added in v0.2.

## Status

Draft v0.1. This benchmark is intentionally narrow and should be expanded only
after the first clean and adversarial runs are reproducible.
