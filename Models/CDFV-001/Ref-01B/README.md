# CDFV-001 Ref-01B baseline model

`baseline_model.py` is the first executable model for the Ref-01B computational
benchmark. It represents a vertical cylinder leaving still water at a
prescribed constant upward velocity.

## Run

From the repository root (any working directory works; the model resolves its
output directory relative to its own file):

```bash
python Models/CDFV-001/Ref-01B/baseline_model.py
```

The default run evaluates `0.10`, `0.25`, and `0.50 m/s` and writes:

```text
Models/CDFV-001/Ref-01B/results/
├── Ref-01B-B-0p10mps.csv     frozen result artifact (hash-registered)
├── Ref-01B-B-0p25mps.csv     frozen result artifact (hash-registered)
├── Ref-01B-B-0p50mps.csv     frozen result artifact (hash-registered)
├── summary.csv               frozen result artifact (hash-registered)
├── verification.json         frozen report artifact (hash-registered)
├── verification_report.md    frozen report artifact (hash-registered)
└── local_run_meta.json       generated local metadata (git-ignored, never hashed)
```

All CSV output uses LF terminators on every platform, and the verifier writes
no timestamp and no machine path into the frozen artifacts. Regenerating the
model on Windows and on Ubuntu therefore produces byte-identical files. If a
frozen artifact hash changes, the Research Object validator fails — that is
intentional and means the frozen evidence moved.

A smaller/faster run is useful while editing:

```bash
python Models/CDFV-001/Ref-01B/baseline_model.py --dt 0.01
```

To run a different set of velocities, write to a scratch directory rather than
over the frozen results:

```bash
python Models/CDFV-001/Ref-01B/baseline_model.py \
  --velocities 0.10 0.20 0.30 \
  --output-dir Models/CDFV-001/Ref-01B/results/test_run
```

## Verify

```bash
# clean baseline (exit 0 on PASS, 1 on FAIL)
python Models/CDFV-001/Ref-01B/verify_baseline.py

# an adversarial case (expected to exit non-zero)
python Models/CDFV-001/Ref-01B/verify_baseline.py \
  --results-dir Benchmarks/ANRI-RV-001/adversarial/A01_wrong_weight/results

# verifier self-tests: column matching, units, monotonicity
python Models/CDFV-001/Ref-01B/verify_negative_cases.py
```

## Interpretation

The model uses the convention that positive `z` and positive force are
upward. The cylinder centre is measured relative to the still-water surface.
The output `constraint_force_N` is the algebraic force needed to maintain the
prescribed motion:

```text
m*a = F_constraint + F_buoyancy - F_weight
```

For the first version, `a=0`, `free_surface_force_N=0` (checked explicitly),
drag is omitted, and added mass is omitted. Thus this quantity is a model
residual, not a measured propeller thrust or a validated CDFV load.

## Frozen reference values

| Quantity | Value | Source |
|---|---:|---|
| Mass | `2.030 kg` | P002 Table 1 |
| Diameter | `0.090 m` | P002 Table 1 |
| Length | `0.323 m` | P002 Table 1 |
| Water density | `1000 kg/m^3` | `A-FRESHWATER` assumption |
| Gravity | `9.80665 m/s^2` | `A-GRAVITY` assumption |
| Force tolerance | `1e-4 N` | verifier acceptance tolerance |
| Weight | `19.9074995 N` | `m*g` |
| Full-submerged buoyancy | `20.1510694 N` | `rho*g*pi*(D/2)^2*L` |

## Sanity checks

With the frozen inputs above, a fully submerged cylinder has:

```text
buoyancy         = 20.1510694 N
weight           = 19.9074995 N
constraint force = -0.2435699 N
```

When fully emerged, buoyancy is zero and the constant-speed constraint force is
`+19.9074995 N`. If these values change unexpectedly, check the geometry, mass,
density, gravity and sign convention before adding more physics.

Note the margin: the fully submerged constraint force is only about 0.24 N
against a 19.91 N weight (about 1.2 %). The baseline is near-neutral, so it is
sensitive to any change in mass, density, gravity or diameter. Those four inputs
are recorded machine-readably in `Research_Objects/RO-CDFV-001-Ref-01B.json`,
and `scripts/validate_research_object.py` fails if the object, the model and the
verifier disagree by more than a relative 1e-12.

## Provenance and scope

- Diameter, length, and mass are from the P002 cylindrical experimental model.
- Freshwater density and gravity are explicit, frozen modelling assumptions.
- P002's free-surface observation is not used as a validated CDFV-001 input in
  this baseline.
- The benchmark is for a prescribed vertical translation only; it does not
  represent a complete aerial-underwater vehicle.
- Review status and the independent-review record live in the Research Object,
  not in this file.
