# P002 Free Surface Hydrodynamics HAUV 2022

## Metadata

- Title: Experimental study on trans-media hydrodynamics of a cylindrical hybrid unmanned aerial underwater vehicle
- Authors: Tongjin Wei et al.
- Year: 2022
- Journal: Ocean Engineering 252, 111190
- DOI: https://doi.org/10.1016/j.oceaneng.2022.111190
- Relation: AQ001
- Status: Source-mapped literature extraction; modeling checks and CDFV validation remain open
- Revision: resolved_v2; original 1–16 section structure restored
- Source convention: page numbers below refer to the supplied 15-page PDF, matching its printed page numbers.
- Evidence convention: paper observations, author interpretations, and ANRI proposals are distinguished. No raw experimental dataset has been recovered or digitized.

---

# 1. Research Question

What physical phenomena dominate HAUV air-water transition?

Working ANRI extension: Which measured transition phenomena should be considered when defining the CDFV-001 model? This is a research question, not an established design requirement.

# 2. Why Selected

Direct evidence source for:

- time-varying force during constrained water exit;
- free-surface interaction and suction;
- acceleration-dependent resultant force;
- attitude-dependent moment.

Primary scope: a cylindrical model representing the Nezha main body. Applicability to CDFV-001 requires separate assessment.

# 3. Abstract Extraction

## Problem

The paper investigates nonlinear water-air transition and its time-varying forces and moments.

## Method

A constrained-motion platform measures forces and moments while varying velocity, acceleration, and attitude.

## Findings

Source: Abstract, p. 1; detailed support in Sections 4.1–4.3.

1. Suction increases with velocity between approximately 0.1 and 0.25 m/s, then remains approximately unchanged above 0.25 m/s in the studied range. The reported maximum is about 10% of vehicle weight, not 10% of gravitational acceleration.
2. Under low-acceleration conditions, the resultant vertical force is approximately proportional to time squared. Section 4.2 tests 0.07–0.15 m/s²; this is not a universal force law.
3. Moment time histories differ with attitude. Section 4.3 distinguishes small-angle behavior from the 20°–25° cases; this describes evolution over time at fixed attitudes, not a simple moment-versus-angle function.
4. The authors interpret the larger-angle behavior as evidence that moments from hydrodynamic effects other than time-varying buoyancy cannot be ignored.

## Contribution to AQ001

ANRI interpretation: examine whether free-surface effects, acceleration-dependent loading, and attitude-dependent moment are needed in the CDFV-001 model.

## Evidence Status

- Source mapping: established for the three core evidence cards.
- Quantitative reuse: limited by plotting, measurement/reference conventions, and incomplete uncertainty information.
- CDFV transfer: not established by P002.
- No unconditional “High confidence” rating is assigned solely because the observations are experimental.

# 4. Introduction Extraction

## Research Context

HAUVs can operate in air and water and cross the interface. The study focuses on constrained water exit of a cylindrical HAUV representation.

## Research Problem

The transition includes underwater motion, near-surface motion, surface crossing, and separation from the free surface.

## Existing Limitations and Research Gap

Source: Section 1, pp. 1–2. The authors identify a shortage of direct HAUV transition-force and moment measurements relative to motion/trajectory studies. This is the paper's literature assessment, not a claim that no related measurements exist anywhere.

## Contributions

- C1: Develop the measurement platform.
- C2: Obtain time-varying force and moment data under controlled conditions.
- C3: Analyze suction and free-surface phenomena.

# 5. Method Extraction

## Model Simplification

Source: Section 2.1, pp. 2–3; Fig. 1; Section 3.2, p. 5.

- Research object: Nezha HAUV.
- Simplification: cylindrical main-body model.
- Purpose: isolate basic water-exit behavior before broader geometry studies.
- The paper also includes a limited with-arms comparison; it is incorrect to say arms were never tested.

## Transition Process Decomposition

Source: Section 2.1, p. 3.

