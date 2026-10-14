#!/usr/bin/env python3
"""Finalize a genealogy agent run: optional validator, append manifest, clear pending."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from agent_run_lib import collect_manifests, render_manifest_block, validate_manifest  # noqa: E402
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


def load_manifest_from_args(args: argparse.Namespace) -> dict | None:
    if args.pending:
        pending_path = Path(args.pending)
        if not pending_path.is_file():
            return None
        data = json.loads(pending_path.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            raise ValueError("Pending manifest JSON must be an object.")
        return data

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

    if not args.route_key:
        return None

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


def manifest_exists(vault_path: Path, run_id: str) -> bool:
    for entry in collect_manifests(vault_path):
        if entry.get("run_id") == run_id:
            return True
    return False


def run_validator(vault_path: Path, prior_route_key: str, write_report: bool) -> tuple[str, int]:
    cmd = [
        sys.executable,
        str(REPO_ROOT / "scripts/run-validator.py"),
        "--vault-path",
        str(vault_path),
        "--prior-route-key",
        prior_route_key,
    ]
    if write_report:
        cmd.append("--write-report")
    cmd.append("--json")

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode == 2:
        raise RuntimeError(result.stderr.strip() or "Validator could not run.")
    if result.returncode == 1:
        return "FAIL", 1
    return "PASS", 0


def run_append(vault_path: Path, manifest: dict, standalone: bool, dry_run: bool) -> subprocess.CompletedProcess:
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8") as handle:
        json.dump(manifest, handle, indent=2)
        temp_path = handle.name

    cmd = [
        sys.executable,
        str(REPO_ROOT / "scripts/append-agent-run.py"),
        "--vault-path",
        str(vault_path),
        "--manifest",
        temp_path,
    ]
    if standalone:
        cmd.append("--standalone")
    if dry_run:
        cmd.append("--dry-run")

    try:
        return subprocess.run(cmd, capture_output=True, text=True)
    finally:
        Path(temp_path).unlink(missing_ok=True)


def clear_pending(pending_path: Path) -> None:
    if pending_path.is_file():
        pending_path.unlink()


def add_finalize_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--pending",
        default=str(DEFAULT_PENDING),
        help="Pending manifest path (default: .cursor/pending-agent-run.json)",
    )
    parser.add_argument("--manifest", help="Manifest JSON file (skip pending file)")
    parser.add_argument("--stdin", action="store_true", help="Read manifest JSON from stdin")
    parser.add_argument("--vault-path")
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
    parser.add_argument("--vault-files-changed")
    parser.add_argument("--negative-results-logged", type=int, default=0)
    parser.add_argument("--handoffs-created")
    parser.add_argument("--reroutes-triggered")
    parser.add_argument("--validator-result", default="N/A")
    parser.add_argument("--validator-report-path")
    parser.add_argument("--confidence-notes")
    parser.add_argument(
        "--run-validator",
        action="store_true",
        help="Run run-validator.py before append (also honored from pending JSON)",
    )
    parser.add_argument(
        "--skip-validator",
        action="store_true",
        help="Do not run validator even when pending JSON requests it",
    )
    parser.add_argument("--standalone", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument(
        "--keep-pending",
        action="store_true",
        help="Do not delete pending manifest after success",
    )
    parser.add_argument("--json", action="store_true", help="Emit result JSON on stdout")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Finalize an agent run: optional validator, append manifest, clear pending."
    )
    add_finalize_args(parser)
    args = parser.parse_args()

    pending_path = Path(args.pending)
    used_pending_file = bool(args.pending and pending_path.is_file() and not args.manifest and not args.stdin and not args.route_key)

    try:
        data = load_manifest_from_args(args)
        if data is None:
            if args.json:
                print(json.dumps({"status": "skipped", "reason": "no_pending_manifest"}))
            return 0

        vault_path_value = resolve_vault_path(REPO_ROOT, data)
        if not vault_path_value:
            raise ValueError(
                "Missing vault_path. Pass --vault-path or set VAULT_PATH in .env.local."
            )
        vault_path = Path(vault_path_value)
        if not vault_path.is_dir():
            raise ValueError(f"Vault path not found: {vault_path}")

        validate_manifest(data)

        run_validator_flag = bool(data.pop("run_validator", False) or args.run_validator)
        if args.skip_validator:
            run_validator_flag = False
        standalone = bool(data.pop("standalone", False) or args.standalone)
        data.pop("vault_path", None)

        prior_route_key = data.get("prior_route_key") or data.get("route_key")
        validator_exit = 0
        if run_validator_flag and prior_route_key:
            validator_result, validator_exit = run_validator(
                vault_path, prior_route_key, write_report=not args.dry_run
            )
            data["validator_result"] = validator_result
            if not args.dry_run:
                data["validator_report_path"] = "validator_report.md"

        render_manifest_block(data)
        run_id = data["run_id"]
        if not args.dry_run and manifest_exists(vault_path, run_id):
            result = {
                "status": "skipped",
                "reason": "manifest_already_logged",
                "run_id": run_id,
                "vault_path": str(vault_path),
            }
            if used_pending_file and not args.keep_pending:
                clear_pending(pending_path)
            if args.json:
                print(json.dumps(result, indent=2))
            else:
                print(f"Manifest already logged for run_id {run_id}; skipped append.")
            return 0

        append_result = run_append(vault_path, data, standalone=standalone, dry_run=args.dry_run)
        if append_result.returncode != 0:
            message = append_result.stderr.strip() or append_result.stdout.strip() or "append failed"
            raise RuntimeError(message)

        if used_pending_file and not args.dry_run and not args.keep_pending:
            clear_pending(pending_path)

        result = {
            "status": "ok",
            "run_id": run_id,
            "vault_path": str(vault_path),
            "validator_result": data.get("validator_result", "N/A"),
            "validator_exit_code": validator_exit,
            "standalone": standalone,
            "dry_run": args.dry_run,
        }
        if args.json:
            print(json.dumps(result, indent=2))
        else:
            print(append_result.stdout.strip())
            if run_validator_flag:
                print(f"validator_result: {data.get('validator_result', 'N/A')}")
        return 0

    except (ValueError, json.JSONDecodeError, RuntimeError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        if args.json:
            print(json.dumps({"status": "error", "message": str(exc)}))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
