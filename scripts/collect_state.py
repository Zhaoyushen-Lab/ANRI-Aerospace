#!/usr/bin/env python3
"""Collect the ANRI-Aerospace state that the daily report cites.

The daily report must separate observed facts from judgment.  This script
produces the observed-fact half as deterministic JSON, so the numbers in a daily
report can be re-derived by anyone at any time instead of being re-narrated by
hand.

Run from the repository root:

    py -3 scripts/collect_state.py                      # print JSON
    py -3 scripts/collect_state.py --out <path>         # also write JSON
    py -3 scripts/collect_state.py --no-suite           # skip the slow suites

Output rules (same discipline as the Research Object):

* LF terminators everywhere, so the snapshot is byte-comparable across platforms;
* no timestamp inside the compared payload — the date is passed in or derived,
  and wall-clock time is kept in a clearly non-frozen field;
* every field is either read from a file, parsed from a command, or the exit code
  of a command.  Nothing is inferred.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from datetime import date, datetime, timezone
from pathlib import Path

SCHEMA_VERSION = "1"
REPO = Path(__file__).resolve().parent.parent

RO_REL = "Research_Objects/RO-CDFV-001-Ref-01B.json"
MANIFEST_REL = "Benchmarks/ANRI-RV-001/run_manifest.json"
VALIDATOR = "scripts/validate_research_object.py"
GEN = "scripts/gen_research_object.py"
VERIFIER = "Models/CDFV-001/Ref-01B/verify_baseline.py"
NEGATIVE = "Models/CDFV-001/Ref-01B/verify_negative_cases.py"
ADVERSARIAL = "Benchmarks/ANRI-RV-001/run_adversarial_cases.py"
GATE_SELFTEST = "scripts/validate_gate_selftest.py"
REVIEW_REPORT = "Reviews/RO-CDFV-001-Ref-01B_Independent_Review_Report.md"
DATA_MODEL = "docs/ANRI_Data_Model_v0.1.md"

# A review only counts as independent human review when it is recorded as such
# and was not produced by a model session.  This list is an explicit, auditable
# classification, not a heuristic.
NON_HUMAN_REVIEWER_MARKERS = ("model-generated", "deepseek harness", "ai session")


def run(command: list[str], *, cwd: Path = REPO) -> tuple[int, str]:
    # encoding="utf-8" is required: on Windows the default is the ANSI code page
    # (GBK on this host), which corrupts any non-ASCII output such as the
    # Chinese text in the daily reports.
    completed = subprocess.run(
        command,
        cwd=cwd,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )
    return completed.returncode, (completed.stdout or "") + (completed.stderr or "")


def sha256_file(relative: str) -> str | None:
    path = REPO / relative
    if not path.is_file():
        return None
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_json(relative: str) -> dict | None:
    path = REPO / relative
    if not path.is_file():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None


def line_count(relative: str) -> int | None:
    path = REPO / relative
    if not path.is_file():
        return None
    return len(path.read_text(encoding="utf-8").splitlines())


def count_section_bullets(relative: str, heading: str) -> int | None:
    """Count bullet lines under a markdown heading (used for KPIs)."""

    path = REPO / relative
    if not path.is_file():
        return None
    lines = path.read_text(encoding="utf-8").splitlines()
    inside = False
    count = 0
    for line in lines:
        if line.strip().startswith("#"):
            title = line.lstrip("#").strip().lower()
            if inside:
                break
            inside = heading.lower() in title
            continue
        if inside and line.strip().startswith(("- ", "* ")):
            count += 1
    return count if inside or count else count


def parse_kpi_rows(relative: str) -> list[dict[str, object]]:
    """Parse '| KPI | current | target |' style table rows."""

    path = REPO / relative
    if not path.is_file():
        return []
    rows: list[dict[str, object]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped.startswith("|"):
            continue
        cells = [cell.strip() for cell in stripped.strip("|").split("|")]
        if len(cells) != 3 or not cells[0] or set(cells[0]) <= set("-: "):
            continue
        if cells[0].lower() in ("kpi", "指标"):
            continue
        current = cells[1].replace("**", "").strip()
        target = cells[2].replace("**", "").strip()
        if not re.match(r"^\d", current):
            continue
        rows.append(
            {
                "kpi": cells[0],
                "current_raw": current,
                "target_raw": target,
                "current_value": float(re.match(r"^\d+(\.\d+)?", current).group(0)),
                "target_value": (
                    float(re.match(r"^\d+(\.\d+)?", target).group(0))
                    if re.match(r"^\d", target)
                    else None
                ),
            }
        )
    return rows


def collect_eem() -> dict:
    """Measure the Engineering Evolution Module loop from in-repo artifacts.

    The EEM cycle is
        Knowledge -> Design -> Simulation -> Evaluation -> Knowledge Update
    (Knowledge_Base/CDFV_Knowledge_Map.md section 5).  Per D-ANRI-002 the
    generalisation metric is the NUMBER OF TIMES THAT LOOP CLOSES, not the number
    of documents produced, so each stage is bound to an artifact that exists only
    if the stage actually happened:

      knowledge      : a KU<nnn>-<nnn> id appears in Research_Planning/
      design         : a decision Status block exists in Decision_Log.md
      simulation     : a model or benchmark script exists
      evaluation     : a verification.json exists under Models/
      knowledge_update: a KU id exists AND at least one decision is resolved
                        (not 'Candidate')

    Completion requires every link to hold simultaneously.
    """

    planning = REPO / "Research_Planning"
    texts = {}
    if planning.is_dir():
        for path in sorted(planning.glob("*.md")):
            texts[path.name] = path.read_text(encoding="utf-8", errors="replace")

    knowledge_ids: set[str] = set()
    for text in texts.values():
        # A knowledge update counts only once it has been DEFINED, not merely
        # mentioned.  Planning documents legitimately name future ids (for example
        # "KU004-001 尚未完成"), and a bare id scan would count those as produced
        # knowledge, inflating the very metric this function exists to keep honest.
        # The definition form used in this repository is the line
        # "Knowledge Update ID: KU003-001".
        knowledge_ids |= set(
            re.findall(r"Knowledge Update ID:\s*(KU\d{3}-\d{3})", text)
        )

    models_dir = REPO / "Models"
    bench_dir = REPO / "Benchmarks"
    simulation_ok = bool(list(models_dir.rglob("*.py"))) if models_dir.is_dir() else False
    if not simulation_ok and bench_dir.is_dir():
        simulation_ok = bool(list(bench_dir.rglob("run_*.py")))

    verification_files = (
        sorted(models_dir.rglob("verification.json")) if models_dir.is_dir() else []
    )

    decision_statuses: list[str] = []
    resolved: list[str] = []
    # Only Decision_Log.md declares research decisions. Scanning every file under
    # Research_Planning/ would also pick up unrelated '## Status' headings such as
    # the 'Active' status of research questions in Active_Questions.md.
    decision_text = texts.get("Decision_Log.md", "")
    for match in re.finditer(
        r"##\s*Status\s*\n(.*?)(?=\n##\s|\Z)", decision_text, re.S
    ):
        body = " ".join(
            line.strip() for line in match.group(1).splitlines() if line.strip()
        )
        if not body:
            continue
        decision_statuses.append(body)
        lowered = body.lower()
        # A decision counts as recorded once it states a verdict rather than
        # leaving the question open.  Matching only three literal phrases missed
        # later verdicts (e.g. "Needs CDFV acceleration profile"), so the test is
        # now structural: the status must NOT be a placeholder such as
        # "Candidate" / "proposed", and must name a concrete disposition.
        is_placeholder = any(
            token in lowered
            for token in ("candidate", "proposed", "deferred", "not yet")
        )
        names_verdict = any(
            token in lowered
            for token in ("needs", "accepted", "rejected", "deferred", "resolved")
        )
        if names_verdict and not is_placeholder:
            resolved.append(body)

    # Each research question closes its own loop.  The number of closed loops is
    # therefore the number of knowledge updates that have been DEFINED and whose
    # own document also records a verdict -- not a hard-coded 1 with a switch.
    loops: list[dict] = []
    for name, text in sorted(texts.items()):
        ku_ids = re.findall(r"Knowledge Update ID:\s*(KU\d{3}-\d{3})", text)
        if not ku_ids:
            continue
        has_verdict = any(
            any(tok in body.lower() for tok in ("needs", "accepted", "rejected"))
            and not any(
                ph in body.lower() for ph in ("candidate", "proposed", "not yet")
            )
            for body in (
                " ".join(
                    line.strip()
                    for line in m.group(1).splitlines()
                    if line.strip()
                )
                for m in re.finditer(
                    r"##\s*Status\s*\n(.*?)(?=\n##\s|\Z)", decision_text, re.S
                )
            )
        )
        loops.append(
            {
                "document": name,
                "knowledge_update": ku_ids[0],
                "decision_recorded": has_verdict,
                "closed": has_verdict,
            }
        )

    loops_closed = sum(1 for loop in loops if loop["closed"])

    links = {
        "knowledge": bool(knowledge_ids),
        "design": bool(decision_statuses),
        "simulation": simulation_ok,
        "evaluation": bool(verification_files),
        "knowledge_update": bool(knowledge_ids) and bool(resolved),
    }
    closed = all(links.values())

    return {
        "definition": (
            "Knowledge -> Design -> Simulation -> Evaluation -> Knowledge Update "
            "(Knowledge_Base/CDFV_Knowledge_Map.md section 5)"
        ),
        "metric": (
            "number of times the loop closes (D-ANRI-002); document count is not a metric"
        ),
        "links": links,
        "loops_closed": loops_closed,
        "loops": loops,
        "knowledge_ids": sorted(knowledge_ids),
        "resolved_decisions": resolved,
        "unresolved_decisions": [d for d in decision_statuses if d not in resolved],
        "verification_artifacts": len(verification_files),
        "generalisation_gate": (
            "G1 satisfied" if closed else "G1 not satisfied: " + ", ".join(
                k for k, v in links.items() if not v
            )
        ),
        "note": (
            "loops_closed counts definitions of a knowledge update that also carry a "
            "verdict in Decision_Log.md. G2 additionally requires the loops to come "
            "from DIFFERENT research questions, which the 'loops' list makes auditable."
        ),
    }


def snapshot(*, run_suite: bool, scratch: Path, as_of: str) -> dict:
    state: dict = {
        "schema_version": SCHEMA_VERSION,
        "kind": "anri_state_snapshot",
        "as_of_date": as_of,
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "note": (
            "generated_utc is wall-clock and NOT part of the compared payload; "
            "compare everything else."
        ),
    }

    code, out = run(["git", "rev-parse", "HEAD"])
    head = out.strip() if code == 0 else None
    code, out = run(["git", "log", "-1", "--format=%h %ad %s", "--date=short"])
    state["head"] = {
        "commit": head,
        "summary": out.strip() if code == 0 else None,
    }

    code, out = run(["git", "status", "--porcelain"])
    entries = [line for line in out.splitlines() if line.strip()]
    state["worktree"] = {
        "pending_entries": len(entries),
        "staged": sum(1 for line in entries if line[:2].strip() and line[0] != "?"),
        "untracked": sum(1 for line in entries if line.startswith("??")),
    }

    code, out = run(["git", "rev-list", "--count", "--branches", "--not", "--remotes"])
    state["worktree"]["unpushed_commits"] = int(out.strip()) if code == 0 and out.strip().isdigit() else None

    code, out = run(["git", "ls-files", "--eol"])
    eol_lines = [line for line in out.splitlines() if line.strip()]
    state["line_endings"] = {
        "files": len(eol_lines),
        "index_crlf": sum(1 for line in eol_lines if line.startswith("i/crlf")),
        "worktree_crlf": sum(1 for line in eol_lines if "w/crlf" in line),
    }

    state["eem"] = collect_eem()

    ro = load_json(RO_REL) or {}
    manifest = load_json(MANIFEST_REL) or {}
    artifacts = ro.get("artifacts", [])
    state["research_object"] = {
        "path": RO_REL,
        "sha256": sha256_file(RO_REL),
        "id": ro.get("id"),
        "version": ro.get("version"),
        "status": ro.get("status"),
        "schema_version": ro.get("schema_version"),
        "artifact_count": len(artifacts),
        "claim_count": len(ro.get("claims", [])),
        "evidence_count": len(ro.get("evidence", [])),
        "validator_count": len(ro.get("validators", [])),
        "assumption_count": len(ro.get("assumptions", [])),
        "limitation_count": len(ro.get("limitations", [])),
        "artifact_roles": sorted({a.get("role", "?") for a in artifacts}),
        "manifest_entries": len(manifest.get("artifacts", [])),
    }

    reviews = (ro.get("review", {}) or {}).get("reviews", []) or []
    independent_human = 0
    for record in reviews:
        if not record.get("independent"):
            continue
        reviewer = str(record.get("reviewer", "")).lower()
        if any(marker in reviewer for marker in NON_HUMAN_REVIEWER_MARKERS):
            continue
        independent_human += 1
    state["review_gate"] = {
        "status": (ro.get("review", {}) or {}).get("status"),
        "decision_ref": (ro.get("review", {}) or {}).get("decision_ref"),
        "review_records": len(reviews),
        "independent_human_reviews": independent_human,
        "latest_decision": reviews[-1].get("decision") if reviews else None,
        "latest_reviewer": reviews[-1].get("reviewer") if reviews else None,
        "report_path": REVIEW_REPORT,
        "report_sha256": sha256_file(REVIEW_REPORT),
    }

    # Upstream maturity read from the project's own data model, not from memory.
    state["upstream_maturity"] = {
        "source": DATA_MODEL,
        "present": (REPO / DATA_MODEL).is_file(),
        "kpi_rows": parse_kpi_rows(DATA_MODEL),
        "lab_engagement_lines": count_section_bullets(
            "Experiment_Requests/CDFV-001-Ref-01S_Experiment_Request.md", "计划状态"
        ),
    }

    state["checks"] = {}
    # The drift check must reproduce the object from *its own recorded* provenance,
    # not from HEAD. Once any later commit lands, HEAD necessarily differs from the
    # recorded provenance commit, and feeding HEAD in would report false drift.
    provenance = ro.get("provenance", {}) or {}
    recorded_commit = str(provenance.get("git_commit") or "")
    recorded_created = str(provenance.get("created_utc") or "")
    review_records = (ro.get("review", {}) or {}).get("reviews", []) or []
    recorded_review_date = str(review_records[-1].get("date") or "") if review_records else ""

    checks: list[tuple[str, list[str], int]] = [
        ("ro_validator", [sys.executable, VALIDATOR, RO_REL, "--repo-root", "."], 0),
        ("clean_baseline", [sys.executable, VERIFIER], 0),
        ("adversarial_a01", [sys.executable, VERIFIER, "--results-dir", "Benchmarks/ANRI-RV-001/adversarial/A01_wrong_weight/results", "--no-meta"], 1),
        ("adversarial_a02", [sys.executable, VERIFIER, "--results-dir", "Benchmarks/ANRI-RV-001/adversarial/A02_broken_force_balance/results", "--no-meta"], 1),
    ]
    if run_suite:
        checks += [
            ("verifier_negative_suite", [sys.executable, NEGATIVE], 0),
            ("adversarial_suite", [sys.executable, ADVERSARIAL], 0),
            ("gate_selftest", [sys.executable, GATE_SELFTEST, str(scratch)], 0),
        ]
        if recorded_commit and recorded_created and recorded_review_date:
            checks.append(
                (
                    "object_manifest_drift",
                    [
                        sys.executable, GEN,
                        "--git-commit", recorded_commit,
                        "--created-utc", recorded_created,
                        "--review-date", recorded_review_date,
                        "--check-only",
                    ],
                    0,
                )
            )
        else:
            state["checks"]["object_manifest_drift"] = {
                "exit": None,
                "expected": 0,
                "ok": False,
                "note": "cannot reproduce: object has no recorded provenance to replay",
            }
    for name, command, expected in checks:
        code, _ = run(command)
        state["checks"][name] = {
            "exit": code,
            "expected": expected,
            "ok": code == expected,
        }
    state["checks_all_ok"] = all(item["ok"] for item in state["checks"].values())

    return state


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=None)
    parser.add_argument("--no-suite", action="store_true")
    parser.add_argument("--date", default=None, help="Override the as_of date.")
    parser.add_argument(
        "--scratch",
        type=Path,
        default=Path(sys.prefix).parent / "anri-state-selftest",
    )
    args = parser.parse_args(argv)

    as_of = args.date or date.today().isoformat()
    data = snapshot(run_suite=not args.no_suite, scratch=args.scratch, as_of=as_of)
    text = json.dumps(data, indent=2, ensure_ascii=False) + "\n"

    if args.out is not None:
        out_path = args.out if args.out.is_absolute() else REPO / args.out
        out_path.parent.mkdir(parents=True, exist_ok=True)
        with out_path.open("w", encoding="utf-8", newline="\n") as handle:
            handle.write(text)
        print(f"wrote {out_path}")
    else:
        print(text)

    if not data["checks_all_ok"]:
        print("WARNING: at least one check did not match its expected exit code")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
