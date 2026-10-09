#!/usr/bin/env python3
"""Validate an ANRI Research Object without third-party dependencies."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("object", type=Path)
    parser.add_argument("--repo-root", type=Path, default=Path.cwd())
    args = parser.parse_args()

    errors: list[str] = []
    repo_root = args.repo_root.resolve()

    try:
        obj = json.loads(args.object.read_text(encoding="utf-8"))
    except Exception as exc:
        print(f"FAIL: cannot read object JSON: {exc}")
        return 1

    required = {
        "schema_version", "id", "type", "version", "status", "title",
        "purpose", "scope", "claims", "evidence", "validators",
        "artifacts", "assumptions", "limitations", "review", "provenance",
    }
    missing = sorted(required - obj.keys())
    if missing:
        fail(errors, f"missing top-level fields: {', '.join(missing)}")

    if obj.get("schema_version") != "0.1":
        fail(errors, "schema_version must be 0.1")
    if obj.get("type") != "research_object":
        fail(errors, "type must be research_object")
    if not re.fullmatch(r"RO-[A-Za-z0-9][A-Za-z0-9-]*", str(obj.get("id", ""))):
        fail(errors, "invalid research object id")
    if not re.fullmatch(r"[0-9]+\.[0-9]+\.[0-9]+", str(obj.get("version", ""))):
        fail(errors, "version must use semver, for example 0.1.0")

    claims = {item.get("id"): item for item in obj.get("claims", [])}
    evidence = {item.get("id"): item for item in obj.get("evidence", [])}
    validators = {item.get("id"): item for item in obj.get("validators", [])}
    limitations = {item.get("id"): item for item in obj.get("limitations", [])}

    for claim_id, claim in claims.items():
        if not claim_id:
            fail(errors, "claim without id")
        for ref in claim.get("evidence_refs", []):
            if ref not in evidence:
                fail(errors, f"{claim_id}: missing evidence ref {ref}")
        for ref in claim.get("validator_refs", []):
            if ref not in validators:
                fail(errors, f"{claim_id}: missing validator ref {ref}")
        for ref in claim.get("limitation_refs", []):
            if ref not in limitations:
                fail(errors, f"{claim_id}: missing limitation ref {ref}")

    for evidence_id, item in evidence.items():
        for ref in item.get("supports", []):
            if ref not in claims:
                fail(errors, f"{evidence_id}: missing supported claim {ref}")

    artifact_paths: set[str] = set()
    for item in obj.get("artifacts", []):
        path_text = item.get("path", "")
        artifact_paths.add(path_text)
        path = (repo_root / path_text).resolve()
        if not path.is_file():
            fail(errors, f"artifact does not exist: {path_text}")
            continue
        expected = item.get("sha256", "")
        actual = sha256(path)
        if expected != actual:
            fail(errors, f"sha256 mismatch: {path_text} expected={expected} actual={actual}")

    commit = obj.get("provenance", {}).get("git_commit", "")
    if not re.fullmatch(r"[a-f0-9]{40}", str(commit)):
        fail(errors, "provenance.git_commit must be a 40-character lowercase hash")

    if errors:
        print("Research Object validation: FAIL")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Research Object validation: PASS")
    print(f"- id: {obj['id']}")
    print(f"- status: {obj['status']}")
    print(f"- claims: {len(claims)}")
    print(f"- evidence: {len(evidence)}")
    print(f"- validators: {len(validators)}")
    print(f"- artifacts: {len(artifact_paths)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
