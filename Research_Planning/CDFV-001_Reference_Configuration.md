# CDFV-001 Reference Configuration

## Metadata

- Configuration ID: CDFV-001-Ref-01
- Version: v0.3
- Status: Benchmark defined; scaled experiment candidate under review
- Defined by task: P003-A
- Parent question: AQ001
- Related decision: D002-001
- Reference evidence: P002 / E002-001

## 1. Purpose

Define a minimal reference configuration for investigating
free-surface loading during vertical water exit.

This configuration is a research model.
It is not a finalized flight-vehicle design.

## 2. Research Question

What configuration and operating conditions are needed to compare
a baseline load model with a model containing an additional
free-surface contribution?

## 3. Proposed Scope

- Motion: prescribed vertical water exit
- Attitude: fixed for the initial study
- Geometry: one simplified main body
- Propulsion: outside the initial scope
- Primary output: vertical load during transition
- Initial method: analytical or numerical study

These choices are proposed assumptions, not measured properties.

## 4. Configuration Decisions

| Item | Proposed choice | Reason | Status |
|---|---|---|---|
| Motion | Prescribed vertical motion | Limit the initial question | Proposed |
| Geometry | Cylinder as first candidate | Enable comparison with P002 | Proposed |
| Attitude | Fixed upright orientation | Isolate the first comparison | Proposed |
| Arms and appendages | Excluded initially | Limit initial geometry complexity | Proposed |
| Physical prototype | Not required for this version | Begin with a reference model | Proposed |

## 5. Parameter Register

## CDFV-001-Ref-01B — P002 Computational Benchmark

### Purpose

Ref-01B is a literature-based computational benchmark.
It is used to test the baseline modeling workflow against
the conditions reported in P002.

It is not a finalized CDFV-001 vehicle design and does not
represent a CDFV-specific experimental validation.

### Source

- Primary source: P002
- Geometry and physical parameters: P002 Table 1
- Coordinate definitions: P002 Section 2.2
- Experimental platform: P002 Section 3.1
- Velocity conditions: P002 Section 4.1
- Attitude conditions: P002 Section 4.3
- Suction-force evidence: P002 Figures 11–12

### Confirmed Parameters

| Parameter | Value | Basis | Status |
|---|---:|---|---|
| Body diameter | 0.090 m | P002 Table 1 | Literature reference |
| Body length | 0.323 m | P002 Table 1 | Literature reference |
| Model mass | 2.030 kg | P002 Table 1 | Literature reference |
| CG position | (0, 0, -0.175) m | P002 Table 1 | Coordinate review required |
| Ix | 0.147 kg·m² | P002 Table 1 | Literature reference |
| Iy | 0.145 kg·m² | P002 Table 1 | Literature reference |
| Water-exit velocity | 0.1–0.5 m/s | P002 Section 4.1 | Literature reference |
| Velocity interval | 0.05 m/s | P002 Section 4.1 | Literature reference |
| Initial attitude | 0° for first benchmark | Research simplification | Proposed |
| Fluid | Fresh water assumption | Modeling assumption | Provisional |
| Free-surface term | Excluded from baseline | Model definition | Defined |

### Parameters Not Yet Used

| Parameter | Status | Reason |
|---|---|---|
| Initial immersion depth | Open | P002 conditions vary between experiments |
| Digital filter | Not reported in P002 | Cannot be reconstructed reliably |
| Complete force/moment transformation | Review required | Coordinate convention must be confirmed |
| Propulsion thrust | Not modeled | Motion is treated as prescribed |
| CDFV-specific geometry | Not represented | Ref-01B is a P002 benchmark |
| Hydrodynamic resistance coefficient | Blocked — source required | No coefficient selected yet |

### Derived Geometry and Buoyancy Estimate

The external cylindrical volume is estimated as:

V = pi × (D / 2)^2 × L

Using:

- D = 0.090 m
- L = 0.323 m

The estimated volume is approximately:

V ≈ 0.002055 m³

Under a provisional freshwater assumption:

- water density = 1000 kg/m³
- gravitational acceleration = 9.81 m/s²

Estimated fully submerged buoyancy:

B ≈ 20.16 N

Estimated model weight:

W = m × g ≈ 19.91 N

This estimate suggests near-neutral or slightly positive buoyancy
under the stated assumptions.

This buoyancy estimate is calculated from the external cylindrical
dimensions and a freshwater assumption. It is not a directly reported
P002 measurement and must not be treated as validated CDFV data.

## Ref-01B Motion Scenario

### Motion Type

- Transition type: vertical water exit
- Primary degree of freedom: vertical translation
- Attitude: fixed upright reference attitude
- Motion profile: prescribed velocity or prescribed acceleration
- Fluid surface: initially calm
- Primary output: vertical force during transition

### Initial Research Boundary

Included:

- vertical water-exit motion;
- free-surface interaction;
- vertical resultant force;
- velocity-dependent loading;
- baseline-versus-extended model comparison.

Excluded:

- horizontal motion;
- water entry;
- changing attitude;
- autonomous control;
- rotor thrust modeling;
- arm and appendage effects;
- full six-degree-of-freedom dynamics;
- complete flight-vehicle design.

