# P002 Free Surface Hydrodynamics HAUV 2022


## Metadata

Title:

Experimental study on trans-media hydrodynamics of a cylindrical hybrid unmanned aerial underwater vehicle


Year:

2022


Relation:

AQ001


Status:

Reading


---

# 1. Research Question

What physical phenomena dominate HAUV air-water transition?


---

# 2. Why Selected

Direct evidence source for:

- time-varying hydrodynamic force
- free surface effect
- attitude-dependent moment


---

# 3. Abstract Extraction


## Problem

The paper investigates the hydrodynamic characteristics of hybrid unmanned aerial underwater vehicles (HAUVs) during the water-air trans-media transition process.

The key problem is that the transition process involves strong nonlinear interactions between the vehicle and the changing fluid environment. The time-varying hydrodynamic forces and moments during this process remain insufficiently understood.


---

## Method

The authors developed a novel experimental platform capable of controlling HAUV water-air transition profiles under different:

- velocities
- accelerations
- attitudes

The platform enables precise measurement of hydrodynamic forces and moments during the transition process.

A series of constrained model experiments were conducted to analyze how hydrodynamic forces change with vehicle motion conditions.


---

## Findings

The experiments revealed several important transition dynamics:


### 1. Free surface suction effect

When the velocity exceeds 0.1 m/s, the suction force caused by the free surface effect initially increases and then becomes approximately constant.

The maximum suction force reaches about 10% of gravity.


### 2. Acceleration-dependent vertical force

At low accelerations (<0.15 m/s²), the vertical force approximately increases with the square of time.


### 3. Attitude-dependent hydrodynamic moment

The hydrodynamic moment changes significantly with vehicle attitude.

When attitude is below 15°, the moment first decreases and then increases.

When attitude increases further, the moment decreases toward a stable value.


### 4. Additional hydrodynamic effects

The influence of hydrodynamic moments caused by effects other than time-varying buoyancy cannot be ignored.


---

## Contribution to AQ001

This paper provides experimental evidence that HAUV air-water transition dynamics are governed by:

- free surface interaction
- time-varying hydrodynamic forces
- attitude-dependent hydrodynamic moments
- non-buoyancy hydrodynamic effects

---

## Evidence Status

Status:

Preliminary


Confidence:

High for experimental observations

Medium for generalization to full HAUV systems

# 4. Introduction Extraction


## Research Context

HAUVs enable repeated air-water transitions.
Multi-rotor HAUVs are suitable for smooth and controllable transitions.


## Research Problem

Water-air transition is strongly nonlinear and includes:
- single medium motion
- near free surface motion
- free surface breaking


## Existing Limitations

Previous studies mainly focused on:
- vehicle motion
- trajectory
- kinematics

However, direct measurement of hydrodynamic forces during transition was lacking.


## Research Gap

Lack of experimentally measured time-varying hydrodynamic forces and moments during HAUV transition.


## Contributions

C1:
Develop hydrodynamic measurement platform.

C2:
Obtain force and moment data under different velocities, accelerations, and attitudes.

C3:
Analyze free surface suction force and surge effect.


# 5. Method Extraction

### Model Simplification

Research Object:
Nezha HAUV

Simplified Model:
Vertical Cylinder

Reason:
Extract fundamental transition dynamics.

---

### Transition Process Decomposition

Stage 1:
Underwater floating

Stage 2:
Near free surface

Stage 3:
Surface crossing

Stage 4:
Air separation

---

### State Representation

Coordinate:
Earth frame + Body frame

Variables:
Velocity
Force
Moment

## Coordinate System Representation

### Frames

Earth/Measurement Frame (E):
Used for external measurements.

Body Frame (O):
Attached to vehicle center of mass.

---

### State Variables

Velocity:
vE = Earth frame velocity
v = Body frame velocity

Force:
FE = Earth frame force
F = Body frame force

Moment:
ME = Earth frame moment
M = Body frame moment


---

### Transformation

v = J^-1 vE

where J represents attitude-dependent coordinate transformation.

Variables:
theta = pitch angle
psi = yaw angle

---

### ANRI Relevance

CDFV knowledge representation requires explicit coordinate frames because transition dynamics involve changing vehicle attitudes and multi-environment forces.

# 6. Evidence


E1:

Free surface suction force


E2:

Velocity-dependent force change


E3:

Attitude-dependent hydrodynamic moment


---

# 7. Research Impact


Before:

...


After:

...


---

# 8. Limitations


- Simplified cylindrical model
- Limited transition conditions
