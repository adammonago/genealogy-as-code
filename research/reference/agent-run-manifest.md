# Agent Run Manifest

Structured observability record for every genealogy autoresearch agent session. Manifests complement free-form search logs in `Research_Log.md` by capturing route, metric, hat, and follow-up data in a consistent shape.

## Purpose

- Audit what an agent run changed and why
- Chain runs across reroutes, handoffs, and validator passes
- Feed dogfooding review without parsing chat transcripts

## Entry type

Every manifest uses:

```yaml
type: agent_run
```

Store manifests inline in `[VAULT_PATH]/Research_Log.md` (recommended) or as standalone files under `[VAULT_PATH]/agent_runs/` when you want one file per session.

## Required fields

| Field | Type | Description |
|---|---|---|
| `type` | string | Always `agent_run` |
| `run_id` | string | Unique id: `{ISO8601 compact}-{route_key slug}` |
| `created` | ISO 8601 datetime | When the run finished |
| `route_key` | string | Route executed |
| `hat_at_close` | enum | `orchestrator`, `research_executor`, `human_bridge`, `validator` |
| `recommended_next_route` | string | Next route from graph or orchestrator |

## Recommended fields

| Field | Type | Description |
|---|---|---|
| `prior_route_key` | string | Source route for validator or reroute chains |
| `iterations_completed` | number | Prompt iterations finished |
| `iterations_planned` | number | Prompt iteration budget |
| `metric_name` | string | Verify metric label |
| `metric_before` | number | Metric at loop start |
| `metric_after` | number | Metric at loop end |
| `metric_delta` | number | Signed change |
| `vault_files_changed` | list | Paths touched |
| `negative_results_logged` | number | Negative search count |
| `handoffs_created` | list | Handoff file paths |
| `reroutes_triggered` | list | `{condition, from, to}` objects |
| `validator_result` | enum | `PASS`, `FAIL`, `N/A` |
| `validator_report_path` | string | Path when validator ran |
| `confidence_notes` | string | Free text summary |
| `platform` | string | `claude`, `codex`, `cursor`, `gemini`, `generic` |

## Relationship to Run Summary

The mandatory Run Summary in chat (see `agents/genealogy-autoresearch-agent.md`) is the human-facing footer. The manifest is the durable vault record with the same fields plus `run_id` and `created`.

Every agent run must:

1. Emit Run Summary in the session output
2. Append a matching manifest to `Research_Log.md`

Use `scripts/append-agent-run.py` to append from JSON or flags.

### Inline vs standalone storage

| Mode | Flag | Research_Log entry | Full manifest |
|---|---|---|---|
| Inline (default) | none | Full YAML block | Same file |
| Standalone | `--standalone` | Compact `agent_run_index` pointer | `[VAULT_PATH]/agent_runs/{run_id}.md` |

Use standalone when a run produces long notes or many vault file references.

### Query and validate

- `scripts/list-agent-runs.py --vault-path [VAULT_PATH]` lists manifests from inline blocks and `agent_runs/`
- `scripts/validate-agent-run-manifests.py` checks required fields on example manifests (CI friendly)

## Example JSON payload

```json
{
  "route_key": "prompt:01-tree-expansion",
  "hat_at_close": "research_executor",
  "iterations_completed": 5,
  "iterations_planned": 8,
  "metric_name": "named_individuals_in_family_tree",
  "metric_before": 42,
  "metric_after": 47,
  "metric_delta": 5,
  "vault_files_changed": ["Family_Tree.md", "people/Example_Person.md"],
  "negative_results_logged": 3,
  "handoffs_created": [],
  "reroutes_triggered": [],
  "recommended_next_route": "workflow:validator-pass",
  "validator_result": "N/A",
  "confidence_notes": "Five new ancestors added; all marked (unverified) pending audit.",
  "platform": "cursor"
}
```

## Chaining runs

| Scenario | Set `prior_route_key` | Set `reroutes_triggered` |
|---|---|---|
| Normal prompt run | omit | `[]` |
| Validator after tree expansion | `prompt:01-tree-expansion` | omit |
| Reroute mid-loop | prior route | `[{condition, from, to}]` |
| Handoff only | source route | optional |

## Template

Copy from [vault-template/templates/agent-run-manifest.md](../vault-template/templates/agent-run-manifest.md).
