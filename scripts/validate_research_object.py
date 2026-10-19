#!/usr/bin/env python3
"""Validate an ANRI Research Object without third-party dependencies.

Checks performed, in order:

1. the object parses as JSON;
2. the object conforms to ``schema/research_object.schema.json`` using a small
   built-in JSON Schema (draft 2020-12 subset) engine, so schema drift is a
   hard failure rather than a silent pass;
3. every ``artifacts[].path`` exists and its recorded SHA-256 matches the bytes
   on disk;
4. every ``evidence[].source`` path exists (POSIX, repository-relative);
5. every ``validators[].result_ref`` and ``report_ref`` path exists;
6. claim / evidence / validator / limitation / review references close;
7. the machine-readable ``reference_configuration`` agrees with the executable
   model constants (this is what catches a gravity change);
8. the verifier's own reference constants agree with the model;
9. the object contains no personal absolute path (no drive letters, no home
   directories, no ``file://`` URLs);
10. a run manifest listed in ``artifacts`` declares the same hashes and the same
    file set as the object;
11. ``status: verified`` is refused unless ``review.status`` is ``approved``.

Every failure prints the offending field or path and the process exits non-zero.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import re
import sys
from pathlib import Path
from typing import Any, Iterable, Sequence

DEFAULT_SCHEMA = Path("schema/research_object.schema.json")
MODEL_MODULE = Path("Models/CDFV-001/Ref-01B/baseline_model.py")
VERIFIER_MODULE = Path("Models/CDFV-001/Ref-01B/verify_baseline.py")

# Quantities that must agree between the object, the model and the verifier.
REFERENCE_FIELDS = (
    "mass_kg",
    "diameter_m",
    "length_m",
    "water_density_kg_m3",
    "gravity_m_s2",
)

RELATIVE_TOLERANCE = 1e-12

ABSOLUTE_PATH_PATTERNS: tuple[tuple[str, str], ...] = (
    # A Windows drive path, but not the scheme of an https/ftp URL.  The scheme
    # is checked first by requiring the drive letter to be a real path root
    # followed by a separator and a non-slash character.
    (r"\b[A-Za-z]:\\(?![/\\])", "Windows drive path"),
    (r"\b[A-Za-z]:/(?![/\\])", "Windows drive path"),
    (r"\\\\[A-Za-z0-9._-]+\\", "UNC path"),
    (r"(?<![A-Za-z0-9._-])/(?:Users|home|root|mnt|Volumes)/", "POSIX home path"),
    (r"\bfile://", "file URL"),
)

# Exact strings that must never be reported as a machine-specific path.
ALLOWED_PATH_LIKE_STRINGS = {
    "https://github.com/Zhaoyushen-Lab/ANRI-Aerospace.git",
}


class SchemaError(Exception):
    """Raised when the schema itself cannot be used."""


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


# --------------------------------------------------------------------------
# Minimal JSON Schema (draft 2020-12 subset) engine
# --------------------------------------------------------------------------


def resolve_ref(ref: str, root: Any) -> Any:
    if not ref.startswith("#"):
        raise SchemaError(f"only local $ref values are supported, got {ref!r}")
    node = root
    tokens = ref[2:].split("/") if ref.startswith("#/") else []
    for raw in tokens:
        token = raw.replace("~1", "/").replace("~0", "~")
        if isinstance(node, list):
            node = node[int(token)]
        elif isinstance(node, dict) and token in node:
            node = node[token]
        else:
            raise SchemaError(f"unresolvable $ref {ref!r}")
    return node


def type_matches(instance: Any, expected: str) -> bool:
    if expected == "object":
        return isinstance(instance, dict)
    if expected == "array":
        return isinstance(instance, list)
    if expected == "string":
        return isinstance(instance, str)
    if expected == "number":
        return isinstance(instance, (int, float)) and not isinstance(instance, bool)
    if expected == "integer":
        return isinstance(instance, int) and not isinstance(instance, bool)
    if expected == "boolean":
        return isinstance(instance, bool)
    if expected == "null":
        return instance is None
    raise SchemaError(f"unsupported schema type {expected!r}")


def check_format(instance: str, fmt: str) -> bool:
    if fmt == "date":
        return bool(re.fullmatch(r"\d{4}-\d{2}-\d{2}", instance))
    if fmt == "date-time":
        return bool(
            re.fullmatch(
                r"\d{4}-\d{2}-\d{2}[Tt ]\d{2}:\d{2}:\d{2}(\.\d+)?([Zz]|[+-]\d{2}:?\d{2})",
                instance,
            )
        )
    # Unknown formats are annotations, per the JSON Schema specification.
    return True


def validate_schema(
    instance: Any,
    schema: Any,
    root: Any,
    path: str,
    errors: list[str],
) -> None:
    if not isinstance(schema, dict):
        return

    if "$ref" in schema:
        try:
            target = resolve_ref(str(schema["$ref"]), root)
        except SchemaError as exc:
            errors.append(f"{path}: {exc}")
            return
        validate_schema(instance, target, root, path, errors)
        return

    if "oneOf" in schema:
        matches = 0
        branch_errors: list[list[str]] = []
        for branch in schema["oneOf"]:
            branch_problems: list[str] = []
            validate_schema(instance, branch, root, path, branch_problems)
            branch_errors.append(branch_problems)
            if not branch_problems:
                matches += 1
        if matches != 1:
            summary = "; ".join(
                ", ".join(problems[:2]) for problems in branch_errors if problems
            )
            errors.append(
                f"{path}: matched {matches} of {len(schema['oneOf'])} oneOf branches "
                f"({summary})"
            )
            return

    if "const" in schema and instance != schema["const"]:
        errors.append(f"{path}: expected const {schema['const']!r}, got {instance!r}")
        return

    if "enum" in schema and instance not in schema["enum"]:
        errors.append(
            f"{path}: value {instance!r} is not one of "
            f"{sorted(map(str, schema['enum']))}"
        )
        return

    expected_type = schema.get("type")
    if expected_type is not None:
        candidates = (
            expected_type if isinstance(expected_type, list) else [expected_type]
        )
        if not any(type_matches(instance, candidate) for candidate in candidates):
            errors.append(
                f"{path}: expected type {expected_type!r}, got "
                f"{type(instance).__name__} ({instance!r})"
            )
            return

    if isinstance(instance, str):
        min_length = schema.get("minLength")
        if min_length is not None and len(instance) < min_length:
            errors.append(f"{path}: shorter than minLength {min_length}")
        pattern = schema.get("pattern")
        if pattern is not None and not re.search(pattern, instance):
            errors.append(
                f"{path}: value {instance!r} does not match pattern {pattern!r}"
            )
        fmt = schema.get("format")
        if fmt is not None and not check_format(instance, fmt):
            errors.append(f"{path}: value {instance!r} is not a valid {fmt}")

    if isinstance(instance, (int, float)) and not isinstance(instance, bool):
        minimum = schema.get("minimum")
        if minimum is not None and instance < minimum:
            errors.append(f"{path}: {instance} is below minimum {minimum}")
        maximum = schema.get("maximum")
        if maximum is not None and instance > maximum:
            errors.append(f"{path}: {instance} is above maximum {maximum}")

    if isinstance(instance, dict):
        for key in schema.get("required", []):
            if key not in instance:
                errors.append(f"{path}: missing required property {key!r}")

        properties = schema.get("properties", {})
        for key, subschema in properties.items():
            if key in instance:
                validate_schema(instance[key], subschema, root, f"{path}.{key}", errors)

        additional = schema.get("additionalProperties", True)
        extra_keys = [key for key in instance if key not in properties]
        if additional is False:
            for key in extra_keys:
                errors.append(f"{path}: additional property {key!r} is not allowed")
        elif isinstance(additional, dict):
            for key in extra_keys:
                validate_schema(
                    instance[key], additional, root, f"{path}.{key}", errors
                )

    if isinstance(instance, list):
        min_items = schema.get("minItems")
        if min_items is not None and len(instance) < min_items:
            errors.append(f"{path}: fewer than minItems {min_items}")
        items = schema.get("items")
        if isinstance(items, dict):
            for index, item in enumerate(instance):
                validate_schema(item, items, root, f"{path}[{index}]", errors)


# --------------------------------------------------------------------------
# Research-object specific checks
# --------------------------------------------------------------------------


def load_module(module_path: Path, module_name: str) -> Any:
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"cannot load module from {module_path}")
    module = importlib.util.module_from_spec(spec)
    # Register before executing: dataclasses resolve their module through
    # sys.modules, so an unregistered module breaks @dataclass definitions.
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


def walk_strings(node: Any, path: str = "") -> Iterable[tuple[str, str]]:
    if isinstance(node, dict):
        for key, value in node.items():
            yield from walk_strings(value, f"{path}.{key}" if path else str(key))
    elif isinstance(node, list):
        for index, value in enumerate(node):
            yield from walk_strings(value, f"{path}[{index}]")
    elif isinstance(node, str):
        yield path, node


def close_enough(left: float, right: float) -> bool:
    if left == right:
        return True
    scale = max(abs(left), abs(right), 1.0)
    return abs(left - right) <= RELATIVE_TOLERANCE * scale


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Validate an ANRI Research Object and its evidence chain."
    )
    parser.add_argument("object", type=Path)
    parser.add_argument("--repo-root", type=Path, default=Path.cwd())
    parser.add_argument(
        "--schema",
        type=Path,
        default=None,
        help=(
            "Path to the JSON Schema (default: <repo-root>/"
            f"{DEFAULT_SCHEMA.as_posix()})."
        ),
    )
    parser.add_argument(
        "--skip-model-cross-check",
        action="store_true",
        help="Do not compare reference_configuration against the executable model.",
    )
    args = parser.parse_args(argv)

    errors: list[str] = []
    warnings: list[str] = []
    repo_root = args.repo_root.resolve()
    schema_path = (
        args.schema.resolve()
        if args.schema is not None
        else (repo_root / DEFAULT_SCHEMA).resolve()
    )

    try:
        obj = json.loads(args.object.read_text(encoding="utf-8"))
    except Exception as exc:
        print(f"FAIL: cannot read object JSON: {exc}")
        return 1

    # --- 2. schema conformance ------------------------------------------------
    schema: Any = None
    if not schema_path.is_file():
        errors.append(f"schema file does not exist: {schema_path}")
    else:
        try:
            schema = json.loads(schema_path.read_text(encoding="utf-8"))
        except Exception as exc:
            errors.append(f"cannot read schema {schema_path}: {exc}")
    if schema is not None:
        validate_schema(obj, schema, schema, "$", errors)

    # --- 3. artifacts ---------------------------------------------------------
    artifact_hashes: dict[str, str] = {}
    # The run manifest to cross-check is named explicitly by the object. An
    # artifact role is not used as the link, because the object also lists itself
    # and a role-based rule would silently pick the wrong file.
    manifest_paths: list[str] = []
    manifest_ref = obj.get("run_manifest_ref")
    if manifest_ref:
        if re.match(r"[A-Za-z]:[\\/]", str(manifest_ref)) or str(
            manifest_ref
        ).startswith("/"):
            errors.append(
                f"run_manifest_ref must be a repository-relative POSIX path, "
                f"got {manifest_ref!r}"
            )
        elif not (repo_root / str(manifest_ref)).is_file():
            errors.append(f"run_manifest_ref does not exist: {manifest_ref}")
        else:
            manifest_paths.append(str(manifest_ref))
    else:
        warnings.append(
            "run_manifest_ref is not set, so no run manifest was cross-checked"
        )
    # Files that legitimately cannot store their own digest (an object or manifest
    # that records itself) declare the digest as "self".  Those entries are
    # skipped by the hash comparison on both sides and are resolved through the
    # other file's entry.
    self_declared: set[str] = set()

    obj_path_text = args.object.resolve()
    try:
        obj_rel = obj_path_text.relative_to(repo_root).as_posix()
    except ValueError:
        obj_rel = obj_path_text.name

    for index, item in enumerate(obj.get("artifacts", [])):
        path_text = str(item.get("path", ""))
        record = f"artifacts[{index}] ({path_text})"
        if not path_text:
            errors.append(f"{record}: empty path")
            continue
        if path_text.startswith("/") or re.match(r"[A-Za-z]:", path_text):
            errors.append(f"{record}: must be a repository-relative POSIX path")
            continue
        artifact_hashes[path_text] = str(item.get("sha256", ""))
        if item.get("sha256") == "self":
            if path_text != obj_rel:
                errors.append(
                    f"{record}: a real file must carry its own SHA-256; the "
                    "'self' placeholder is only allowed for the object itself"
                )
            else:
                self_declared.add(path_text)
            path = repo_root / path_text
        else:
            path = repo_root / path_text
        if not path.is_file():
            errors.append(f"artifact does not exist: {path_text}")
            continue
        if path_text in self_declared:
            continue
        actual = sha256(path)
        if item.get("sha256", "") != actual:
            errors.append(
                f"sha256 mismatch: {path_text} "
                f"expected={item.get('sha256', '')} actual={actual}"
            )

    # --- 4. evidence sources --------------------------------------------------
    for index, item in enumerate(obj.get("evidence", [])):
        source = str(item.get("source", ""))
        record = f"evidence[{index}] ({item.get('id')})"
        if not source:
            errors.append(f"{record}: empty source")
            continue
        if re.match(r"[A-Za-z]:[\\/]", source) or source.startswith("\\\\"):
            errors.append(f"{record}: source must not be an absolute host path")
            continue
        if not (repo_root / source).is_file():
            errors.append(f"evidence source does not exist: {source}")

    # --- 5. validators --------------------------------------------------------
    validators = {
        item.get("id"): item for item in obj.get("validators", []) if item.get("id")
    }
    for validator_id, item in validators.items():
        for field in ("result_ref", "report_ref"):
            ref = item.get(field)
            if ref is None:
                continue
            if re.match(r"[A-Za-z]:[\\/]", str(ref)):
                errors.append(f"{validator_id}.{field}: must not be an absolute path")
                continue
            if not (repo_root / str(ref)).is_file():
                errors.append(f"{validator_id}.{field} does not exist: {ref}")

    # --- 6. reference closure -------------------------------------------------
    claims = {item.get("id"): item for item in obj.get("claims", []) if item.get("id")}
    evidence = {
        item.get("id"): item for item in obj.get("evidence", []) if item.get("id")
    }
    limitations = {
        item.get("id"): item for item in obj.get("limitations", []) if item.get("id")
    }
    assumptions = {
        item.get("id"): item for item in obj.get("assumptions", []) if item.get("id")
    }

    if not claims:
        errors.append("object declares no claims")
    for claim_id, claim in claims.items():
        for ref in claim.get("evidence_refs", []):
            if ref not in evidence:
                errors.append(f"{claim_id}: missing evidence ref {ref}")
        for ref in claim.get("validator_refs", []):
            if ref not in validators:
                errors.append(f"{claim_id}: missing validator ref {ref}")
        for ref in claim.get("limitation_refs", []):
            if ref not in limitations:
                errors.append(f"{claim_id}: missing limitation ref {ref}")
    for evidence_id, item in evidence.items():
        if not item.get("supports"):
            errors.append(f"{evidence_id}: declares no supported claim")
        for ref in item.get("supports", []):
            if ref not in claims:
                errors.append(f"{evidence_id}: missing supported claim {ref}")
    for validator_id, item in validators.items():
        if not item.get("command"):
            errors.append(f"{validator_id}: missing command")

    reviews = obj.get("review", {}).get("reviews", [])
    review_ids: set[str] = set()
    for index, record in enumerate(reviews):
        review_id = str(record.get("review_id", ""))
        if review_id in review_ids:
            errors.append(f"review[{index}]: duplicate review_id {review_id}")
        review_ids.add(review_id)
        if not record.get("independent"):
            warnings.append(f"review[{index}] ({review_id}): marked as not independent")

    # --- 7. reference configuration vs executable model -----------------------
    reference = obj.get("reference_configuration", {})
    if reference and not args.skip_model_cross_check:
        model_path = repo_root / MODEL_MODULE
        if not model_path.is_file():
            errors.append(f"model module does not exist: {MODEL_MODULE.as_posix()}")
        else:
            model = None
            model_values: dict[str, float] = {}
            try:
                model = load_module(model_path, "anri_baseline_model")
                model_cfg = model.Ref01BConfig()
                model_values = {
                    "mass_kg": model_cfg.mass_kg,
                    "diameter_m": model_cfg.diameter_m,
                    "length_m": model_cfg.length_m,
                    "water_density_kg_m3": model_cfg.water_density_kg_m3,
                    "gravity_m_s2": model_cfg.gravity_m_s2,
                }
            except Exception as exc:  # pragma: no cover - diagnostic path
                errors.append(f"cannot load the baseline model: {exc}")

            if model_values:
                for field in REFERENCE_FIELDS:
                    declared = reference.get(field)
                    if not isinstance(declared, dict):
                        errors.append(
                            f"reference_configuration.{field}: missing "
                            "machine-readable value"
                        )
                        continue
                    if not close_enough(
                        float(declared["value"]), float(model_values[field])
                    ):
                        errors.append(
                            f"reference_configuration.{field} disagrees with the "
                            f"model: object={declared['value']} "
                            f"({declared.get('unit')}) vs model={model_values[field]}"
                        )

                declared_free_surface = reference.get("free_surface_force_n")
                if isinstance(declared_free_surface, dict) and not close_enough(
                    float(declared_free_surface["value"]), 0.0
                ):
                    errors.append(
                        "reference_configuration.free_surface_force_n disagrees with "
                        "the baseline definition: "
                        f"object={declared_free_surface['value']} vs model=0.0"
                    )

                # --- 8. verifier constants vs model ---------------------------
                verifier_path = repo_root / VERIFIER_MODULE
                if not verifier_path.is_file():
                    errors.append(
                        f"verifier module does not exist: {VERIFIER_MODULE.as_posix()}"
                    )
                else:
                    try:
                        verifier = load_module(verifier_path, "anri_verify_baseline")
                    except Exception as exc:  # pragma: no cover - diagnostic path
                        errors.append(f"cannot load the baseline verifier: {exc}")
                    else:
                        for field, model_value in model_values.items():
                            verifier_value = getattr(verifier, field.upper(), None)
                            if verifier_value is None:
                                errors.append(
                                    f"verifier does not define {field.upper()}, "
                                    "so it cannot be cross-checked"
                                )
                                continue
                            if not close_enough(
                                float(verifier_value), float(model_value)
                            ):
                                errors.append(
                                    f"verifier constant {field.upper()} disagrees with "
                                    f"the model: verifier={verifier_value} "
                                    f"model={model_value}"
                                )

    # --- assumptions must cover the frozen inputs -----------------------------
    gravity_assumption = assumptions.get("A-GRAVITY")
    declared_gravity = reference.get("gravity_m_s2", {})
    if gravity_assumption is None:
        errors.append("assumptions: A-GRAVITY is required")
    else:
        if isinstance(declared_gravity, dict):
            if gravity_assumption.get("value") is None:
                errors.append("A-GRAVITY: missing numeric value")
            elif not close_enough(
                float(gravity_assumption["value"]), float(declared_gravity["value"])
            ):
                errors.append(
                    "A-GRAVITY value disagrees with "
                    "reference_configuration.gravity_m_s2: "
                    f"{gravity_assumption['value']} vs {declared_gravity['value']}"
                )
            if gravity_assumption.get("unit") != declared_gravity.get("unit"):
                errors.append(
                    "A-GRAVITY unit disagrees with "
                    "reference_configuration.gravity_m_s2: "
                    f"{gravity_assumption.get('unit')!r} vs "
                    f"{declared_gravity.get('unit')!r}"
                )
        if not gravity_assumption.get("source"):
            errors.append("A-GRAVITY: missing source")

    # --- 9. no personal absolute paths ---------------------------------------
    for field_path, value in walk_strings(obj):
        if value in ALLOWED_PATH_LIKE_STRINGS:
            continue
        for pattern, label in ABSOLUTE_PATH_PATTERNS:
            if re.search(pattern, value):
                errors.append(
                    f"{field_path}: contains a machine-specific {label} ({value!r})"
                )
                break

    # --- 10. run manifest agreement ------------------------------------------
    # Both the object and its run manifest record the other's digest, which is
    # circular, so each declares its own entry as "self" and the validator
    # resolves the pair through the other file's real record.  A "self" entry is
    # therefore never compared against the file's own bytes; it only has to be
    # the object itself or the manifest itself.
    for manifest_text in manifest_paths:
        placeholder_ok = {manifest_text, obj_rel}
        manifest_map: dict[str, str] = {}
        manifest_full = repo_root / manifest_text
        if not manifest_full.is_file():
            continue
        try:
            manifest = json.loads(manifest_full.read_text(encoding="utf-8"))
        except Exception as exc:
            errors.append(f"{manifest_text}: cannot read manifest: {exc}")
            continue

        manifest_artifacts = manifest.get("artifacts")
        if not isinstance(manifest_artifacts, list):
            errors.append(f"{manifest_text}: missing 'artifacts' array")
            continue

        for index, item in enumerate(manifest_artifacts):
            path_text = str(item.get("path", ""))
            digest = str(item.get("sha256", ""))
            if not path_text or not digest:
                errors.append(
                    f"{manifest_text}: artifacts[{index}] needs path and sha256"
                )
                continue
            if digest == "self":
                # A file cannot contain its own digest. The only permitted
                # placeholder is the manifest's entry for the object itself; the
                # object's entry for the manifest carries a real digest, so the
                # pair is not circular.
                if path_text != obj_rel:
                    errors.append(
                        f"{manifest_text}: the 'self' placeholder is only allowed "
                        f"on the entry for the object itself ({obj_rel}), but "
                        f"{path_text} uses it"
                    )
                    continue
                digest = sha256(repo_root / path_text)
            manifest_map[path_text] = digest
            full = repo_root / path_text
            if not full.is_file():
                errors.append(f"{manifest_text}: artifact does not exist: {path_text}")
                continue
            actual = sha256(full)
            if digest != actual:
                errors.append(
                    f"{manifest_text}: sha256 mismatch for {path_text} "
                    f"expected={digest} actual={actual}"
                )

        for path_text, digest in manifest_map.items():
            if path_text not in artifact_hashes:
                errors.append(
                    f"{manifest_text}: hashes {path_text} but the Research "
                    "Object artifacts list does not"
                )
            elif digest == "self" or artifact_hashes[path_text] == "self":
                # A "self" entry carries no comparable digest by construction.
                continue
            elif artifact_hashes[path_text] != digest:
                errors.append(
                    f"{manifest_text}: hash for {path_text} disagrees with the "
                    f"Research Object: manifest={digest} "
                    f"object={artifact_hashes[path_text]}"
                )
        for path_text in artifact_hashes:
            if path_text not in manifest_map:
                if path_text == manifest_text:
                    # The manifest cannot list its own digest; the object's entry
                    # for it was already compared against the real bytes.
                    continue
                errors.append(
                    f"{manifest_text}: does not hash {path_text}, which the "
                    "Research Object artifacts list contains"
                )

        git_commit = str(manifest.get("repository", {}).get("git_commit", ""))
        if git_commit and not re.fullmatch(r"[a-f0-9]{40}", git_commit):
            errors.append(
                f"{manifest_text}: repository.git_commit must be 40 lowercase hex"
            )

    # --- 11. review gate ------------------------------------------------------
    review_status = str(obj.get("review", {}).get("status", ""))
    object_status = str(obj.get("status", ""))
    if object_status == "verified" and review_status != "approved":
        errors.append(
            f"status is 'verified' but review.status is {review_status!r}; "
            "an object may only be verified after an approved independent review"
        )
    if object_status == "verified" and not reviews:
        errors.append("status is 'verified' but no review record exists")
    if review_status == "approved":
        for index, record in enumerate(reviews):
            if record.get("decision") not in ("approve", "approve_with_minor_fixes"):
                errors.append(
                    f"review.status is 'approved' but review[{index}] decision is "
                    f"{record.get('decision')!r}"
                )
            if not record.get("independent"):
                errors.append(
                    f"review.status is 'approved' but review[{index}] is not independent"
                )
    if review_status not in ("pending", "revision_requested", "approved", "rejected"):
        errors.append(f"review.status has unsupported value {review_status!r}")

    provenance_commit = obj.get("provenance", {}).get("git_commit", "")
    if not re.fullmatch(r"[a-f0-9]{40}", str(provenance_commit)):
        errors.append("provenance.git_commit must be a 40-character lowercase hash")

    # --- report ---------------------------------------------------------------
    if errors:
        print("Research Object validation: FAIL")
        for error in errors:
            print(f"- {error}")
        if warnings:
            print("Warnings:")
            for warning in warnings:
                print(f"- {warning}")
        return 1

    print("Research Object validation: PASS")
    print(f"- id: {obj['id']}")
    print(f"- status: {obj['status']}")
    print(f"- schema: {schema_path.name}")
    print(f"- claims: {len(claims)}")
    print(f"- evidence: {len(evidence)}")
    print(f"- validators: {len(validators)}")
    print(f"- artifacts: {len(artifact_hashes)}")
    print(f"- reviews: {len(reviews)} (review.status={review_status})")
    for warning in warnings:
        print(f"- warning: {warning}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
