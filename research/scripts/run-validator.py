#!/usr/bin/env python3
"""Post-run vault validator for genealogy autoresearch."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass
from datetime import date
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
REPORT_TEMPLATE = REPO_ROOT / "vault-template/templates/validator-report.md"

CORE_FILES = ("Family_Tree.md", "Open_Questions.md", "Research_Log.md")

SOURCE_SIGNALS = re.compile(
    r"(?i)(source|citation|http|https|find a grave|familysearch|ancestry|\[[^\]]+\]\([^)]+\.md\))",
)


@dataclass
class Finding:
    check: str
    severity: str
    path: str
    detail: str


def strip_frontmatter(text: str) -> tuple[dict[str, str], str]:
    if not text.startswith("---"):
        return {}, text
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}, text
    meta: dict[str, str] = {}
    for line in parts[1].splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        meta[key.strip()] = value.strip().strip('"').strip("'")
    return meta, parts[2]


def count_yaml_list_items(frontmatter_block: str, key: str) -> int:
    lines = frontmatter_block.splitlines()
    in_key = False
    count = 0
    for line in lines:
        if re.match(rf"^{re.escape(key)}:\s*$", line):
            in_key = True
            continue
        if in_key:
            if re.match(r"^\s*-\s+", line):
                count += 1
                continue
            if not line.startswith(" "):
                in_key = False
    return count


def read_frontmatter_block(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return ""
    parts = text.split("---", 2)
    return parts[1] if len(parts) >= 2 else ""


def parse_person_confidence(path: Path) -> tuple[str, int]:
    block = read_frontmatter_block(path)
    if not block:
        return "", 0
    confidence = ""
    for line in block.splitlines():
        if line.startswith("confidence:"):
            confidence = line.split(":", 1)[1].strip()
            break
    sources = count_yaml_list_items(block, "sources")
    return confidence, sources


def iter_markdown_files(vault_path: Path) -> list[Path]:
    return sorted(p for p in vault_path.rglob("*.md") if p.is_file())


def check_wiki_links(vault_path: Path) -> list[Finding]:
    findings: list[Finding] = []
    for path in iter_markdown_files(vault_path):
        text = path.read_text(encoding="utf-8")
        if "[[" in text:
            findings.append(
                Finding(
                    check="wiki_links",
                    severity="blocking",
                    path=str(path.relative_to(vault_path)),
                    detail="Obsidian wiki link syntax detected; use standard Markdown links",
                )
            )
    return findings


def check_core_files(vault_path: Path) -> list[Finding]:
    findings: list[Finding] = []
    for name in CORE_FILES:
        if not (vault_path / name).is_file():
            findings.append(
                Finding(
                    check="missing_core_files",
                    severity="warning",
                    path=name,
                    detail="Expected core vault file is missing",
                )
            )
    return findings


def check_unverified_tree(vault_path: Path) -> list[Finding]:
    path = vault_path / "Family_Tree.md"
    if not path.is_file():
        return []
    text = path.read_text(encoding="utf-8")
    count = text.lower().count("(unverified)")
    if not count:
        return []
    return [
        Finding(
            check="unverified_tree_entries",
            severity="warning",
            path="Family_Tree.md",
            detail=f"Found {count} (unverified) marker(s); confirm sources or run cross-reference audit",
        )
    ]


def split_question_sections(text: str) -> list[str]:
    _, body = strip_frontmatter(text)
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


def check_resolved_questions(vault_path: Path) -> list[Finding]:
    path = vault_path / "Open_Questions.md"
    if not path.is_file():
        return []
    text = path.read_text(encoding="utf-8")
    findings: list[Finding] = []
    for section in split_question_sections(text):
        upper = section.upper()
        resolved = (
            re.search(r"\*\*STATUS\*\*:\s*RESOLVED\b", section, flags=re.IGNORECASE)
            or re.search(r"\bRESOLVED\s*\(", section, flags=re.IGNORECASE)
        )
        if not resolved:
            continue
        if not SOURCE_SIGNALS.search(section):
            title = section.splitlines()[0].strip("# ").strip()
            findings.append(
                Finding(
                    check="resolved_without_source",
                    severity="blocking",
                    path="Open_Questions.md",
                    detail=f"Question appears RESOLVED without citation signals: {title}",
                )
            )
    return findings


def check_person_sources(vault_path: Path) -> list[Finding]:
    findings: list[Finding] = []
    for path in iter_markdown_files(vault_path):
        block = read_frontmatter_block(path)
        if "type: person" not in block:
            continue
        confidence, sources = parse_person_confidence(path)
        rel = str(path.relative_to(vault_path))
        if confidence == "high" and sources < 2:
            findings.append(
                Finding(
                    check="high_confidence_under_sourced",
                    severity="blocking",
                    path=rel,
                    detail=f"confidence high with {sources} source(s); need at least two independent sources",
                )
            )
        elif confidence == "moderate" and sources < 2:
            findings.append(
                Finding(
                    check="moderate_confidence_under_sourced",
                    severity="warning",
                    path=rel,
                    detail=f"confidence moderate with {sources} source(s); corroboration recommended",
                )
            )
    return findings


def recommend_routes(findings: list[Finding]) -> list[str]:
    checks = {finding.check for finding in findings if finding.severity == "blocking"}
    routes: list[str] = []
    if "resolved_without_source" in checks or "high_confidence_under_sourced" in checks:
        routes.append("workflow:discrepancy-resolution")
    if "wiki_links" in checks:
        routes.append("prompt:02-cross-reference-audit")
    if any(
        finding.check in {"high_confidence_under_sourced", "moderate_confidence_under_sourced"}
        for finding in findings
    ):
        routes.append("prompt:05-source-citation-audit")
    deduped: list[str] = []
    for route in routes:
        if route not in deduped:
            deduped.append(route)
    return deduped


def run_validation(vault_path: Path, prior_route_key: str | None = None) -> dict:
    vault_path = vault_path.resolve()
    findings: list[Finding] = []
    findings.extend(check_core_files(vault_path))
    findings.extend(check_wiki_links(vault_path))
    findings.extend(check_unverified_tree(vault_path))
    findings.extend(check_resolved_questions(vault_path))
    findings.extend(check_person_sources(vault_path))

    blocking = [f for f in findings if f.severity == "blocking"]
    warnings = [f for f in findings if f.severity == "warning"]
    return {
        "prior_route_key": prior_route_key,
        "vault_path": str(vault_path),
        "result": "FAIL" if blocking else "PASS",
        "blocking_count": len(blocking),
        "warning_count": len(warnings),
        "findings": [asdict(f) for f in findings],
        "recommended_corrective_routes": recommend_routes(findings),
    }


def render_report(result: dict) -> str:
    today = date.today().isoformat()
    blocking = [f for f in result["findings"] if f["severity"] == "blocking"]
    warnings = [f for f in result["findings"] if f["severity"] == "warning"]
    prior = result.get("prior_route_key") or "unknown"

    lines = [
        "---",
        "type: reference",
        f"created: {today}",
        f"updated: {today}",
        f"prior_route_key: {prior}",
        "tags: [genealogy, validator]",
        f"blocking_count: {result['blocking_count']}",
        f"warning_count: {result['warning_count']}",
        "---",
        "",
        "# Validator Report",
        "",
        "Most recent post-run quality gate. Generated by `workflow:validator-pass` and `scripts/run-validator.py`.",
        "",
        "## Context",
        "",
        f"- **Prior route**: `{prior}`",
        f"- **Date**: {today}",
        f"- **Vault path**: `{result['vault_path']}`",
        "",
        "## Summary",
        "",
        "| Severity | Count |",
        "|---|---|",
        f"| Blocking | {result['blocking_count']} |",
        f"| Warning | {result['warning_count']} |",
        "",
        f"**Result**: {result['result']}",
        "",
        "## Findings",
        "",
        "### Blocking",
        "",
        "| Check | File | Detail |",
        "|---|---|---|",
    ]
    if blocking:
        for item in blocking:
            lines.append(f"| {item['check']} | {item['path']} | {item['detail']} |")
    else:
        lines.append("| | | None |")

    lines.extend(
        [
            "",
            "### Warnings",
            "",
            "| Check | File | Detail |",
            "|---|---|---|",
        ]
    )
    if warnings:
        for item in warnings:
            lines.append(f"| {item['check']} | {item['path']} | {item['detail']} |")
    else:
        lines.append("| | | None |")

    lines.extend(["", "## Recommended corrective routes", ""])
    routes = result.get("recommended_corrective_routes") or []
    if routes:
        for index, route in enumerate(routes, start=1):
            lines.append(f"{index}. `{route}`")
    else:
        lines.append("1. None")

    lines.extend(["", "## Notes", "", "Automated report. Review warnings before dismissing.", ""])
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate vault quality after an agent run.")
    parser.add_argument("--vault-path", required=True, help="Path to genealogy vault")
    parser.add_argument("--prior-route-key", help="Route that ran before validation")
    parser.add_argument("--write-report", action="store_true", help="Write validator_report.md")
    parser.add_argument("--json", action="store_true", help="Emit JSON output")
    args = parser.parse_args()

    vault_path = Path(args.vault_path)
    if not vault_path.is_dir():
        print(f"Error: vault path not found: {vault_path}", file=sys.stderr)
        return 2

    result = run_validation(vault_path, args.prior_route_key)

    if args.write_report:
        report_path = vault_path / "validator_report.md"
        report_path.write_text(render_report(result), encoding="utf-8")
        result["report_path"] = str(report_path)

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(f"result: {result['result']}")
        print(f"blocking_count: {result['blocking_count']}")
        print(f"warning_count: {result['warning_count']}")
        if result["recommended_corrective_routes"]:
            print("recommended_corrective_routes: " + ", ".join(result["recommended_corrective_routes"]))
        for item in result["findings"]:
            print(f"[{item['severity']}] {item['check']} :: {item['path']} :: {item['detail']}")
        if args.write_report:
            print(f"report_path: {result.get('report_path')}")

    return 1 if result["blocking_count"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
