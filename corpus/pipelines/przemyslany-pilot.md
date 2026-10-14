---
type: Playbook
subtype: HKF Pipeline
title: Przemyślany HKF Pilot Pipeline
description: Bounded pilot pipeline for extracting and validating a small HKF fixture from Przemyślany births.
tags: [hkf, przemyslany, pipeline, pilot]
status: draft
hkf_version: "0.1"
generated:
  by: human:adammonago
  at: 2026-08-11T04:00:00Z
sources:
  - id: hkf-spec
    resource: /corpus/HKF-SPEC.md
    title: Historical Knowledge Fabric Specification
  - id: fixture
    resource: /corpus/examples/przemyslany/index.md
    title: Przemyślany HKF fixture
---

# Przemyślany HKF pilot pipeline

## Goal

Demonstrate HKF Core / Provenanced behavior on **one act location** (1899 / act 412), not the full register corpus.

## Steps

1. **Select segment** — year, act, and image from the register concept. The full place bundle stays in a community corpus.
2. **Record SourceSegment** with `EvidenceLocator`.
3. **Run Extraction** (may run multiple versions; do not delete prior runs).
4. **Emit EntityReferences** with `resolution_state` unresolved or parked when needed.
5. **Emit Claims** with evidence + `extraction_state: candidate`.
6. **Optional IdentityAssertion** — park or propose; never silent merge.
7. **Optional HistoricalInterpretation** — list supports and challenges.
8. **Record DerivationRun** with inputs, outputs, software revisions.
9. **Validate** via [validate-hkf.md](../computations/validate-hkf.md).

## Non-goals

- Publishing person-level public conclusions for living or private individuals.
- Loading full index spreadsheets into Git.
- Auto-accepting model identity matches.

## Outputs

Fixture directory: [examples/przemyslany/](../examples/przemyslany/).
