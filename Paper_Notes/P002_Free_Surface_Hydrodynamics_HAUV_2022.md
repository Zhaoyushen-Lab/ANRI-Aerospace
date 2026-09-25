# P002 Free Surface Hydrodynamics HAUV 2022

## Metadata

- **Title:** Experimental study on trans-media hydrodynamics of a cylindrical hybrid unmanned aerial underwater vehicle
- **Year:** 2022
- **Relation:** AQ001
- **Status:** Evidence extraction complete; decision candidate pending validation
- **Research object:** Nezha HAUV, represented experimentally by a constrained cylindrical model

---

# 1. Research Question

What physical phenomena dominate HAUV air-water transition, and how should their time-varying forces and moments be represented in the CDFV-001 transition model?

# 2. Why Selected

P002 is a direct evidence source for:

- time-varying hydrodynamic force;
- free-surface interaction and suction;
- acceleration-dependent vertical loading;
- attitude-dependent hydrodynamic moment;
- non-buoyancy effects during water-air transition.

# 3. Abstract Extraction

## Problem

HAUV water-air transition involves strongly nonlinear interaction with a changing fluid environment. The transient forces and moments during the transition are insufficiently measured and understood.

## Method

The authors built a constrained experimental platform that controls velocity, acceleration, and attitude while measuring six-component force and moment data during water exit.

## Findings

1. When velocity exceeds approximately 0.1 m/s, free-surface suction initially increases and then approaches a stable trend. The maximum reported suction force is approximately 10% of vehicle gravity.
2. At accelerations below approximately 0.15 m/s², the vertical force approximately follows a square-of-time trend under the reported conditions.
3. Hydrodynamic moment varies significantly with attitude. Below approximately 15°, the moment first decreases and then increases; at larger attitudes it decreases toward a stable value.
4. Effects other than time-varying buoyancy cannot be ignored.

## Contribution to AQ001

P002 indicates that a useful CDFV transition model must represent free-surface interaction, transient force, attitude-dependent moment, and transition-stage-dependent loading.

---

# 4. Introduction Extraction

## Research Context

HAUVs enable repeated air-water transitions. Multi-rotor HAUVs can provide smooth and controllable transition motion.

## Research Problem and Gap

Earlier work emphasized vehicle motion, trajectory, and kinematics. Direct time-resolved measurement of hydrodynamic forces and moments during free-surface crossing remained limited.

## Contributions

- C1: Develop a hydrodynamic measurement platform.
- C2: Measure force and moment under varying velocity, acceleration, and attitude.
- C3: Analyze free-surface suction and transition-force effects.

# 5. Method Extraction

## Model Simplification

- Research object: Nezha HAUV.
- Experimental representation: vertical cylindrical model.
- Purpose: isolate fundamental transition dynamics before introducing full-vehicle geometry.

## Transition Stages

1. Underwater floating.
2. Near free surface.
3. Surface crossing.
4. Air separation.

## Coordinate and State Representation

- Earth/measurement frame `E`: external measurements.
- Body frame `O`: attached to the vehicle center of mass.
- State quantities: velocity, force, and moment.
- Reported relationship: `v = J^-1 vE`, where `J` is an attitude-dependent transformation.
- Attitude variables reported in the notes: pitch `theta` and yaw `psi`.

**Open data requirement:** record the paper's exact definition of `J`, angle convention, force/moment sign convention, and sensor reference point before implementing equations.

---

# 6. Experimental Setup Extraction

## 6.1 Purpose

The experiment supplies controlled motion, measurable force and moment, and time-resolved data needed to characterize transient transition dynamics.

## 6.2 Platform

The experiment used the Shanghai Jiao Tong University towing tank:

| Parameter | Value |
|---|---|
| Tank length | 110 m |
| Tank width | 6 m |
| Water depth | 3 m |
| Velocity range | 0–0.5 m/s |
| Acceleration range | 0.07–1 m/s² |
| Attitude range | -26° to 26° |
| Attitude accuracy | 0.1° |
| Measurement frequency | 1000 Hz |

The platform includes an actuating motor, sliding module, six-component force balance, transformer, adjustable-angle platform, modular main structure, structural support, and triangular connection module.

## 6.3 Measurement System

The six-component balance measures three force components and three moment components. The exact units, filtering procedure, calibration coefficients, and coordinate transformation must be copied from the corresponding paper section before quantitative reuse.

## 6.4 ANRI Knowledge Object

```yaml
Experimental_Platform:
  purpose: Measure HAUV transition dynamics
  inputs:
    - velocity
    - acceleration
    - attitude
  process: constrained water-exit motion
  measurements:
    - force_x
    - force_y
    - force_z
    - moment_roll
    - moment_pitch
    - moment_yaw
  output: time-varying hydrodynamic force and moment data
  transferability: constrained cylindrical model to be validated on full HAUV
```

---

# 7. Results Extraction

The entries below capture the results stated in the current notes. Replace `Figure/Table: pending` with the exact paper figure or table identifiers before publication.

## 7.1 Velocity Effect

- **Variable:** transition velocity.
- **Observation:** free-surface suction increases after approximately 0.1 m/s and then approaches a stable trend.
- **Quantitative result:** maximum suction is approximately 10% of vehicle gravity under the reported conditions.
- **Figure/Table:** pending exact source identifier.
- **Interpretation:** free-surface interaction contributes a velocity-dependent transient load.
- **CDFV implication:** transition velocity must be an explicit model and experiment parameter.

