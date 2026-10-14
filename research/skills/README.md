# Skills Package

This directory packages the repository workflows and prompts into a reusable skill system.

## Included package

- `genealogy-autoresearch` at `skills/genealogy-autoresearch/SKILL.md`
- Route manifest at `routes.json`
- Portable renderer at `scripts/run-route.py`

## How to use

1. Load the main skill file.
2. State your task with a route hint such as `workflow:discrepancy-resolution` or `prompt:11-immigration-search`.
3. Fill placeholder variables before execution (`[SURNAME]`, `[ANCESTOR]`, `[LOCATION]`, `[DATE]`, `[VAULT_PATH]`, `[GEDCOM_PATH]`).
4. Validate routing: `python scripts/check-routes-sync.py`
5. Measure prompt progress: `python scripts/verify-metric.py --route-key <prompt> --vault-path <vault>`
6. Post-run validate: `python scripts/run-validator.py --vault-path <vault> --prior-route-key <route> --write-report`
7. Log session: `python scripts/append-agent-run.py --vault-path <vault> --route-key <route> ...`
8. Post-run finalize: `python scripts/write-pending-agent-run.py ...` then Cursor stop hook or `python scripts/finalize-agent-run.py`
9. Review runs: `python scripts/list-agent-runs.py --vault-path <vault>`

## Purpose

This packaging keeps your workflow logic and prompt logic in one place while preserving the original source files under `workflows/` and `prompts/`.
