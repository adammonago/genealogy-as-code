---
name: genealogy-autoresearch
description: "Orchestrate genealogy research workflows and prompts. Triggers include: run genealogy research, expand my tree, find ancestor records, resolve discrepancy, OCR this document, and family history vault workflows."
---

# Genealogy Autoresearch Skill

Orchestrate genealogy research by routing requests to the existing workflow and prompt library in this repository.

## Scope

This skill does not replace source documents. It is a routing and execution contract over the files in `workflows/` and `prompts/`.

## Inputs

- `route_key`: One key from `ROUTING_TABLE.md`
- `vault_path`: Usually your notes root (or `VAULT_PATH` from `.env.local`)
- Optional placeholders used by prompts: `[SURNAME]`, `[ANCESTOR]`, `[LOCATION]`, `[DATE]`, `[GEDCOM_PATH]`
- Optional mode: `workflow` or `prompt`
- Optional external OKF context: `OKF_BUNDLE_PATH` and `OKF_TOWN` from `.env.local` or from `Data_Inventory.md` in the vault

## Required behavior

1. Read `ROUTING_TABLE.md`.
2. When `OKF_BUNDLE_PATH` and `OKF_TOWN` are both set, read `{OKF_BUNDLE_PATH}/{OKF_TOWN}/index.md` as read-only community context before executing the route. Do not treat corpus prose as vault evidence; cite vault sources for family conclusions. Follow this toolkit's `corpus/` conventions and `reference/hkf-consumer.md` (do not invent `verified`; do not silently merge unresolved identities).
3. Resolve `route_key` to a concrete file under `workflows/` or `prompts/`.
4. Read and execute that source file exactly, replacing placeholders only when values are provided.
5. Apply repository conventions from `CLAUDE.md` and `AUTHORING_GUIDELINES.md`.
6. Enforce source first claims and confidence tiers.
7. Log negative results when no evidence is found.

## Execution policy

- If task ambiguity is high, start with `workflow:phase-planning`.
- If records are raw or unprocessed, run `workflow:document-triage` before research prompts.
- If facts conflict, route to `workflow:discrepancy-resolution` before expanding claims.
- If the task already has a tight event + place + year target, prefer `workflow:civil-record-browse-planning` before broad web prompts.
- If the task is really an identity collision or spouse-cluster problem, prefer `workflow:identity-bridge-resolution`.
- If the task is a Hebrew or Yiddish tombstone photo, route to `prompt:13-hebrew-headstone` instead of generic OCR.
- If the correct source is known but blocked, route to `workflow:interactive-handoff`.
- For autonomous loops, use one prompt route at a time and verify before switching.

## Orchestrator policy

After resolving a `route_key`, read its graph edges in `routes.json`:

1. **Before starting**: Check whether another route's `reroute_triggers` better matches the task shape (identity, browse, handoff, tombstone).
2. **During execution**: When a `reroute_conditions` key fires, exit the current route, log source and target `route_key` in `Research_Log.md`, and run the target route. Do not continue the wrong protocol or burn remaining iterations.
3. **After a successful run**: Recommend the first applicable route from the current route's `follow_up` list. Prefer default chains in `ROUTING_TABLE.md` when the vault state matches.
4. **After handoff**: `workflow:interactive-handoff` sets `return_route` on the handoff packet; resume there after manual work completes.
5. **On metric plateau**: Prompt routes with a `metric_plateau` trigger should stop and recommend `workflow:phase-planning`.
6. **After canonical vault changes**: When the completed route is listed in `routes.json` → `validator_recommended_after`, recommend `workflow:validator-pass` before the route's other `follow_up` entries.

The orchestrator hat (see `agents/genealogy-autoresearch-agent.md`) owns route selection and follow-up recommendation; the research executor hat owns vault writes per route contract; the validator hat owns post-run checks only.

## Output contract

- Use standard Markdown links only.
- Never use wiki links.
- Include `.md` in local links.
- Separate evidence, interpretation, and open questions.
- Propagate confirmed corrections to shared canonical files (`Family_Tree.md`, `Timeline.md`, `Research_Log.md`, `Open_Questions.md`) when the selected route requires it.
- After every agent run, write a pending manifest and finalize per [reference/post-run-hooks.md](../../reference/post-run-hooks.md) (appends `agent_run` to `Research_Log.md`).

## Quick examples

- `route_key=workflow:discrepancy-resolution` with `ancestor=...`
- `route_key=prompt:11-immigration-search` with `location=...` and `date=...`
- `route_key=prompt:13-hebrew-headstone` with `ancestor=...` and headstone image(s)

## Source index

- Routing map: `skills/genealogy-autoresearch/ROUTING_TABLE.md`
- Workflows: `workflows/`
- Prompts: `prompts/`
