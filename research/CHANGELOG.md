# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased]

### Agent Run Manifest (Tier 3: Observability)

- Added [reference/agent-run-manifest.md](reference/agent-run-manifest.md) schema for structured session logging.
- Added [vault-template/templates/agent-run-manifest.md](vault-template/templates/agent-run-manifest.md) and example entry in [Research_Log.md](vault-template/Research_Log.md).
- Added [scripts/append-agent-run.py](scripts/append-agent-run.py) to append manifests from JSON or CLI flags.
- Added [scripts/list-agent-runs.py](scripts/list-agent-runs.py) and [scripts/validate-agent-run-manifests.py](scripts/validate-agent-run-manifests.py) for manifest query and CI validation.
- Added [scripts/agent_run_lib.py](scripts/agent_run_lib.py) shared parsing and rendering helpers.
- `append-agent-run.py --standalone` writes full manifests to `agent_runs/{run_id}.md` with index pointers in Research_Log.
- Post-run hooks: [reference/post-run-hooks.md](reference/post-run-hooks.md), [scripts/write-pending-agent-run.py](scripts/write-pending-agent-run.py), [scripts/finalize-agent-run.py](scripts/finalize-agent-run.py), [.cursor/hooks.json](.cursor/hooks.json).
- Updated agent spec and SKILL to require manifest append after Run Summary.

### Agent Orchestration (Tier 3: Validator)

- Added [workflows/validator-pass.md](workflows/validator-pass.md) post-run quality gate workflow.
- Added [scripts/run-validator.py](scripts/run-validator.py) with blocking and warning checks for wiki links, under-sourced persons, unverified tree entries, and RESOLVED questions without citations.
- Added [vault-template/templates/validator-report.md](vault-template/templates/validator-report.md).
- Extended [routes.json](routes.json) to schema 1.2 with `validator_recommended_after` and `workflow:validator-pass` route graph edges.

### Agent Orchestration (PR 5)

- Added [scripts/check-routes-sync.py](scripts/check-routes-sync.py) to validate `routes.json` against `ROUTING_TABLE.md`, source files, and graph edges.
- Added [scripts/verify-metric.py](scripts/verify-metric.py) for executable Verify checks on prompts `01`, `02`, and `08`.
- Updated [vault-template/Open_Questions.md](vault-template/Open_Questions.md) with explicit Status field convention.
- Updated Verify clauses in prompts `01`, `02`, and `08` to use the metric script.
- Updated [DOGFOODING_CHECKLIST.md](DOGFOODING_CHECKLIST.md) and [genealogy-autoresearch-agent.md](agents/genealogy-autoresearch-agent.md) with verify workflow.

### Agent Orchestration (PR 4)

- Extended [routes.json](routes.json) to schema 1.1 with `reroute_conditions`, per-route `follow_up`, and `reroute_triggers`.
- Added [workflows/interactive-handoff.md](workflows/interactive-handoff.md) for structured manual handoff production.
- Updated [ROUTING_TABLE.md](skills/genealogy-autoresearch/ROUTING_TABLE.md) with default chains and reroute trigger tables.
- Added orchestrator policy to [SKILL.md](skills/genealogy-autoresearch/SKILL.md) and route graph guidance to [genealogy-autoresearch-agent.md](agents/genealogy-autoresearch-agent.md).
- [run-route.py](scripts/run-route.py) now prints follow-up and reroute edges when rendering a route.

### Agent Orchestration (PR 3)

- Added [prompts/13-hebrew-headstone.md](prompts/13-hebrew-headstone.md) as the canonical route wrapper for Hebrew/Yiddish tombstone extraction (H3 v8.1 core).
- Registered `prompt:13-hebrew-headstone` in [routes.json](routes.json) and [ROUTING_TABLE.md](skills/genealogy-autoresearch/ROUTING_TABLE.md).
- Updated [SKILL.md](skills/genealogy-autoresearch/SKILL.md), [workflows/ocr-pipeline.md](workflows/ocr-pipeline.md), [workflows/document-triage.md](workflows/document-triage.md), and [prompts/03-findagrave-sweep.md](prompts/03-findagrave-sweep.md) to route tombstones through the new prompt.