## 7.2 Acceleration Effect

- **Variable:** transition acceleration.
- **Observation:** under low acceleration, approximately below 0.15 m/s², vertical force follows an approximate square-of-time trend.
- **Figure/Table:** pending exact source identifier.
- **Interpretation:** loading depends on the acceleration profile, not velocity alone.
- **CDFV implication:** acceleration history must be retained in the transition state and experiment record.

## 7.3 Attitude Effect

- **Variable:** vehicle attitude.
- **Observation:** hydrodynamic moment changes non-monotonically with attitude; the reported trend differs below and above approximately 15°.
- **Figure/Table:** pending exact source identifier.
- **Interpretation:** orientation changes the force/moment distribution during free-surface crossing.
- **CDFV implication:** attitude-dependent moment must be represented in stability analysis.

---

# 8. Evidence Cards

## E002-001 — Free-Surface Suction Effect

- **Source:** P002 Results, exact section/figure pending.
- **Type:** experimental force measurement.
- **Observation:** suction increases above approximately 0.1 m/s and then approaches a stable trend.
- **Quantitative result:** approximately 10% of vehicle gravity at the reported maximum.
- **Confidence:** high for the tested model and conditions; medium for full HAUV generalization.
- **Implication:** free-surface interaction must be included in CDFV transition dynamics.

## E002-002 — Acceleration-Dependent Vertical Force

- **Source:** P002 Results, exact section/figure pending.
- **Type:** time-resolved vertical-force measurement.
- **Observation:** at low acceleration, vertical force approximately follows a square-of-time trend.
- **Confidence:** high for the tested conditions; medium outside the tested acceleration range.
- **Implication:** acceleration history is a required input to transition-load modeling.

## E002-003 — Attitude-Dependent Hydrodynamic Moment

- **Source:** P002 Results, exact section/figure pending.
- **Type:** six-component moment measurement.
- **Observation:** moment varies significantly with attitude and changes trend around the reported 15° region.
- **Confidence:** high for the experiment; medium for full-vehicle transfer.
- **Implication:** orientation-dependent moment must be included in transition stability analysis.

---

# 9. Figure and Data Mapping

| Evidence | Required source mapping | ANRI role |
|---|---|---|
| E002-001 | Exact Results figure/table for suction vs. velocity | Direct force evidence |
| E002-002 | Exact Results figure/table for vertical force vs. acceleration/time | Acceleration-load evidence |
| E002-003 | Exact Results figure/table for moment vs. attitude | Stability evidence |
| Calibration | Calibration figure/table and error metric | Evidence reliability |
| Experimental model | Model/platform figure | Research-object definition |
| Typical recording | Force-time recording figure | Time-resolved evidence |

**Completion rule:** no evidence card is considered publication-ready until its source section and figure/table identifier are filled in.

# 10. Decision Candidate

## D002-001 — Transition Model Scope

**Based on:** E002-001, E002-002, and E002-003.

**Decision candidate:** CDFV-001 transition analysis should include free-surface interaction, transient hydrodynamic force, acceleration history, and attitude-dependent moment. A buoyancy-only representation is insufficient for the next modeling stage.

**Status:** Candidate; validate against CDFV-001 geometry and future experiments.

# 11. AQ001 Update

**Previous focus:** general transition hydrodynamic optimization.

**Updated research question:** How can time-varying force and attitude-dependent moment evidence be represented and modeled to support stable CDFV-001 air-water transition?

**Reason for update:** P002 shows that transition loading is coupled to free-surface state, velocity, acceleration history, and attitude.

# 12. Knowledge Update

## Before P002

CDFV transition was represented mainly through buoyancy, vehicle motion, and trajectory.

## After P002

The CDFV knowledge model must explicitly represent:

- transition stage;
- velocity and acceleration history;
- free-surface interaction;
- time-varying force;
- attitude-dependent moment;
- experimental uncertainty and transferability limits.

# 13. Research Impact

P002 supplies an experimental basis for converting transition dynamics from a qualitative motion problem into a measurable force-and-moment modeling problem.

# 14. Limitations

- The model is a simplified cylinder rather than the complete HAUV geometry.
- Motion is constrained and may differ from free-flight transition.
- The tested velocity, acceleration, and attitude ranges are limited.
- Scale effects may limit direct transfer to the full-size vehicle.
- Rotor arms, appendages, and propulsion-induced flow are not fully represented.
- Quantitative reuse requires the paper's exact units, filtering, calibration, and coordinate conventions.
- Results require validation on the CDFV-001 geometry and, ultimately, autonomous transition tests.

# 15. Open Questions for P003

1. Which state variables are sufficient to represent the measured transition loads?
2. How should free-surface suction be parameterized as a function of velocity and stage?
3. How should acceleration history enter the vertical-force model?
4. How should attitude-dependent moment be coupled to the CDFV stability model?
5. Which P002 findings transfer to the full CDFV geometry, and which require new experiments?

# 16. ROS Handoff

```yaml
ResearchObject:
  paper: P002
  question: AQ001
  evidence:
    - E002-001
    - E002-002
    - E002-003
  knowledge_update: KU002-001
  decision_candidate: D002-001
  next_plan: P003
  closure_status: Evidence-to-decision path established; source mapping and CDFV validation pending
```
