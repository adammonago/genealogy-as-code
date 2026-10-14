#!/usr/bin/env python3
"""Compute autoresearch prompt metrics for a vault path."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
ROUTES_PATH = REPO_ROOT / "routes.json"

SUPPORTED_ROUTES = {
    "prompt:01-tree-expansion",
    "prompt:02-cross-reference-audit",
    "prompt:08-open-question-resolution",
}

METRIC_LABELS = {
    "prompt:01-tree-expansion": "named_individuals_in_family_tree",
    "prompt:02-cross-reference-audit": "unresolved_discrepancies",
    "prompt:08-open-question-resolution": "open_questions",
}


def load_routes() -> dict:
    return json.loads(ROUTES_PATH.read_text(encoding="utf-8"))


def resolve_route(routes: dict, route_key: str) -> dict:
    for route in routes["routes"]:
        if route["key"] == route_key:
            return route
    valid = ", ".join(sorted(r["key"] for r in routes["routes"]))
    raise ValueError(f"Unknown route_key '{route_key}'. Valid keys: {valid}")


def strip_frontmatter(text: str) -> str:
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) >= 3:
            return parts[2]
    return text


def count_named_individuals(family_tree_path: Path) -> int:
    if not family_tree_path.is_file():
        raise FileNotFoundError(f"Missing Family_Tree.md: {family_tree_path}")

    body = strip_frontmatter(family_tree_path.read_text(encoding="utf-8"))
    count = 0
    seen: set[str] = set()

    for line in body.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        for match in re.finditer(r"\*\*([^*]+)\*\*", stripped):
            name = match.group(1).strip()
            if not re.search(r"[A-Za-z]", name):
                continue
            if name.upper() in seen:
                continue
            seen.add(name.upper())
            count += 1

    return count


def count_unresolved_discrepancies(audit_path: Path) -> int:
    if not audit_path.is_file():
        return 0

    text = audit_path.read_text(encoding="utf-8")
    unresolved = 0
    in_table = False

    for line in text.splitlines():
        if line.strip().startswith("|") and "Status" in line and "---" not in line:
            in_table = True
            continue
        if not in_table or not line.strip().startswith("|"):
            continue
        if re.match(r"^\|\s*-+\s*\|", line):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if not cells:
            continue
        status = cells[-1].upper()
        if status and status != "RESOLVED":
            unresolved += 1

    if unresolved:
        return unresolved

    return len(
        re.findall(
            r"\b(?:DISCREPANCY|MISMATCH|CONFLICT)\b",
            text,
            flags=re.IGNORECASE,
        )
    )


def split_question_sections(text: str) -> list[str]:
    body = strip_frontmatter(text)
    sections: list[str] = []
    current: list[str] = []
    for line in body.splitlines():
        if re.match(r"^###\s+\d+\.", line):
            if current:
                sections.append("\n".join(current))
            current = [line]
        elif current:
            current.append(line)
    if current:
        sections.append("\n".join(current))
    return sections


def question_is_open(section: str) -> bool:
    upper = section.upper()
    if "PARTIALLY_RESOLVED" in upper:
        return False
    if re.search(r"\*\*STATUS\*\*:\s*OPEN\b", section, flags=re.IGNORECASE):
        return True
    if re.search(r"\*\*STATUS\*\*:\s*BLOCKED\b", section, flags=re.IGNORECASE):
        return True
    if re.search(r"\bRESOLVED\s*\(", section, flags=re.IGNORECASE):
        return False
    if re.search(r"\*\*STATUS\*\*:\s*RESOLVED\b", section, flags=re.IGNORECASE):
        return False
    if "OPEN" in upper and "RESOLVED" not in upper and "PARTIALLY" not in upper:
        if re.search(r"\*\*STATUS\*\*:\s*OPEN\b", section, flags=re.IGNORECASE):
            return True
    return False


def count_open_questions(open_questions_path: Path) -> int:
    if not open_questions_path.is_file():
        raise FileNotFoundError(f"Missing Open_Questions.md: {open_questions_path}")

    text = open_questions_path.read_text(encoding="utf-8")
    sections = split_question_sections(text)
    if not sections:
        return 0
    return sum(1 for section in sections if question_is_open(section))


def compute_metric(route_key: str, vault_path: Path) -> dict:
    if route_key not in SUPPORTED_ROUTES:
        supported = ", ".join(sorted(SUPPORTED_ROUTES))
        raise ValueError(
            f"Verify script not implemented for {route_key}. Supported: {supported}"
        )

    vault_path = vault_path.resolve()

    if route_key == "prompt:01-tree-expansion":
        value = count_named_individuals(vault_path / "Family_Tree.md")
        direction = "maximize"
    elif route_key == "prompt:02-cross-reference-audit":
        value = count_unresolved_discrepancies(vault_path / "cross_reference_audit.md")
        direction = "minimize"
    elif route_key == "prompt:08-open-question-resolution":
        value = count_open_questions(vault_path / "Open_Questions.md")
        direction = "minimize"
    else:
        raise ValueError(f"Unhandled route: {route_key}")

    return {
        "route_key": route_key,
        "metric": METRIC_LABELS[route_key],
        "value": value,
        "direction": direction,
        "vault_path": str(vault_path),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Compute prompt metric for a vault.")
    parser.add_argument("--route-key", required=True, help="Route key from routes.json")
    parser.add_argument("--vault-path", required=True, help="Path to genealogy vault")
    parser.add_argument("--json", action="store_true", help="Emit JSON output")
    args = parser.parse_args()

    routes = load_routes()
    route = resolve_route(routes, args.route_key)
    if route.get("type") != "prompt":
        print(f"Error: {args.route_key} is not a prompt route.", file=sys.stderr)
        return 2

    vault_path = Path(args.vault_path)
    if not vault_path.is_dir():
        print(f"Error: vault path not found: {vault_path}", file=sys.stderr)
        return 2

    try:
        result = compute_metric(args.route_key, vault_path)
    except FileNotFoundError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(f"route_key: {result['route_key']}")
        print(f"metric: {result['metric']}")
        print(f"value: {result['value']}")
        print(f"direction: {result['direction']}")
        print(f"vault_path: {result['vault_path']}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