## Ref-01B Baseline Model

The first baseline model excludes free-surface loading.

State variables:

- vertical position: z(t)
- vertical velocity: v(t)
- vertical acceleration: a(t)

The general baseline force interface is:

F_baseline =
    F_gravity
  + F_buoyancy
  + F_inertial
  + F_resistance

The free-surface term is initially set to:

F_free_surface = 0

The extended model will later compare:

F_extended =
    F_baseline
  + F_free_surface(z, v)

The exact hydrodynamic-resistance coefficient has not yet been
selected. No coefficient should be invented before a source or
explicit modeling assumption is recorded.

### Baseline Modeling Assumptions

- Motion is prescribed rather than generated by a detailed propulsion model.
- The first output is vertical resultant force.
- Attitude remains fixed.
- P002 geometry is used as a literature benchmark.
- The baseline does not claim to reproduce the complete P002 force curve.
- Free-surface loading is evaluated as a separate candidate contribution.

## Representative Benchmark Cases

| Case | Velocity | Purpose | Status |
|---|---:|---|---|
| B-01 | 0.10 m/s | P002 lower velocity region | Defined |
| B-02 | 0.25 m/s | Approximate transition to suction plateau | Defined |
| B-03 | 0.50 m/s | Upper tested velocity | Defined |

For each case, record:

- prescribed velocity;
- prescribed acceleration, if available;
- assumed water density;
- initial immersion condition;
- calculated buoyancy;
- calculated weight;
- included baseline terms;
- excluded free-surface term;
- missing coefficients or assumptions.

If the initial immersion depth or acceleration profile is unavailable,
record:

Blocked — source required

Do not infer initial immersion depth from the length of the connecting
rod used in P002.

## Ref-01B Completion Criteria

Ref-01B is complete when:

- all benchmark parameters have a source or explicit assumption;
- derived quantities can be recalculated;
- coordinate, unit, and sign conventions are recorded;
- the baseline and extended model boundaries are explicit;
- the three representative velocity cases are defined;
- missing coefficients are explicitly identified;
- no P002 result is presented as a CDFV-001 validation result.

### Status

```yaml
configuration_id: CDFV-001-Ref-01B
type: P002 computational benchmark
status: computational benchmark defined
experimental_validation: deferred
cdfv_transfer: not established
free_surface_term: excluded from baseline
next_task: define and run baseline sensitivity analysis
```

## 6. Baseline Model Interface

Before implementing equations, specify:

- coordinate origin and positive direction;
- prescribed motion and initial conditions;
- included force contributions;
- predicted output;
- force measurement/reference convention;
- assumptions and validity limits.

## 7. Acceptance Criteria for P003-A

- The research purpose is explicit.
- Geometry and operating conditions are selected.
- Each selected value has a source or design rationale.
- Assumptions are distinguished from measurements.
- Inputs are sufficient to begin P003-B.
- The accepted configuration version is recorded.

## 8. Limitations

Results for this reference configuration do not establish
the performance of a complete CDFV vehicle.

## 9. Revision Log

Record each configuration change, its reason,
and the downstream models or tasks affected.
| v0.3 | Added P002 benchmark and 0.5-scale experimental candidate | Separate computational benchmark from manufacturable test model |


## 10. Research Scenario

The first CDFV-001 study investigates vertical water-exit
transition under fixed attitude.

The purpose is to determine whether a free-surface loading term
should be added to the baseline transition model.

This is a research reference configuration,
not a finalized flight-vehicle design.

## 11. Motion Scenario

- Transition type: water exit
- Motion direction: vertical
- Primary degree of freedom: vertical translation
- Attitude: fixed
- Initial attitude: upright reference attitude
- Motion profile: prescribed velocity or prescribed acceleration
- Water condition: initially calm free surface
- Primary output: vertical force during water exit

## 12. Geometry Strategy

The first reference body adopts the P002 cylindrical model
as a literature-referenced research geometry.

This choice is made to:
- preserve direct comparability with P002;
- reduce the number of unknown geometric variables;
- establish a reproducible baseline before introducing
  non-cylindrical geometry, arms, or propulsion effects.

The P002 geometry is not claimed to be the final CDFV-001 geometry.

## 13. Initial Research Boundary

Included:

- vertical water-exit motion;
- free-surface interaction;
- vertical resultant force;
- velocity-dependent loading;
- baseline-versus-extended model comparison.

Excluded from the first study:

- horizontal motion;
- water entry;
- changing attitude;
- autonomous control;
- rotor thrust modeling;
- arm and appendage effects;
- full six-degree-of-freedom dynamics;
- complete flight-vehicle design.

## 14. System Boundary

The first model contains:

- a rigid reference body;
- gravity;
- buoyancy;
- basic hydrodynamic resistance;
- optional free-surface loading term.

The first model does not claim to represent:

- propulsion-induced flow;
- flexible structures;
- autonomous control;
- complete CDFV aerodynamics;
- full-scale vehicle performance.

## 15. Required Outputs

The study should produce:

