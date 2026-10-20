#!/usr/bin/env python3
"""Compare two ANRI state snapshots and evaluate the documented triggers.

This is the tool the daily report's "what changed since last time" section is
built from.  It removes two sources of drift that hand-written dailies suffer
from: forgetting which numbers moved, and quietly skipping a trigger that had
already been committed to a date threshold.

Run from the repository root:

    py -3 scripts/compare_snapshots.py                    # latest vs previous
    py -3 scripts/compare_snapshots.py --markdown         # report-ready tables
    py -3 scripts/compare_snapshots.py --prior <a.json> --current <b.json>

Triggers are declared in ``TRIGGERS`` below with an explicit date threshold and
the factor adjustment that was promised in the report that created them.  Adding
a trigger is a deliberate edit, and the daily report must then honour it.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import date
from pathlib import Path
from typing import Any

REPO = Path(__file__).resolve().parent.parent
LOG_DIR = REPO / "Research_Log"


def force_utf8_io() -> None:
    """Emit and accept UTF-8 regardless of the Windows ANSI code page.

    Without this, a GBK console cannot print the Chinese text these reports
    contain, and the failure is an encoding error rather than a report.
    """

    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if reconfigure is not None:
            try:
                reconfigure(encoding="utf-8", errors="replace")
            except Exception:
                pass

# Declared triggers. `threshold` is the first date on which the trigger fires
# (inclusive). `effect` is the adjustment promised when the trigger was created.
TRIGGERS: list[dict[str, Any]] = [
    {
        "id": "T1",
        "created": "2026-10-11",
        "description": (
            "The reproducibility repair is still not committed "
            "(head still abc9103 and pending entries > 0)."
        ),
        "threshold": "2026-10-14",
        "effect": "L2 -0.05, L3 -0.05",
        "check": "worktree_dirty",
    },
    {
        "id": "T2",
        "created": "2026-10-11",
        "description": "Ref-01S laboratory engagement has no recorded response.",
        "threshold": "2026-10-25",
        "effect": "L1-lab -> 0.25",
        "check": "lab_engagement",
    },
    {
        "id": "T3",
        "created": "2026-10-11",
        "description": (
            "A second Research Object exists and has been reviewed by someone "
            "other than the author."
        ),
        "threshold": "2026-10-11",
        "effect": "L2 -> 0.65, L5 -> 0.40",
        "check": "second_object_reviewed",
    },
    {
        "id": "T4",
        "created": "2026-10-11",
        "description": "ClawsGO or a comparable product publishes long-horizon metrics.",
        "threshold": "2026-10-11",
        "effect": "re-estimate L1-agent from published numbers (manual)",
        "check": "manual",
    },
    {
        "id": "T5",
        "created": "2026-10-11",
        "description": "An updated long-horizon benchmark supersedes AutoLab.",
        "threshold": "2026-10-11",
        "effect": "re-estimate L1-agent and threshold A (manual)",
        "check": "manual",
    },
    {
        "id": "T6",
        "created": "2026-10-11",
        "description": (
            "A public implementation of automatic exploration-graph compilation "
            "(the Ara L3 gap) appears, so the project should integrate rather "
            "than build."
        ),
        "threshold": "2027-02-01",
        "effect": "L2 +0.05 and replace the build item with integration (manual)",
        "check": "manual",
    },
    {
        "id": "T7",
        "created": "2026-10-11",
        "description": (
            "A publication binds a review state machine / publication gate to "
            "hash-frozen artifacts, pre-empting the one remaining narrow novel "
            "claim (C2c in the peer-progress report)."
        ),
        "threshold": "2027-04-01",
        "effect": "C2c scoop probability -> 0.70; drop the independent claim (manual)",
        "check": "manual",
    },
    {
        "id": "T8",
        "created": "2026-10-11",
        "description": (
            "A public cross-domain / HAUV vertical water-exit hydrostatic "
            "baseline appears with the same reference parameters."
        ),
        "threshold": "2027-04-01",
        "effect": "treat C1 as pre-empted; stop submitting it as a result (manual)",
        "check": "manual",
    },
    {
        "id": "T9",
        "created": "2026-10-11",
        "description": (
            "The A59-style adversarial verification protocol is formally adopted "
            "by a domain journal or conference."
        ),
        "threshold": "2027-10-01",
        "effect": "freeze C2a as pre-empted in the peer-progress report (manual)",
        "check": "manual",
    },
    {
        "id": "T10",
        "created": "2026-10-11",
        "threshold": "2026-11-10",
        "description": (
            "[RETIRED 2026-10-20] Premise dissolved by the Stage 1 reframing, not by "
            "filling the table. The original rule read 'P003 Stage 1 still has "
            "unresolved Blocked cells, i.e. the research question itself is still "
            "blocked', and its check counted table rows whose status cell contained "
            "'blocked'. Those four cells were blocked by the FRAMING - the table asked "
            "CDFV-001 for absolute mass, length, velocity and attitude - not by a "
            "missing measurement, and section 7.5.5 already supplied the correct "
            "dimensionless structure. Stage 1 now states transfer conditions instead "
            "of demanding values, so the count is zero and would have cleared this "
            "trigger silently. That would have been the exact self-deception T10 was "
            "built to catch, so it is retired explicitly and the obligation it "
            "approximated is carried by T18. Original text: P003 Stage 1 still has "
            "unresolved 'Blocked' cells in the CDFV-001 column, i.e. the research "
            "question itself is still blocked."
        ),
        "effect": "none (retired); see T18",
        "check": "manual",
    },
    {
        "id": "T11",
        "created": "2026-10-11",
        "description": (
            "No independent human review has been recorded, so ANRI Principle 5 "
            "('Human expertise remains part of the loop') is not institutionalised."
        ),
        "threshold": "2027-01-09",
        "effect": "D-ANRI-001: mark Principle 5 as not institutionalised; L4 -> 0.15",
        "check": "human_review",
    },
    {
        "id": "T12",
        "created": "2026-10-12",
        "description": (
            "An institutional platform (e.g. CAS ROCK/Panshi) publishes its "
            "provenance or trusted-evaluation specification, and it turns out to "
            "include cryptographic hash freezing or a review-state gate. Raised "
            "after the 2026-10-01 Panshi announcement, whose wording overlaps "
            "C2c but whose mechanism is not yet public."
        ),
        "threshold": "2027-04-01",
        "effect": (
            "C2c scoop probability -> 0.85; per D-ANRI-001 adopt their "
            "specification and drop the independent claim (manual)"
        ),
        "check": "manual",
    },
    {
        "id": "T13",
        "created": "2026-10-12",
        "description": (
            "The local repair commits are still unpushed, so reproducibility is "
            "not yet exposed to any third party."
        ),
        "threshold": "2026-10-19",
        "effect": "L2 -0.03, L3 -0.03",
        "check": "unpushed",
    },
    {
        "id": "T14",
        "created": "2026-10-13",
        "description": (
            "The remote CI run is still failing, so the gate has never passed in a "
            "real environment. Raised after the 2026-10-13 finding that all four "
            "GitHub Actions runs failed from the workflow's inception."
        ),
        "threshold": "2026-10-20",
        "effect": (
            "L3 -0.05; declare the gate unable to pass in a real environment (manual)"
        ),
        "check": "manual",
    },
    {
        "id": "T15",
        "created": "2026-10-13",
        "threshold": "2026-10-20",
        "description": (
            "[RETIRED 2026-10-20] Superseded by T17. This rule compared the FILE COUNTS "
            "of main and feat; after PR #1 both stand at 162 files, so the measure can "
            "no longer see work that has moved to another branch. Kept in the list "
            "rather than deleted because the 2026-10-13, 10-19 and 10-20 reports "
            "reference it, and removing the id would make those references point at "
            "nothing. T17 replaces it with a commit-distance test that depends on "
            "neither branch names nor file counts. Original text: main and feat still "
            "differ by more than 50 files, i.e. the real research content has stayed "
            "off the default branch."
        ),
        "effect": "none (retired); see T17",
        "check": "manual",
    },
    {
        "id": "T16",
        "created": "2026-10-19",
        "description": (
            "The default branch differs from the branch where CI last passed, so the "
            "gate is green only off the default branch and the default branch itself "
            "carries no working gate. Raised on 2026-10-19 after finding that main had "
            "stayed on the pre-repair commit for six days while CI was green on feat."
        ),
        "threshold": "2026-10-26",
        "effect": (
            "L3 -0.03; declare the gate effective only off the default branch (manual)"
        ),
        "check": "manual",
    },
    {
        "id": "T17",
        "created": "2026-10-20",
        "description": (
            "A long-lived branch stays at least five commits ahead of main. Raised "
            "after correcting the fetch refspec: 'unpushed' had in fact been measuring "
            "'ahead of origin/main', so fixing the refspec cleared T13 while the real "
            "problem - the work is pushed but not merged into the default branch - "
            "remained."
        ),
        "threshold": "2026-10-27",
        "effect": (
            "L3 -0.03; declare the gate usable but the results stranded off the "
            "default branch (manual)"
        ),
        "check": "manual",
    },
    {
        "id": "T18",
        "created": "2026-10-20",
        "description": (
            "CDFV-001 still has no independent specification: no mass, no geometry, no "
            "velocity envelope, no attitude envelope of its own. Numbers used so far are "
            "the P002 cylinder reused as a computational benchmark (CDFV-001-Ref-01B, "
            "scale 1.0), which was a documented configuration decision - but section 12 "
            "of the reference configuration states the P002 geometry is not claimed to be "
            "the final CDFV-001 geometry. Acceptable while the work is analytical. Not "
            "acceptable once Ref-01S must be manufactured, because a scaled physical "
            "model needs real dimensions, and not acceptable for verifying any of the "
            "transfer conditions Stage 1 now states."
        ),
        "threshold": "2026-12-31",
        "effect": (
            "L4 -0.05; record that the project has produced a verification "
            "infrastructure for a vehicle that has never been specified (manual)"
        ),
        "check": "manual",
    },
]

REPAIR_BASE_COMMIT = "abc91031930943c308edea73a97a120cbd6b8bf5"

# Fields compared between snapshots, as dotted paths.
COMPARED_PATHS = [
    "head.commit",
    "worktree.pending_entries",
    "worktree.staged",
    "worktree.untracked",
    "worktree.unpushed_commits",
    "line_endings.files",
    "line_endings.index_crlf",
    "line_endings.worktree_crlf",
    "research_object.sha256",
    "research_object.status",
    "research_object.artifact_count",
    "research_object.claim_count",
    "research_object.evidence_count",
    "research_object.validator_count",
    "research_object.manifest_entries",
    "review_gate.status",
    "review_gate.review_records",
    "review_gate.independent_human_reviews",
    "review_gate.latest_decision",
    "checks_all_ok",
]


def dig(data: dict, dotted: str) -> Any:
    node: Any = data
    for part in dotted.split("."):
        if not isinstance(node, dict) or part not in node:
            return None
        node = node[part]
    return node


def load_snapshots() -> list[tuple[str, dict]]:
    snapshots: list[tuple[str, dict]] = []
    for path in sorted(LOG_DIR.glob("*_ANRI_State.json")):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            continue
        snapshots.append((data.get("as_of_date", path.stem), data))
    return snapshots


def p003_stage1_blocked_count() -> int | None:
    """Count unresolved 'Blocked' cells in the P003 Stage 1 comparison table.

    Returns None when the table cannot be located, so a missing file is reported
    as "cannot evaluate" rather than silently counting as zero blockers.
    """

    path = REPO / "Research_Planning" / "P003_Free_Surface_Loading.md"
    if not path.is_file():
        return None
    lines = path.read_text(encoding="utf-8").splitlines()
    inside = False
    blocked = 0
    for line in lines:
        if line.strip().startswith("#"):
            title = line.strip().lstrip("#").strip().lower()
            if inside:
                break
            inside = "stage 1" in title
            continue
        if not inside or not line.strip().startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 3 or set(cells[0]) <= set("-: "):
            continue
        if "blocked" in cells[2].lower():
            blocked += 1
    return blocked


def count_second_objects() -> int:
    directory = REPO / "Research_Objects"
    if not directory.is_dir():
        return 0
    return len([p for p in directory.glob("RO-*.json") if p.is_file()])


def check_trigger(trigger: dict[str, Any], current: dict, today: date) -> dict[str, Any]:
    kind = trigger["check"]
    threshold = date.fromisoformat(trigger["threshold"])
    wires = today >= threshold

    if kind == "worktree_dirty":
        pending = dig(current, "worktree.pending_entries") or 0
        fired = wires and pending > 0
        detail = f"pending_entries={pending}"
    elif kind == "repair_uncommitted":
        head = dig(current, "head.commit") or ""
        pending = dig(current, "worktree.pending_entries") or 0
        fired = wires and head == REPAIR_BASE_COMMIT and pending > 0
        detail = f"head={head[:7] or 'unknown'} pending={pending}"
    elif kind == "lab_engagement":
        lines = dig(current, "upstream_maturity.lab_engagement_lines")
        fired = wires and bool(lines)
        detail = f"lab_engagement_lines={lines} (no machine-readable response field exists)"
    elif kind == "second_object_reviewed":
        objects = count_second_objects()
        reviews = dig(current, "review_gate.independent_human_reviews") or 0
        fired = wires and objects >= 2 and reviews >= 1
        detail = f"research_objects={objects} independent_human_reviews={reviews}"
    elif kind == "p003_stage1":
        blocked = p003_stage1_blocked_count()
        if blocked is None:
            fired = False
            detail = "cannot evaluate: P003 Stage 1 table not found"
        else:
            fired = wires and blocked > 0
            detail = f"P003 Stage 1 unresolved Blocked cells = {blocked}"
    elif kind == "unpushed":
        unpushed = dig(current, "worktree.unpushed_commits")
        if unpushed is None:
            fired = False
            detail = "cannot evaluate: snapshot has no unpushed_commits field"
        else:
            fired = wires and unpushed > 0
            detail = f"unpushed_commits = {unpushed}"
    elif kind == "human_review":
        reviews = dig(current, "review_gate.independent_human_reviews")
        if reviews is None:
            fired = False
            detail = "cannot evaluate: snapshot has no review_gate field"
        else:
            fired = wires and reviews < 1
            detail = f"independent_human_reviews = {reviews}"
    else:
        fired = False
        detail = "manual check; not machine-evaluable"

    return {
        "id": trigger["id"],
        "description": trigger["description"],
        "threshold": trigger["threshold"],
        "effect": trigger["effect"],
        "detail": detail,
        "status": "FIRED" if fired else ("pending" if not wires else "not met"),
    }


def render_markdown(
    prior_date: str | None,
    current_date: str,
    deltas: list[dict[str, Any]],
    triggers: list[dict[str, Any]],
    trend: list[tuple[str, dict]],
) -> str:
    lines: list[str] = []
    lines.append(f"### Δ {prior_date or '(baseline)'} → {current_date}")
    lines.append("")
    if not prior_date:
        lines.append("No earlier snapshot exists; this is the baseline.")
    elif not deltas:
        lines.append("No compared field changed.")
    else:
        lines.append("| Field | Before | After |")
        lines.append("|---|---|---|")
        for item in deltas:
            lines.append(f"| `{item['field']}` | `{item['before']}` | `{item['after']}` |")
    lines.append("")
    lines.append("### Trigger status")
    lines.append("")
    lines.append("| ID | Threshold | Status | Observed | Promised effect |")
    lines.append("|---|---|---|---|---|")
    for item in triggers:
        lines.append(
            f"| {item['id']} | {item['threshold']} | **{item['status']}** | "
            f"{item['detail']} | {item['effect']} |"
        )
    lines.append("")
    lines.append("### Snapshot trend")
    lines.append("")
    lines.append(
        "| Date | head | pending | artifacts | independent human reviews | checks ok |"
    )
    lines.append("|---|---|---:|---:|---:|---|")
    for as_of, data in trend:
        head = (dig(data, "head.commit") or "?")[:7]
        lines.append(
            f"| {as_of} | `{head}` | {dig(data, 'worktree.pending_entries')} | "
            f"{dig(data, 'research_object.artifact_count')} | "
            f"{dig(data, 'review_gate.independent_human_reviews')} | "
            f"{dig(data, 'checks_all_ok')} |"
        )
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    force_utf8_io()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--prior", type=Path, default=None)
    parser.add_argument("--current", type=Path, default=None)
    parser.add_argument("--markdown", action="store_true")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--date", default=None)
    args = parser.parse_args(argv)

    today = date.fromisoformat(args.date) if args.date else date.today()

    if args.current is not None:
        current = json.loads(args.current.read_text(encoding="utf-8"))
        current_date = current.get("as_of_date", args.current.stem)
        if args.prior is not None:
            prior = json.loads(args.prior.read_text(encoding="utf-8"))
            prior_date = prior.get("as_of_date", args.prior.stem)
        else:
            prior, prior_date = None, None
    else:
        snapshots = load_snapshots()
        if not snapshots:
            print(
                "ERROR: no snapshots found. Run scripts/collect_state.py first.",
            )
            return 2
        current_date, current = snapshots[-1]
        if len(snapshots) >= 2:
            prior_date, prior = snapshots[-2]
        else:
            prior, prior_date = None, None

    deltas: list[dict[str, Any]] = []
    if prior is not None:
        for path in COMPARED_PATHS:
            before, after = dig(prior, path), dig(current, path)
            if before != after:
                deltas.append({"field": path, "before": before, "after": after})

    triggers = [check_trigger(item, current, today) for item in TRIGGERS]

    result = {
        "prior_date": prior_date,
        "current_date": current_date,
        "deltas": deltas,
        "triggers": triggers,
        "fired": [item["id"] for item in triggers if item["status"] == "FIRED"],
    }

    if args.markdown:
        print(
            render_markdown(
                prior_date, current_date, deltas, triggers, load_snapshots()
            )
        )
    elif args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(f"prior: {prior_date or '(baseline)'}  current: {current_date}")
        print(f"changed fields: {len(deltas)}")
        for item in deltas:
            print(f"  {item['field']}: {item['before']!r} -> {item['after']!r}")
        fired = result["fired"]
        print(f"triggers fired: {fired if fired else 'none'}")
        for item in triggers:
            print(f"  {item['id']} [{item['status']}] {item['detail']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
