---
type: Reference
subtype: OKF Migration Guide
title: OKF v0.1 → v0.2 Migration for genealogy-as-code
description: Incremental migration rules for timestamp, Citations, singular source, curation_status, and parked bundle state under HKF.
tags: [hkf, okf, migration]
status: draft
hkf_version: "0.1"
generated:
  by: human:adammonago
  at: 2026-08-11T04:00:00Z
sources:
  - id: hkf-spec
    resource: /corpus/HKF-SPEC.md
    title: Historical Knowledge Fabric Specification
  - id: okf-v02
    resource: https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md
    title: Open Knowledge Format v0.2 Specification
---

# OKF v0.1 → v0.2 migration

Adopt OKF v0.2 **incrementally**. Do not rewrite every town bundle on a flag day. Full rules: [HKF-SPEC.md](/corpus/HKF-SPEC.md) §§43–49.

## Field map

| v0.1 / project | v0.2 / HKF | Notes |
|---|---|---|
| `timestamp` | `generated.at` (+ `generated.by`) | Do **not** invent `by` if unknown; leave `timestamp` until next meaningful edit |
| `# Citations` | `sources` frontmatter + keyed footnotes | Legacy section MAY remain during transition |
| singular `source:` | `sources: [{id, resource, title}]` | Prefer `sources` on new HKF concepts |
| `curation_status` | keep as workflow field | MUST NOT invent `verified` from `curated` |
| `bundle_status: parked` | keep | MUST NOT become OKF `status: parked` |
| `okf_version: "0.1"` | `"0.2"` when bundle adopts v0.2 | Consumers fall back to `timestamp` when `generated` absent |

## Trust vs workflow

```text
OKF status:       draft | stable | deprecated
OKF verified:     trust signal only
curation_status:  project workflow
bundle_status:    active | candidate | parked
HKF states:       extraction_state, resolution_state, interpretation_state, …
```

## Pilot migration

The Przemyślany births register is the first fully migrated register concept (known producer via `volunteer`). Other documents migrate on edit.