- vertical position over time;
- vertical velocity over time;
- vertical acceleration over time;
- resultant vertical force;
- comparison between baseline and extended models;
- validity limits and unresolved assumptions.

## 16. Initial Design Constraints

| Constraint | Initial decision | Status |
|---|---|---|
| Transition type | Vertical water exit | Defined |
| Attitude | Fixed upright reference attitude | Defined |
| Main geometry | P002 cylindrical reference body | Proposed |
| Arms and appendages | Excluded initially | Defined |
| Motion complexity | One translational degree of freedom | Defined |
| Fluid state | Initially calm free surface | Proposed |
| Propulsion | Represented as prescribed input, not modeled in detail | Proposed |
| Primary measurement | Vertical resultant force | Defined |
| Free-surface term | Excluded from baseline; tested in extended model | Defined |

## 17. Reference Configuration Parameters

### 17.1 P002 Benchmark Configuration

- Configuration ID: CDFV-001-Ref-01B
- Purpose: Literature benchmark and model reproduction
- Scale ratio: 1.0
- Status: Accepted as computational benchmark
- Source: P002 Table 1 and Section 4.1

| Parameter | Value | Basis | Status |
|---|---:|---|---|
| Body diameter | 0.090 m | P002 Table 1 | Literature reference |
| Body length | 0.323 m | P002 Table 1 | Literature reference |
| Mass | 2.030 kg | P002 Table 1 | Literature reference |
| CG position | (0, 0, -0.175) m | P002 Table 1 | Coordinate review required |
| Ix | 0.147 kg·m² | P002 Table 1 | Literature reference |
| Iy | 0.145 kg·m² | P002 Table 1 | Literature reference |
| Water-exit velocity | 0.1–0.5 m/s | P002 Section 4.1 | Literature reference |
| Initial attitude | 0° | Initial research simplification | Proposed |
| Initial immersion | Not selected | Must not be inferred from rod length | Open |
| Fluid properties | Fresh water; temperature not yet specified | Experiment definition | Open |

### 17.2 Scaled Experimental Candidate

- Configuration ID: CDFV-001-Ref-01S
- Purpose: Manufacturable single-axis water-exit experiment
- Scale ratio: 0.5
- Similarity priority: Froude similarity
- Status: Candidate — hardware feasibility not yet checked

| Parameter | Candidate value | Derivation | Status |
|---|---:|---|---|
| Body diameter | 0.045 m | 0.5 × 0.090 m | Candidate |
| Body length | 0.1615 m | 0.5 × 0.323 m | Candidate |
| Mass | 0.254 kg | 0.5³ × 2.030 kg | Candidate |
| CG z-coordinate | -0.0875 m | 0.5 × -0.175 m | Coordinate review required |
| Ix | 0.00459 kg·m² | 0.5⁵ × 0.147 kg·m² | Candidate |
| Iy | 0.00453 kg·m² | 0.5⁵ × 0.145 kg·m² | Candidate |
| Water-exit velocity | 0.071–0.354 m/s | sqrt(0.5) × P002 range | Candidate |
| Initial attitude | 0° | Initial research simplification | Proposed |
| Initial immersion | Not selected | Must satisfy model and tank constraints | Open |
| Fluid properties | Fresh water; temperature to be measured | Experiment definition | Open |

### 17.3 Scaling Rules

The scaled candidate uses geometric similarity and prioritizes
Froude similarity:

- Length scale: Ls = λLp
- Velocity scale: vs = sqrt(λ)vp
- Time scale: ts = sqrt(λ)tp
- Mass scale: ms = λ³mp
- Force scale: Fs = λ³Fp
- Moment scale: Ms = λ⁴Mp
- Inertia scale: Is = λ⁵Ip

These relations are candidate design assumptions.
Reynolds, Weber, and Bond similarity are not simultaneously preserved.

### 17.4 Acceptance Conditions for Ref-01S

Ref-01S may be accepted for experiment only after confirming:

- model fits the available manufacturing process;
- model fits the water tank;
- vertical travel is sufficient;
- actuator reaches the required velocity;
- load-cell range and resolution are sufficient;
- required ballast can reproduce the target mass and CG;
- Reynolds and surface-tension effects remain acceptable;
- expected force is above the measurement-noise floor.

## 18. Baseline Model Definition

The first baseline model will exclude free-surface loading:

m z_ddot = T(t) + B(z) - m g - D(z_dot)

The extended model will test:

m z_ddot = T(t) + B(z) - m g - D(z_dot) + F_fs

where F_fs represents the candidate free-surface contribution.

The baseline must be defined before F_fs is introduced.

## 19. Validity Statement

Results from CDFV-001-Ref-01 apply only to the selected
cylindrical reference geometry and prescribed vertical
water-exit conditions.

They do not establish the performance of a complete CDFV vehicle.

## 20. Acceptance Criteria for P003-A

P003-A is complete when:

- the first research scenario is fixed;
- the system boundary is explicit;
- included and excluded phenomena are recorded;
- each initial parameter has a source, assumption, or open status;
- the baseline model interface is defined;
- the next parameter-selection task is clear.
