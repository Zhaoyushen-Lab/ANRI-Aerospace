"""Generate a tampered copy of the verification baseline for blind testing.

Purpose
-------
The clean-room replication brief asks an outside person to judge whether the
repository's "verified" result can be reproduced.  Reproducing it on the intact
repository only proves the reproduction path runs.  The stronger question is
whether the reader's procedure can DETECT a wrong number, which is what a
verifier is actually for.

This script builds the blind copy used for that second test:

  * copies only git-tracked files, so the copy has no build residue and no
    untracked scratch of the author's;
  * applies exactly one fault, chosen by id (see ``--list``);
  * writes an answer key OUTSIDE the blind copy, so that whoever receives the
    copy cannot read the answer even if they look around the tree;
  * optionally runs the repository's own verifier against the copy and reports
    whether the fault was detected, which is the author-side self-test.

Every fault here is detectable from the repository's own documented facts alone
(the force balance, the stated model constants, and the column meanings), so a
reader who follows the brief's section 3 can find it without extra knowledge.

Usage
-----
    py -3 .\\Benchmarks\\ANRI-RV-001\\make_blind_copy.py --list
    py -3 .\\Benchmarks\\ANRI-RV-001\\make_blind_copy.py --fault F1
    py -3 .\\Benchmarks\\ANRI-RV-001\\make_blind_copy.py --fault F1 --verify
    py -3 .\\Benchmarks\\ANRI-RV-001\\make_blind_copy.py --fault F2 --dest D:\\hand-off

Exit codes: 0 success, 1 the fault was NOT detected (only with ``--verify``),
2 usage or input error.
"""

from __future__ import annotations

import argparse
import csv
import io
import shutil
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
RESULTS_REL = Path("Models/CDFV-001/Ref-01B/results")
VERIFIER_REL = Path("Models/CDFV-001/Ref-01B/verify_baseline.py")
DEFAULT_DEST = REPO / "Blind_Copies"

# The three baseline result files, all crossing the free surface.
TARGETS = (
    "Ref-01B-B-0p10mps.csv",
    "Ref-01B-B-0p25mps.csv",
    "Ref-01B-B-0p50mps.csv",
)


