# Validator Pass

Post-run quality gate for vault changes. Read-only on canonical facts: flag problems, write a validator report, recommend corrective routes. Do not fix tree facts during validation unless explicitly asked to re-run a correction route.

## When to Use This Workflow

Run after any route that may have modified canonical vault files, especially:

- `prompt:01-tree-expansion`
- `prompt:03-findagrave-sweep`
- `prompt:08-open-question-resolution`
- `prompt:13-hebrew-headstone`
- `workflow:new-ancestor-intake`

Also run when an agent run summary lists vault file changes to `Family_Tree.md`, person files, or `Open_Questions.md`.

## Validator Hat

Switch to the **Validator** hat (see `agents/genealogy-autoresearch-agent.md`). Validators may write `validator_report.md` only. They do not add ancestors, resolve questions, or merge identities.

## Step 1: Record Context

Capture:

- `prior_route_key`: the route that just finished
- `vault_files_changed`: from the prior run summary, if available
- Timestamp

## Step 2: Run Mechanical Checks

From the repository root, run:

```bash
python scripts/run-validator.py --vault-path "[VAULT_PATH]" --prior-route-key [prior_route_key] --write-report
```

Optional JSON for automation:

```bash
python scripts/run-validator.py --vault-path "[VAULT_PATH]" --prior-route-key [prior_route_key] --json
```

The script checks:

| Check | Severity | Meaning |
|---|---|---|
| `wiki_links` | blocking | Obsidian wiki links (`[[...]]`) in vault markdown |
| `resolved_without_source` | blocking | Open question marked RESOLVED without citation signals |
| `high_confidence_under_sourced` | blocking | Person file `confidence: high` with fewer than two sources |
| `unverified_tree_entries` | warning | `(unverified)` markers in `Family_Tree.md` |
| `moderate_confidence_under_sourced` | warning | Person file `confidence: moderate` with fewer than two sources |
| `missing_core_files` | warning | Expected vault files absent |

Exit codes:

- `0`: pass (warnings allowed)
- `1`: blocking issues found; corrective route required before trusting changes
- `2`: validator could not run (missing vault, script error)

## Step 3: Review Findings

Read `[VAULT_PATH]/validator_report.md` (created when using `--write-report`) or the script output.

Classify each finding:

- **Blocking**: stop propagation; run a corrective route before continuing research
- **Warning**: acceptable if intentional; document in Research_Log if kept

## Step 4: Recommend Corrective Routes

| Finding type | Recommended route |
|---|---|
| Source conflicts, mismatched dates/names | `workflow:discrepancy-resolution` or `prompt:02-cross-reference-audit` |
| Same-name or merge risk | `workflow:identity-bridge-resolution` |
| Under-sourced persons | `prompt:05-source-citation-audit` |
| Unverified tree additions | Keep marked; run `prompt:02-cross-reference-audit` |
| RESOLVED without Strong Signal | Reopen question; run `workflow:discrepancy-resolution` |

## Step 5: Log and Summarize

1. Append a structured manifest with `scripts/append-agent-run.py` (see [reference/agent-run-manifest.md](../reference/agent-run-manifest.md)).
2. Note validator outcome in the manifest when `--prior-route-key` applies.
3. Set `recommended_next_route` to the first corrective route if blocking issues exist; otherwise the prior route's next `follow_up`.
4. End with the mandatory Run Summary. Set `hat_at_close: validator`.

## Required Output Checklist

1. Mechanical check command executed (or documented why not)
2. `validator_report.md` updated when `--write-report` used
3. Research_Log entry
4. Corrective route recommendation when blocking issues exist
5. Mandatory Run Summary
