# Active Research Questions

## Purpose

This document records the active research questions
currently under investigation.

Unlike Candidate Problems, which collect potential
research directions, Active Questions represent
the questions that are currently guiding literature
reading, knowledge extraction, and research planning.

Only a small number of active questions should exist
at any given time.

Current Status:

- Active: 3
- Frozen: 0
- Solved: 0

---

# AQ001

## Title

Understanding Time-varying Air-water Transition Dynamics

## Priority

★★★★★ Critical

## Status

Active

## Motivation

Air-water transition is the core bottleneck
connecting vehicle design and motion control.

Without understanding the underlying transition
physics, later work on optimization and control
will be built on weak foundations.

## Research Question

How do the physical characteristics change
during the air-water transition process?

Specifically:

- Added mass
- Buoyancy
- Hydrodynamic forces
- Aerodynamic forces
- Water impact
- Flow separation

## Related Candidate Problems

CP002

Time-varying Hydrodynamics During Transition

## Expected Knowledge

After answering this question, we should understand:

- What changes?
- Why does it change?
- Which parameters dominate?
- How can these effects be modeled?

## Next Evidence Required

Find a research paper focusing on:

- transition dynamics
- hydrodynamic modeling
- CFD or experimental validation

---

# AQ002

## Title

Optimal Configuration of Multimodal HAUV

## Priority

★★★★☆

## Status

Active

## Motivation

Current HAUV designs exhibit trade-offs between:

- flight efficiency
- underwater performance
- transition stability

## Research Question

How should a multimodal HAUV
be configured to balance these objectives?

## Related Candidate Problems

CP001

Multimodal HAUV Configuration Optimization

## Current Blocker

Requires better understanding of AQ001.

---

# AQ003

## Title

Robust Cross-domain Motion Control

## Priority

★★★★☆

## Status

Active

## Motivation

Reliable deployment requires
stable operation under:

- wind
- waves
- parameter uncertainty

## Research Question

Can one control framework
operate across:

- air
- transition
- underwater

without manual switching?

## Related Candidate Problems

CP003

Robust Cross-domain Motion Control

---

# Question Dependency Map

AQ001

Transition Dynamics

↓

supports

↓

AQ002

Vehicle Configuration

↓

supports

↓

AQ003

Cross-domain Control

---

# Current Research Decision

Current focus:

AQ001

Reason:

Transition dynamics forms the physical foundation for both vehicle design and control.

Next milestone:

Identify 3 high-quality papers focused on transition dynamics.

## Current Blocker

Requires dynamic models from AQ001.
