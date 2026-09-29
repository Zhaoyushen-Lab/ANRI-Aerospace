# CDFV-001 Ref-01B baseline model

`baseline_model.py` is the first executable model for the Ref-01B computational
benchmark. It represents a vertical cylinder leaving still water at a
prescribed constant upward velocity.

## Run

From the repository root:

```bash
python Models/CDFV-001/Ref-01B/baseline_model.py
```

The default run evaluates `0.10`, `0.25`, and `0.50 m/s` and writes:

```text
Models/CDFV-001/Ref-01B/results/
├── Ref-01B-B-0p10mps.csv
├── Ref-01B-B-0p25mps.csv
├── Ref-01B-B-0p50mps.csv
└── summary.csv
```

A smaller/faster run is useful while editing:

```bash
python Models/CDFV-001/Ref-01B/baseline_model.py --dt 0.01
```

To run a different set of velocities:

```bash
python Models/CDFV-001/Ref-01B/baseline_model.py \
  --velocities 0.10 0.20 0.30 \
  --output-dir Models/CDFV-001/Ref-01B/results/test_run
```

## Interpretation

The model uses the convention that positive `z` and positive force are
upward. The cylinder centre is measured relative to the still-water surface.
The output `constraint_force_N` is the algebraic force needed to maintain the
prescribed motion:

```text
m*a = F_constraint + F_buoyancy - F_weight
```

For the first version, `a=0`, `free_surface_force_N=0`, drag is omitted, and
added mass is omitted. Thus this quantity is a model residual, not a measured
propeller thrust or a validated CDFV load.

## Sanity checks

With the default freshwater assumption, a fully submerged cylinder has
approximately:

```text
buoyancy = 20.15 N
weight   = 19.91 N
constraint force = -0.24 N
```

When fully emerged, buoyancy is zero and the constant-speed constraint force
is approximately `+19.91 N`. If these values change unexpectedly, check the
geometry, mass, density, and sign convention before adding more physics.

## Provenance and scope

- Diameter, length, and mass are from the P002 cylindrical experimental model.
- Freshwater density and gravity are explicit modelling assumptions.
- P002's free-surface observation is not used as a validated CDFV-001 input in
  this baseline.
- The benchmark is for a prescribed vertical translation only; it does not
  represent a complete aerial-underwater vehicle.