1. Vertical floating / underwater stage.
2. Motion near the free surface.
3. Crossing the free surface.
4. Separation from the free surface / air stage.

## State Representation

Velocity, force, and moment must carry explicit frame labels.

## Coordinate System Representation

### Frames

Source: Section 2.2, pp. 3–4; Fig. 2, p. 3.

- E: measuring frame.
- O: body frame; the text places O at the vehicle center of mass.
- Attitude notation: (0, theta, psi).

### State Variables

- Measuring-frame velocity: vE = (uE, vE, wE)^T.
- Body-frame velocity: v = (u, v, w)^T.
- Measuring-frame force: FE = (XE, YE, ZE)^T.
- Body-frame force: F = (X, Y, Z)^T.
- Measuring-frame moment: ME = (KE, ME, NE)^T.
- Body-frame moment: M = (K, M, N)^T.

### Transformation

The paper gives v = J^-1 vE and prints J on p. 4.

Source status: located, not absent. Implementation status: review required. The previous transcription's J(1,3) term contains an additional sin(psi), which raises a rotation-matrix consistency concern. Do not silently replace it with a conventional matrix or use that transcription in code; compare the printed expression and Fig. 2, then document any proposed correction separately.

The relation between the sensor moment reference point and the body-frame origin also needs explicit resolution before modeling. The text places O at the center of mass, while Table 1 lists a nonzero center-of-gravity position. Do not assume these refer to identical origins.

### ANRI Relevance

Keep measured Z/ZE and M distinct from isolated hydrodynamic components. A measured resultant may contain gravity, buoyancy, and other contributions.

# 6. Experimental Setup Extraction

## 6.1 Purpose of Experiment

Obtain time-resolved force and moment under controlled water-exit motion.

### ANRI Interpretation

The setup links a research question to controlled inputs and measurable outputs; it does not itself establish a CDFV design decision.

## 6.2 Experimental Platform

### Platform Overview

Source: Section 3.1, pp. 4–5; Figs. 3–4.

Shanghai Jiao Tong University towing tank: 110 m long, 6 m wide, 3 m water depth. Components include actuating motor, sliding module, six-component balance, transformer, adjustable-angle platform, modular structure, supports, and triangular connection module.

### Experimental Capability

| Parameter | Reported capability |
|---|---|
| Velocity | 0–0.5 m/s |
| Acceleration | 0.07–1 m/s² |
| Attitude adjustment | -26° to 26° |
| Attitude accuracy | 0.1° |
| Balance sampling | 1000 Hz |
| Speed deviation | Supplier estimate below 5% at design load |

Platform capability must not be confused with the stable experimental range: acceleration results were reported for 0.07–0.15 m/s²; vibration degraded data at 0.2 m/s² or greater.

### Measurement System

Three force and three moment components. Sources: Section 3.1; coordinate definitions in Section 2.2. Figures use force-time and moment-time curves; values should retain the paper's axis units when digitized.

### Calibration and Repeatability

- Section 3.1, pp. 4–5, Fig. 5(a): add 300 g increments and record balance output.
- Levelness calibration using a level instrument.
- Fig. 5(b), p. 5: sphere water-exit comparison with Ni (2018) simulations at Froude numbers 0.16 and 0.41; maximum deviation 7.7%.
- The 7.7% figure is comparison deviation, not a universal sensor uncertainty bound.
- Section 4.1, p. 6, Fig. 8: three runs per velocity case; reported repeatability error no more than 15%, with early braking affecting one run.
- Early processing considered averaging; later results show a single run. Fig. 11 aligns time origins for comparison.
- Digital filter specification and complete uncertainty budget: not identified in the supplied paper.

### Model Parameters

Source: Section 3.2, Table 1, p. 5; Fig. 6.

| Parameter | Value | Unit |
|---|---|---|
| Mass | 2.030 | kg |
| Listed center-of-gravity position | (0, 0, -0.175) | m |
| Ix | 0.147 | kg·m² |
| Iy | 0.145 | kg·m² |
| Diameter | 0.090 | m |
| Length | 0.323 | m |

