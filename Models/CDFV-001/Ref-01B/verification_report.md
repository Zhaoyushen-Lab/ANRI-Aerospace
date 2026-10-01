# Ref-01B Baseline Verification

- Generated (UTC): `2026-09-30T10:16:25.565203+00:00`
- Overall status: **PASS**
- Results directory: `C:\Users\xiangming\ANRI-Aerospace\Models\CDFV-001\Ref-01B\results`

## Reference configuration

- Mass: `2.03 kg`
- Cylinder: `0.09 m × 0.323 m`
- Weight: `19.9074995 N`
- Full-submerged buoyancy: `20.1510694 N`
- Force-balance tolerance: `0.0001 N`

## File checks

| File | Rows | Status |
|---|---:|---|
| `Ref-01B-B-0p10mps.csv` | 4846 | **PASS** |
| `Ref-01B-B-0p25mps.csv` | 1940 | **PASS** |
| `Ref-01B-B-0p50mps.csv` | 971 | **PASS** |

## `Ref-01B-B-0p10mps.csv`

| Check | Status | Detail |
|---|---|---|
| read_csv | **PASS** | 14 columns, 4846 data rows |
| non_empty | **PASS** | 4846 rows |
| numeric_time | **PASS** | column=time_s; missing_or_non_numeric=0 |
| numeric_position | **PASS** | column=z_center_m; missing_or_non_numeric=0 |
| numeric_speed | **PASS** | column=velocity_m_s; missing_or_non_numeric=0 |
| numeric_buoyancy | **PASS** | column=buoyancy_N; missing_or_non_numeric=0 |
| numeric_weight | **PASS** | column=weight_N; missing_or_non_numeric=0 |
| numeric_constraint | **PASS** | column=constraint_force_N; missing_or_non_numeric=0 |
| monotonic_time | **PASS** | increasing |
| monotonic_position | **PASS** | increasing |
| weight_reference | **PASS** | max_error=0 N; expected=19.9074995 N |
| buoyancy_range | **PASS** | range=[0, 20.1510694] N; expected=[0, 20.1510694] N |
| force_balance | **PASS** | max_abs(constraint + buoyancy - weight)=3.55271368e-15 N |

Recognised columns:

```json
{
  "time": "time_s",
  "position": "z_center_m",
  "speed": "velocity_m_s",
  "buoyancy": "buoyancy_N",
  "weight": "weight_N",
  "constraint": "constraint_force_N"
}
```

## `Ref-01B-B-0p25mps.csv`

| Check | Status | Detail |
|---|---|---|
| read_csv | **PASS** | 14 columns, 1940 data rows |
| non_empty | **PASS** | 1940 rows |
| numeric_time | **PASS** | column=time_s; missing_or_non_numeric=0 |
| numeric_position | **PASS** | column=z_center_m; missing_or_non_numeric=0 |
| numeric_speed | **PASS** | column=velocity_m_s; missing_or_non_numeric=0 |
| numeric_buoyancy | **PASS** | column=buoyancy_N; missing_or_non_numeric=0 |
| numeric_weight | **PASS** | column=weight_N; missing_or_non_numeric=0 |
| numeric_constraint | **PASS** | column=constraint_force_N; missing_or_non_numeric=0 |
| monotonic_time | **PASS** | increasing |
| monotonic_position | **PASS** | increasing |
| weight_reference | **PASS** | max_error=0 N; expected=19.9074995 N |
| buoyancy_range | **PASS** | range=[0, 20.1510694] N; expected=[0, 20.1510694] N |
| force_balance | **PASS** | max_abs(constraint + buoyancy - weight)=3.55271368e-15 N |

Recognised columns:

```json
{
  "time": "time_s",
  "position": "z_center_m",
  "speed": "velocity_m_s",
  "buoyancy": "buoyancy_N",
  "weight": "weight_N",
  "constraint": "constraint_force_N"
}
```

## `Ref-01B-B-0p50mps.csv`

| Check | Status | Detail |
|---|---|---|
| read_csv | **PASS** | 14 columns, 971 data rows |
| non_empty | **PASS** | 971 rows |
| numeric_time | **PASS** | column=time_s; missing_or_non_numeric=0 |
| numeric_position | **PASS** | column=z_center_m; missing_or_non_numeric=0 |
| numeric_speed | **PASS** | column=velocity_m_s; missing_or_non_numeric=0 |
| numeric_buoyancy | **PASS** | column=buoyancy_N; missing_or_non_numeric=0 |
| numeric_weight | **PASS** | column=weight_N; missing_or_non_numeric=0 |
| numeric_constraint | **PASS** | column=constraint_force_N; missing_or_non_numeric=0 |
| monotonic_time | **PASS** | increasing |
| monotonic_position | **PASS** | increasing |
| weight_reference | **PASS** | max_error=0 N; expected=19.9074995 N |
| buoyancy_range | **PASS** | range=[0, 20.1510694] N; expected=[0, 20.1510694] N |
| force_balance | **PASS** | max_abs(constraint + buoyancy - weight)=3.55271368e-15 N |

Recognised columns:

```json
{
  "time": "time_s",
  "position": "z_center_m",
  "speed": "velocity_m_s",
  "buoyancy": "buoyancy_N",
  "weight": "weight_N",
  "constraint": "constraint_force_N"
}
```

## Interpretation

`PASS` means the available check passed. `PARTIAL` means the file was readable but one or more checks could not be performed because the column was not recognised. `FAIL` requires investigation before treating the baseline as verified.

This computational baseline excludes free-surface force, drag, and added mass. Passing these checks does not constitute experimental validation.
