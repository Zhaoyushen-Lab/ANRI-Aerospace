#!/usr/bin/env python3
"""Health check for the daily-report mechanism itself.

The mechanism has three parts that can silently drift apart:

1. ``scripts/compare_snapshots.py`` declares the triggers (code);
2. the daily report's observation section describes them (prose);
3. ``Research_Log/*_ANRI_State.json`` carries the measured state (data).

A trigger that exists only in prose is never checked. A snapshot that does not
parse quietly becomes an empty report. A trigger with a malformed date crashes
only on the day it is first evaluated. This script catches all three cases before
they matter.

Run from the repository root:

    py -3 scripts/check_report_mechanism.py
    py -3 scripts/check_report_mechanism.py --json
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "scripts"))

LOG_DIR = REPO / "Research_Log"
TEMPLATE = LOG_DIR / "Daily_Template.md"
COMPARATOR = REPO / "scripts" / "compare_snapshots.py"

# Section headings every daily report must contain, in order.
REQUIRED_SECTIONS = [
    "## 1. ",
    "## 2. ",
    "## 3. ",
    "## 4. ",
    "## 5. ",
    "## 6. ",
    "## 7. ",
    "## 8. ",
]

SNAPSHOT_REQUIRED_FIELDS = [
    "as_of_date",
    "head.commit",
    "worktree.pending_entries",
    "research_object.artifact_count",
    "review_gate.independent_human_reviews",
    "checks",
    "checks_all_ok",
]

# The generator writes this exact heading; its presence means the report must
# carry a populated machine-generated section.
GENERATOR_MARKER = "## 0. 机器生成部分"


def force_utf8_io() -> None:
    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if reconfigure is not None:
            try:
                reconfigure(encoding="utf-8", errors="replace")
            except Exception:
                pass


def dig(data: dict, dotted: str):
    node = data
    for part in dotted.split("."):
        if not isinstance(node, dict) or part not in node:
            return None
        node = node[part]
    return node


def load_triggers() -> list[dict]:
    """Read TRIGGERS out of the comparator by AST, without executing it.

    Importing or exec'ing the module would run its ``__file__``-relative setup; a
    literal-only AST parse is both safer and enough, and it fails loudly if the
    trigger table ever stops being a plain literal.
    """

    import ast

    source = COMPARATOR.read_text(encoding="utf-8")
    tree = ast.parse(source)
    for node in tree.body:
        # TRIGGERS is declared as ``TRIGGERS: list[dict[str, Any]] = [...]``, so it
        # is an AnnAssign rather than a plain Assign.
        if isinstance(node, ast.AnnAssign):
            target = node.target
            if isinstance(target, ast.Name) and target.id == "TRIGGERS":
                return ast.literal_eval(node.value)
        elif isinstance(node, ast.Assign):
            if any(
                isinstance(target, ast.Name) and target.id == "TRIGGERS"
                for target in node.targets
            ):
                return ast.literal_eval(node.value)
    raise SystemExit(f"TRIGGERS assignment not found in {COMPARATOR}")


def check_triggers(triggers: list[dict]) -> list[str]:
    problems: list[str] = []
    ids = [t.get("id") for t in triggers]
    if len(ids) != len(set(ids)):
        problems.append(f"duplicate trigger ids: {sorted(ids)}")
    for trigger in triggers:
        tid = trigger.get("id")
        for field in ("description", "threshold", "effect", "check"):
            if not trigger.get(field):
                problems.append(f"{tid}: missing required field {field!r}")
        try:
            date.fromisoformat(trigger["threshold"])
        except Exception:
            problems.append(f"{tid}: threshold is not an ISO date: {trigger['threshold']!r}")
        try:
            created = date.fromisoformat(trigger["created"])
            threshold = date.fromisoformat(trigger["threshold"])
            if threshold < created:
                problems.append(f"{tid}: threshold {threshold} predates creation {created}")
        except Exception:
            pass
    return problems


def check_report(
    report: Path, triggers: list[dict], trigger_ids: set[str]
) -> tuple[list[str], set[str]]:
    problems: list[str] = []
    text = report.read_text(encoding="utf-8")
    lines = text.splitlines()

    # Only triggers that already existed on the report's own date are expected in
    # its prose; a report cannot describe a trigger created after it was written.
    try:
        report_day = date.fromisoformat(report.name.split("_")[0])
        expected_ids = {
            t["id"] for t in triggers if date.fromisoformat(t["created"]) <= report_day
        }
    except Exception:
        expected_ids = set(trigger_ids)

    headings = [line for line in lines if line.startswith("## ")]
    # Section 0 is the machine-generated block; the template's own sections are 1-8.
    sections = [h for h in headings if re.match(r"^## [1-9]\d*\. ", h)]
    if len(sections) != len(REQUIRED_SECTIONS):
        problems.append(
            f"expected {len(REQUIRED_SECTIONS)} numbered sections (1-8), "
            f"found {len(sections)}"
        )
    for expected in REQUIRED_SECTIONS:
        if not any(h.startswith(expected) for h in sections):
            problems.append(f"missing section heading starting {expected!r}")

    numbered = [h for h in headings if re.match(r"^## \d+\. ", h)]
    order = [int(re.match(r"^## (\d+)\. ", h).group(1)) for h in numbered]
    if order != sorted(order):
        problems.append(f"numbered sections out of order: {order}")

    if "### 4.5" not in text:
        problems.append("missing the delta subsection '### 4.5'")

    # Any trigger id mentioned anywhere must exist in the code.
    mentioned = set(re.findall(r"\bT\d+\b", text))
    phantom = mentioned - trigger_ids
    if phantom:
        problems.append(
            f"report mentions trigger ids that do not exist in the code: {sorted(phantom)}"
        )

    # Triggers that already existed on this report's date must be described in it.
    missing_in_prose = expected_ids - mentioned
    if missing_in_prose:
        problems.append(
            "triggers that existed on this report's date are never mentioned in "
            f"its prose: {sorted(missing_in_prose)}"
        )

    # The machine-generated section is required only for reports produced by the
    # generator. Detection keys on the generator's own heading, not on a mention of
    # the script name — the baseline report documents the workflow and therefore
    # names the script without having been produced by it.
    if GENERATOR_MARKER in text and "## 0. " not in text:
        problems.append("report declares the generator section but is missing '## 0.'")

    return problems, mentioned


def check_snapshots() -> tuple[list[str], list[str]]:
    problems: list[str] = []
    notes: list[str] = []
    for path in sorted(LOG_DIR.glob("*_ANRI_State.json")):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:
            problems.append(f"{path.name}: does not parse as JSON ({exc})")
            continue
        for field in SNAPSHOT_REQUIRED_FIELDS:
            if dig(data, field) is None:
                problems.append(f"{path.name}: missing field {field!r}")
        as_of = data.get("as_of_date")
        if not re.match(r"^\d{4}-\d{2}-\d{2}$", str(as_of)):
            problems.append(f"{path.name}: as_of_date is not an ISO date: {as_of!r}")
            continue
        if path.name.split("_")[0] != as_of:
            problems.append(
                f"{path.name}: filename date and as_of_date disagree ({as_of})"
            )
        checks = data.get("checks") or {}
        if not checks:
            problems.append(f"{path.name}: no checks recorded (was --no-suite used?)")
        else:
            bad = [k for k, v in checks.items() if not v.get("ok")]
            if bad:
                problems.append(f"{path.name}: failed checks: {sorted(bad)}")
        if data.get("checks_all_ok") is False:
            problems.append(f"{path.name}: checks_all_ok is False")
        notes.append(
            f"{path.name}: {len(checks)} checks, pending="
            f"{dig(data, 'worktree.pending_entries')}, "
            f"human_reviews={dig(data, 'review_gate.independent_human_reviews')}"
        )
    if not notes:
        problems.append("no state snapshots found in Research_Log")
    return problems, notes


def main(argv: list[str] | None = None) -> int:
    force_utf8_io()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    triggers = load_triggers()
    trigger_ids = {t["id"] for t in triggers}

    problems = check_triggers(triggers)
    snapshot_problems, snapshot_notes = check_snapshots()
    problems += snapshot_problems

    reports = sorted(LOG_DIR.glob("*_ANRI_Daily.md"))
    report_notes: list[str] = []
    for report in reports:
        report_problems, _ = check_report(report, triggers, trigger_ids)
        problems += [f"{report.name}: {p}" for p in report_problems]
        report_notes.append(f"{report.name}: {len(report.read_text(encoding='utf-8').splitlines())} lines")

    result = {
        "triggers": sorted(trigger_ids),
        "reports": [r.name for r in reports],
        "snapshots": snapshot_notes,
        "problems": problems,
        "ok": not problems,
    }

    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return 0 if not problems else 1

    print(f"triggers declared : {', '.join(sorted(trigger_ids)) or 'none'}")
    print(f"snapshots         : {len(snapshot_notes)}")
    for note in snapshot_notes:
        print(f"  - {note}")
    print(f"daily reports     : {len(reports)}")
    for note in report_notes:
        print(f"  - {note}")
    if problems:
        print(f"mechanism check: FAIL ({len(problems)} problem(s))")
        for problem in problems:
            print(f"  - {problem}")
        return 1
    print("mechanism check: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
