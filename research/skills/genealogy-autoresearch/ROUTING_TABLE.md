# Genealogy Autoresearch Routing Table

Use this table to choose the right workflow or prompt. Route graph edges (`follow_up`, `reroute_triggers`) are defined in [routes.json](../../routes.json) schema version 1.2.

## Workflow routes

| Route key | Use when | Source |
|---|---|---|
| `workflow:getting-started` | You are setting up a fresh vault and process | `workflows/getting-started.md` |
| `workflow:ocr-pipeline` | You need OCR extraction from scans or photos | `workflows/ocr-pipeline.md` |
| `workflow:new-ancestor-intake` | You discovered a new person and need normalization | `workflows/new-ancestor-intake.md` |
| `workflow:document-triage` | You must classify incoming records before processing | `workflows/document-triage.md` |
| `workflow:oral-history-protocol` | You are collecting interview evidence | `workflows/oral-history-protocol.md` |
| `workflow:discrepancy-resolution` | Sources conflict on dates, names, places, or relationships | `workflows/discrepancy-resolution.md` |
| `workflow:civil-record-browse-planning` | You already have a narrow event / place / year target and need an image-level browse plan | `workflows/civil-record-browse-planning.md` |
| `workflow:identity-bridge-resolution` | The real problem is same-name collision, alias drift, spouse split, or household sorting | `workflows/identity-bridge-resolution.md` |
| `workflow:phase-planning` | You need to pick the next research phase | `workflows/phase-planning.md` |
| `workflow:interactive-handoff` | The right source is known but blocked; produce a structured manual handoff packet | `workflows/interactive-handoff.md` |
| `workflow:validator-pass` | Post-run quality gate after canonical vault changes | `workflows/validator-pass.md` |

## Prompt routes

| Route key | Use when | Source |
|---|---|---|
| `prompt:01-tree-expansion` | Expand all branches from current known ancestors | `prompts/01-tree-expansion.md` |
| `prompt:02-cross-reference-audit` | Detect and resolve source conflicts at scale | `prompts/02-cross-reference-audit.md` |
| `prompt:03-findagrave-sweep` | Find and extract memorial evidence | `prompts/03-findagrave-sweep.md` |
| `prompt:04-gedcom-completeness` | Validate and fill GEDCOM coverage | `prompts/04-gedcom-completeness.md` |
| `prompt:05-source-citation-audit` | Improve citation density and quality | `prompts/05-source-citation-audit.md` |
| `prompt:06-unresolved-persons` | Identify unnamed or ambiguous people | `prompts/06-unresolved-persons.md` |
| `prompt:07-timeline-gap-analysis` | Find record gaps in a person timeline | `prompts/07-timeline-gap-analysis.md` |
| `prompt:08-open-question-resolution` | Work down explicit unresolved questions | `prompts/08-open-question-resolution.md` |
| `prompt:09-bygdebok-extraction` | Extract evidence from local history books | `prompts/09-bygdebok-extraction.md` |
| `prompt:10-colonial-records-search` | Search pre 1800 colonial sources | `prompts/10-colonial-records-search.md` |
| `prompt:11-immigration-search` | Find manifests and naturalization records | `prompts/11-immigration-search.md` |
| `prompt:12-dna-chromosome-analysis` | Map DNA segments to genealogy hypotheses | `prompts/12-dna-chromosome-analysis.md` |
| `prompt:13-hebrew-headstone` | Transcribe and translate Hebrew or Yiddish tombstone inscriptions | `prompts/13-hebrew-headstone.md` |

## Default chains

Recommended sequential routes after a successful run. Skip steps that do not apply to your vault state.

| After this route | Consider these follow-ups (in order) |
|---|---|
| `workflow:getting-started` | `workflow:phase-planning` → `workflow:document-triage` |
| `workflow:document-triage` | `workflow:ocr-pipeline` → `workflow:new-ancestor-intake` |
| `workflow:ocr-pipeline` | `workflow:new-ancestor-intake` |
| `workflow:new-ancestor-intake` | `prompt:02-cross-reference-audit` → `prompt:05-source-citation-audit` |
| `prompt:01-tree-expansion` | `workflow:validator-pass` → `prompt:02-cross-reference-audit` → `prompt:05-source-citation-audit` |
| `prompt:03-findagrave-sweep` | `workflow:validator-pass` → `prompt:05-source-citation-audit` → `prompt:02-cross-reference-audit` |
| `prompt:11-immigration-search` | `prompt:07-timeline-gap-analysis` → `prompt:02-cross-reference-audit` |
| `prompt:13-hebrew-headstone` | `workflow:validator-pass` → `prompt:02-cross-reference-audit` → `workflow:discrepancy-resolution` |
| `prompt:08-open-question-resolution` | `workflow:validator-pass` → `workflow:phase-planning` |
| `workflow:new-ancestor-intake` | `workflow:validator-pass` → `prompt:02-cross-reference-audit` |
| `workflow:civil-record-browse-planning` | `prompt:08-open-question-resolution` |
| `workflow:identity-bridge-resolution` | `workflow:civil-record-browse-planning` → `prompt:08-open-question-resolution` |
| `workflow:interactive-handoff` | Re-run `return_route` from the handoff packet after manual work |

## Reroute triggers

When a condition fires during a run, exit the current route and switch to the target. Log the switch in `Research_Log.md`. Condition definitions live in `routes.json` under `reroute_conditions`.

| Condition | Meaning | Typical target |
|---|---|---|
| `identity_collision` | Same-name, alias, spouse, or household problem | `workflow:identity-bridge-resolution` |
| `interactive_wall` | Source known but login, subscription, or browse blocked | `workflow:interactive-handoff` |
| `narrow_browse` | Tight event + place + year; needs register browse | `workflow:civil-record-browse-planning` |
| `metric_plateau` | Autoresearch metric unchanged for 2 iterations | `workflow:phase-planning` |
| `hebrew_headstone` | Hebrew or Yiddish tombstone inscription | `prompt:13-hebrew-headstone` |
| `source_conflict` | Sources disagree on a fact | `workflow:discrepancy-resolution` |
| `raw_documents` | Unprocessed scans awaiting triage or OCR | `workflow:ocr-pipeline` |

Per-route trigger lists are in `routes.json` on each route's `reroute_triggers` field.

## Validator pass

After routes listed in `routes.json` → `validator_recommended_after`, run `workflow:validator-pass` before trusting canonical changes:

`python scripts/run-validator.py --vault-path <vault> --prior-route-key <route> --write-report`

Blocking findings require a corrective route before further propagation.
