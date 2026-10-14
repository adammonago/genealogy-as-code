# Research Tools TODO

Technology backlog for the research-tooling side of this system.

This is separate from genealogy research plans such as `Research_Strategy.md`.
That plan answers: "What family-history questions should we work next?"

This note answers: "What technology should we build or improve so the research system itself gets stronger?"

## Purpose

Use this file to track:

- workflow gaps discovered during real research
- prompt and routing improvements
- country- or record-type-specific helper logic
- packaging and dogfooding needs
- automation ideas that would materially improve research throughput or reliability

## Prioritization Rules

Prioritize tooling work that does at least one of these:

- prevents repeated hallucination or over-merge risk
- turns repeated manual rescue into a reusable workflow
- improves image-browse or archive handoff quality
- strengthens country-specific record handling
- makes private dogfooding easier and safer

## Current High-Priority TODO

### 1. DNA Match Triage Workflow

**Why**:
- The repo has DNA interpretation guardrails and chromosome-painting guidance, but not a reusable workflow for deciding which DNA matches deserve follow-up first.

**Add**:
- A workflow such as `workflow:dna-match-triage`
- A prioritization rubric covering:
  - shared cM / segment size
  - number of large segments versus many tiny segments
  - shared-match cluster quality
  - tree quality and surname/locality overlap
  - endogamy inflation risk
  - platform context (`Ancestry`, `GEDmatch`, `FTDNA`, `MyHeritage`, `23andMe`)
  - responsiveness / outreach value

**Output should include**:
- follow-up now
- follow-up later
- archive only
- insufficient evidence

### 2. Memorial Packet Extraction Workflow

**Why**:
- Holocaust memorial stones, Yad Vashem result bundles, and similar packets need literal extraction plus cautious genealogical interpretation.

**Add**:
- A workflow for line-by-line memorial extraction
- Structured handling for uncertainty, titles, kinship phrases, and person-mapping decisions

### 3. Country-Specific Matching Aids

**Why**:
- Polish matching rules are now better represented in documentation, but similar high-value helper rules may be needed for other branches.

**Done**:
- Jewish Galicia town-name and partition-language variant aid — `archives/galicia-jewish.md` (2026-06-14); cross-links in `archives/poland.md` and `archives/jewish-genealogy.md`; OKF bundle loading via `OKF_BUNDLE_PATH` / `OKF_TOWN` (Phase 1)
- HKF consumer guidance — `reference/hkf-consumer.md` (2026-08-11); aligns agents with genealogy-as-code `HKF-SPEC.md` evidence/claim/identity/interpretation model

**Add next**:
- Italian civil-register browse heuristics by archive / commune pattern
- stronger immigration-name variant guidance by region
- Optional route/helper that runs `{OKF_BUNDLE_PATH}/scripts/hkf-evidence-path.py` when answering from HKF fixtures
- Identity-resolution workflow that emits HKF `IdentityAssertion` YAML (`proposed` / `parked`) instead of silent merges

### 4. Interactive Handoff Templates

**Why**:
- Many high-value searches end not with failure but with a well-defined manual next step.

**Add**:
- reusable handoff templates for:
  - image-only browse sets
  - login-required free databases
  - subscription databases
  - archive requests

### 5. Research Planning Templates For Technology Work

**Why**:
- We now have a data-side research strategy template, but not a parallel template for tooling strategy.

**Add**:
- a lightweight template for:
  - problem
  - current workaround
  - target workflow or helper
  - required inputs
  - desired outputs
  - risks
  - dogfooding test case

## Medium-Priority TODO

### 6. Workflow Test Fixtures

Build small example fixtures for:
- civil-record browse planning
- identity-bridge resolution
- immigration handoff packet generation
- future DNA match triage

Purpose:
- make dogfooding more repeatable
- verify prompts produce the expected shapes

### 7. Route Selection Guidance Tightening

Improve the skill and README guidance so users choose the right route faster when:
- they are not starting from scratch
- the problem is narrow and browse-first
- the problem is identity-heavy rather than source-discovery-heavy

### 8. Private Dogfooding Validation Pass

Add a repeatable validation pass that checks:
- route map consistency
- README / workflow count consistency
- JSON route integrity
- no accidental machine-local references in tracked docs

### 11. Agent Run Manifest (Observability)

**Status**: Started (2026-06-14)

**Done**:
- Schema: [reference/agent-run-manifest.md](../reference/agent-run-manifest.md)
- Template: [vault-template/templates/agent-run-manifest.md](../vault-template/templates/agent-run-manifest.md)
- Append script: [scripts/append-agent-run.py](../scripts/append-agent-run.py)

**Done (2026-06-14, follow-up)**:
- `scripts/list-agent-runs.py` to query manifests from Research_Log or `agent_runs/`
- Standalone `agent_runs/` directory mode via `append-agent-run.py --standalone`
- `scripts/validate-agent-run-manifests.py` for CI friendly example manifest checks
- Shared parsing in `scripts/agent_run_lib.py`

**Add next**:
- CI hook for `validate-agent-run-manifests.py` alongside route sync checks

