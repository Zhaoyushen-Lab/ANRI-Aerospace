# CDFV-001 Reference Configuration

## Metadata

- Configuration ID: CDFV-001-Ref-01
- Version: v0.1
- Status: Draft
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

| Parameter | Value | Basis | Status |
|---|---|---|---|
| Body diameter | Not selected | Geometry decision | Open |
| Body length | Not selected | Geometry decision | Open |
| Mass | Not selected | Buoyancy and model purpose | Open |
| Displaced volume | Not calculated | Derived from selected geometry | Open |
| Water-exit velocity | Not selected | Study conditions | Open |
| Initial immersion | Not selected | Define transition interval | Open |
| Fluid properties | Not selected | Specify study environment | Open |

Parameter basis must be one of:
literature reference, design assumption, calculation, or measurement.

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
