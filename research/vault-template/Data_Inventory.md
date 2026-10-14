---
type: reference
created: YYYY-MM-DD
tags: [genealogy, data, inventory, sources]
---

# Data Inventory

Complete inventory of all ancestry-related data assets. Each tagged with source, type, reliability, and suggested use.

## Genetic Data

| File | Source | Type | Reliability | Suggested Use |
|---|---|---|---|---|
| [path to raw genome] | [Provider] | Raw SNP data | High (lab-generated) | Upload to GEDmatch; custom analysis |
| [path to ethnicity PDF] | [Provider] | Ethnicity estimate | High | Primary ancestry reference |

## Genealogical Documents

### High Reliability (official records, primary sources)

| Document | Family | Location |
|---|---|---|
| [Document description] | [Surname] | `vault_note_link` |

### Moderate Reliability (newspaper, secondary sources)

| Document | Family | Location |
|---|---|---|
| [Document description] | [Surname] | `vault_note_link` or OCR path |

### Low Reliability (anecdotal, interpreted)

| Document | Family | Notes |
|---|---|---|
| [Document description] | [Surname] | [Why reliability is low] |

## Research Notes

[Count] markdown files in `[VAULT_PATH]/`

## External OKF context

Optional read-only pointers to a community OKF knowledge bundle (for example a local clone of `genealogy-as-code`). OKF documents towns, registers, and archive metadata for any JRI researcher. It does not hold personal family conclusions.

| Setting | Value | Notes |
|---|---|---|
| Bundle root | `OKF_BUNDLE_PATH` in `.env.local` | Absolute path to the OKF repository root |
| Town slug | `[town-slug]` | Directory name under the bundle root (e.g. `{OKF_BUNDLE_PATH}/[town-slug]/`) |
| Entry file | `{OKF_BUNDLE_PATH}/[town-slug]/index.md` | Loaded by the skill and agent when both paths above are configured |

Guidelines:

- Record the town slug here so research sessions know which bundle to load.
- Keep person files, transcriptions, and hypotheses in this vault, not in the OKF repo.
- When OKF and vault facts differ, vault evidence wins; use OKF for search targets, archive signatures, and place-name disambiguation.

## Source Document Archive

| Collection | Files | Size | Location | OCR Status |
|---|---|---|---|---|
| [Collection Name] | [count] | [size] | `~/Files/Genealogy/[path]/` | [status] |

## What's Missing (Acquisition Priorities)

See [Open_Questions](Open_Questions.md) for the full list. Top gaps:

1. [Most important missing data source]
2. [Second most important]
3. [Third]