The authors state that main dimensions and selected physical properties match Nezha's main body. The earlier blanket claim that this was a smaller-scale vehicle model was unsupported.

### Connecting Rods

Section 3.3, pp. 5–6, Fig. 7: 1.0 m for basic uniform-velocity tests, 0.1 m for uniform-acceleration tests, 0.30 m for constant-velocity attitude tests. Rod length is not automatically identical to the definition of immersion depth.

### ANRI Knowledge Object

```yaml
Experimental_Platform:
  purpose: Measure constrained HAUV water-exit loads
  inputs: [velocity, acceleration, attitude]
  measurements: [force, moment]
  sampling_hz: 1000
  output: time-resolved load curves
  source: P002 Sections 3.1-3.3
  transferability: requires CDFV-specific assessment
```

# 7. Results Extraction

## 7.1 Velocity Effect

- Sources: Section 4.1, p. 6; Section 4.1.2, pp. 9–11; Figs. 11–12.
- Conditions: uniform water exit, 0.1–0.5 m/s in 0.05 m/s increments.
- Fig. 11, p. 9: resultant Z versus time; time origins shifted for comparison.
- Fig. 12, p. 9, with explanation on p. 10: suction increases for 0.1 < w < 0.25 m/s and is approximately unchanged above 0.25 m/s in the tested range.
- Reported maximum: approximately 10% of vehicle weight.
- Reported fit statistics: R² = 0.9721; SSE = 0.03391. These describe the fit, not CDFV prediction accuracy.
- Author interpretation: free-surface interaction produces the suction phenomenon.
- ANRI implication: consider a velocity-dependent free-surface contribution; do not treat 0.25 m/s as a universal operating recommendation.
- Additional sources: Figs. 9–10, pp. 7–8, for images; Fig. 13, p. 10, is water-entry data, not the principal water-exit source.

## 7.2 Acceleration Effect

- Source: Section 4.2, p. 11; Figs. 15–16, p. 11.
- Conditions: uniform acceleration 0.07–0.15 m/s², interval 0.01 m/s²; reported initial depth 0.1 m.
- Observation: larger acceleration shortens water-exit time and increases the rate of resultant-force change. At low acceleration the resultant force is approximately quadratic in time.
- Boundary: vibration at acceleration 0.2 m/s² or greater degrades the data; resonance is the authors' suggested explanation.
- Correction: the preceding statement “test velocity 0.1 m/s” belongs to the arm comparison, not to these accelerating runs.
- ANRI implication: investigate acceleration-dependent loading without fitting a universal time-squared law from the abstract alone.

## 7.3 Attitude Effect

- Source: Section 4.3, pp. 13–14; Figs. 17–21, pp. 11–13.
- Conditions: wE = 0.1 m/s; attitudes 5°–25° in 5° increments; initial depth 0.3 m. Fig. 19 also includes the 0° comparison.
- Each attitude was separately calibrated with supplier assistance due to center-of-gravity/balance alignment effects.
- Fig. 20: M versus time differs between smaller attitudes and the 20°–25° cases. The paper describes a decrease/recovery pattern below 15° and a more direct decrease at 20°–25°; do not infer a precisely established continuous threshold from these discrete tests.
- Fig. 21: at 25°, moment changes settle over a shorter interval than force changes.
- Author interpretation: non-buoyancy hydrodynamic moments matter at larger attitudes.
- ANRI implication: compare buoyancy-based and extended moment models within these conditions.

## 7.4 Supplemental Arm Comparison

Source: Fig. 14, p. 10; discussion in Section 4.1.2, p. 11. At 0.1 m/s, the authors report arm effects concentrated around 0.5–1.0 s apart from weight differences. This is a limited comparison, not full validation of all appendage or propulsion effects.

# 8. Evidence Cards

## E002-001 — Free-Surface Suction Effect

