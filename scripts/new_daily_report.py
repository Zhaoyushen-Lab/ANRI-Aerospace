#!/usr/bin/env python3
"""Initialise a daily report from the template plus machine-derived sections.

The daily report has two halves: sections that must be measured (date, snapshot
reference, Δ table, trigger status, trend) and sections that need judgement
(upstream findings, layer assessment, probabilities).  This script fills the
first half from the snapshots so the author cannot accidentally hand-write a
number that disagrees with the snapshot, and leaves the second half explicitly
marked TODO.

Run from the repository root:

    py -3 scripts/new_daily_report.py                       # today, if absent
    py -3 scripts/new_daily_report.py --date 2026-10-12
    py -3 scripts/new_daily_report.py --date 2026-10-12 --force
    py -3 scripts/new_daily_report.py --date 2026-10-12 --stdout
"""

from __future__ import annotations

import argparse
import json
import re
from datetime import date
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
LOG_DIR = REPO / "Research_Log"
TEMPLATE = LOG_DIR / "Daily_Template.md"

import subprocess  # noqa: E402
import sys  # noqa: E402


def force_utf8_io() -> None:
    """Emit UTF-8 regardless of the Windows ANSI code page."""

    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if reconfigure is not None:
            try:
                reconfigure(encoding="utf-8", errors="replace")
            except Exception:
                pass


def run_helper(args: list[str]) -> str:
    # encoding="utf-8" is required: the default on Windows is the ANSI code page,
    # which would corrupt the Chinese text produced by the comparator.
    completed = subprocess.run(
        [sys.executable, *args],
        cwd=REPO,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )
    return completed.stdout


def snapshot_path(day: str) -> Path:
    return LOG_DIR / f"{day}_ANRI_State.json"


def daily_path(day: str) -> Path:
    return LOG_DIR / f"{day}_ANRI_Daily.md"


def build(day: str) -> str:
    template = TEMPLATE.read_text(encoding="utf-8") if TEMPLATE.is_file() else ""
    delta_md = run_helper(
        ["scripts/compare_snapshots.py", "--markdown", "--date", day]
    ).strip()

    snapshot = snapshot_path(day)
    snapshot_note = (
        f"`Research_Log/{snapshot.name}`"
        if snapshot.is_file()
        else f"`Research_Log/{snapshot.name}`（**尚未生成**：先运行 `py -3 .\\scripts\\collect_state.py --out \"Research_Log\\{snapshot.name}\"`）"
    )

    body = template
    if body:
        # Replace the template's placeholder header block with concrete values.
        body = body.replace("`YYYY-MM-DD`", f"`{day}`", 1)
        # Use a lambda so Windows-style backslashes in the replacement are not
        # interpreted as regex escapes.
        replacement = f"- 状态快照：{snapshot_note}"
        body = re.sub(
            r"^- 状态快照：.*$",
            lambda _match: replacement,
            body,
            count=1,
            flags=re.MULTILINE,
        )
        # Drop the template's own usage preamble (everything before the first ---).
        parts = body.split("\n---\n", 1)
        if len(parts) == 2:
            body = parts[1]

    machine_block = (
        f"\n---\n\n## 0. 机器生成部分（由脚本填充，请勿手改）\n\n"
        f"> 生成命令：\n>\n"
        f"> ```powershell\n"
        f"> py -3 .\\scripts\\collect_state.py --out \"Research_Log\\{snapshot.name}\"\n"
        f"> py -3 .\\scripts\\compare_snapshots.py --markdown --date {day}\n"
        f"> ```\n\n"
        f"{delta_md}\n"
    )

    header = (
        f"# ANRI / AI4S / AI4E 日报 — {day}\n\n"
        f"- 日期：{day}\n"
        f"- 口径版本：`v1`\n"
        f"- 状态快照：{snapshot_note}\n"
        f"- 上一份日报：见 §4.5（由 `compare_snapshots.py` 自动识别）\n"
    )

    return header + machine_block + "\n---\n" + body


def main(argv: list[str] | None = None) -> int:
    force_utf8_io()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--date", default=None)
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--stdout", action="store_true")
    parser.add_argument(
        "--allow-missing-snapshot",
        action="store_true",
        help=(
            "Generate even when that day's state snapshot is absent. By default "
            "this is refused, because such a report silently loses its "
            "machine-generated section and can no longer be cross-checked."
        ),
    )
    args = parser.parse_args(argv)

    day = args.date or date.today().isoformat()
    target = daily_path(day)
    text = build(day)

    if not args.allow_missing_snapshot and not snapshot_path(day).is_file():
        print(
            f"ERROR: snapshot {snapshot_path(day).name} does not exist.\n"
            f"  Run: py -3 .\\scripts\\collect_state.py --out "
            f"\"Research_Log\\{snapshot_path(day).name}\"\n"
            "  or pass --allow-missing-snapshot to accept an empty machine section.",
            file=sys.stderr,
        )
        return 2

    if args.stdout:
        print(text)
        return 0

    if target.exists() and not args.force:
        print(f"refusing to overwrite existing report: {target.name} (use --force)")
        return 1

    with target.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write(text)
    print(f"wrote {target.relative_to(REPO).as_posix()}")
    if not snapshot_path(day).is_file():
        print(
            f"NOTE: snapshot {snapshot_path(day).name} does not exist yet; "
            "§0 will be empty until it is collected."
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
