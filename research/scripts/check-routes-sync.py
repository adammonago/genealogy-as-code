#!/usr/bin/env python3
"""Validate routes.json against ROUTING_TABLE.md and repository files."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
ROUTES_PATH = REPO_ROOT / "routes.json"
ROUTING_TABLE_PATH = REPO_ROOT / "skills/genealogy-autoresearch/ROUTING_TABLE.md"

ROUTE_KEY_PATTERN = re.compile(r"`((?:workflow|prompt):[^`]+)`")


def load_routes() -> dict:
    return json.loads(ROUTES_PATH.read_text(encoding="utf-8"))


def extract_routing_table_keys(text: str) -> set[str]:
    return set(ROUTE_KEY_PATTERN.findall(text))


def validate_routes_sync() -> list[str]:
    errors: list[str] = []
    routes_data = load_routes()
    routes = routes_data["routes"]
    route_by_key = {route["key"]: route for route in routes}
    keys_json = set(route_by_key)

    table_text = ROUTING_TABLE_PATH.read_text(encoding="utf-8")
    keys_table = extract_routing_table_keys(table_text)

    missing_in_table = sorted(keys_json - keys_table)
    missing_in_json = sorted(keys_table - keys_json)

    if missing_in_table:
        errors.append(
            "routes.json keys missing from ROUTING_TABLE.md: " + ", ".join(missing_in_table)
        )
    if missing_in_json:
        errors.append(
            "ROUTING_TABLE.md keys missing from routes.json: " + ", ".join(missing_in_json)
        )

    conditions = routes_data.get("reroute_conditions") or {}
    for route in routes:
        key = route["key"]
        source = route.get("source")
        if not source:
            errors.append(f"{key}: missing source path")
            continue
        source_path = REPO_ROOT / source
        if not source_path.is_file():
            errors.append(f"{key}: source file not found: {source}")

        for follow_up in route.get("follow_up") or []:
            if follow_up not in keys_json:
                errors.append(f"{key}: invalid follow_up target: {follow_up}")

        for trigger in route.get("reroute_triggers") or []:
            condition = trigger.get("condition")
            target = trigger.get("route")
            if condition not in conditions:
                errors.append(f"{key}: unknown reroute condition: {condition}")
            if target not in keys_json:
                errors.append(f"{key}: invalid reroute target: {target}")

        table_sources = [
            line.split("|")[3].strip().strip("`")
            for line in table_text.splitlines()
            if line.startswith("| `") and key in line
        ]
        if table_sources and table_sources[0] != source:
            errors.append(
                f"{key}: ROUTING_TABLE source {table_sources[0]!r} != routes.json source {source!r}"
            )

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate route manifest sync.")
    parser.parse_args()

    if not ROUTES_PATH.is_file():
        print(f"Error: missing {ROUTES_PATH}", file=sys.stderr)
        return 2
    if not ROUTING_TABLE_PATH.is_file():
        print(f"Error: missing {ROUTING_TABLE_PATH}", file=sys.stderr)
        return 2

    errors = validate_routes_sync()
    if errors:
        print("Route sync check failed:", file=sys.stderr)
        for error in errors:
            print(f"  - {error}", file=sys.stderr)
        return 2

    routes_data = load_routes()
    route_count = len(routes_data["routes"])
    print(f"Route sync OK ({route_count} routes, schema {routes_data['schema_version']})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
