# Paper_001

Title:
Review of hybrid aerial underwater vehicle: Cross-domain mobility and transitions control

Type:
Review / Survey Paper

Domain:
Hybrid Aerial Underwater Vehicle (HAUV)

Purpose:
Review existing HAUV designs and cross-domain mobility technologies.

## Background

HAUV aims to combine aerial mobility and underwater operation,enabling continuous observation and sampling across two environments.

## Existing Research Areas

1. HAUV platform design

Research focuses on different vehicle configurationsthat enable both aerial and underwater operation.

2. Cross-domain mobility

Research focuses on mechanisms and methodsallowing vehicles to transition between air and water.

## Challenge 001

Problem:
How to achieve repeated smooth air-water transitions?

Observation:
The control system is considered the core component.

Difficulty:
Vehicle dynamics change significantly between air and water environments.

## Challenge 002

Problem:
How to model HAUV dynamics during cross-domain motion?


Environmental factors:

- Wind disturbance
- Wave disturbance
- Complex sea states


Research need:
Accurate dynamic models for reliable control.

## Challenge 003

Problem:
How to achieve persistent autonomous operation?


Requirement:

HAUV should perform long-duration autonomous missions without continuous human intervention.

# Preliminary Research Gaps


## Gap 001

Current studies focus on transition control,but achieving robust autonomous cross-domain operation remains challenging.


## Gap 002

HAUV involves multiple physical domains:

- Aerodynamics
- Hydrodynamics
- Control

Integrated design remains difficult.


## Gap 003

Environmental disturbances such as wind and waves increase uncertainty in real-world deployment.

# ANRI Relevance

This paper reveals that HAUV development is a multidisciplinary problem.

Potential ANRI value:

Organize fragmented knowledge from:

- vehicle design
- hydrodynamics
- aerodynamics
- control theory

into an integrated research workflow.

## Key Challenges Extracted

Challenge 001:
Transition Control

Challenge 002:
Dynamic Modeling

Challenge 003:
Persistent Autonomy

## Introduction Extraction


### Background

Traditional underwater vehicles cannot satisfy
air-sea cross-domain missions.


### Motivation

HAUV enables:

- aerial observation
- underwater detection
- integrated missions


### Key Challenges

1. Cross-domain mobility

2. Smooth air-water transition

3. Autonomous operation under disturbances


### Fundamental Conflicts

Air optimization conflicts with underwater optimization.


### ANRI Relevance

HAUV represents a multidisciplinary research problem
requiring integration of:

- aerodynamics
- hydrodynamics
- control
- autonomous systems

## 2. Current Status of HAUV


## Field Maturity

HAUV technology is currently in an early exploration stage.

Current status:

- Multiple concepts proposed
- Prototype demonstrations exist
- Practical deployment remains limited
  
## HAUV Design Classification


### 1. Bioinspired HAUV

Concept:

Inspired by animals capable of air-water locomotion.


Advantages:

Natural cross-domain mobility.


Limitations:

Low technology maturity and limited payload capability.


### 2. UAV/UUV-based HAUV

Categories:

- Fixed-wing HAUV
- Multi-rotor HAUV
- Multimodal HAUV

## Fixed-wing HAUV


Strength:

- High speed
- Long endurance
- Aerodynamic efficiency


Weakness:

- Difficult low-speed operation
- Difficult water transition
- High impact during entry/exit


Design conflict:

Air performance vs transition safety

## Multi-rotor HAUV


Strength:

- Hovering capability
- VTOL
- Stable transition


Weakness:

- High power consumption
- Limited range


Design conflict:

Maneuverability vs endurance

## Multimodal HAUV


Goal:

Combine advantages of:

- Fixed-wing flight
- Multi-rotor VTOL
- Underwater gliding


Expected benefits:

- High maneuverability
- Long endurance
- Low underwater energy consumption


Remaining challenge:

System complexity increases.

## Research Gaps Extracted from Current Status


### Gap 001

Current HAUV architectures still struggle to simultaneously achieve:

- aerial efficiency
- underwater capability
- reliable transition


### Gap 002

Existing designs optimize individual modes,
but cross-domain performance remains the bottleneck.


### Gap 003

Multimodal integration improves capability,but increases system complexity.


## ANRI Interpretation


Current HAUV research reveals a multi-objective multidisciplinary design problem.


The design must balance:

Aerodynamics
+
Hydrodynamics
+
Control
+
Energy


Potential ANRI role:

Assist in organizing knowledge and exploring trade-offs between different HAUV architectures.

## Core Technology

Cross-domain motion control is one of the fundamental technologies required for HAUV operation.

The main challenge:

Maintaining stable motion while crossing air-water interface.

## Challenge 001

### Time-varying Dynamics During Transition


Problem:

The vehicle dynamics change significantly
during air-water transition.


Causes:

- Buoyancy variation
- Additional mass effect
- Hydrodynamic damping change


Implication:

A fixed control model is insufficient.

## Knowledge Node

Cross-domain HAUV requires
a hybrid dynamic model.


The model should include:

- Aerodynamic forces
- Hydrodynamic forces
- Buoyancy
- Added mass
- Damping
- Propulsion characteristics

## Fixed-wing Control Status


Approach:

State feedback controller
with switching law.


Result:

Experimental success rate was limited.


Insight:

Cross-domain transition remains unreliable
despite controller design.

## Multi-rotor Control


Common methods:

- PD control
- PID control
- Gain scheduling PID


Advantage:

Stable closed-loop control.


Limitation:

Requires predefined models and parameters.

## Fundamental Concept

HAUV can be modeled as a hybrid system:


Air dynamics

+

Transition dynamics

+

Water dynamics


Connected by switching events.

