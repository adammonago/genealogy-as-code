#!/usr/bin/env python3
"""Validate example agent_run manifests in the repository vault template."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from agent_run_lib import AGENT_RUNS_DIR, collect_manifests, validate_manifest  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate agent_run manifests in a vault.")
    parser.add_argument(
        "--vault-path",
        default=str(REPO_ROOT / "vault-template"),
        help="Vault path to validate (default: vault-template)",
    )
    args = parser.parse_args()

    vault_path = Path(args.vault_path)
    if not vault_path.is_dir():
        print(f"Error: vault path not found: {vault_path}", file=sys.stderr)
        return 2

    entries = collect_manifests(vault_path)
    if not entries:
        print(f"No agent_run manifests found in {vault_path}")
        return 1

    errors: list[str] = []
    for entry in entries:
        run_id = entry.get("run_id", "<unknown>")
        try:
            validate_manifest(entry)
        except ValueError as exc:
            errors.append(f"{run_id}: {exc}")

    runs_dir = vault_path / AGENT_RUNS_DIR
    if runs_dir.is_dir():
        for path in sorted(runs_dir.glob("*.md")):
            if not path.read_text(encoding="utf-8").strip():
                errors.append(f"{path.name}: empty manifest file")

    if errors:
        print("Manifest validation failed:", file=sys.stderr)
        for error in errors:
            print(f"  - {error}", file=sys.stderr)
        return 1

    print(f"Validated {len(entries)} agent_run manifest(s) in {vault_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
