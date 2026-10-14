#!/usr/bin/env python3
"""Build distributable bundles for Claude, Codex, and Gemini targets."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import tarfile
import zipfile
from datetime import datetime, timezone
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
DIST_ROOT = REPO_ROOT / "dist"

TARGETS = ("claude", "codex", "gemini")
CODEX_PLUGIN_NAME = "genealogy-autoresearch"
CLAUDE_PLUGIN_NAME = "genealogy-autoresearch-claude"
COMMON_FILES = [
    "routes.json",
    "run-route",
    "scripts/run-route.py",
    "skills/genealogy-autoresearch/SKILL.md",
    "skills/genealogy-autoresearch/ROUTING_TABLE.md",
    "agents/genealogy-autoresearch-agent.md",
]
COMMON_DIRS = ["prompts", "workflows"]
ADAPTER_FILE_BY_TARGET = {
    "claude": "adapters/claude.md",
    "codex": "adapters/codex.md",
    "gemini": "adapters/gemini.md",
}
SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+$")


def copy_file(relative_path: str, out_root: Path) -> None:
    source = REPO_ROOT / relative_path
    dest = out_root / relative_path
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, dest)


def copy_dir(relative_path: str, out_root: Path) -> None:
    source = REPO_ROOT / relative_path
    dest = out_root / relative_path
    if dest.exists():
        shutil.rmtree(dest)
    shutil.copytree(source, dest)


def sha256_for_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        while True:
            chunk = f.read(1024 * 64)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()


def write_install_doc(target: str, out_root: Path, version: str) -> None:
    title = target.capitalize()
    if target == "codex":
        content = (
            f"# Install {title} Plugin Bundle\n\n"
            f"Version: `{version}`\n\n"
            "## Contents\n\n"
            "- Codex plugin manifest (`.codex-plugin/plugin.json`)\n"
            "- Canonical route manifest (`routes.json`)\n"
            "- Prompts and workflows\n"
            "- Portable route runner (`run-route`, `scripts/run-route.py`)\n"
            f"- Platform adapter (`{ADAPTER_FILE_BY_TARGET[target]}`)\n\n"
            "## Quick start\n\n"
            "1. Extract `codex.zip`.\n"
            f"2. Move `{CODEX_PLUGIN_NAME}/` into `~/plugins/`.\n"
            "3. Register the plugin in `~/.agents/plugins/marketplace.json`.\n"
            "4. Restart Codex if the plugin does not appear immediately.\n\n"
            "## Marketplace entry\n\n"
            "```json\n"
            "{\n"
            f'  "name": "{CODEX_PLUGIN_NAME}",\n'
            '  "source": {\n'
            '    "source": "local",\n'
            f'    "path": "./plugins/{CODEX_PLUGIN_NAME}"\n'
            "  },\n"
            '  "policy": {\n'
            '    "installation": "AVAILABLE",\n'
            '    "authentication": "ON_INSTALL"\n'
            "  },\n"
            '  "category": "Productivity"\n'
            "}\n"
            "```\n\n"
            "## Smoke test\n\n"
            f"```bash\n./run-route --platform {target} --route-key workflow:discrepancy-resolution --vault-path \"/path/to/vault\" --print-only\n```\n"
        )
    elif target == "claude":
        content = (
            f"# Install {title} Plugin Bundle\n\n"
            f"Version: `{version}`\n\n"
            "## Contents\n\n"
            "- Claude friendly plugin archives (`claude.zip`, `claude.plugin`)\n"
            "- Claude plugin manifest (`.claude-plugin/plugin.json`)\n"
            "- Root plugin manifest (`plugin.json`)\n"
            "- Canonical route manifest (`routes.json`)\n"
            "- Prompts and workflows\n"
            "- Portable route runner (`run-route`, `scripts/run-route.py`)\n"
            f"- Platform adapter (`{ADAPTER_FILE_BY_TARGET[target]}`)\n\n"
            "## Quick start\n\n"
            "1. Use `claude.zip` first, fall back to `claude.plugin` if needed.\n"
            "2. Import archive into Claude plugin or extension installer.\n"
            "3. If validation still fails, verify installer manifest requirements against `plugin.json`.\n"
            "4. Open the installed package and run a smoke test.\n\n"
            "## Smoke test\n\n"
            f"```bash\n./run-route --platform {target} --route-key workflow:discrepancy-resolution --vault-path \"/path/to/vault\" --print-only\n```\n"
        )
    else:
        content = (
            f"# Install {title} Bundle\n\n"
            f"Version: `{version}`\n\n"
            "## Contents\n\n"
            "- Canonical route manifest (`routes.json`)\n"
            "- Prompts and workflows\n"
            "- Portable route runner (`run-route`, `scripts/run-route.py`)\n"
            f"- Platform adapter (`{ADAPTER_FILE_BY_TARGET[target]}`)\n\n"
            "## Quick start\n\n"
            "1. Extract the archive.\n"
            "2. Open the extracted folder in your target platform.\n"
            "3. Render a route:\n\n"
            f"```bash\n./run-route --platform {target} --route-key workflow:discrepancy-resolution --vault-path \"/path/to/vault\" --print-only\n```\n\n"
            "4. Paste rendered content into your agent session and execute.\n"
        )
    (out_root / "INSTALL.md").write_text(content, encoding="utf-8")


def write_codex_plugin_manifest(out_root: Path, plugin_version: str) -> None:
    plugin_dir = out_root / ".codex-plugin"
    plugin_dir.mkdir(parents=True, exist_ok=True)
    manifest = {
        "name": CODEX_PLUGIN_NAME,
        "version": plugin_version,
        "description": "Genealogy research routes, prompts, and workflows for Codex.",
        "keywords": ["genealogy", "research"],
        "skills": "./skills/",
        "interface": {
            "displayName": "Genealogy Autoresearch",
            "shortDescription": "Packaged genealogy workflows and prompt routes.",
            "longDescription": "A local Codex plugin that installs genealogy research workflows, prompts, and a routing skill for structured investigation.",
            "developerName": "Local Plugin",
            "category": "Productivity",
            "capabilities": ["Interactive", "Write"],
            "defaultPrompt": [
                "Run the genealogy discrepancy resolution workflow.",
                "Use the document triage workflow on new records.",
                "Route a genealogy question to the right packaged prompt.",
            ],
            "brandColor": "#2F6F4F",
        },
    }
    (plugin_dir / "plugin.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def write_claude_plugin_manifest(out_root: Path, plugin_version: str) -> None:
    # Claude validators typically look for a strict manifest at .claude-plugin/plugin.json.
    plugin_dir = out_root / ".claude-plugin"
    plugin_dir.mkdir(parents=True, exist_ok=True)
    strict_manifest = {
        "name": CLAUDE_PLUGIN_NAME,
        "version": plugin_version,
        "description": "Genealogy workflows and prompts packaged for Claude.",
        "author": "Local Plugin",
    }
    (plugin_dir / "plugin.json").write_text(json.dumps(strict_manifest, indent=2), encoding="utf-8")

    # Also keep root level metadata for installers that inspect root first.
    root_manifest = {
        "name": CLAUDE_PLUGIN_NAME,
        "version": plugin_version,
        "description": strict_manifest["description"],
    }
    (out_root / "plugin.json").write_text(json.dumps(root_manifest, indent=2), encoding="utf-8")


def write_manifest(target: str, out_root: Path, plugin_version: str) -> None:
    files = []
    for p in sorted(out_root.rglob("*")):
        if p.is_file():
            rel = p.relative_to(out_root).as_posix()
            files.append(
                {
                    "path": rel,
                    "size": p.stat().st_size,
                    "sha256": sha256_for_file(p),
                }
            )
    manifest = {
        "target": target,
        "version": plugin_version,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "file_count": len(files),
        "files": files,
    }
    (out_root / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def pack_archive(target: str, build_root: Path, version: str) -> Path:
    archive_name = DIST_ROOT / f"genealogy-agent-{target}-{version}.tar.gz"
    with tarfile.open(archive_name, mode="w:gz") as tar:
        tar.add(build_root, arcname=f"genealogy-agent-{target}-{version}")
    return archive_name


def pack_codex_zip(build_root: Path) -> Path:
    archive_name = DIST_ROOT / "codex.zip"
    if archive_name.exists():
        archive_name.unlink()
    with zipfile.ZipFile(archive_name, mode="w", compression=zipfile.ZIP_DEFLATED) as zf:
        for path in sorted(build_root.rglob("*")):
            if path.is_file():
                arcname = Path(CODEX_PLUGIN_NAME) / path.relative_to(build_root)
                zf.write(path, arcname.as_posix())
    return archive_name


def pack_claude_archives(build_root: Path) -> tuple[Path, Path]:
    zip_archive = DIST_ROOT / "claude.zip"
    plugin_archive = DIST_ROOT / "claude.plugin"
    if zip_archive.exists():
        zip_archive.unlink()
    if plugin_archive.exists():
        plugin_archive.unlink()

    with zipfile.ZipFile(zip_archive, mode="w", compression=zipfile.ZIP_DEFLATED) as zf:
        for path in sorted(build_root.rglob("*")):
            if path.is_file():
                # Keep files at archive root for strict plugin validators.
                arcname = path.relative_to(build_root)
                zf.write(path, arcname.as_posix())

    shutil.copy2(zip_archive, plugin_archive)
    return zip_archive, plugin_archive


def build_target(target: str, version: str, plugin_version: str) -> dict:
    out_root = DIST_ROOT / target
    if out_root.exists():
        shutil.rmtree(out_root)
    out_root.mkdir(parents=True, exist_ok=True)

    for rel in COMMON_FILES:
        copy_file(rel, out_root)
    for rel in COMMON_DIRS:
        copy_dir(rel, out_root)
    copy_file(ADAPTER_FILE_BY_TARGET[target], out_root)
    if target == "codex":
        write_codex_plugin_manifest(out_root, plugin_version)
    if target == "claude":
        write_claude_plugin_manifest(out_root, plugin_version)

    write_install_doc(target, out_root, version)
    write_manifest(target, out_root, plugin_version)
    archive = pack_archive(target, out_root, version)
    result = {"target": target, "archive": archive.name}
    if target == "codex":
        result["plugin_archive"] = pack_codex_zip(out_root).name
    if target == "claude":
        claude_zip, claude_plugin = pack_claude_archives(out_root)
        result["plugin_archive"] = claude_zip.name
        result["plugin_file"] = claude_plugin.name
    return result


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build dist bundles by platform target.")
    parser.add_argument(
        "--target",
        default="all",
        choices=["all", *TARGETS],
        help="Target platform to build",
    )
    parser.add_argument(
        "--version",
        default=datetime.now(timezone.utc).strftime("%Y%m%d"),
        help="Version label in archive names (default: UTC date)",
    )
    parser.add_argument(
        "--plugin-version",
        default="1.0.0",
        help="Semantic version for plugin and manifest files (default: 1.0.0)",
    )
    parser.add_argument(
        "--clean",
        action="store_true",
        help="Delete dist directory before building",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if not SEMVER_RE.match(args.plugin_version):
        raise SystemExit("Error: --plugin-version must use semantic version format, e.g. 1.0.0")
    if args.clean and DIST_ROOT.exists():
        shutil.rmtree(DIST_ROOT)
    DIST_ROOT.mkdir(parents=True, exist_ok=True)

    targets = TARGETS if args.target == "all" else (args.target,)
    results = [build_target(target, args.version, args.plugin_version) for target in targets]
    summary = {
        "version": args.version,
        "plugin_version": args.plugin_version,
        "targets": results,
    }
    (DIST_ROOT / "build-summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
