#!/usr/bin/env python3
"""Portable route runner for genealogy prompts and workflows."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
ROUTES_PATH = REPO_ROOT / "routes.json"


def load_routes() -> dict:
    return json.loads(ROUTES_PATH.read_text(encoding="utf-8"))


def resolve_route(routes: dict, route_key: str) -> dict:
    for route in routes["routes"]:
        if route["key"] == route_key:
            return route
    valid = ", ".join(sorted(r["key"] for r in routes["routes"]))
    raise ValueError(f"Unknown route_key '{route_key}'. Valid keys: {valid}")


def parse_var_pairs(items: list[str]) -> dict[str, str]:
    parsed: dict[str, str] = {}
    for item in items:
        if "=" not in item:
            raise ValueError(f"Invalid --var value '{item}'. Use KEY=VALUE.")
        key, value = item.split("=", 1)
        key = key.strip().upper()
        if not key:
            raise ValueError(f"Invalid --var key in '{item}'.")
        parsed[key] = value.strip()
    return parsed


def render_content(raw: str, values: dict[str, str]) -> str:
    rendered = raw
    for key, value in values.items():
        rendered = rendered.replace(f"[{key}]", value)
    if "ANCESTOR" in values:
        rendered = rendered.replace("[ANCESTOR NAME]", values["ANCESTOR"])
    return rendered


def format_route_graph(route: dict, routes: dict) -> str:
    lines: list[str] = []
    follow_up = route.get("follow_up") or []
    if follow_up:
        lines.append("Follow-up routes: " + ", ".join(follow_up))
    triggers = route.get("reroute_triggers") or []
    if triggers:
        lines.append("Reroute triggers:")
        conditions = routes.get("reroute_conditions") or {}
        for item in triggers:
            condition = item.get("condition", "")
            target = item.get("route", "")
            desc = conditions.get(condition, "")
            suffix = f" ({desc})" if desc else ""
            lines.append(f"  - {condition}{suffix} -> {target}")
    return "\n".join(lines)


def build_platform_hint(platform: str, route_key: str, values: dict[str, str]) -> str:
    args = " ".join(f"{k}={v}" for k, v in sorted(values.items()))
    if platform == "claude":
        return (
            "Claude CLI invocation guidance:\n"
            "1. Open Claude in this repository.\n"
            "2. Start your agent or /autoresearch flow.\n"
            f"3. Run route {route_key} with variables: {args}"
        )
    if platform == "codex":
        return (
            "Codex or Cursor agent invocation guidance:\n"
            "1. Open this repository in the agent.\n"
            "2. Ask it to execute the route by key.\n"
            f"3. Use route_key={route_key} and variables: {args}"
        )
    if platform == "gemini":
        return (
            "Gemini CLI invocation guidance:\n"
            "1. Run Gemini from this repository root.\n"
            "2. Paste the rendered route content as the task.\n"
            f"3. Include route_key={route_key} and variables: {args}"
        )
    return "Generic invocation guidance: use the rendered content with your preferred agent runner."


def main() -> int:
    parser = argparse.ArgumentParser(description="Render and run a packaged genealogy route.")
    parser.add_argument("--route-key", required=True, help="Route key from routes.json")
    parser.add_argument(
        "--platform",
        default="generic",
        choices=["generic", "claude", "codex", "gemini"],
        help="Platform specific guidance to print",
    )
    parser.add_argument("--vault-path", help="Value for [VAULT_PATH]")
    parser.add_argument("--gedcom-path", help="Value for [GEDCOM_PATH]")
    parser.add_argument("--surname", help="Value for [SURNAME]")
    parser.add_argument("--ancestor", help="Value for [ANCESTOR] and [ANCESTOR NAME]")
    parser.add_argument("--location", help="Value for [LOCATION]")
    parser.add_argument("--date", help="Value for [DATE]")
    parser.add_argument(
        "--var",
        action="append",
        default=[],
        help="Extra KEY=VALUE placeholders. Repeat as needed.",
    )
    parser.add_argument(
        "--print-only",
        action="store_true",
        help="Only print rendered content and instructions.",
    )
    args = parser.parse_args()

    routes = load_routes()
    route = resolve_route(routes, args.route_key)

    values = parse_var_pairs(args.var)
    fixed = {
        "VAULT_PATH": args.vault_path,
        "GEDCOM_PATH": args.gedcom_path,
        "SURNAME": args.surname,
        "ANCESTOR": args.ancestor,
        "LOCATION": args.location,
        "DATE": args.date,
    }
    for key, value in fixed.items():
        if value:
            values[key] = value

    missing = [k for k in route.get("required_inputs", []) if k not in values]
    if missing:
        msg = ", ".join(missing)
        raise ValueError(
            f"Missing required inputs for {args.route_key}: {msg}. "
            "Pass values with flags such as --vault-path or --var KEY=VALUE."
        )

    source_path = REPO_ROOT / route["source"]
    raw = source_path.read_text(encoding="utf-8")
    rendered = render_content(raw, values)
    hint = build_platform_hint(args.platform, args.route_key, values)

    print(f"Route key: {args.route_key}")
    print(f"Route type: {route['type']}")
    print(f"Source file: {route['source']}")
    graph = format_route_graph(route, routes)
    if graph:
        print()
        print(graph)
    print()
    print(hint)
    print()
    print("----- BEGIN RENDERED CONTENT -----")
    print(rendered)
    print("----- END RENDERED CONTENT -----")

    if args.print_only:
        return 0

    print()
    print("Note: this script renders and validates route inputs. It does not execute external LLM CLIs.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        raise SystemExit(2)
