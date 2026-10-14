# autoresearch-genealogy

Structured prompts, vault templates, and research workflows for AI-assisted genealogy research. Built for Claude Code, adaptable to any AI tool or manual workflow.

This project extracts and generalizes methods developed during a real genealogy research effort that produced 105 files spanning 9 generations across 6 family lines, using Claude Code's autonomous research capabilities.

## Who This Is For

- **Genealogy researchers** who want to use AI to accelerate their family history work without sacrificing source rigor
- **AI/tech enthusiasts** who want a concrete example of autonomous research loops applied to a humanities domain
- **Anyone** who has a box of old photos, a DNA test, and unanswered questions about their family

## Quick Start

1. Clone this repo
2. Copy the `vault-template/` folder into your genealogy repository (or any markdown workspace)
3. Fill in `Family_Tree.md` with what you already know (start with yourself, work backward)
4. Scan any physical documents you have (certificates, photos, letters)
5. Open Claude Code, paste the contents of `prompts/01-tree-expansion.md`, and run it
6. Review the results, then run `prompts/02-cross-reference-audit.md` to verify

See `workflows/getting-started.md` for the full walkthrough.

## Skills And Agent Package

This repository now includes a packaged skill system and agent entrypoint:

- Skill pack root: `skills/`
- Main skill: `skills/genealogy-autoresearch/SKILL.md`
- Route map: `skills/genealogy-autoresearch/ROUTING_TABLE.md`
- Agent spec: `agents/genealogy-autoresearch-agent.md`
- Machine readable routes: `routes.json`
- Cross platform wrappers: `adapters/`
- Portable route renderer: `scripts/run-route.py`
- One command wrapper: `./run-route`
- Dist builder: `./build-dist`

Use a `route_key` to run packaged logic, for example `workflow:discrepancy-resolution` or `prompt:11-immigration-search`.

Example:

```bash
./run-route --platform codex --route-key prompt:11-immigration-search --vault-path "/path/to/vault" --ancestor "Example Person" --location "New York" --date "1880-1910" --print-only
```

Distribution pipeline docs live at `adapters/DIST_PIPELINE.md`.

For Codex specifically, `./build-dist --target codex` now produces an installable plugin zip at `dist/codex.zip` with the required `.codex-plugin/plugin.json` wrapper.

For private use before any public release, see `DOGFOODING_CHECKLIST.md`.

For the technology backlog behind the research system itself, see `RESEARCH_TOOLS_TODO.md`.

## Local Data Pointers (Not Committed)

Use local environment variables to expose private datasets and external knowledge bundles to your agent workflow without committing files to this repository.

Copy `.env.local.example` to `.env.local` in this `research/` directory and set absolute paths for your machine:

```bash
VAULT_PATH="/absolute/path/to/your/genealogy-vault"
# Community corpus of place bundles. Not this toolkit root.
OKF_BUNDLE_PATH="/absolute/path/to/your-community-corpus"
# OKF_TOWN="town-slug"   # optional; may also live in vault Data_Inventory.md
# Optional local index-to-scan mappings. Keep the files outside this repository.
# LOCAL_INDEX_PATH="/absolute/path/to/your-local-index"
```

Guidelines:

- Keep source data outside the repository.
- Commit only metadata and research notes, not raw private datasets.
- In prompts and workflows, reference `VAULT_PATH`, `OKF_BUNDLE_PATH`, and `LOCAL_INDEX_PATH` instead of hardcoded machine-specific paths.
- If you move machines, recreate `.env.local` with the new absolute paths.

### External OKF context (optional)

When both `OKF_BUNDLE_PATH` and `OKF_TOWN` are set (in `.env.local` or recorded in your vault `Data_Inventory.md`), the skill and agent load:

`{OKF_BUNDLE_PATH}/{OKF_TOWN}/index.md`

Treat that file as **read-only community context**: place registers, archive signatures, and place-name rules from a community corpus. It does not replace vault evidence. Personal conclusions stay in your vault under `VAULT_PATH`.

Historical Knowledge Fabric materials live in this toolkit's `corpus/` directory, not inside the community corpus. See `reference/hkf-consumer.md`.

Repository boundaries are in the toolkit [README](../README.md).

## What's Included

### Prompts (`prompts/`)

12 autoresearch prompts designed for Claude Code's `/autoresearch` command (plus specialized routes such as Hebrew headstone extraction). Each defines a Goal, Metric, Direction, Verify condition, Guard rails, Iterations, and Protocol. They run autonomously: searching the web, updating your vault, and verifying their own work.

| Prompt | Purpose |
| --- | --- |
| 01-tree-expansion | Push every branch as far back as possible using web research |
| 02-cross-reference-audit | Find and fix discrepancies between your tree and source documents |
| 03-findagrave-sweep | Locate Find a Grave memorials for every deceased ancestor |
| 04-gedcom-completeness | Ensure your GEDCOM file matches your vault data |
| 05-source-citation-audit | Verify every person file cites at least two independent sources |
| 06-unresolved-persons | Identify and resolve unnamed people mentioned in your documents |
| 07-timeline-gap-analysis | Find life events where records should exist but have not been found |
| 08-open-question-resolution | Systematically attack every open research question |
| 09-bygdebok-extraction | Extract data from digitized local history books (any country) |
| 10-colonial-records-search | Search for colonial American ancestors in pre-1800 records |
| 11-immigration-search | Locate passenger manifests and naturalization records |
| 12-dna-chromosome-analysis | Analyze per-chromosome ancestry data to map genetic segments |
| 13-hebrew-headstone | Transcribe and translate Hebrew/Yiddish tombstone inscriptions (H3 v8.1) |

