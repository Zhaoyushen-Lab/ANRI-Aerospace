# P003 — CDFV-001 Free-Surface Loading Assessment

## Metadata

- Research object: CDFV-001
- Parent question: AQ001
- Parent decision candidate: D002-001
- Primary evidence: P002, E002-001
- Status: Planned
- Type: Evidence-to-model transfer task
- Revision: v0.1

---

# 1. Research Question

Does the velocity-dependent free-surface loading reported in P002 remain significant for CDFV-001 water-exit conditions?

This is narrower than “optimize the transition.” The task first determines whether the effect must be represented in the CDFV-001 model and, if so, what minimum representation is justified.

# 2. Why This Task Exists

P002 reports that, in the tested cylindrical model:

- suction increases between approximately 0.1 and 0.25 m/s;
- suction is approximately unchanged above 0.25 m/s within the tested range;
- maximum suction is about 10% of vehicle weight;
- the result comes from a constrained experiment and a reported fit.

These results do not establish that the same loading applies to CDFV-001. P003 tests transferability rather than assuming it.

# 3. Parent Evidence and Decision

## 3.1 Parent Evidence

- Evidence ID: E002-001
- Source: P002 Section 4.1.2, Figures 11–12
- Type: time-resolved resultant-force data and suction-force fit
- Limitation: no raw time-series dataset has been recovered or digitized

## 3.2 Parent Decision Candidate

D002-001: CDFV-001 transition analysis should compare a baseline model with a model containing a velocity-dependent free-surface loading term.

Status: Candidate. P003 must provide evidence to accept, reject, or narrow this decision.

# 4. Scope

## Included

- Compare the P002 cylinder and CDFV-001 geometry and transition conditions.
- Determine whether CDFV-001 operates in a velocity regime where P002's effect could matter.
- Define the minimum state variables and loading term needed for a first model comparison.
- Define one validation criterion and the next measurement if analytical transfer is insufficient.

## Excluded

- Claiming that P002 validates CDFV-001.
- Building a full autonomous controller.
- Reconstructing all P002 raw data from plots without recording digitization uncertainty.
- Extrapolating the P002 fit beyond its tested conditions.
- Building an AI agent or a complete ROS platform.

# 5. Working Hypotheses

These are hypotheses to test, not conclusions.

- H1: Free-surface loading is material within at least part of the CDFV-001 operating envelope.
- H2: A first CDFV model can represent the effect as a stage- and velocity-dependent additional vertical load, with explicit validity limits.
- H3: The P002 cylindrical fit cannot be transferred numerically to CDFV-001 without a geometry or experiment correction.

# 6. Inputs Required

## From P002

- E002-001 evidence card.
- P002 Figures 11–12 and captions.
- Tested velocity range: 0.1–0.5 m/s.
- Transition-stage definitions and force notation.
- Model geometry and limitations.

## From CDFV-001

- water-exit velocity range;
- vehicle mass and weight reference;
- body diameter, length, and wetted geometry near the free surface;
- expected attitude during exit;
- current baseline force model;
- target force or stability tolerance;
- available sensor or simulation data.

If an input is unavailable, record “Blocked — source required.” Do not substitute P002 cylinder values.

# 7. Method

## Stage 1 — Regime and Geometry Comparison

Create and fill this table:

| Quantity | P002 cylinder | CDFV-001 | Source / status |
|---|---:|---:|---|
| Water-exit velocity | 0.1–0.5 m/s | Blocked — source required | P002 §4.1 |
| Mass / weight reference | 2.030 kg | Blocked — CDFV mass record required | P002 Table 1 |
| Main diameter | 0.090 m | Not directly applicable until geometry mapping | P002 Table 1 |
| Main length | 0.323 m | Blocked — CDFV geometry record required | P002 Table 1 |
| Attitude condition | 5°–25°, at 0.1 m/s | Blocked — transition attitude required | P002 §4.3 |
| Free-surface load data | Figs. 11–12 | Not yet measured or simulated | P002 §4.1.2 |