### Agent Orchestration (PR 2)

- Replaced duplicated Output Mode sections in all 12 prompts with shared contract references.
- Added reroute and handoff guardrails to every prompt; browse-first and identity-bridge exits now log and stop the loop.
- Updated prompts `07`, `08`, and `11` to create handoff files from `[VAULT_PATH]/templates/handoff-packet.md`.
- Updated [workflows/civil-record-browse-planning.md](workflows/civil-record-browse-planning.md) to use the handoff template.
- Updated [prompts/README.md](prompts/README.md) to document shared contracts and handoff behavior.

### Agent Orchestration (PR 1)

- Added [prompts/_shared-output-contract.md](prompts/_shared-output-contract.md) as the canonical output contract for all routes.
- Added [prompts/_shared-iteration-stop-rules.md](prompts/_shared-iteration-stop-rules.md) for shared autoresearch loop stop conditions.
- Added [vault-template/templates/handoff-packet.md](vault-template/templates/handoff-packet.md) for structured AI-to-human research handoffs.
- Expanded [agents/genealogy-autoresearch-agent.md](agents/genealogy-autoresearch-agent.md) with role hats, autonomy matrix, mandatory run summary, and failure modes.
- Updated [AUTHORING_GUIDELINES.md](AUTHORING_GUIDELINES.md) to reference shared contracts instead of duplicating Output Mode text.

## [0.2.0] - 2026-05-26

### Workflows

- Added `workflow:civil-record-browse-planning` for narrow date/place/event targets that should be handled as image-level register browsing rather than generic web search.
- Added `workflow:identity-bridge-resolution` for same-name collisions, alias-heavy lines, spouse splits, and household-structure problems.
- Updated `workflows/phase-planning.md` with route-selection heuristics for browse-first and identity-bridge cases.

### Prompt Improvements

- Updated `prompt:07-timeline-gap-analysis` to distinguish browse-first, search-first, and interactive-handoff gap work.
- Updated `prompt:08-open-question-resolution` to reroute identity-bridge and narrow browse questions instead of forcing generic web search.
- Updated `prompt:11-immigration-search` to require explicit interactive handoff packets when the right collection is known but direct retrieval is blocked.

### Routing

- Added the new workflows to `skills/genealogy-autoresearch/ROUTING_TABLE.md`.
- Updated `skills/genealogy-autoresearch/SKILL.md` execution policy so the agent prefers browse-planning and identity-bridge routes when appropriate.
- Added the new workflow routes to `routes.json`.

### Private Dogfooding

- Added `DOGFOODING_CHECKLIST.md` for private-use readiness before any public release.
- Added `RESEARCH_TOOLS_TODO.md` to track the technology backlog separately from genealogy-data research plans.
- Normalized `CLAUDE.md` and `AGENTS.md` so they no longer hardcode a machine-local vault path.
- Added a repo-native DNA cluster intake template under `vault-template/templates/`.
- Updated onboarding and prompt guidance so users choose planning, browse, or identity workflows before defaulting to tree expansion when appropriate.
- Expanded Polish guidance in `archives/poland.md` and `reference/naming-conventions.md` with variant-handling rules informed by real Polish-record workflows.

## [0.1.0] - 2026-04-26

### Base

- Forked from `mattprusak/autoresearch-genealogy` (MIT licensed).
- Upstream baseline includes initial release content, global archive guides, and expanded README structure.

### Repository Packaging and Governance

- Added `NOTICE` to document provenance and derivative work attribution.
- Added `THIRD_PARTY_LICENSES.md` to track external code and license obligations.
- Added `RELEASE_CHECKLIST.md` for repeatable pre-release validation.
- Updated `README.md` with provenance and release-governance references.

### Notes

- This release focuses on publication hygiene and attribution structure.
- Future entries should capture substantive prompt, workflow, and template changes.
