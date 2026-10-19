# ANRI-RV-001 decision log

## Decision

**Decision ID:** D-ANRI-RV-001-001
**Date:** 2026-10-11
**Status:** revision_requested

The CDFV-001 Ref-01B computational baseline is accepted as an internally
consistent baseline *under author self-check only*. The independent review gate
is **not** approved: the independent reviewer returned `REQUEST_CHANGES` with
blocking findings, recorded in
`Reviews/RO-CDFV-001-Ref-01B_Independent_Review_Report.md` and summarised in
`Research_Objects/RO-CDFV-001-Ref-01B.json` under `review`.

## Evidence

- Verifier report: `Models/CDFV-001/Ref-01B/results/verification_report.md`
- Machine-readable report: `Models/CDFV-001/Ref-01B/results/verification.json`
- Verifier self-tests: `Models/CDFV-001/Ref-01B/verify_negative_cases.py`
- Benchmark rubric: `Benchmarks/ANRI-RV-001/rubric.yaml`
- Run manifest: `Benchmarks/ANRI-RV-001/run_manifest.json`
- Adversarial case set: `Benchmarks/ANRI-RV-001/adversarial/adversarial_cases.json`
- Independent review: `Reviews/RO-CDFV-001-Ref-01B_Independent_Review_Report.md`
- Review checklist: `Reviews/RO-CDFV-001-Ref-01B_Review_Checklist.md`

## Findings

- Clean cases: 0.10, 0.25 and 0.50 m/s, all PASS.
- Maximum internal force-balance residual: `3.55271368e-15 N`
  (tolerance `1e-4 N`).
- Near-neutral margin: fully submerged constraint force `-0.2435699 N` against
  weight `19.9074995 N`, about 1.2 %.
- Adversarial cases: 12 cases (A01–A12) spanning all three velocity cases and
  seven fault families; every case is detected by its intended check.
- Verifier negative-case suite: 18 synthetic cases, all as expected.

## Review gate state

| Field | Value |
|---|---|
| `review.status` | `revision_requested` |
| Reviewer | DeepSeek Harness independent review (read-only session) |
| Independent | yes — separate session, no author involvement in the verdict |
| Decision | `request_changes` |
| Report | `Reviews/RO-CDFV-001-Ref-01B_Independent_Review_Report.md` |
| Blocking findings | F1–F4, F6, F9 (see the Research Object `review.reviews[0].blocking_findings`) |

An object may only carry `status: verified` once `review.status` is `approved`.
`scripts/validate_research_object.py` enforces that rule and CI fails otherwise.

## Scope and limitations

- The model is hydrostatic and computational.
- Free-surface force is excluded, set to zero, and now explicitly checked to
  remain zero.
- Drag and added mass are excluded.
- No laboratory measurement has been performed.
- The result must not be described as experimental validation.
- The frozen artifacts contain no timestamp and no machine path, so their
  SHA-256 values are reproducible on Windows and Ubuntu.
- The claim holds only within the near-neutral margin stated above; it is an
  algebraic consistency statement, not a physical validation.

## Next action

Close the blocking findings of
`Reviews/RO-CDFV-001-Ref-01B_Independent_Review_Report.md`, re-run
`scripts/validate_research_object.py`, `verify_baseline.py` and
`verify_negative_cases.py`, then have an independent reviewer re-review and
record a new `review.reviews[]` entry. Define the smallest free-surface loading
sensitivity model only after `review.status` becomes `approved`.
