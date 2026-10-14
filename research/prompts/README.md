# Prompts

Autoresearch prompts for AI-assisted genealogy research. Designed for Claude Code's `/autoresearch` command but adaptable to any AI tool that supports autonomous iteration.

## How to Use

1. Open Claude Code in your genealogy repository directory
2. Type `/autoresearch` and paste the contents of a prompt file
3. Replace all `[PLACEHOLDER]` values with your actual data
4. The AI will run autonomously for the specified number of iterations

## Prompt Anatomy

Every prompt contains these fields:

| Field | Purpose |
|---|---|
| **Shared Contracts** | References to `_shared-output-contract.md` and `_shared-iteration-stop-rules.md` |
| **Goal** | What the prompt is trying to accomplish |
| **Metric** | A measurable quantity that tracks progress |
| **Direction** | Whether to maximize or minimize the metric |
| **Verify** | A command or check that measures current state |
| **Guard** | What the prompt should NOT do (safety rails) |
| **Iterations** | How many autonomous loops to run |
| **Protocol** | Step-by-step instructions for each iteration |

## Which Prompt to Use When

If you are not sure a prompt is the right first move, start with a workflow instead:

- Use `workflow:phase-planning` when the next step is unclear.
- Use `workflow:civil-record-browse-planning` when you already have a narrow event/place/year target and need a register browse plan.
- Use `workflow:identity-bridge-resolution` when the core problem is same-name collision, spouse split, alias drift, or household sorting.

**Starting from scratch?**
Start with `01-tree-expansion`. It will search the web for every ancestor you've listed and try to extend every branch.

**Already have a populated tree?**
Run `02-cross-reference-audit` to find and fix discrepancies between your tree file and your source documents.

**Have deceased ancestors without memorial links?**
Run `03-findagrave-sweep` to locate Find a Grave memorials and extract data from them.

**Have Hebrew or Yiddish tombstone photos?**
Run `13-hebrew-headstone` (`route_key=prompt:13-hebrew-headstone`). It wraps the H3 v8.1 core at `hebrew-headstone-helper/prompts/H3_v8_1_prompt.txt`.

**Want to export your tree?**
Run `04-gedcom-completeness` to build or verify a GEDCOM file that matches your notes.

**Need to package a blocked database search for later manual work?**
Prompts `07`, `08`, and `11` create handoff files from `[VAULT_PATH]/templates/handoff-packet.md` when the right source is known but not directly retrievable.

## Prerequisites

| Prompt | Requires |
|---|---|
| 01-tree-expansion | A `Family_Tree.md` file with at least your known ancestors listed |
| 02-cross-reference-audit | A populated `Family_Tree.md` plus person files or transcription notes |
| 03-findagrave-sweep | A `Family_Tree.md` with death dates or "deceased" notations |
| 04-gedcom-completeness | A `Family_Tree.md` and optionally an existing `.ged` file |
| 13-hebrew-headstone | Headstone image(s); `[VAULT_PATH]` for transcription output; `[ANCESTOR]` optional but recommended |

## Shared Contracts

All prompts reference shared contracts instead of duplicating Output Mode text:

- Output contract: [prompts/_shared-output-contract.md](_shared-output-contract.md)
- Iteration stop rules: [prompts/_shared-iteration-stop-rules.md](_shared-iteration-stop-rules.md)
- Handoff template (in vault): `[VAULT_PATH]/templates/handoff-packet.md`

Agents load these at startup per [agents/genealogy-autoresearch-agent.md](../agents/genealogy-autoresearch-agent.md).

## Placeholders

All prompts use these placeholders. Replace them with your actual data before running:

- `[SURNAME]` — A family surname (e.g., "Johnson")
- `[ANCESTOR]` — A specific ancestor's name (e.g., "Gustav M. Johnson")
- `[LOCATION]` — A geographic location (e.g., "Clinton, Minnesota")
- `[DATE]` — A date or date range (e.g., "1866" or "1880-1920")
- `[VAULT_PATH]` — The path to your genealogy notes root inside your repository
- `[GEDCOM_PATH]` — The path to your GEDCOM file
