---
type: index
created: YYYY-MM-DD
updated: YYYY-MM-DD
tags: [genealogy, family-history]
---

# Genealogy

Master index for family history research, genetic ancestry, and digitized archives.

## Ancestry Research System

| Layer | File | Description |
|---|---|---|
| Family Tree | [Family_Tree](Family_Tree.md) | Complete merged tree (all lines) |
| Research Log | [Research_Log](Research_Log.md) | Chronological record of research actions, agent_run manifests, and findings |
| Open Questions | [Open_Questions](Open_Questions.md) | Research gaps ranked by priority |
| Data Inventory | [Data_Inventory](Data_Inventory.md) | All source files tagged by type and reliability |
| Timeline | [Timeline](Timeline.md) | Every dated event, ordered chronologically |

## Regions (Geographic Deep Dives)

| Region | Families | Genetic Signal |
|---|---|---|
| `REGION_NAME` | [SURNAME-1], [SURNAME-2] | [percentage]% [category] |

## Surnames (Origin Research)

| Surname | Origin | Notes |
|---|---|---|
| `SURNAME` | [Country] | [Brief note on origin] |

## Source Collections

| Collection | Files | Size | Source | Status |
|---|---|---|---|---|
| [Collection Name] | [count] | [size] | `~/Files/Genealogy/[path]/` | [OCR status] |

## File Locations

- **Originals (scans)**: `~/Files/Genealogy/`
- **Notes (transcriptions and references)**: this folder
- **Genomics**: (path to DNA data if applicable)

## Family Lines

### [Maternal/Paternal Line Name]

- `SURNAME` — Brief description of this family line

### [Other Line Name]

- `SURNAME` — Brief description

## Person Files

### [Surname] Family
- `Person_Name` — Brief bio (b. YYYY, d. YYYY. Occupation. Location.)

## Processing Pipeline

OCR toolchain: Tesseract + ocrmypdf + ImageMagick + Claude multimodal

### Document Classification

| Category | Count | Description | OCR Method |
|---|---|---|---|
| photo_only | — | Portraits, group photos, buildings | Catalog only |
| printed_text | — | Certificates, newspaper clippings, diplomas | ocrmypdf (Tesseract) |
| handwritten | — | Record books, letters, funeral notes | Claude multimodal |
| mixed | — | Postcards (front/back), annotated docs | Layered approach |
