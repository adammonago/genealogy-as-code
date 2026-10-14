"""Shared helpers for agent_run manifest parsing and rendering."""

from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path


REQUIRED_FIELDS = ("route_key", "hat_at_close", "recommended_next_route")
HATS = {"orchestrator", "research_executor", "human_bridge", "validator"}
VALIDATOR_RESULTS = {"PASS", "FAIL", "N/A"}
LOGGING_CONVENTION_HEADER = "## Logging Convention"
AGENT_RUNS_DIR = "agent_runs"


def slugify_route(route_key: str) -> str:
    return re.sub(r"[^a-zA-Z0-9]+", "-", route_key).strip("-").lower()


def default_run_id(route_key: str, created: datetime) -> str:
    stamp = created.strftime("%Y%m%d-%H%M%S")
    return f"{stamp}-{slugify_route(route_key)}"


def parse_simple_yaml(block: str) -> dict:
    data: dict = {}
    current_list_key: str | None = None
    current_dict: dict | None = None

    for raw_line in block.splitlines():
        line = raw_line.rstrip()
        if not line.strip() or line.strip().startswith("#"):
            continue

        if line.startswith("  -") and current_list_key:
            item = line[3:].strip()
            if item == "" and current_list_key == "reroutes_triggered":
                current_dict = {}
                data.setdefault(current_list_key, []).append(current_dict)
                continue
            if current_dict is not None and line.startswith("    "):
                sub_key, _, sub_value = line.strip().partition(":")
                current_dict[sub_key.strip()] = _parse_scalar(sub_value.strip())
                continue
            data.setdefault(current_list_key, []).append(_parse_scalar(item))
            current_dict = None
            continue

        if line.startswith("    ") and current_dict is not None:
            sub_key, _, sub_value = line.strip().partition(":")
            current_dict[sub_key.strip()] = _parse_scalar(sub_value.strip())
            continue

        if ":" not in line:
            continue

        key, _, value = line.partition(":")
        key = key.strip()
        value = value.strip()
        current_dict = None

        if value == "":
            current_list_key = key
            data[key] = []
            continue

        current_list_key = None
        if value == "[]":
            data[key] = []
        elif value.startswith("[") and value.endswith("]"):
            inner = value[1:-1].strip()
            data[key] = [] if not inner else [_parse_scalar(part.strip()) for part in inner.split(",")]
        else:
            data[key] = _parse_scalar(value)

    return data


def _parse_scalar(value: str):
    if not value:
        return ""
    if value.startswith('"') and value.endswith('"'):
        return value[1:-1].replace('\\"', '"')
    if value.isdigit():
        return int(value)
    lowered = value.lower()
    if lowered in {"true", "false"}:
        return lowered == "true"
    return value


def extract_frontmatter_blocks(text: str) -> list[tuple[dict, str]]:
    blocks: list[tuple[dict, str]] = []
    parts = text.split("---")
    index = 1
    while index + 1 < len(parts):
        yaml_block = parts[index]
        body = parts[index + 1]
        data = parse_simple_yaml(yaml_block)
        if data.get("type") == "agent_run":
            blocks.append((data, body))
        index += 2
    return blocks


def parse_manifest_file(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    blocks = extract_frontmatter_blocks(text)
    if not blocks:
        raise ValueError(f"No agent_run frontmatter found in {path}")
    data, _ = blocks[0]
    data["_source_path"] = str(path)
    return data


def collect_manifests(vault_path: Path) -> list[dict]:
    vault_path = vault_path.resolve()
    manifests: dict[str, dict] = {}

    log_path = vault_path / "Research_Log.md"
    if log_path.is_file():
        for data, _ in extract_frontmatter_blocks(log_path.read_text(encoding="utf-8")):
            run_id = str(data.get("run_id", ""))
            entry = dict(data)
            entry["_source_path"] = str(log_path)
            entry["_storage"] = "inline"
            if run_id:
                manifests[run_id] = entry

    runs_dir = vault_path / AGENT_RUNS_DIR
    if runs_dir.is_dir():
        for path in sorted(runs_dir.glob("*.md")):
            try:
                data = parse_manifest_file(path)
            except ValueError:
                continue
            run_id = str(data.get("run_id", path.stem))
            entry = dict(data)
            entry["_source_path"] = str(path)
            entry["_storage"] = "standalone"
            manifests[run_id] = entry

    return sorted(manifests.values(), key=lambda item: str(item.get("created", "")), reverse=True)


def validate_manifest(data: dict) -> None:
    missing = [field for field in REQUIRED_FIELDS if not data.get(field)]
    if missing:
        raise ValueError(f"Missing required manifest fields: {', '.join(missing)}")

    hat = data["hat_at_close"]
    if hat not in HATS:
        raise ValueError(f"Invalid hat_at_close '{hat}'. Expected one of: {', '.join(sorted(HATS))}")

    validator_result = data.get("validator_result", "N/A")
    if validator_result not in VALIDATOR_RESULTS:
        raise ValueError(
            f"Invalid validator_result '{validator_result}'. Expected PASS, FAIL, or N/A."
        )


def yaml_scalar(value) -> str:
    if value is None:
        return ""
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (int, float)):
        return str(value)
    text = str(value)
    if not text:
        return '""'
    if any(ch in text for ch in ":#{}[],&*?|>-\"\\"):
        escaped = text.replace('"', '\\"')
        return f'"{escaped}"'
    return text


