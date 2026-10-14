#!/usr/bin/env python3
"""List structured agent_run manifests from a vault Research_Log and agent_runs/."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from agent_run_lib import collect_manifests  # noqa: E402


PUBLIC_FIELDS = (
    "run_id",
    "created",
    "route_key",
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
    "recommended_next_route",
    "manifest_path",
    "_source_path",
    "_storage",
)


def public_view(entry: dict) -> dict:
    return {key: entry[key] for key in PUBLIC_FIELDS if key in entry}


def print_table(entries: list[dict]) -> None:
    if not entries:
        print("No agent_run manifests found.")
        return

    headers = ("created", "route_key", "hat_at_close", "validator", "storage", "run_id")
    rows = []
    for entry in entries:
        rows.append(
            (
                str(entry.get("created", "")),
                str(entry.get("route_key", "")),
                str(entry.get("hat_at_close", "")),
                str(entry.get("validator_result", "N/A")),
                str(entry.get("_storage", "")),
                str(entry.get("run_id", "")),
            )
        )

    widths = [len(header) for header in headers]
    for row in rows:
        widths = [max(width, len(cell)) for width, cell in zip(widths, row)]

    def format_row(cells: tuple[str, ...]) -> str:
        return "  ".join(cell.ljust(width) for cell, width in zip(cells, widths))

    print(format_row(headers))
    print(format_row(tuple("-" * width for width in widths)))
    for row in rows:
        print(format_row(row))


def main() -> int:
    parser = argparse.ArgumentParser(description="List agent_run manifests from a vault.")
    parser.add_argument("--vault-path", required=True, help="Path to genealogy vault")
    parser.add_argument("--route-key", help="Filter by route_key (exact match)")
    parser.add_argument("--limit", type=int, help="Maximum number of manifests to return")
    parser.add_argument("--json", action="store_true", help="Emit JSON array")
    args = parser.parse_args()

    vault_path = Path(args.vault_path)
    if not vault_path.is_dir():
        print(f"Error: vault path not found: {vault_path}", file=sys.stderr)
        return 2

    entries = collect_manifests(vault_path)
    if args.route_key:
        entries = [entry for entry in entries if entry.get("route_key") == args.route_key]
    if args.limit is not None:
        entries = entries[: max(args.limit, 0)]

    if args.json:
        print(json.dumps([public_view(entry) for entry in entries], indent=2))
    else:
        print_table(entries)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
