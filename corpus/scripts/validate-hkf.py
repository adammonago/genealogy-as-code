#!/usr/bin/env python3.11
"""Validate HKF YAML records against corpus schemas and semantic rules.

Usage (from repo root):
  python3.11 corpus/scripts/validate-hkf.py
  python3.11 corpus/scripts/validate-hkf.py --fixture-dir path --schemas-dir path
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import sys
from pathlib import Path
from typing import Any

try:
    import yaml
    from jsonschema import Draft202012Validator
except ImportError as exc:  # pragma: no cover
    sys.stderr.write(
        "validate-hkf.py requires PyYAML and jsonschema (python3.11 recommended): "
        f"{exc}\n"
    )
    sys.exit(2)


KIND_TO_SCHEMA = {
    "SourceSegment": "source-segment.schema.yaml",
    "Extraction": "extraction.schema.yaml",
    "Entity": "entity.schema.yaml",
    "EntityReference": "entity-reference.schema.yaml",
    "Claim": "claim.schema.yaml",
    "IdentityAssertion": "identity-assertion.schema.yaml",
    "HistoricalInterpretation": "interpretation.schema.yaml",
    "DerivationRun": "derivation-run.schema.yaml",
}


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def load_yaml(path: Path) -> Any:
    with path.open(encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def stringify_datetimes(node: Any) -> Any:
    """PyYAML may parse ISO timestamps as datetime; HKF treats them as strings."""
    import datetime as dt

    if isinstance(node, dict):
        return {k: stringify_datetimes(v) for k, v in node.items()}
    if isinstance(node, list):
        return [stringify_datetimes(v) for v in node]
    if isinstance(node, dt.datetime):
        if node.tzinfo is None:
            return node.isoformat() + "Z"
        return node.astimezone(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    if isinstance(node, dt.date):
        return node.isoformat()
    return node


def resolve_local_refs(node: Any, schemas_dir: Path, stack: set[str] | None = None) -> Any:
    """Inline file-local $ref values such as evidence-locator.schema.yaml."""
    if stack is None:
        stack = set()
    if isinstance(node, list):
        return [resolve_local_refs(item, schemas_dir, stack) for item in node]
    if not isinstance(node, dict):
        return node

    if set(node.keys()) == {"$ref"} and isinstance(node["$ref"], str):
        ref = node["$ref"]
        if ref.startswith("#/"):
            return node
        if ref in stack:
            raise ValueError(f"circular schema ref: {ref}")
        target = schemas_dir / ref
        if not target.exists():
            raise FileNotFoundError(f"schema $ref not found: {ref}")
        stack.add(ref)
        resolved = resolve_local_refs(load_yaml(target), schemas_dir, stack)
        stack.remove(ref)
        # Drop $schema/$id from inlined documents to avoid nested meta confusion.
        if isinstance(resolved, dict):
            resolved = {k: v for k, v in resolved.items() if k not in {"$schema", "$id"}}
        return resolved

    return {k: resolve_local_refs(v, schemas_dir, stack) for k, v in node.items()}


def load_schema(schemas_dir: Path, name: str) -> dict:
    raw = load_yaml(schemas_dir / name)
    if not isinstance(raw, dict):
        raise ValueError(f"schema root must be mapping: {name}")
    return resolve_local_refs(copy.deepcopy(raw), schemas_dir)


def iter_records(fixture_dir: Path) -> list[tuple[Path, dict]]:
    records: list[tuple[Path, dict]] = []
    for path in sorted(fixture_dir.glob("*.yaml")):
        data = load_yaml(path)
        if isinstance(data, dict) and "kind" in data:
            records.append((path, stringify_datetimes(data)))
    return records


def semantic_issues(record: dict) -> list[str]:
    issues: list[str] = []
    kind = record.get("kind")

    if kind == "IdentityAssertion":
        if record.get("resolution_state") == "parked" and record.get("decision") != "unresolved":
            issues.append("parked IdentityAssertion MUST have decision: unresolved")
        if record.get("resolution_state") == "reviewed":
            verified = record.get("verified") or []
            if not verified:
                issues.append("reviewed IdentityAssertion SHOULD include verified (warning)")

    if kind == "EntityReference":
        if record.get("resolution_state") == "resolved" and not record.get("resolved_entity_ref"):
            issues.append("resolved EntityReference MUST include resolved_entity_ref")
        if record.get("resolution_state") == "parked" and record.get("resolved_entity_ref"):
            issues.append("parked EntityReference MUST remain unresolved (no resolved_entity_ref)")

    if kind == "Claim":
        if record.get("extraction_state") == "reviewed":
            verified = record.get("verified") or []
            if not verified:
                issues.append("reviewed Claim SHOULD include verified (warning)")

    if kind == "HistoricalInterpretation":
        if record.get("interpretation_state") == "superseded" and not record.get("superseded_by"):
            issues.append("superseded interpretation SHOULD identify superseded_by (warning)")

    return issues


def collect_ids(records: list[tuple[Path, dict]]) -> set[str]:
    return {r["id"] for _, r in records if isinstance(r.get("id"), str)}


def referential_warnings(record: dict, known: set[str]) -> list[str]:
    warnings: list[str] = []
    refs: list[str] = []

    for key in (
        "segment_ref",
        "extraction_ref",
        "resolved_entity_ref",
        "superseded_by",
    ):
        val = record.get(key)
        if isinstance(val, str):
            refs.append(val)

    for key in ("supports", "challenges", "basis_claims", "supersedes"):
        vals = record.get(key) or []
        if isinstance(vals, list):
            refs.extend(v for v in vals if isinstance(v, str))

    for term_key in ("subject", "object"):
        term = record.get(term_key)
        if isinstance(term, dict) and isinstance(term.get("entity_ref"), str):
            refs.append(term["entity_ref"])

    for ref in refs:
        prefix = ref.split(":", 1)[0] + ":"
        if prefix in {
            "segment:",
            "extraction:",
            "entity:",
            "entityref:",
            "claim:",
            "identity:",
            "interpretation:",
            "run:",
        } and ref not in known:
            if any(
                ref.startswith(p)
                for p in ("segment:", "extraction:", "claim:", "interpretation:", "entityref:", "entity:")
            ):
                warnings.append(f"unresolved fixture reference: {ref}")

    return warnings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--fixture-dir",
        type=Path,
        default=Path("corpus/examples/przemyslany"),
    )
    parser.add_argument(
        "--schemas-dir",
        type=Path,
        default=Path("corpus/schemas"),
    )
    args = parser.parse_args()

    if not args.schemas_dir.is_dir():
        sys.stderr.write(f"schemas dir not found: {args.schemas_dir}\n")
        return 2
    if not args.fixture_dir.is_dir():
        sys.stderr.write(f"fixture dir not found: {args.fixture_dir}\n")
        return 2

    records = iter_records(args.fixture_dir)
    known_ids = collect_ids(records)

    schema_blob = "".join(
        p.read_text(encoding="utf-8") for p in sorted(args.schemas_dir.glob("*.schema.yaml"))
    )
    input_blob = "".join(p.read_text(encoding="utf-8") for p, _ in records)

    errors = 0
    warnings = 0
    report_lines: list[str] = []
    report_lines.append(f"HKF validate: {len(records)} records in {args.fixture_dir}")
    report_lines.append(f"schema_sha256: {sha256_text(schema_blob)}")
    report_lines.append(f"input_sha256: {sha256_text(input_blob)}")

    for path, record in records:
        kind = record.get("kind")
        schema_name = KIND_TO_SCHEMA.get(kind)
        if not schema_name:
            report_lines.append(f"ERROR {path.name}: unknown kind {kind!r}")
            errors += 1
            continue

        schema = load_schema(args.schemas_dir, schema_name)
        Draft202012Validator.check_schema(schema)
        validator = Draft202012Validator(schema)

        schema_errors = sorted(validator.iter_errors(record), key=lambda e: list(e.path))
        if schema_errors:
            for err in schema_errors:
                loc = ".".join(str(p) for p in err.path) or "(root)"
                report_lines.append(f"ERROR {path.name}: [{loc}] {err.message}")
                errors += 1
        else:
            report_lines.append(f"OK    {path.name}: {record.get('id')}")

        for issue in semantic_issues(record):
            if "SHOULD" in issue or "warning" in issue.lower():
                report_lines.append(f"WARN  {path.name}: {issue}")
                warnings += 1
            else:
                report_lines.append(f"ERROR {path.name}: {issue}")
                errors += 1

        for warn in referential_warnings(record, known_ids):
            report_lines.append(f"WARN  {path.name}: {warn}")
            warnings += 1

    report_lines.append(f"exit summary: errors={errors} warnings={warnings}")
    report = "\n".join(report_lines) + "\n"
    sys.stdout.write(report)
    sys.stdout.write(f"report_sha256: {sha256_text(report)}\n")

    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