def yaml_list(key: str, items: list) -> list[str]:
    if not items:
        return [f"{key}: []"]
    lines = [f"{key}:"]
    for item in items:
        if isinstance(item, dict):
            lines.append("  -")
            for sub_key, sub_value in item.items():
                lines.append(f"    {sub_key}: {yaml_scalar(sub_value)}")
        else:
            lines.append(f"  - {yaml_scalar(item)}")
    return lines


def render_manifest_block(data: dict) -> str:
    created_raw = data.get("created")
    if created_raw:
        created = datetime.fromisoformat(str(created_raw).replace("Z", "+00:00"))
    else:
        created = datetime.now(timezone.utc)
        data["created"] = created.replace(microsecond=0).isoformat().replace("+00:00", "Z")

    if not data.get("run_id"):
        data["run_id"] = default_run_id(data["route_key"], created)

    lines = [
        "---",
        "type: agent_run",
        f"run_id: {yaml_scalar(data['run_id'])}",
        f"created: {yaml_scalar(data['created'])}",
        f"route_key: {yaml_scalar(data['route_key'])}",
    ]

    optional_scalar = [
        "prior_route_key",
        "hat_at_close",
        "platform",
        "iterations_completed",
        "iterations_planned",
        "metric_name",
        "metric_before",
        "metric_after",
        "metric_delta",
        "negative_results_logged",
        "validator_result",
        "validator_report_path",
        "recommended_next_route",
        "confidence_notes",
        "manifest_path",
    ]
    for key in optional_scalar:
        if key in data and data[key] is not None and data[key] != "":
            lines.append(f"{key}: {yaml_scalar(data[key])}")

    for key in ("vault_files_changed", "handoffs_created", "reroutes_triggered"):
        items = data.get(key) or []
        lines.extend(yaml_list(key, items))

    lines.extend(
        [
            "tags: [genealogy, agent_run]",
            "---",
            "",
            f"## Agent run: `{data['route_key']}`",
            "",
        ]
    )

    notes = data.get("confidence_notes")
    if notes:
        lines.extend([notes, ""])

    lines.extend(
        [
            "### Follow-up",
            "",
            f"- **Recommended next route**: `{data['recommended_next_route']}`",
            f"- **Validator**: {data.get('validator_result', 'N/A')}",
            "",
            "---",
            "",
        ]
    )
    return "\n".join(lines)


def render_index_block(data: dict, manifest_rel_path: str) -> str:
    return "\n".join(
        [
            "---",
            "type: agent_run_index",
            f"run_id: {yaml_scalar(data['run_id'])}",
            f"created: {yaml_scalar(data['created'])}",
            f"route_key: {yaml_scalar(data['route_key'])}",
            f"manifest_path: {yaml_scalar(manifest_rel_path)}",
            "tags: [genealogy, agent_run]",
            "---",
            "",
            f"## Agent run index: `{data['route_key']}`",
            "",
            f"Standalone manifest: [{manifest_rel_path}]({manifest_rel_path})",
            "",
            "---",
            "",
        ]
    )


def insert_before_logging_convention(research_log: str, block: str) -> str:
    if LOGGING_CONVENTION_HEADER in research_log:
        head, tail = research_log.split(LOGGING_CONVENTION_HEADER, 1)
        if not head.endswith("\n"):
            head += "\n"
        return head + block + LOGGING_CONVENTION_HEADER + tail
    if not research_log.endswith("\n"):
        research_log += "\n"
    return research_log + "\n" + block
