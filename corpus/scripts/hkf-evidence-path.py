#!/usr/bin/env python3.11
"""Print an evidence path for an HKF interpretation or claim in the pilot fixture.

Usage:
  python3.11 corpus/scripts/hkf-evidence-path.py interpretation:przemyslany:1899:act-412:birth-year
  python3.11 corpus/scripts/hkf-evidence-path.py claim:przemyslany:1899:act-412:residence
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

try:
    import yaml
except ImportError as exc:  # pragma: no cover
    sys.stderr.write(f"PyYAML required (python3.11 recommended): {exc}\n")
    sys.exit(2)


def load_index(fixture_dir: Path) -> dict[str, dict]:
    index: dict[str, dict] = {}
    for path in sorted(fixture_dir.glob("*.yaml")):
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        if isinstance(data, dict) and isinstance(data.get("id"), str):
            index[data["id"]] = data
    return index


def fmt_locator(loc: dict) -> str:
    selectors = loc.get("selectors") or {}
    sel = ", ".join(f"{k}={v}" for k, v in selectors.items())
    return f"{loc.get('source_ref')} [{sel}]"


def path_for_claim(claim: dict, index: dict[str, dict], indent: int = 0) -> list[str]:
    pad = "  " * indent
    lines = [f"{pad}- Claim {claim['id']} ({claim.get('predicate')})"]
    for ev in claim.get("evidence") or []:
        lines.append(f"{pad}  - Evidence: {fmt_locator(ev)}")
    eref = claim.get("extraction_ref")
    if eref:
        lines.append(f"{pad}  - Extraction: {eref}")
        extraction = index.get(eref)
        if extraction and extraction.get("segment_ref"):
            seg_id = extraction["segment_ref"]
            lines.append(f"{pad}  - Segment: {seg_id}")
            seg = index.get(seg_id)
            if seg and isinstance(seg.get("locator"), dict):
                lines.append(f"{pad}    - Locator: {fmt_locator(seg['locator'])}")
    subject = (claim.get("subject") or {}).get("entity_ref")
    obj = claim.get("object") or {}
    if subject:
        lines.append(f"{pad}  - Subject: {subject}")
    if obj.get("entity_ref"):
        lines.append(f"{pad}  - Object: {obj['entity_ref']}")
    elif obj.get("temporal"):
        lines.append(f"{pad}  - Object temporal: {obj['temporal'].get('original')}")
    elif obj.get("literal"):
        lines.append(f"{pad}  - Object literal: {obj['literal'].get('value')}")
    return lines


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("id", help="interpretation:* or claim:* id")
    parser.add_argument(
        "--fixture-dir",
        type=Path,
        default=Path("corpus/examples/przemyslany"),
    )
    args = parser.parse_args()

    index = load_index(args.fixture_dir)
    record = index.get(args.id)
    if not record:
        sys.stderr.write(f"Unknown id in fixture: {args.id}\n")
        return 1

    lines: list[str] = []
    if record.get("kind") == "HistoricalInterpretation":
        lines.append(f"Interpretation: {record['id']}")
        lines.append(f"State: {record.get('interpretation_state')}")
        lines.append(f"Statement: {record.get('statement', '').strip()}")
        lines.append("Supports:")
        for cid in record.get("supports") or []:
            claim = index.get(cid)
            if claim:
                lines.extend(path_for_claim(claim, index, indent=1))
            else:
                lines.append(f"  - missing claim {cid}")
        lines.append("Challenges:")
        for cid in record.get("challenges") or []:
            claim = index.get(cid)
            if claim:
                lines.extend(path_for_claim(claim, index, indent=1))
            else:
                lines.append(f"  - missing claim {cid}")
    elif record.get("kind") == "Claim":
        lines.extend(path_for_claim(record, index))
    else:
        sys.stderr.write(f"Unsupported kind for evidence path: {record.get('kind')}\n")
        return 1

    # Identity assumptions linked via entityrefs in claims
    identity_lines: list[str] = []
    for rec in index.values():
        if rec.get("kind") == "IdentityAssertion":
            identity_lines.append(
                f"- {rec['id']}: decision={rec.get('decision')} "
                f"resolution_state={rec.get('resolution_state')}"
            )
    if identity_lines:
        lines.append("Identity assertions in fixture:")
        lines.extend(identity_lines)

    sys.stdout.write("\n".join(lines) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
