# Adversarial cases

These cases are generated from the clean Ref-01B results and are never written
over the clean results. Regenerate the whole set with:

```bash
python Benchmarks/ANRI-RV-001/make_adversarial_cases.py \
  --source Models/CDFV-001/Ref-01B/results \
  --dest Benchmarks/ANRI-RV-001/adversarial
```

Every case directory contains a `mutation.json` that records the mutation kind,
the exact mutation detail, the SHA-256 of the mutated CSV, the check that must
detect it, and the expected status. `adversarial_cases.json` lists all cases
with the hash of each `mutation.json`.

| Case | Source case | Fault | Must be detected by | Expected status |
|---|---|---|---|---|
| A01_wrong_weight | 0.10 m/s | `weight_N` +0.1 N in one row | `weight_reference` | FAIL |
| A02_broken_force_balance | 0.10 m/s | `constraint_force_N` +1.0 N in one row | `force_balance` | FAIL |
| A03_wrong_weight_mid | 0.25 m/s | `weight_N` +0.05 N in one row | `weight_reference` | FAIL |
| A04_broken_force_balance_high | 0.50 m/s | `constraint_force_N` -0.5 N mid-file | `force_balance` | FAIL |
| A05_time_not_monotonic | 0.10 m/s | adjacent `time_s` swapped | `monotonic_time` | FAIL |
| A06_position_not_monotonic | 0.25 m/s | adjacent `z_center_m` swapped | `monotonic_position` | FAIL |
| A07_missing_buoyancy_column | 0.50 m/s | `buoyancy_N` column removed | `column_match_buoyancy` | FAIL |
| A08_missing_weight_column | 0.10 m/s | `weight_N` column removed | `column_weight` | FAIL |
| A09_buoyancy_out_of_range | 0.50 m/s | `buoyancy_N` above full submergence | `buoyancy_range` | FAIL |
| A10_weight_wrong_unit_mN | 0.10 m/s | `weight_N` scaled by 1e-3 (mN written as N) | `weight_reference` | FAIL |
| A11_buoyancy_wrong_unit_kN | 0.25 m/s | `buoyancy_N` scaled by 1e-3 (kN written as N) | `buoyancy_range` | FAIL |
| A12_free_surface_nonzero | 0.50 m/s | non-zero `free_surface_force_N` | `free_surface_zero` | FAIL |

Coverage notes:

- every clean velocity case (0.10, 0.25, 0.50 m/s) is mutated, so a verifier that
  silently stopped inspecting one file cannot pass the suite;
- the same fault class appears in more than one case;
- the mutated row is not always the first row;
- `A07`/`A08` remove a column instead of changing a value, which is what the
  negative-case suite covers in depth.

Additional verifier self-tests live in
`Models/CDFV-001/Ref-01B/verify_negative_cases.py` (18 synthetic cases covering
header matching, duplicates, units, monotonicity, missing columns and the
excluded free-surface term).

## Mutation record

For every adversarial case `mutation.json` records:

- source file and mutated file (repository-relative POSIX paths);
- mutation kind and the exact human-readable mutation detail;
- mutated file SHA-256 and row count;
- expected detection check and expected status;
- the assertion that the clean results were not touched.

## Not covered here

Two earlier drafts in this file described faults that no automated check can
detect in this repository, and they are recorded here as review-gate duties
instead:

- **wrong velocity label** — the CSV `case_id` and `velocity_m_s` columns are
  not cross-checked against the file name. Adding that check is a valid future
  extension; until then the case label is verified by reading the file.
- **unsupported scientific claim** — a conclusion that contradicts the stated
  limitations is caught by the review gate
  (`Research_Objects/RO-CDFV-001-Ref-01B.json`, `review.status`), not by the
  numeric verifier.