### Specialized Prompt Packs

- **Hebrew headstone extraction**: `prompt:13-hebrew-headstone` wraps `hebrew-headstone-helper/` (H3 v8.1) for Hebrew/Yiddish tombstone transcription, translation, and Hebrew date conversion.
- Integrated into workflow guidance for tombstone photos in `workflows/ocr-pipeline.md`, `workflows/document-triage.md`, and `prompts/03-findagrave-sweep.md`.

### Vault Template (`vault-template/`)

19 files: a complete genealogy workspace starter kit with YAML frontmatter, plain markdown, readable anywhere.

## Markdown Authoring Policy

Generated output in this repository uses GitHub-compatible Markdown conventions:

- Use standard Markdown links: `[Label](relative/path/to/file.md)`
- Do not use wiki links (`[[...]]`)
- Always include `.md` for local note links
- Prefer canonical targets under `people/`, `surnames/`, `transcriptions/`, and `references/` when those files exist
- If a target does not exist, use plain text unless explicitly creating a stub note

See `AUTHORING_GUIDELINES.md` for the full contract used by writing tools.

- **Core files**: Family tree, research log, open questions, data inventory, timeline, genetic profile, chromosome painting, witness network, unresolved persons, research strategy
- **Templates**: Person, transcription, certificate, postcard, region, surname, hypothesis, draft letter, DNA cluster intake

### Archive Guides (`archives/`)

24 country and region-specific guides covering where to find records, what is free vs paid, and what AI tools can access directly vs what requires a browser.

**Europe**: Ireland, England/Wales, Scotland, France, Italy, Spain/Portugal, Germany, Netherlands, Austria, Hungary, Norway, Sweden, Poland, Russia/Ukraine

**Americas**: USA (colonial, immigration, census, vital records), African American, Canada, Mexico/Latin America

**Oceania**: Australia/New Zealand

**Cross-national**: Jewish genealogy

### Reference Guides (`reference/`)

9 methodology documents: confidence tiers, source hierarchy, DNA interpretation guardrails, naming conventions (patronymics, farm names, przydomki), GEDCOM format guide, common pitfalls, glossary, AI capabilities assessment, and the case for autoresearch in genealogy.

### Workflows (`workflows/`)

11 step-by-step guides: getting started, OCR pipeline, new ancestor intake, document triage, oral history protocol, discrepancy resolution, civil-record browse planning, identity-bridge resolution, phase planning, interactive handoff, and validator pass.

The OCR and triage workflows include a tombstone-specific route: Hebrew/Yiddish inscriptions should be processed with `prompt:13-hebrew-headstone` rather than treated as photo-only catalog items.

If you are not starting from scratch and already have a specific research problem, do not default blindly to tree expansion. Use `workflow:phase-planning`, `workflow:civil-record-browse-planning`, or `workflow:identity-bridge-resolution` first when those shapes fit better.

### Examples (`examples/`)

6 anonymized worked examples showing autoresearch in action: tree expansion session, cross-reference audit, DNA-to-genealogy mapping, name resolution, colonial deep dive.

## Philosophy

**Structured autonomous research with mechanical verification, not AI guessing.**

Genealogy is different from most AI tasks. There is no compiler. Sources disagree with each other. Confidence is probabilistic, not binary. A name that appears as "Sakkarias" in one record and "Zacharias" in another might both be correct. A date listed as 1820 in one source and 1925 in another is almost certainly wrong somewhere.

The autoresearch approach adapts to this by:

- **Defining measurable metrics** (count of sourced claims, count of resolved questions, count of remaining discrepancies)
- **Requiring verification after every iteration** (cross-reference audit, not just accumulation)
- **Logging negative results** (what you searched for and did not find is as important as what you found)
- **Maintaining confidence tiers** (Strong Signal / Moderate Signal / Speculative) rather than treating all claims as equal

This is inspired by Andrej Karpathy's autoresearch concept: autonomous goal-directed loops where the AI modifies, verifies, keeps or discards, and repeats. Applied to genealogy, the "compiler" is replaced by cross-referencing independent sources.

## License

MIT. See `LICENSE`.

## Provenance and Attribution

This repository is based on the MIT licensed project `mattprusak/autoresearch-genealogy`.
See `NOTICE` for derivative work attribution and `THIRD_PARTY_LICENSES.md` for third-party tracking.
This repository also includes `hebrew-headstone-helper` prompt materials under CC BY-NC 4.0; see `NOTICE` and `hebrew-headstone-helper/LICENSE`.

## Contributing

Contributions welcome. If you have prompts, workflows, or archive guides that worked for your research, open a PR. Please ensure all examples use placeholder names (no real family data).
