#!/usr/bin/env python3
"""Write a pending agent_run manifest for post-run hook finalization."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from agent_run_lib import validate_manifest  # noqa: E402
from env_utils import resolve_vault_path  # noqa: E402

DEFAULT_PENDING = REPO_ROOT / ".cursor/pending-agent-run.json"


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
        "vault_path": args.vault_path,
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
        "run_validator": args.run_validator,
        "standalone": args.standalone,
    }
    return {key: value for key, value in data.items() if value is not None}


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Write a pending agent_run manifest for post-run finalization."
    )
    parser.add_argument(
        "--pending-path",
        default=str(DEFAULT_PENDING),
        help="Path to pending manifest JSON (default: .cursor/pending-agent-run.json)",
    )
    parser.add_argument("--manifest", help="Path to JSON manifest file")
    parser.add_argument("--stdin", action="store_true", help="Read manifest JSON from stdin")
    parser.add_argument("--vault-path", help="Genealogy vault path (falls back to VAULT_PATH in .env.local)")
    parser.add_argument("--route-key")
    parser.add_argument("--prior-route-key")
    parser.add_argument("--hat-at-close")
    parser.add_argument("--recommended-next-route")
    parser.add_argument("--platform", default="cursor")
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
    parser.add_argument(
        "--run-validator",
        action="store_true",
        help="Ask finalize-agent-run.py to run run-validator.py before append",
    )
    parser.add_argument(
        "--standalone",
        action="store_true",
        help="Ask finalize-agent-run.py to write agent_runs/{run_id}.md",
    )
    args = parser.parse_args()

    if not args.manifest and not args.stdin:
        if not args.route_key or not args.hat_at_close or not args.recommended_next_route:
            parser.error(
                "Provide --manifest, --stdin, or the flags "
                "--route-key, --hat-at-close, and --recommended-next-route."
            )

    try:
        data = load_manifest(args)
        vault_path = resolve_vault_path(REPO_ROOT, data)
        if not vault_path:
            raise ValueError(
                "Missing vault_path. Pass --vault-path or set VAULT_PATH in .env.local."
            )
        data["vault_path"] = vault_path
        validate_manifest(data)
    except (ValueError, json.JSONDecodeError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2

    pending_path = Path(args.pending_path)
    pending_path.parent.mkdir(parents=True, exist_ok=True)
    pending_path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote pending agent run manifest to {pending_path}")
    print(f"route_key: {data['route_key']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