def read_rows(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    """Read a CSV, keeping the field order and rejecting anything unexpected."""

    text = path.read_text(encoding="utf-8")
    reader = csv.DictReader(io.StringIO(text))
    if reader.fieldnames is None:
        raise SystemExit(f"{path}: no header row")
    return list(reader.fieldnames), list(reader)


def write_rows(path: Path, fieldnames: list[str], rows: list[dict[str, str]]) -> None:
    """Write a CSV with LF endings only, byte-compatible with the originals."""

    buffer = io.StringIO(newline="")
    writer = csv.DictWriter(buffer, fieldnames=fieldnames, lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    path.write_bytes(buffer.getvalue().encode("utf-8"))


# --------------------------------------------------------------------------
# Faults.  Each returns a human-readable description of what it changed.
# --------------------------------------------------------------------------


def fault_f1(results: Path) -> str:
    """Add 5% to the buoyancy force on one row, leaving the balance broken.

    This is the fault that speaks directly to the brief's question 1: the reader
    is asked whether every row satisfies the force balance.  A 5% buoyancy
    change on a single row is invisible to the eye (the value still looks like a
    plausible force) but shows up immediately in the balance residual.
    """

    name = "Ref-01B-B-0p25mps.csv"
    path = results / name
    fieldnames, rows = read_rows(path)
    index = len(rows) // 2
    old = float(rows[index]["buoyancy_N"])
    new = old * 1.05
    rows[index]["buoyancy_N"] = repr(new)
    write_rows(path, fieldnames, rows)
    return (
        f"{name}: row {index} (time_s={rows[index]['time_s']}) buoyancy_N "
        f"{old!r} -> {new!r} (+5%)"
    )


def fault_f2(results: Path) -> str:
    """Make the time column non-uniform by nudging one interior timestamp.

    The verifier only requires monotonicity, and the timestamps look like a plain
    uniform grid, so a reader who assumes "time is uniform" will not check it.
    The brief never claims the grid is uniform, so a careful reader is entitled
    to test it.
    """

    name = "Ref-01B-B-0p25mps.csv"
    path = results / name
    fieldnames, rows = read_rows(path)
    index = len(rows) // 3
    old = rows[index]["time_s"]
    new = round(float(old) + 0.002, 6)
    rows[index]["time_s"] = repr(new)
    write_rows(path, fieldnames, rows)
    return f"{name}: row {index} time_s {old} -> {new} (breaks the uniform 0.001 s step)"


def fault_f3(results: Path) -> str:
    """Scale one file's weight column by 0.85, i.e. a wrong mass assumption.

    The balance still holds if the reader recomputes mass from the weight column,
    but the weight no longer matches the documented 2.030 kg x 9.80665 m/s^2.
    Detecting it requires checking a stated constant rather than an internal
    identity.
    """

    name = "Ref-01B-B-0p25mps.csv"
    path = results / name
    fieldnames, rows = read_rows(path)
    for row in rows:
        row["weight_N"] = repr(float(row["weight_N"]) * 0.85)
    write_rows(path, fieldnames, rows)
    return f"{name}: weight_N multiplied by 0.85 on all {len(rows)} rows"


FAULTS = {
    "F1": (
        "buoyancy_N +5% on one interior row; balance residual 0.503 N, "
        "everything else unchanged",
        fault_f1,
    ),
    "F2": ("one interior time_s nudged; breaks the strictly increasing time column", fault_f2),
    "F3": (
        "weight_N x0.85 on every row; balance residual 2.99 N, and the weight "
        "column also contradicts the documented 2.030 kg",
        fault_f3,
    ),
}

# Measured against this repository's verifier, so the answer key can state what a
# competent independent check should see rather than only that a fault exists.
EXPECTED_RESIDUAL = {
    "F1": "0.503 N (row 970 only; every other row is exact)",
    "F2": "not applicable — the time column stops being strictly increasing",
    "F3": "2.986 N (every row)",
}


def copy_tracked_files(dest: Path) -> int:
    """Copy the working tree's tracked files into dest, preserving mode."""

    listing = subprocess.run(
        ["git", "ls-files", "-z"],
        cwd=REPO,
        capture_output=True,
        check=True,
    ).stdout.decode("utf-8")
    count = 0
    for relative in [p for p in listing.split("\0") if p]:
        source = REPO / relative
        target = dest / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
        count += 1
    return count


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fault", default="F1", help="fault id to apply (default F1)")
    parser.add_argument("--dest", default=None, help="output directory")
    parser.add_argument(
        "--name", default=None, help="copy directory name (default: blind-<fault>)"
    )
    parser.add_argument("--list", action="store_true", help="list faults and exit")
    parser.add_argument(
        "--verify",
        action="store_true",
        help="run the repository's verifier against the copy and report detection",
    )
    args = parser.parse_args(argv)

    if args.list:
        print("available faults:")
        for key, (description, _) in FAULTS.items():
            print(f"  {key}: {description}")
        return 0

    fault_id = args.fault.upper()
    if fault_id not in FAULTS:
        print(f"unknown fault {args.fault!r}; use --list", file=sys.stderr)
        return 2

    dest_root = Path(args.dest).resolve() if args.dest else DEFAULT_DEST
    dest_root.mkdir(parents=True, exist_ok=True)
    copy_dir = dest_root / (args.name or f"blind-{fault_id.lower()}")
    if copy_dir.exists():
        shutil.rmtree(copy_dir)

    copied = copy_tracked_files(copy_dir)
    description = FAULTS[fault_id][1](copy_dir / RESULTS_REL)

    # The answer key lives beside the copy, never inside it, so the recipient
    # cannot stumble onto it.
    key_path = dest_root / f"ANSWER_KEY-{fault_id}.txt"
    key_path.write_text(
        "\n".join(
            [
                f"fault id    : {fault_id}",
                f"copy        : {copy_dir.name}",
                f"description : {description}",
                "",
                "what an independent check should see:",
                f"  force-balance residual : {EXPECTED_RESIDUAL[fault_id]}",
                "",
                "how to score the outcome (see the brief's author-only section):",
                "  detected     -> the reader's procedure has discriminating power.",
                "  not detected -> either the procedure only runs scripts without",
                "                  checking them, or its tolerance was set so loosely",
                "                  that a real error fits inside it.  Record which.",
                "",
                "note on F1: its residual is deliberately the smallest of the three.",
                "A reader who adopts an unjustified loose tolerance (say 1 N) will miss",
                "F1 while still catching F3.  That is the discriminating case, so if",
                "only one fault is used, use F1.",
                "",
            ]
        ),
        encoding="utf-8",
        newline="\n",
    )

    print(f"copy        : {copy_dir}  ({copied} tracked files)")
    print(f"fault       : {fault_id} — {description}")
    print(f"answer key  : {key_path}")

    if not args.verify:
        return 0

    verifier = copy_dir / VERIFIER_REL
    proc = subprocess.run(
        [sys.executable, str(verifier)],
        cwd=copy_dir,
        capture_output=True,
        encoding="utf-8",
        errors="replace",
    )
    detected = proc.returncode != 0
    print("")
    print(f"verifier exit code : {proc.returncode}")
    print(f"verifier detected  : {'YES' if detected else 'NO'}")
    tail = [line for line in (proc.stdout or "").splitlines() if line.strip()][-6:]
    for line in tail:
        print(f"  | {line}")
    if not detected:
        print("")
        print("WARNING: the repository verifier passed a tampered file, so this fault")
        print("is not detectable through the documented path. Pick another fault.")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
