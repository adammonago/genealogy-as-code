---
type: Reference
subtype: Historical Knowledge Dataset
title: Przemyślany HKF Pilot Fixture
description: >
  Small fictionalized HKF fixture for Przemyślany births act 412 (1899),
  demonstrating evidence paths, parked identity, contradiction, and dual extractions.
tags: [hkf, przemyslany, pilot, fixture]
status: draft
hkf_version: "0.1"
hkf_namespace: gaac:przemyslany
generated:
  by: human:adammonago
  at: 2026-08-11T12:30:00Z
sources:
  - id: birth-register
    resource: ./segment-1899-act-412.yaml
    title: Fixture source segment for the 1899 act used in this example
  - id: hkf-spec
    resource: /corpus/HKF-SPEC.md
    title: Historical Knowledge Fabric Specification
---

# Przemyślany HKF pilot fixture

**Scope:** one representative act location (1899 / act 412 / image 501). Person names in the fixture are illustrative. Register locators such as `/przemyslany/registers/births-1877-1904.md` name the concept in a community corpus; that town bundle is not stored in this toolkit.

## Records

| File | Kind | ID |
|---|---|---|
| [segment-1899-act-412.yaml](./segment-1899-act-412.yaml) | SourceSegment | `segment:przemyslany:1899:act-412` |
| [extraction-1899-act-412-v1.yaml](./extraction-1899-act-412-v1.yaml) | Extraction | `extraction:…:v1` |
| [extraction-1899-act-412-v2.yaml](./extraction-1899-act-412-v2.yaml) | Extraction | `extraction:…:v2` |
| [entity-place-przemyslany.yaml](./entity-place-przemyslany.yaml) | Entity | `entity:place:przemyslany` |
| [entityref-1899-act-412-residence.yaml](./entityref-1899-act-412-residence.yaml) | EntityReference | residence (`unresolved`) |
| [entityref-1899-act-412-person-1.yaml](./entityref-1899-act-412-person-1.yaml) | EntityReference | person (`parked`) |
| [claim-1899-act-412-residence.yaml](./claim-1899-act-412-residence.yaml) | Claim | residence |
| [claim-1899-act-412-birth-year.yaml](./claim-1899-act-412-birth-year.yaml) | Claim | birth year A |
| [claim-contradiction-birth-year.yaml](./claim-contradiction-birth-year.yaml) | Claim | birth year B (contradiction) |
| [identity-miasto-parked.yaml](./identity-miasto-parked.yaml) | IdentityAssertion | parked Miasto |
| [interpretation-birth-year.yaml](./interpretation-birth-year.yaml) | HistoricalInterpretation | disputed |
| [derivation-run-pilot.yaml](./derivation-run-pilot.yaml) | DerivationRun | pilot run |

## Pilot questions covered

| # | Question | Demonstrated by |
|---:|---|---|
| 1 | Claim → precise source location | claim evidence selectors |
| 2 | Original + normalized | temporal `original` / range fields |
| 3 | Machine extraction visibly unreviewed | `extraction_state: candidate`, no `verified` |
| 5 | Contradictory claims coexist | birth-year A + B |
| 6–7 | Unresolved / parked identity | residence + identity assertion |
| 8 | Identity rationale | `identity-miasto-parked.yaml` |
| 9 | Supports + challenges | interpretation |
| 10 | Multiple extractions | v1 + v2 |
| 12 | Bulk outside Git | fixture is small; dataset manifest pattern in HKF-SPEC §34 |
| 13 | Evidence path | `corpus/scripts/hkf-evidence-path.py` |

Validate:

```bash
python3.11 corpus/scripts/validate-hkf.py
python3.11 corpus/scripts/hkf-evidence-path.py interpretation:przemyslany:1899:act-412:birth-year
```
