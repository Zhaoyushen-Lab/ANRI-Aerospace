# ANRI-Aerospace

Exploring AI-Native Research Infrastructure for Cross-Domain Flight Vehicle Design.

# Background

## The Rise of AI-Native Scientific Infrastructure

Recent developments in AI for Science indicate a transition
from AI-assisted research tools toward AI-native research
infrastructure.

Future scientific workflows are expected to integrate:

- Scientific literature
- Scientific data
- Knowledge representation
- Physics-based simulation
- AI agents
- Autonomous design and discovery

Instead of treating papers and experimental data as static
resources, AI-native research infrastructure aims to transform
scientific knowledge into machine-understandable and
machine-actionable assets.

# Project Timeline

## 2026

### August 18, 2026

Initial creation of ANRI-CDFV repository.

The project was initiated during the emerging period of
AI-native scientific infrastructure development, with the
goal of exploring its application in cross-domain flight
vehicle research.

### First Research Node

Seed paper:

"Review of hybrid aerial underwater vehicle:
Cross-domain mobility and transitions control"

Research focus:

- HAUV architecture
- Cross-domain transition mechanisms
- Multi-physics challenges
- Future research opportunities

## Vision

This project explores how AI can enhance aerospace research workflows,
including knowledge management, engineering design, simulation and iteration.

## Current Stage

ANRI-CDFV v0.1.1

Focus:
- Aerospace knowledge base
- Literature analysis
- AI-assisted engineering workflow

## Where the project actually is (2026-10-20)

The narrative above describes the intent. This section describes the state, and the
two are further apart than the version string suggests.

> **Which commit these numbers describe.** The table below reflects the branch
> `fix/gate-and-brief` as of 2026-10-20, which is 21 commits ahead of `main`.
> `main` currently holds **71** registered artifacts rather than 87, and lacks the
> cold-start job, the accelerated cases, and the three reports listed under
> "Reading order". The pull request states the difference.

### What exists and is verified

| | |
|---|---|
| Research Object | `Research_Objects/RO-CDFV-001-Ref-01B.json`, schema v0.2, **87 hash-registered artifacts** |
| Validator | `scripts/validate_research_object.py` — offline JSON Schema engine, hash check, path existence, review gate |
| Gate self-test | `scripts/validate_gate_selftest.py` — 13 tamper scenarios, plus a control |
| Verifier | `Models/CDFV-001/Ref-01B/verify_baseline.py` over 9 cases (3 constant-speed, 6 accelerated) |
| Negative cases | 18, in `verify_negative_cases.py` |
| Adversarial suite | 12 cases, `Benchmarks/ANRI-RV-001/` |
| CI | `.github/workflows/anri-validation.yml`, two jobs: `validate` and `cold-start` |
| Branch protection on `main` | deletion, force-push, required PR, required `validate` check |

Start with `Reviews/ANRI_Failure_Mode_Report_v0.1.md`. It is the most useful document
here, because it explains why seven layers of checking still let a defect through, and
what that implies about trusting this repository.

### What this repository does NOT establish

- **No independent human review has occurred.** `independent_human_reviews = 0`. Every
  conclusion here is self-assessed.
- **The engineering result is not settled.** P003 and P004 both terminate at
  `unresolved`, conditionally. Two research questions have completed one loop each
  (`loops_closed = 2`), which exercises the process; it does not answer either question.
- **The benchmark body is P002's cylinder, by design.** `CDFV-001-Ref-01B` is defined at
  scale ratio 1.0 from P002 Table 1, so diameter, length, mass, inertias and the
  0.1–0.5 m/s envelope are literature values deliberately reused, not measured here.
  Analyses that appear numeric inherit that. What genuinely does not exist:
  **the water-exit acceleration profile**, and the initial immersion depth and fluid
  temperature, both of which §17.1 marks `Open`.
- **`main` carries a bypass for the repository admin.** The protection constrains
  collaborators and automation, not the owner. It is auditable, not absolute.

### Reading order

| If you want to | Read |
|---|---|
| Understand what fails and why | `Reviews/ANRI_Failure_Mode_Report_v0.1.md` |
| See which errors the gate cannot see | `Reviews/Ref-01B_Verifier_Coverage_Matrix.md` |
| See the engineering content | `Research_Planning/P003_Free_Surface_Loading.md`, `P004_Added_Mass_Screening.md` |
| See how much the conclusions depend on their inputs | `Research_Planning/P004_Sensitivity_Analysis.md` |
| See the decisions and their reversals | `Research_Planning/Decision_Log.md` |
| Reproduce the repository from scratch | `Experiment_Requests/CLEANROOM-Replication_Task.md` |
| See what was reviewed from outside | `Reviews/RO-CDFV-001-Ref-01B_Independent_Review_Report.md` |

### Reproducing it

```powershell
py -3 .\scripts\validate_research_object.py .\Research_Objects\RO-CDFV-001-Ref-01B.json --repo-root .
py -3 .\Models\CDFV-001\Ref-01B\verify_baseline.py
py -3 .\Models\CDFV-001\Ref-01B\verify_negative_cases.py
py -3 .\Benchmarks\ANRI-RV-001\run_adversarial_cases.py
py -3 .\scripts\check_report_mechanism.py
```

All five exit 0 on the branch under review (`fix/gate-and-brief`) as of 2026-10-20,
and on `main` for the subset `main` contains. `main` is behind that branch: see the
pull request for the current difference. The `cold-start` CI job additionally
repeats the first three inside a `git archive` export with no `.git`, because a tree
without VCS metadata takes a different code path in the verifier and once wrote a
checkout-dependent path into a hashed artifact.

## Roadmap

2026:
- Build Cross-Domain Flight Vehicle Design knowledge base
- Develop Knowledge Agent prototype
- Explore AI-native engineering workflows

