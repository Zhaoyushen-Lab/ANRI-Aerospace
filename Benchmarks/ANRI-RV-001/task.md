# ANRI-RV-001 task

You are reviewing the CDFV-001 Ref-01B computational baseline.

## Inputs

Read the following files from the repository:

- `Research_Planning/CDFV-001_Reference_Configuration.md`
- `Models/CDFV-001/Ref-01B/baseline_model.py`
- `Models/CDFV-001/Ref-01B/verify_baseline.py`
- all CSV files under `Models/CDFV-001/Ref-01B/results/`

## Required actions

1. Identify the reference mass, diameter, length, water density, gravity, and
   force-balance tolerance.
2. Run the baseline verifier from the repository root.
3. Record the exact command, Python version, Git commit, input files, output
   files, and verifier status.
4. Check all criteria in `rubric.yaml`.
5. State which findings are internal computational checks and which claims
   would require an experiment.
6. Do not infer a free-surface suction force from this baseline. The baseline
   explicitly sets that term to zero.

## Required output

Create a report containing:

- overall status: PASS, FAIL, or INCONCLUSIVE;
- a criterion-by-criterion result;
- evidence references using file names and, where available, column names;
- the exact command and run metadata;
- limitations and the next validation action.

The report must include this sentence or an equivalent statement:

> The baseline is internally computationally consistent within the stated
> assumptions; it is not experimental validation of free-surface loading.