**Done (2026-06-14, post-run hooks)**:
- [reference/post-run-hooks.md](../reference/post-run-hooks.md) Cursor and cross-platform finalize flow
- [scripts/write-pending-agent-run.py](../scripts/write-pending-agent-run.py) and [scripts/finalize-agent-run.py](../scripts/finalize-agent-run.py)
- Project hooks in [.cursor/hooks.json](../.cursor/hooks.json) (`stop`, `afterShellExecution`)

## Lower-Priority TODO

### 9. Dist Build Verification

Before public release, verify:
- `build-dist`
- `run-route`
- adapter docs
- installable Codex bundle behavior

For now, this is secondary to private dogfooding usefulness.

### 10. Public Release Hardening

Keep public-release polish separate from research-tool utility.

Includes:
- broader docs cleanup
- example refresh
- release packaging walkthrough
- public-facing narrative refinement

## Candidate First Implementation Order

1. DNA match triage workflow
2. Memorial packet extraction workflow
3. Interactive handoff templates
4. Tooling-strategy template
5. Workflow fixtures

## Decision Log

- 2026-05-29: Feder / Fried cluster dogfooding showed that DNA triage needs an explicit `documentary bridge packet before outreach` sub-output. The workflow should compare DNA strength, surname rings, localities, correspondence claims, missing source targets, hypotheses, and focused outreach questions before recommending contact.

- 2026-05-29: Fried / Bank DNA cluster dogfooding confirmed that `workflow:dna-match-triage` should handle branch-specific queues, not just global top-match ranking. The workflow should accept a research question plus platform exports/notes and produce `follow up now`, `follow up later`, `archive only`, and `insufficient evidence`, while weighing correspondence overlap, locality clues, known branch anchors, and endogamy risk.

- 2026-05-30: Pinkas Fried CAHJP dogfooding surfaced a reusable `overseas-contact-bridge` pattern: foreign refugee / emigration forms often name overseas relatives or friends without enough detail for immediate identity proof. A workflow module should extract the named contacts, preserve exact relationship labels, generate name-variant clusters, rank U.S. record targets, and recommend candidate-table building before outreach.

- 2026-05-30: Hyman Fried census dogfooding surfaced a reusable `census-address-browse-handoff` pattern: when indexed searches fail but a near-date address exists, the workflow should convert address to federal ED or NY State AD/ED, define the exact browse target, list name/address variants, and log page-level negatives instead of repeating generic name searches.

- 2026-05-30: Fried / Przemyslany AGAD scan dogfooding surfaced a reusable `archive-scan-batch-triage` pattern: legacy image batches need source-bundle creation, image-level extraction, crop/zoom notes, confidence scoring, and collision handling before updating people. The workflow should produce `promote`, `collision / do not merge`, `misfiled or irrelevant`, and `needs paleographic review` buckets, plus a next-image-pull queue.

- 2026-05-30: Fried / Meryszczow planning surfaced a reusable `small-town-household-reconstruction` module: when one surname recurs across nearby households, the workflow should build a table keyed by parent pair, house number, village, event year, occupation, witnesses, midwives, spouses, and source pointer before suggesting merges. It should explicitly produce `same household`, `possible collateral`, `collision / keep separate`, and `needs image pull` buckets, and it should support adjacent-row checks for twin hypotheses.

- 2026-05-30: Jides Fried marriage-image intake surfaced a reusable `person-stub branch-integrity` guardrail: before promoting a person note, detect boilerplate or source references that belong to an unrelated geography, archive, or family branch. Flag inherited wrong-branch text for replacement and require the promoted note to cite the newly reviewed source.

- 2026-06-01: Rudie Fried marriage-image intake surfaced a reusable `diff-aware local-link validation` need: repository-wide checks can bury a clean intake under inherited missing Downloads files, encoded-path debt, and older relative-link mistakes. Validation should report `new breakage`, `new-artifact links`, and `pre-existing debt` separately.

- 2026-06-02: Przemyslany Jewish birth-volume handoff surfaced an `archive-holdings anti-bot fallback` need: the official Warsaw USC page links to a holdings-list PDF, but automated retrieval can hit a JavaScript anti-bot gate. Civil-record browse planning should preserve the official landing page and direct-link failure, fall back to a location-query template with repository contacts, and optionally support browser-assisted/manual extraction or a maintained locality cache rather than silently treating the PDF as searched.

- 2026-08-11: Added `reference/hkf-consumer.md` for Historical Knowledge Fabric consumption from genealogy-as-code (`HKF-SPEC.md`, evidence paths, OKF trust vs HKF certainty). Follow-ups: evidence-path route helper; identity workflow emitting parked/proposed `IdentityAssertion` records.

- 2026-06-14: Closed the Jewish Galicia matching-aid gap with `archives/galicia-jewish.md` and OKF env-var integration (`VAULT_PATH`, `OKF_BUNDLE_PATH`, `OKF_TOWN`). Personal Galicia search parameters remain in the evidence vault; community town context loads from `genealogy-as-code` at runtime.

- 2026-05-26: Created this TODO because the system already had a strong data-side research strategy pattern but no parallel technology backlog.
