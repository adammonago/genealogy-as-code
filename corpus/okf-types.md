---
type: Reference
title: OKF Type Registry — Genealogy Bundles
description: Canonical list of type values for genealogy knowledge bundles that use this toolkit.
tags: [meta, types, registry]
timestamp: 2026-07-30T00:00:00Z
---

This document defines the `type` values used in genealogy OKF bundles. Per the OKF spec, types are not registered centrally — this file is the toolkit-level registry so contributors and consumers can find descriptive, self-explanatory type names.

A community corpus may add a profile for institution-specific fields. Those profile values do not belong in this registry.

All values are case-sensitive. Consumers MUST tolerate unknown types gracefully.

---

# Type Inventory

## Data source types

| Type | Describes |
|---|---|
| `Archive Source` | A national or regional archive collection or fond holding original records. |
| `Local Archive Source` | A local or district-level archive with its own signature system (e.g., "syg" prefix). Use when the archive institution is not a national or regional state archive, or when the institution has not yet been confirmed. |
| `Microfilm Reel` | A single Family History Library (FHL/FamilySearch) microfilm reel containing records. Use when the microfilm number is the primary access path, especially for records not yet digitized. |
| `Digital Collection` | A fully digitized online collection (Ancestry, Geneteka, Szukajwarchiwach, etc.). |
| `Population Record Source` | A population-registration source such as a revision list or household register. Contains household or revision-list records, not civil vital records. |

## Record types

| Type | Describes |
|---|---|
| `Vital Records Register` | A single civil register (births, marriages, or deaths) for a specific year range. Use for post-1877 Austrian civil registration era records. |
| `Mixed Civil Register` | A pre-1826 Duchy of Warsaw / Congress Poland register covering Jewish and non-Jewish records together. |
| `Duplicat Register` | A legally mandated duplicate copy of vital records, required under Austrian Josephinian law. Not an error — the duplicate is an independent archival document that may differ from the primary register and enables cross-verification. |
| `Alegata Collection` | Supplementary annexes attached to vital acts — birth certificates, parental consents, military discharges, widowhood proofs. |
| `Population Record` | A population-registration record — household lists, revision lists, or family registers. Distinct from vital records. |
| `Book of Residents` | A Seelenbeschreibung or Haushaltsregister-style census/population register. |
| `Notarial Record` | Records from a notary public, often property or estate related. |
| `Cemetery Record` | A gravestone transcription or cemetery survey. |

---

## Knowledge / enrichment types

| Type | Describes |
|---|---|
| `Enrichment Note` | Volunteer annotation attached to a specific spreadsheet or register. |
| `Naming Convention` | Rules governing how given names, surnames, and patronymics are normalized in a town's files. |
| `Place Name Registry` | Geographic disambiguation — variant place names (Prosperów = Zawichost), administrative hierarchy, coordinates. |
| `Place Reference` | Geographic disambiguation — variant spellings, administrative hierarchy, coordinates. (Legacy; prefer `Place Name Registry` for new docs.) |
| `Data Quality Report` | Assessment of completeness, accuracy, and consistency for a register or spreadsheet. |
| `Playbook` | Step-by-step procedural guide for volunteers, coordinators, or community editors. |
| `Researcher Guide` | Researcher-facing how-to. Not volunteer curation. |
| `Record Access Guide` | Paths from an index hit to images, microfilm, or archive orders — town or regional. |
| `Coverage Expectations` | Honest scope statement: what an index does and does not contain for a place. |
| `Curation Checklist` | A structured list of tasks a volunteer must complete before a register is considered import-ready. |

## Meta types

| Type | Describes |
|---|---|
| `Town Overview` | Root concept for a town bundle — links to all sub-concepts. |
| `Reference` | A supporting reference document (like this file). Does not describe an asset directly. |
| `Curation Log` | Chronological log of curation activity for a town. |
| `Attested Computation` | OKF v0.2 deterministic computation contract (executor + attester). Used for HKF validation and similar checks. |

### HKF pilot subtypes (use with existing types)

Prefer `subtype` before proposing new top-level types ([HKF-SPEC.md](./HKF-SPEC.md) §37):

| Type | Subtype | Describes |
|---|---|---|
| `Reference` | `Historical Knowledge Fabric Specification` | Normative HKF profile |
| `Reference` | `Architecture Proposal` | Architectural direction / discussion companion to HKF-SPEC |
| `Reference` | `HKF Schema` | Machine-readable HKF schema index or schema docs |
| `Reference` | `Historical Knowledge Dataset` | Manifest for an external/high-volume HKF dataset or fixture |
| `Reference` | `HKF Predicate Registry` | Project-level predicate vocabulary |
| `Reference` | `OKF Migration Guide` | OKF v0.1 → v0.2 migration notes |
| `Enrichment Note` | `Historical Interpretation` | Curated interpretation promoted to Markdown |
| `Enrichment Note` | `Identity Resolution` | Curated identity decision promoted to Markdown |
| `Playbook` | `HKF Pipeline` | Extraction / materialization pipeline description |

HKF index: [README.md](./README.md).

---

# Indexing level vocabulary

Town index documents use an `indexing_level` field to indicate what each database row represents:

| Value | Meaning |
|---|---|
| `act` | Each row = one individual vital act (birth, marriage, death) |
| `register` | Each row = one annual register volume (individual acts not indexed) |
| `microfilm_reel` | Each row = one FHL microfilm reel (may span multiple registers) |
| `unknown` | Indexing level not yet determined |

---

# Extension guidance

When a contributor encounters a record type not listed above:

1. Use the closest existing type and add a `subtype:` frontmatter key to be more specific.
2. Open a PR against this file proposing the new type with a one-line description.
3. A toolkit maintainer approves new type additions.

Do not invent ad-hoc type values inside concept documents — it fragments the corpus and breaks filtering.

Institution-specific codes, such as a database bitmask, belong in that community's corpus profile, not in this registry.

# Citations

[1] [OKF Specification — Frontmatter](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md)
