---
type: Reference
subtype: HKF Predicate Registry
title: HKF Core Predicates
description: Deliberately small initial predicate registry for Historical Knowledge Fabric v0.1.
tags: [hkf, predicates]
status: draft
hkf_version: "0.1"
generated:
  by: human:adammonago
  at: 2026-08-11T04:00:00Z
sources:
  - id: hkf-spec
    resource: /corpus/HKF-SPEC.md
    title: Historical Knowledge Fabric Specification
---

# Core predicates

HKF 0.1 begins with a small registry. Consumers MUST tolerate unknown predicates. Expand only after pilot usage shows need ([HKF-SPEC.md](/corpus/HKF-SPEC.md) §71–72).

| Predicate | Description | Subject | Object | Inverse | Symmetric |
|---|---|---|---|---|---|
| `record.appears_in` | Subject appears in a record or register context | person, other | record, source | — | false |
| `person.has_name` | Source asserts a name for the subject | person | literal | — | false |
| `person.birth_date` | Source asserts a birth date | person | temporal | — | false |
| `person.death_date` | Source asserts a death date | person | temporal | — | false |
| `person.occupation` | Source asserts an occupation | person | literal / entity | — | false |
| `person.residence` | Source asserts a residence | person | place entityref / entity | — | false |
| `kinship.parent_of` | Source asserts subject is parent of object | person | person | `kinship.child_of` | false |
| `kinship.child_of` | Source asserts subject is child of object | person | person | `kinship.parent_of` | false |
| `kinship.spouse_of` | Source asserts a spousal relationship | person | person | `kinship.spouse_of` | true |
| `event.date` | Source asserts an event date | event | temporal | — | false |
| `event.place` | Source asserts an event place | event | place | — | false |
| `event.participant` | Source asserts participation | event | person | — | false |
| `source.references` | Source references another source | source | source | — | false |
| `source.derived_from` | Derived artifact comes from a source | source / record | source | — | false |

## Example definition shape

```yaml
predicate: kinship.parent_of
description: Source asserts that the subject is a parent of the object.
subject_types: [person]
object_types: [person]
inverse: kinship.child_of
symmetric: false
transitive: false
```

Identity is **not** expressed as a bare `sameAs` predicate shortcut — use `IdentityAssertion` ([HKF-SPEC.md](/corpus/HKF-SPEC.md) §73).
