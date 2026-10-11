#!/usr/bin/env python3
"""Self-check: prove the validator rejects each required failure mode.

The Research Object validator is the review gate, so the gate itself needs a
test.  This script copies the working tree (tracked files plus uncommitted
changes) to a scratch directory, applies one mutation per scenario, runs the
real validator, and requires a non-zero exit with a specific message.  One
unmutated control run must still pass, proving the mutations are the only reason
for the failures.

Scenarios covered:

* a referenced evidence file is deleted;
* the JSON Schema is relaxed so the object no longer conforms;
* gravity is changed in the object only, in the object and A-GRAVITY, or in the
  executable model only;
* a ``validators[].result_ref`` points at a missing file;
* an ``artifacts[].sha256`` is wrong;
* ``A-GRAVITY`` is removed from the assumptions;
* ``status: verified`` is set while the review gate is not approved;
* a machine-specific absolute path is present;
* the run manifest's own digest for the object is tampered with;
* the run manifest silently drops an artifact the object records.

Usage:
    py -3 scripts/validate_gate_selftest.py <scratch-dir>
"""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
RO_REL = "Research_Objects/RO-CDFV-001-Ref-01B.json"


def sha256(path: Path) -> str:
    import hashlib

    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def copy_tree(destination: Path) -> None:
    """Copy the working tree (tracked plus not-yet-committed files).

    The repository is mid-repair, so several artifacts are still untracked; the
    control scenario must include them or it would fail for the wrong reason.
    """

    if destination.exists():
        shutil.rmtree(destination)
    destination.mkdir(parents=True)

    listing = subprocess.run(
        ["git", "ls-files", "--cached", "--others", "--exclude-standard", "-z"],
        cwd=REPO,
        capture_output=True,
        check=True,
    ).stdout.split(b"\0")

    copied = 0
    for raw in listing:
        if not raw:
            continue
        relative = raw.decode("utf-8")
        source = REPO / relative
        if not source.is_file():
            continue
        target = destination / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
        copied += 1
    if copied == 0:
        raise SystemExit("copy_tree copied no files")


def load_ro(root: Path) -> dict:
    return json.loads((root / RO_REL).read_text(encoding="utf-8"))


def save_ro(root: Path, obj: dict) -> None:
    (root / RO_REL).write_text(json.dumps(obj, indent=2) + "\n", encoding="utf-8")


