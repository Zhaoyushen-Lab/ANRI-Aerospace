# Ref-01B results directory

Everything in this directory is either a **frozen artifact** or **generated
local metadata**. The distinction matters because frozen artifacts are
hash-registered in `Research_Objects/RO-CDFV-001-Ref-01B.json`.

## Frozen artifacts (committed, hash-registered)

| File | Role | Producer |
|---|---|---|
| `Ref-01B-B-0p10mps.csv` | result | `Models/CDFV-001/Ref-01B/baseline_model.py` |
| `Ref-01B-B-0p25mps.csv` | result | `baseline_model.py` |
| `Ref-01B-B-0p50mps.csv` | result | `baseline_model.py` |
| `summary.csv` | result | `baseline_model.py` |
| `verification.json` | report | `Models/CDFV-001/Ref-01B/verify_baseline.py` |
| `verification_report.md` | report | `verify_baseline.py` |

These files contain no timestamp and no machine-specific path, so they are
byte-identical on Windows and Ubuntu. They must use LF terminators; the
repository is configured with `* -text` in `.gitattributes` so that no checkout
rewrites them to CRLF.

## Generated local metadata (git-ignored, never hashed)

| File | Contents |
|---|---|
| `local_run_meta.json` | UTC time, platform string, Python version, verified file list |

`local_run_meta.json` is matched by `**/local_run_meta.json` in `.gitignore`. It
deliberately carries the non-reproducible operational details that were removed
from the frozen artifacts, so that run provenance is still available locally
without breaking hash reproducibility.

## Regenerating

```bash
# 1. results (deterministic)
python Models/CDFV-001/Ref-01B/baseline_model.py

# 2. verification reports (deterministic)
python Models/CDFV-001/Ref-01B/verify_baseline.py

# 3. adversarial cases derived from the clean results
python Benchmarks/ANRI-RV-001/make_adversarial_cases.py \
  --source Models/CDFV-001/Ref-01B/results \
  --dest Benchmarks/ANRI-RV-001/adversarial

# 4. confirm nothing moved
git status --short
```

Step 4 must print nothing for the tracked frozen artifacts. If it prints a
change, the frozen evidence genuinely moved and the Research Object artifact
hashes must be updated deliberately — never silently.

## History

An earlier revision kept a second copy of these CSV files and reports directly
in `Models/CDFV-001/Ref-01B/` (one directory up) because the model's
`--output-dir` default was used from a different working directory. That
duplicate tree was byte-identical apart from CRLF terminators, was registered
nowhere, and made it ambiguous which copy was authoritative. It was deleted;
see the repair report for the exact files and the reason.