- Source: Section 4.1.2, pp. 9–10; Figs. 11–12, p. 9.
- Evidence type: experimental resultant-force histories and author-extracted suction-versus-velocity fit.
- Conditions: water exit at 0.1–0.5 m/s, 0.05 m/s increments.
- Observation/result: growth between 0.1 and 0.25 m/s, approximate plateau above 0.25 m/s; maximum about 10% of weight.
- Reliability: source verified; general measurement caveats in Section 6 apply. No raw data independently checked.
- ANRI inference: assess a velocity-dependent free-surface model contribution.
- Status: source mapped; CDFV relevance unvalidated.

## E002-002 — Acceleration-Dependent Vertical Force

- Source: Section 4.2, p. 11; Figs. 15–16.
- Evidence type: resultant Z-time measurements under controlled acceleration.
- Conditions: 0.07–0.15 m/s², increments 0.01 m/s²; initial depth 0.1 m.
- Observation: nonlinear resultant-force evolution, approximately quadratic in time at low acceleration.
- Reliability: high-acceleration data degraded by vibration; no universal fit or error bound for the time-squared relation established here.
- ANRI inference: retain acceleration conditions in model comparison and evidence records.
- Status: source mapped; extrapolation unsupported.

## E002-003 — Attitude-Dependent Hydrodynamic Moment

- Source: Section 4.3, pp. 13–14; Figs. 19–21, p. 13.
- Evidence type: force/moment time histories at fixed attitudes.
- Conditions: wE = 0.1 m/s; 5°–25° in 5° steps; initial depth 0.3 m.
- Observation: moment-history patterns differ with attitude; Fig. 21 compares force and moment settling at 25°.
- Author interpretation: additional hydrodynamic moments beyond buoyancy matter at larger attitudes.
- ANRI inference: evaluate an extended moment model; do not equate measured M with a separately isolated non-buoyancy moment.
- Status: source mapped; moment-reference convention needs modeling review.

## E002-004 — Supplemental Arm Effect

- Source: Fig. 14, p. 10; Section 4.1.2, p. 11.
- Conditions: cylinder with/without arms at 0.1 m/s.
- Observation: reported arm influence concentrated around 0.5–1.0 s apart from weight effects.
- ANRI inference: include geometry/appendage applicability checks.
- Status: supplemental evidence; original E002-001–003 IDs unchanged.

# 9. Figure and Data Mapping

| Object | Section / PDF page | Figure or table |
|---|---|---|
| Frames and transformation | 2.2 / pp. 3–4 | Fig. 2; J printed p. 4 |
| Platform and fixation | 3.1 / p. 4 | Figs. 3–4 |
| Calibration | 3.1 / pp. 4–5 | Fig. 5 |
| Model and properties | 3.2 / p. 5 | Fig. 6; Table 1 |
| Rod arrangements | 3.3 / pp. 5–6 | Fig. 7 |
| Repeat recordings | 4.1 / p. 6 | Fig. 8 |
| Free-surface images | 4.1.1 / pp. 6–9 | Figs. 9–10, pp. 7–8 |
| E002-001 | 4.1.2 / pp. 9–10 | Figs. 11–12, p. 9 |
| Water-entry comparison | 4.1.2 / pp. 10–11 | Fig. 13, p. 10 |
| E002-002 | 4.2 / p. 11 | Figs. 15–16 |
| E002-003 | 4.3 / pp. 13–14 | Figs. 19–21, p. 13 |
| Attitude images | 4.3 | Fig. 17, p. 11; Fig. 18, p. 12 |
| E002-004 | 4.1.2 / pp. 10–11 | Fig. 14, p. 10 |

Source mapping does not mean raw data are available. Numerical curve reuse requires documented digitization or an author-supplied dataset, including units and uncertainty.

# 10. Decision Candidate

## D002-001 — Transition Model Scope

