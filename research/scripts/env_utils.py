"""Load repository local environment values."""

from __future__ import annotations

from pathlib import Path


def read_env_local(repo_root: Path) -> dict[str, str]:
    env_path = repo_root / ".env.local"
    if not env_path.is_file():
        return {}

    values: dict[str, str] = {}
    for raw_line in env_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key:
            values[key] = value
    return values


def resolve_vault_path(repo_root: Path, manifest: dict) -> str | None:
    vault_path = manifest.get("vault_path")
    if vault_path:
        return str(vault_path)
    return read_env_local(repo_root).get("VAULT_PATH")
