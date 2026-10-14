---
type: Attested Computation
title: Validate HKF Fixture Dataset
description: Deterministically validates HKF YAML records against approved schemas and semantic rules.
tags: [hkf, validation, attested-computation]
status: draft
hkf_version: "0.1"

runtime: python

parameters:
  - name: fixture_dir
    type: string
    required: false
    description: Directory of HKF YAML records (default: corpus/examples/przemyslany)
  - name: schemas_dir
    type: string
    required: false
    description: Directory of HKF schemas (default: corpus/schemas)

computation: corpus/scripts/validate-hkf.py

executor:
  resource: /corpus/computations/validate-hkf.md
  receipt:
    - input_sha256
    - schema_sha256
    - exit_code
    - report_sha256

generated:
  by: human:adammonago
  at: 2026-08-11T04:00:00Z

sources:
  - id: hkf-spec
    resource: /corpus/HKF-SPEC.md
    title: Historical Knowledge Fabric Specification
  - id: schemas
    resource: /corpus/schemas/index.md
    title: HKF Schemas
---

# Validate HKF fixture dataset

## Computation

Run from the repository root:

```bash
python3.11 corpus/scripts/validate-hkf.py
```

Optional paths:

```bash
python3.11 corpus/scripts/validate-hkf.py \
  --fixture-dir corpus/examples/przemyslany \
  --schemas-dir corpus/schemas
```

## What is checked

1. **Structural** — YAML parse; required fields; enumerations (JSON Schema).
2. **Semantic** — parked identity ⇒ `decision: unresolved`; resolved entityref ⇒ `resolved_entity_ref`; reviewed claim SHOULD warn without `verified`.
3. **Referential (soft)** — warn when IDs referenced in the fixture set are missing.

## Attestation note

Successful exit code attests **process fidelity** (schema + rules ran on these inputs). It does **not** attest that OCR or historical interpretation is correct ([HKF-SPEC.md](/corpus/HKF-SPEC.md) §36).

## Receipt fields (recommended)

| Field | Meaning |
|---|---|
| `input_sha256` | Hash of concatenated fixture YAML |
| `schema_sha256` | Hash of concatenated schema YAML |
| `exit_code` | 0 = pass |
| `report_sha256` | Hash of validator stdout report |
