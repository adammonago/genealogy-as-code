---
type: Reference
subtype: HKF Schema
title: HKF Schemas
description: Machine-readable JSON Schema definitions for Historical Knowledge Fabric v0.1 logical records.
tags: [hkf, schemas, validation]
status: draft
hkf_version: "0.1"
generated:
  by: human:adammonago
  at: 2026-08-11T04:00:00Z
sources:
  - id: hkf-spec
    resource: /corpus/HKF-SPEC.md
    title: Historical Knowledge Fabric (HKF) Specification
---

# HKF schemas

These JSON Schema (YAML) files implement HKF 0.1 record shapes from [HKF-SPEC.md](/corpus/HKF-SPEC.md).

| Schema | Kind |
|---|---|
| [evidence-locator.schema.yaml](./evidence-locator.schema.yaml) | Embedded EvidenceLocator |
| [source-segment.schema.yaml](./source-segment.schema.yaml) | SourceSegment |
| [extraction.schema.yaml](./extraction.schema.yaml) | Extraction |
| [entity.schema.yaml](./entity.schema.yaml) | Entity |
| [entity-reference.schema.yaml](./entity-reference.schema.yaml) | EntityReference |
| [claim.schema.yaml](./claim.schema.yaml) | Claim |
| [identity-assertion.schema.yaml](./identity-assertion.schema.yaml) | IdentityAssertion |
| [interpretation.schema.yaml](./interpretation.schema.yaml) | HistoricalInterpretation |
| [derivation-run.schema.yaml](./derivation-run.schema.yaml) | DerivationRun |

Validate the Przemyślany fixture with:

```bash
python3.11 corpus/scripts/validate-hkf.py
```

Schemas tolerate unknown additional properties (OKF/HKF extension discipline).