def run_validator(root: Path) -> tuple[int, str]:
    completed = subprocess.run(
        [
            sys.executable,
            str(root / "scripts" / "validate_research_object.py"),
            str(root / RO_REL),
            "--repo-root",
            str(root),
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    return completed.returncode, completed.stdout + completed.stderr


# Each scenario: name, mutate(root) -> None, expected substring in the output.
def mutate_remove_evidence_file(root: Path) -> None:
    obj = load_ro(root)
    source = obj["evidence"][0]["source"]
    (root / source).unlink()


def mutate_schema_change(root: Path) -> None:
    path = root / "schema" / "research_object.schema.json"
    schema = json.loads(path.read_text(encoding="utf-8"))
    schema["properties"]["id"]["pattern"] = "^RO-[0-9]+$"
    path.write_text(json.dumps(schema, indent=2) + "\n", encoding="utf-8")


def mutate_gravity_object_only(root: Path) -> None:
    obj = load_ro(root)
    obj["reference_configuration"]["gravity_m_s2"]["value"] = 9.81
    save_ro(root, obj)


def mutate_gravity_with_assumption(root: Path) -> None:
    mutate_gravity_object_only(root)
    obj = load_ro(root)
    for assumption in obj["assumptions"]:
        if assumption["id"] == "A-GRAVITY":
            assumption["value"] = 9.81
    save_ro(root, obj)


def mutate_gravity_in_model(root: Path) -> None:
    path = root / "Models" / "CDFV-001" / "Ref-01B" / "baseline_model.py"
    text = path.read_text(encoding="utf-8")
    path.write_text(text.replace("gravity_m_s2: float = 9.80665", "gravity_m_s2: float = 9.81"), encoding="utf-8")


def mutate_missing_result_ref(root: Path) -> None:
    obj = load_ro(root)
    obj["validators"][0]["result_ref"] = "Models/CDFV-001/Ref-01B/results/does_not_exist.json"
    save_ro(root, obj)


def mutate_wrong_artifact_hash(root: Path) -> None:
    obj = load_ro(root)
    obj["artifacts"][0]["sha256"] = "0" * 64
    save_ro(root, obj)


def mutate_missing_gravity_assumption(root: Path) -> None:
    obj = load_ro(root)
    obj["assumptions"] = [
        item for item in obj["assumptions"] if item["id"] != "A-GRAVITY"
    ]
    save_ro(root, obj)


def mutate_verified_without_approval(root: Path) -> None:
    obj = load_ro(root)
    obj["status"] = "verified"
    save_ro(root, obj)


def mutate_absolute_path(root: Path) -> None:
    obj = load_ro(root)
    obj["purpose"] = "Baseline reproduced on C:\\Users\\someone\\ANRI-Aerospace."
    save_ro(root, obj)


TAMPER_TARGET = "Models/CDFV-001/Ref-01B/baseline_model.py"


def mutate_manifest_hash(root: Path) -> None:
    path = root / "Benchmarks" / "ANRI-RV-001" / "run_manifest.json"
    manifest = json.loads(path.read_text(encoding="utf-8"))
    touched = 0
    for artifact in manifest["artifacts"]:
        if artifact["path"] == TAMPER_TARGET:
            artifact["sha256"] = "1" * 64
            touched += 1
    if touched != 1:
        raise SystemExit(f"tamper target not found in manifest: {TAMPER_TARGET}")
    path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")


def mutate_manifest_drops_artifact(root: Path) -> None:
    path = root / "Benchmarks" / "ANRI-RV-001" / "run_manifest.json"
    manifest = json.loads(path.read_text(encoding="utf-8"))
    before = len(manifest["artifacts"])
    manifest["artifacts"] = [
        item for item in manifest["artifacts"] if item["path"] != TAMPER_TARGET
    ]
    if len(manifest["artifacts"]) != before - 1:
        raise SystemExit(f"drop target not found in manifest: {TAMPER_TARGET}")
    path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")


SCENARIOS = [
    ("evidence file deleted", mutate_remove_evidence_file, "evidence source does not exist"),
    ("schema relaxed", mutate_schema_change, "does not match pattern"),
    ("object gravity changed only", mutate_gravity_object_only, "disagrees with the model"),
    ("object and A-GRAVITY changed", mutate_gravity_with_assumption, "disagrees with the model"),
    ("model gravity changed", mutate_gravity_in_model, "disagrees with the model"),
    ("validator result_ref missing", mutate_missing_result_ref, "does not exist"),
    ("artifact hash wrong", mutate_wrong_artifact_hash, "sha256 mismatch"),
    ("A-GRAVITY removed", mutate_missing_gravity_assumption, "A-GRAVITY is required"),
    ("status verified without approval", mutate_verified_without_approval, "review.status"),
    ("absolute path present", mutate_absolute_path, "machine-specific"),
    (
        "manifest digest for a tracked artifact is tampered",
        mutate_manifest_hash,
        "run_manifest.json: sha256 mismatch",
    ),
    (
        "manifest silently drops an artifact the object records",
        mutate_manifest_drops_artifact,
        "does not hash",
    ),
]


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print(__doc__)
        return 2
    scratch = Path(argv[1]).resolve()

    failures: list[str] = []
    for name, mutate, expected in SCENARIOS:
        root = scratch / name.replace(" ", "_")
        copy_tree(root)
        mutate(root)
        code, output = run_validator(root)
        ok = code != 0 and expected in output
        status = "PASS" if ok else "FAIL"
        print(f"  {status} {name}: exit={code} expected_message={expected!r}")
        if not ok:
            failures.append(name)
            print("    --- output ---")
            for line in output.splitlines()[:12]:
                print(f"    {line}")
        shutil.rmtree(root, ignore_errors=True)

    # The unmutated copy must still validate, proving the mutations are the only
    # reason for the failures above.
    clean_root = scratch / "clean"
    copy_tree(clean_root)
    code, output = run_validator(clean_root)
    clean_ok = code == 0
    print(f"  {'PASS' if clean_ok else 'FAIL'} unmutated control: exit={code}")
    if not clean_ok:
        failures.append("unmutated control")
        print(output)
    shutil.rmtree(clean_root, ignore_errors=True)

    total = len(SCENARIOS) + 1
    if failures:
        print(f"gate self-test: FAIL ({len(failures)} of {total} scenarios)")
        return 1
    print(f"gate self-test: PASS ({total} scenarios)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