- Based on: E002-001, E002-002, E002-003; supplemental E002-004.
- Candidate decision: compare a gravity/buoyancy baseline with models including free-surface and other transient load contributions under clearly specified conditions.
- Reason: the reported suction and attitude-dependent moment behavior justify investigating those additions.
- Status: proposed, not an accepted engineering requirement.
- Next action: choose one measurable comparison and verify its frame, units, geometry, and source data.
- Acceptance condition: record the actual AQ001 scope and approve a bounded follow-up task in the project Decision Log.

# 11. AQ001 Update

Previous formulation: retain the actual wording from the AQ001 record; it is not reproduced as a historical fact here.

Proposed refinement: Which measured transient forces or moments require additions to a gravity/buoyancy baseline for the chosen CDFV-001 water-exit conditions?

Reason: P002 supplies bounded experimental evidence for assessing model scope.

Status: proposal in this paper note only. The separate AQ001 record has not been edited by this document.

# 12. Knowledge Update

## Before P002

The previous project knowledge state must be checked against its actual record. Do not retrospectively assert that CDFV used only buoyancy unless that was documented.

## After P002

Proposed KU002-001:

- Source-backed findings are available for suction, accelerating water exit, and attitude-dependent moment.
- Their conditions and limitations must travel with each claim.
- Frame, resultant/component distinction, geometry, and calibration are required metadata for reuse.
- CDFV applicability remains an open question rather than an established result.

Updated objects proposed: AQ001, D002-001, and the next research task. No external project file is claimed to have been updated.

# 13. Research Impact

P002 provides a traceable experimental basis for refining a transition-model question. Its contribution to ANRI is the connection between a source figure, a bounded claim, an explicit limitation, and a candidate next action.

It does not by itself demonstrate CDFV stability, validate a full ROS platform, or close the research loop. Closure additionally requires an accepted decision and an executable follow-up recorded in the project.

# 14. Limitations

## Reported Experimental Limitations

- Constrained motion and cylindrical main-body representation.
- Connecting rod influences moment as the upper surface exits water (Section 3.2).
- Platform vibration degrades data at acceleration >= 0.2 m/s² (Section 4.2).
- Repeatability and manually controlled braking issues (Section 4.1).
- Limited with-arms comparison; further arm studies and vibration reduction are future work (Section 5).

## ANRI Reuse Limitations

- Transfer to other geometry and autonomous transition is not established.
- No blanket smaller-scale claim: Section 3.2 reports matching Nezha main-body properties.
- Digital filtering details and a complete uncertainty budget were not identified in this PDF.
- Matrix consistency and moment-reference conventions require review before implementation.
- Published plots are not raw experimental time-series data.
- Fitted curves and reported trends should not be extrapolated beyond their supported conditions.

# 15. Open Questions for P003

P003 here retains the prior note's handoff label; if P003 is reserved for the next paper in the repository, assign the modeling task a separate task ID instead.

1. Which narrow AQ001 question will the next paper or task answer?
2. Which P002 claim best supports that question: suction, acceleration, or moment?
3. What are the exact force/moment reference conventions and the valid coordinate transformation?
4. Can the relevant curve be reused from a documented dataset or responsibly digitized?
5. How does CDFV geometry differ from the tested cylinder and arm configuration?
6. What observation would support or reject the proposed baseline-model extension?

Minimum next task: choose one evidence card, define one testable question, specify the required data and completion criterion, and link it to the accepted decision.

# 16. ROS Handoff

```yaml
ResearchObject:
  paper: P002
  question: AQ001
  evidence:
    - E002-001
    - E002-002
    - E002-003
  supplemental_evidence:
    - E002-004
  knowledge_update:
    id: KU002-001
    status: proposed
  decision_candidate:
    id: D002-001
    status: proposed
  next_plan:
    label: P003
    status: scope_and_repository_ID_to_confirm
  source_mapping: established
  quantitative_model_reuse: requires_convention_and_data_checks
  cdfv_transfer: unvalidated
  closure_status: decision_acceptance_and_executable_followup_required
```