Completion condition: every CDFV cell is sourced or explicitly blocked.

## Stage 2 — Baseline Definition

Record the current CDFV baseline, including:

- frame and sign convention;
- gravity and buoyancy terms;
- hydrodynamic terms already included;
- transition-stage definition;
- velocity and attitude inputs;
- output used for the decision.

Do not introduce a new free-surface term before the baseline is recorded.

## Stage 3 — Minimum Model Comparison

Compare the baseline model with a baseline plus candidate free-surface term.

The candidate term must specify:

- velocity definition;
- active transition stage;
- force direction and frame;
- units or normalization;
- validity range;
- uncertainty or confidence statement;
- source and assumptions.

A symbolic term is acceptable initially. Copying P002 numerical coefficients is not acceptable unless geometry and normalization are justified.

## Stage 4 — Validation Choice

Choose one:

1. Analytical screening: show that the term is negligible or potentially material over the CDFV range.
2. Digitized comparison: reproduce the P002 curve with a recorded method and uncertainty.
3. New experiment or simulation: define a CDFV-specific measurement or simulation because transfer cannot be justified analytically.

# 8. Provenance Rules

Every P003 result must identify:

- source file or experiment ID;
- section, figure, table, or dataset;
- geometry and operating condition;
- frame and unit;
- measured, digitized, calculated, or inferred status;
- assumptions and uncertainty;
- relation to E002-001 and D002-001.

Minimum observation record:

Observation ID:
Source:
Condition:
Quantity and unit:
Method:
Observation:
Uncertainty / limitation:
Implication for D002-001:

# 9. Acceptance Criteria

P003 is complete only when:

- CDFV-001 velocity and geometry inputs are sourced or explicitly blocked;
- the current baseline model is documented;
- the candidate free-surface term has frame, units, stage, and validity limits;
- at least one comparison is reproducible from recorded inputs;
- the result states material, immaterial-within-range, or unresolved;
- D002-001 is updated to Accepted, Rejected, or Needs CDFV experiment;
- a subsequent task is created if the result is unresolved.

P003 is not complete if it only says “P002 suggests this is important.”

# 10. Expected Outputs

1. This P003 task file with a progress log.
2. An update to Research_Planning/Decision_Log.md.
3. One provenance-linked comparison table or figure.
4. One CDFV-001 Knowledge Update.
5. A new experiment or modeling task if the result remains unresolved.

# 11. Risks and Controls

| Risk | Control |
|---|---|
| Copying P002 fit directly to CDFV | Require geometry and normalization check |
| Confusing resultant Z with isolated suction | Keep resultant/component labels separate |
| Treating 0.25 m/s as universal | State it is a P002 tested-range observation |
| Hidden coordinate mismatch | Record frame, origin, sign, and moment reference |
| Overfitting digitized plots | Record digitization method and uncertainty |
| Expanding into full ROS software | Keep P003 bounded to one transfer task |

# 12. Decision Update Template

Outcome: Accepted | Rejected | Needs CDFV experiment | Deferred

Evidence reviewed:

Result:

Reason:

New assumptions:

Next task:

# 13. Knowledge Update Template

Knowledge Update ID: KU003-001

Before:

After:

Evidence:

Validity range:

Open limitation:

# 14. Progress Log

| Date | Action | Result | Commit |
|---|---|---|---|
| 2026-09-26 | Created P003 from D002-001 | Scope defined; CDFV inputs not yet filled | To record |

# 15. ROS Handoff

ResearchObject:
  plan: P003
  parent_paper: P002
  parent_evidence: E002-001
  parent_decision: D002-001
  target: CDFV-001
  question: transferability of velocity-dependent free-surface loading
  status: planned
  required_output: bounded model comparison or CDFV experiment specification
  completion_gate: update D002-001 and KU003-001

# 16. First Action

Fill the Stage 1 comparison table from actual CDFV-001 project records. If the velocity range, geometry, or baseline model is unavailable, create a blocker entry instead of guessing. Do not advance to a numerical free-surface term until those inputs are sourced.
