# ANRI Governance v0.1


## Purpose

This document defines the governance principles
for maintaining ANRI as a long-term research infrastructure.


## Core Principles


### 1. Core Principles Protection

The fundamental principles of ANRI should not be changed
without careful review and discussion.


### 2. Architecture Review

Major architecture changes require documentation,
technical reasoning, and review before integration.


### 3. Knowledge Traceability

All important knowledge, decisions, and experiments
must remain traceable through version history.


### 4. Historical Preservation

Previous research records and design decisions
should not be deleted without justification.


### 5. Open Contribution

Contributions are encouraged, but changes should preserve
the long-term goals and engineering philosophy of ANRI.

See `CONTRIBUTING.md`. Contributions are explicitly not limited to code: a clean-room
replication report, a documentation gap, or a failed blind test are all contributions.


### 6. Verification Remains Free

The verifier, the gate, the negative cases, the adversarial suite and the failure-mode
documentation are free and open, permanently.

Reason: verification is the only source of "trustworthy". Putting it behind a paywall would
hand the least-equipped users the least-verifiable results, which is the exact inversion of
this project's purpose.


### 7. No Subsidised Inference

ANRI does not run AI on behalf of its users and does not pay for their inference.

Reason: this is the only design choice that makes cost scale with user count. Once adopted,
survival requires revenue, and revenue pressure reliably breaks Principle 6. This is an
architectural constraint, not a financial preference.


### 8. The Licence Is Irrevocable

`LICENSE` stays MIT. No relicensing, no proprietary split, no open-core carve-out.

Reason: the code was already released under MIT. Changing it later would turn every public
commitment made today into bait, at a cost far above any revenue it could raise.


## Amendment Rules

| Clause | Modifiable | Procedure |
|---|---|---|
| Purpose (this file) | **No** | Changing it makes this a different project |
| Principle 6 (free verification) | **Very hard** | 30-day public comment, objections recorded |
| Principle 7 (no subsidised inference) | Hard | Must show the alternative cannot break Principle 6 |
| Principle 8 (MIT irrevocable) | **No** | Already granted; not revocable in law either |
| Principles 1–5 | Yes | Record in `Research_Planning/Decision_Log.md` |
| Everything else | Yes | Ordinary change |

**Every amendment must leave a record, including rejected proposals and why they were
rejected.**

Funding structure and the candidate routes are in `docs/ANRI_Sustainability.md`.
The commercial assessment that motivates these clauses is `D-ANRI-006` in the decision log.

