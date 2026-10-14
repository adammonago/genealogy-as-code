#!/usr/bin/env python3
"""Append a structured agent_run manifest to a vault Research_Log.md."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from agent_run_lib import (  # noqa: E402
    AGENT_RUNS_DIR,
    collect_manifests,
    default_run_id,
    insert_before_logging_convention,
    render_index_block,
    render_manifest_block,
    validate_manifest,
)


def parse_list(value: str | None) -> list:
    if not value:
        return []
    if value.startswith("["):
        parsed = json.loads(value)
        if not isinstance(parsed, list):
            raise ValueError("List fields must be JSON arrays.")
        return parsed
    return [item.strip() for item in value.split(",") if item.strip()]


def load_manifest(args: argparse.Namespace) -> dict:
    if args.manifest:
        data = json.loads(Path(args.manifest).read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            raise ValueError("Manifest JSON must be an object.")
        return data

    if args.stdin:
        data = json.load(sys.stdin)
        if not isinstance(data, dict):
            raise ValueError("Manifest JSON must be an object.")
        return data

    data = {
        "route_key": args.route_key,
        "hat_at_close": args.hat_at_close,
        "recommended_next_route": args.recommended_next_route,
        "prior_route_key": args.prior_route_key,
        "platform": args.platform,
        "iterations_completed": args.iterations_completed,
        "iterations_planned": args.iterations_planned,
        "metric_name": args.metric_name,
        "metric_before": args.metric_before,
        "metric_after": args.metric_after,
        "metric_delta": args.metric_delta,
        "vault_files_changed": parse_list(args.vault_files_changed),
        "negative_results_logged": args.negative_results_logged,
        "handoffs_created": parse_list(args.handoffs_created),
        "reroutes_triggered": parse_list(args.reroutes_triggered),
        "validator_result": args.validator_result,
        "validator_report_path": args.validator_report_path,
        "confidence_notes": args.confidence_notes,
    }
    return {key: value for key, value in data.items() if value is not None}


def main() -> int:
    parser = argparse.ArgumentParser(description="Append an agent_run manifest to Research_Log.md.")
    parser.add_argument("--vault-path", required=True, help="Path to genealogy vault")
    parser.add_argument("--manifest", help="Path to JSON manifest file")
    parser.add_argument("--stdin", action="store_true", help="Read manifest JSON from stdin")
    parser.add_argument(
        "--standalone",
        action="store_true",
        help=f"Write full manifest to {AGENT_RUNS_DIR}/{{run_id}}.md and append index entry to Research_Log",
    )
    parser.add_argument("--dry-run", action="store_true", help="Print manifest block without writing")
    parser.add_argument("--route-key")
    parser.add_argument("--prior-route-key")
    parser.add_argument("--hat-at-close")
    parser.add_argument("--recommended-next-route")
    parser.add_argument("--platform", default="generic")
    parser.add_argument("--iterations-completed", type=int)
    parser.add_argument("--iterations-planned", type=int)
    parser.add_argument("--metric-name")
    parser.add_argument("--metric-before", type=int)
    parser.add_argument("--metric-after", type=int)
    parser.add_argument("--metric-delta", type=int)
    parser.add_argument("--vault-files-changed", help="Comma-separated paths or JSON array")
    parser.add_argument("--negative-results-logged", type=int, default=0)
    parser.add_argument("--handoffs-created", help="Comma-separated paths or JSON array")
    parser.add_argument(
        "--reroutes-triggered",
        help='JSON array, e.g. [{"condition":"interactive_wall","from":"prompt:11","to":"workflow:interactive-handoff"}]',
    )
    parser.add_argument("--validator-result", default="N/A")
    parser.add_argument("--validator-report-path")
    parser.add_argument("--confidence-notes")
    args = parser.parse_args()

    if not args.manifest and not args.stdin:
        if not args.route_key or not args.hat_at_close or not args.recommended_next_route:
            parser.error(
                "Provide --manifest, --stdin, or the flags "
                "--route-key, --hat-at-close, and --recommended-next-route."
            )

    vault_path = Path(args.vault_path)
    if not vault_path.is_dir():
        print(f"Error: vault path not found: {vault_path}", file=sys.stderr)
        return 2

    log_path = vault_path / "Research_Log.md"
    if not log_path.is_file():
        print(f"Error: missing Research_Log.md in vault: {log_path}", file=sys.stderr)
        return 2

    try:
        data = load_manifest(args)
        validate_manifest(data)
        block = render_manifest_block(data)
    except (ValueError, json.JSONDecodeError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2

    run_id = data["run_id"]
    if args.standalone:
        manifest_rel = f"{AGENT_RUNS_DIR}/{run_id}.md"
        manifest_path = vault_path / manifest_rel
        index_block = render_index_block(data, manifest_rel)
        if args.dry_run:
            print(f"# standalone file: {manifest_path}\n")
            print(block)
            print(f"# Research_Log index entry\n")
            print(index_block)
            return 0

        manifest_path.parent.mkdir(parents=True, exist_ok=True)
        manifest_path.write_text(block, encoding="utf-8")
        updated = insert_before_logging_convention(log_path.read_text(encoding="utf-8"), index_block)
        log_path.write_text(updated, encoding="utf-8")
        print(f"Wrote standalone manifest to {manifest_path}")
        print(f"Appended index entry to {log_path}")
        print(f"run_id: {run_id}")
        return 0

    if args.dry_run:
        print(block)
        return 0

    updated = insert_before_logging_convention(log_path.read_text(encoding="utf-8"), block)
    log_path.write_text(updated, encoding="utf-8")
    print(f"Appended agent_run manifest to {log_path}")
    print(f"run_id: {run_id}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
