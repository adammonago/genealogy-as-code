# Distribution Pipeline

Build installable bundles for Claude, Codex, and Gemini from one shared backend.

## Commands

Build all targets:

```bash
./build-dist --clean --version v1
```

Build a single target:

```bash
./build-dist --target claude --version v1
```

## Outputs

Artifacts are generated under `dist/`:

- `dist/claude/`, `dist/codex/`, `dist/gemini/` working trees
- `dist/genealogy-agent-<target>-<version>.tar.gz` archives
- `dist/codex.zip` installable Codex plugin archive
- `dist/build-summary.json`

Each target folder includes:

- `INSTALL.md`
- `manifest.json` with SHA256 for every file
- canonical `prompts/` and `workflows/`
- route tooling (`routes.json`, `run-route`, `scripts/run-route.py`)
- target specific adapter doc

The Codex target also includes:

- `.codex-plugin/plugin.json`
- an archive root named `genealogy-autoresearch/` inside `dist/codex.zip`

## Install on target platform

1. Copy or extract the target archive.
1. Open extracted folder with your platform CLI.
1. Render and validate route content:

```bash
./run-route --platform <target> --route-key workflow:discrepancy-resolution --vault-path "/path/to/vault" --print-only
```

1. Paste rendered content into platform agent.

## Codex plugin install

`dist/codex.zip` is built as a real Codex plugin bundle. After extracting it:

1. Move `genealogy-autoresearch/` into `~/plugins/`
1. Add a marketplace entry in `~/.agents/plugins/marketplace.json`
1. Restart Codex if needed
