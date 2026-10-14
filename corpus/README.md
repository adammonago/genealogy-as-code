---
type: Reference
title: Historical Knowledge Fabric
description: Spec, schemas, predicates, validator, bundle template, and the Przemyślany fixture.
tags: [hkf, index]
status: draft
okf_version: "0.2"
hkf_version: "0.1"
---

# Corpus

This directory is the portable genealogy knowledge format. Community place inventories live in a separate corpus repository. Copy [template/](template/README.md) to start one. Adam Monago wrote this format so shared notes about records can be reviewed in git and followed back to the evidence. The essay is [Historical Knowledge Fabric](https://www.adammonago.com/historical-knowledge-fabric/). The rest of the origin story is in the [repository README](../README.md#why-this-exists).

| Role | Path |
|---|---|
| Normative specification | [HKF-SPEC.md](HKF-SPEC.md) |
| Architecture proposal | [architecture-proposal.md](architecture-proposal.md) |
| OKF type registry | [okf-types.md](okf-types.md) |
| Schemas | [schemas/](schemas/index.md) |
| Core predicates | [predicates/core.md](predicates/core.md) |
| Przemyślany pilot pipeline | [pipelines/przemyslany-pilot.md](pipelines/przemyslany-pilot.md) |
| Validation | [computations/validate-hkf.md](computations/validate-hkf.md) |
| OKF v0.1 → v0.2 migration | [okf-v02-migration.md](okf-v02-migration.md) |
| Fixture | [examples/przemyslany/](examples/przemyslany/index.md) |
| Bundle starter | [template/](template/README.md) |

From the repository root:

```bash
python3.11 corpus/scripts/validate-hkf.py
python3.11 corpus/scripts/hkf-evidence-path.py interpretation:przemyslany:1899:act-412:birth-year
```

Corpus documentation and schemas are [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).
