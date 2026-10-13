# Independent Review Checklist

## Review target

- Research Object: `RO-CDFV-001-Ref-01B`
- Repository: `C:\Users\xiangming\ANRI-Aerospace`
- Review mode: read-only
- Do not modify, delete, commit, or push files during the review.

## Files to inspect

- `Research_Objects/RO-CDFV-001-Ref-01B.json`
- `schema/research_object.schema.json`
- `scripts/validate_research_object.py`
- `Experiment_Requests/CDFV-001-Ref-01S_Experiment_Request.md`
- `Research_Planning/CDFV-001_Reference_Configuration.md`
- `Models/CDFV-001/Ref-01B/baseline_model.py`
- `Models/CDFV-001/Ref-01B/verify_baseline.py`
- `Models/CDFV-001/Ref-01B/results/`
- `.github/workflows/anri-validation.yml`

## Commands to run

Run from the repository root:

```powershell
py -3 .\scripts\validate_research_object.py `
  .\Research_Objects\RO-CDFV-001-Ref-01B.json `
  --repo-root .

py -3 .\Models\CDFV-001\Ref-01B\verify_baseline.py

git status --short
git log -1 --oneline
git ls-files --eol
```

## Research Object checks

- JSON parses successfully.
- ID is exactly `RO-CDFV-001-Ref-01B`.
- Every claim has supporting evidence.
- Every evidence, validator, and artifact path exists.
- Recorded SHA-256 hashes match the current files.
- Provenance commit is recorded.
- No personal absolute Windows path is used as research provenance.
- No `.bak` file is treated as a primary artifact.

## Scientific checks

- The claim is precise and falsifiable.
- Variables and units are defined.
- Initial and boundary conditions are defined.
- The reference configuration agrees with the implementation.
- The expected result is numerically justified.
- Tolerances are explicit.
- The test distinguishes a valid result from an implementation error.
- Negative or adversarial cases are included where appropriate.

## Reproducibility checks

- A fresh checkout can run the documented commands.
- Commands do not depend on the author's local absolute path.
- The clean baseline case passes.
- A01 and A02 adversarial cases fail for the intended reasons.
- Generated outputs are distinguished from fixed provenance artifacts.
- Line-ending differences cannot silently invalidate recorded hashes.

## GitHub Actions checks

- The workflow uses lowercase `scripts/`.
- The Research Object validator runs.
- The baseline verification runs.
- Expected failure cases are checked.
- The workflow fails when a required check fails.
- The workflow can run on Ubuntu.

## Blocking issue definition

Mark an issue as `BLOCKER` when any of the following is true:

- A referenced file is missing.
- A recorded SHA-256 hash is wrong.
- A required validator does not run.
- An intended adversarial case incorrectly passes.
- Inputs, units, or tolerances are undocumented.
- A fresh checkout cannot reproduce the result.
- The claim contradicts the model or evidence.

## Decision

Choose exactly one:

- `APPROVE`
- `APPROVE_WITH_MINOR_FIXES`
- `REQUEST_CHANGES`
- `REJECT`

## Required review output

### Decision

State one decision from the list above.

### Blocking Findings

For each finding include:

- Severity: `BLOCKER`, `MAJOR`, or `MINOR`
- File and line number or JSON field
- Observed problem
- Why it affects validity or reproducibility
- Concrete correction

### Evidence Checked

List every command actually run and its result.

### Claim Assessment

State whether the evidence supports the claim, partially supports it, or does not support it.

### Reproducibility Assessment

State whether a fresh checkout can reproduce the reported result.

### Recommended Next Action

List the three highest-priority actions in order.

Do not modify files. Do not infer missing evidence. Separate observed facts from assumptions.
