---
type: Reference
subtype: Architecture Proposal
title: Historical Knowledge Fabric — From Genealogy-as-Code to Traversable Historical Evidence
description: A proposed architecture for connecting historical sources, extracted claims, identities, authorities, and interpretations while preserving provenance, uncertainty, and human curation.
tags: [architecture, historical-knowledge, provenance, identity, claims, okf, ai, hkf]
status: draft
hkf_version: "0.1"
generated:
  by: human:adammonago
  at: 2026-08-10T00:00:00Z
sources:
  - id: hkf-spec
    resource: /corpus/HKF-SPEC.md
    title: Historical Knowledge Fabric Specification
  - id: hkf-index
    resource: /corpus/index.md
    title: HKF index
---

# Historical Knowledge Fabric

## Status

**Architecture proposal for discussion** — companion to the normative [`HKF-SPEC.md`](/corpus/HKF-SPEC.md).

This document describes architectural direction for `genealogy-as-code`. It is not a proposal to replace the existing town-bundle model, move bulk genealogical data into Git, or create a universal genealogy database.

Instead, it asks:

> If increasingly large bodies of historical evidence become machine-readable, how can `genealogy-as-code` help turn them into knowledge that is linked, traversable, updateable, reproducible, and still anchored to the original evidence?

The proposed answer is a **Historical Knowledge Fabric**.

---

## Relationship to HKF-SPEC

| Document | Role |
|---|---|
| **This proposal** | Why and where: architectural intent, layers, non-goals, phased rollout |
| **[`HKF-SPEC.md`](/corpus/HKF-SPEC.md)** | How: normative MUST/SHOULD contract, schemas, migration, conformance |
| **[`corpus/`](./README.md)** | Working artifacts: schemas, Przemyślany fixture, validators |

A few refinements from the proposal sketch are now locked in the SPEC:

1. **OKF lifecycle vs HKF state.** OKF `status` remains only `draft` | `stable` | `deprecated`. Values such as disputed, superseded, or parked belong in HKF fields (`interpretation_state`, `resolution_state`, `extraction_state`, `bundle_status`), not in OKF `status`.
2. **Relationships are claim-backed.** Typed relationships are represented as HKF `Claim` records (subject–predicate–object + evidence). Graph edges are a *view* of claims that retain claim identity and evidence paths — not a parallel Relationship record type that drops provenance.
3. **Claim review uses OKF `verified` + HKF `extraction_state`.** The §6 sketch’s nested `review` / `status: reviewed` maps to `extraction_state: reviewed` plus an explicit `verified` event when a human actually reviewed the representation.
4. **Implemented layout.** Schemas, examples, and validators live under [`corpus/`](./README.md).

Phases 0–3 of §23 are underway: this proposal (Phase 0), OKF v0.2 alignment notes and a migrated register concept (Phase 1), machine-readable schemas (Phase 2), and a bounded Przemyślany fixture with validation and evidence-path traversal (Phase 3). Phase 4 (multi-source research traversal) is the next substantive milestone.

---

# 1. Executive summary

`genealogy-as-code` already treats knowledge surrounding genealogical data as something that can be:

- represented in human-readable files;
- versioned in Git;
- enriched incrementally;
- linked across concepts;
- reviewed through pull requests;
- separated from the underlying bulk datasets; and
- maintained collaboratively.

A Historical Knowledge Fabric extends that philosophy one step further.

Rather than treating an OCR transcript, spreadsheet row, archive description, place-name registry, or researcher conclusion as an isolated artifact, the fabric provides a common way to express the relationships among:

**sources → passages/records → claims → entities → identity assertions → interpretations**

with provenance retained at every step.

The objective is not to create a database containing "the truth."

The objective is to create an infrastructure in which we can say:

> **This source says this, about this entity, according to this extraction or curator, with this degree of confidence, and this is how that evidence currently affects our interpretation.**

New evidence can then extend, corroborate, contradict, or supersede an interpretation without destroying the history of how the conclusion was reached.

---

# 2. Why this matters now

Historical digitization is reaching a transition point.

For many years, digitization primarily meant making an image of a page available online. OCR added searchability, but historical OCR was often too inaccurate to support reliable downstream analysis.

New generations of visual-language and OCR models are making it increasingly practical to reprocess historical collections at scale. Projects such as FineBooks demonstrate that millions of historical pages may become substantially more machine-readable without requiring manual transcription of every page.

That is an important breakthrough.

It is also only the beginning.

OCR answers:

> **What characters probably appear on this page?**

Historical research asks progressively harder questions:

> What is this passage describing?

> Which people, places, organizations, records, and events does it mention?

> Is "Lemberg" the same place another source calls "Lwów" or "Lviv"?

> Is "Abram Kohn" in one register the same individual as "Abraham Cohen" in another?

> Does this record corroborate an existing conclusion?

> Does it contradict one?

> Which conclusion was accepted before this evidence was discovered?

> What changed in our understanding, and why?

Those are not fundamentally OCR problems.

They are problems of **evidence, identity, provenance, relationships, time, uncertainty, and interpretation**.

That is the problem space of the Historical Knowledge Fabric.

---

# 3. The central architectural idea

The fabric should distinguish five things that are often accidentally collapsed into one.

## 3.1 Evidence

Evidence is what the historical source actually contains.

Examples:

- an archive image;
- page 174 of a digitized book;
- act 37 in a marriage register;
- one spreadsheet row derived from a register;
- a cemetery inscription;
- a newspaper notice;
- a population-register entry.

Evidence should remain traceable to its original source.

---

## 3.2 Extraction

Extraction describes what a human or machine believes can be read from that evidence.

Examples:

- a transcription;
- an OCR result;
- a person's name;
- a date;
- an occupation;
- a geographic reference;
- a relationship expressed in a record.

Extraction is not the same thing as fact.

An OCR model can be wrong.  
A human transcription can be wrong.  
A spreadsheet index can contain an error.

The extraction therefore needs provenance of its own.

---

## 3.3 Claims

A claim is an assertion supported by some piece of evidence.

For example:

> Act 37 identifies Chaim Rosenberg as the father of Sara Rosenberg.

The fabric should record that as a claim rather than immediately making:

`Chaim Rosenberg → parent_of → Sara Rosenberg`

an unquestioned fact.

The distinction is important because another record might give a different father's name, or later research might show that two people initially thought to be identical were actually different individuals.

---

## 3.4 Identity

Identity answers:

> **What real-world thing does this reference probably describe?**

Identity resolution is a separate process from extraction.

For example:

- Lemberg
- Lwów
- Lvov
- Львів
- Lviv

can be linked to a shared geographic entity while still preserving the exact name used by each source.

Person identity is more difficult.

Two records containing:

`Abraham Rosenberg`

must not automatically become one person merely because the normalized names match.

An identity assertion therefore needs its own evidence, confidence, status, and history.

---

## 3.5 Interpretation

Interpretation is what we currently conclude after considering multiple claims.

An interpretation might state:

> Available evidence suggests that Person A and Person B are the same individual.

or:

> The most likely modern location corresponding to this historical place reference is Lviv, Ukraine.

or:

> Records currently indicate that this register covers births from 1878 through 1884, although 1881 appears incomplete.

Interpretations can change.

Evidence should not.

This gives the fabric one of its most important properties:

> **New knowledge changes the interpretation without rewriting the historical evidence.**

---

# 4. Design principles

## 4.1 Source before assertion

Every meaningful historical claim should be traceable to evidence.

A claim without provenance may be useful as a search lead, but it should never be indistinguishable from a sourced assertion.

---

## 4.2 Claims are not facts

The fabric records what sources and researchers assert.

Agreement among claims can increase confidence, but the system should not erase disagreement simply because one interpretation currently appears stronger.

---

## 4.3 Identity is explicit

Entity resolution should never be an invisible side effect of normalization.

The fabric should represent:

- confirmed matches;
- probable matches;
- possible matches;
- rejected matches; and
- unresolved identity.

The existing concept of **parked identity debt** is therefore not an edge condition. It is an early example of a core Historical Knowledge Fabric principle.

**Unresolved identity is valid knowledge.**

---

## 4.4 Historical names are data

Normalization should add information rather than overwrite it.

If a record says `Lwów`, the fabric should preserve `Lwów`.

It may additionally connect that value to:

- Lemberg;
- Lvov;
- Lviv;
- a geographic identifier;
- historical administrative units; and
- modern coordinates.

The original historical representation remains part of the evidence.

---

## 4.5 Time applies to knowledge as well as events

Historical systems need more than a single `date`.

At least three kinds of time may matter:

1. **Event time** — when the historical event occurred.
2. **Source time** — when the source was created.
3. **Knowledge time** — when an extraction, identity decision, or interpretation was made.

This allows the system to answer not only:

> What happened in 1882?

but eventually:

> What did our corpus support as of January 2026, and what changed afterward?

---

## 4.6 Uncertainty is first-class

The absence of certainty should not force an artificial binary choice.

Candidate states might include:

- `unreviewed`
- `extracted`
- `reviewed`
- `corroborated`
- `disputed`
- `superseded`
- `rejected`

Confidence scores may supplement these states but should not replace human-readable reasoning.

---

## 4.7 Git is the control plane, not necessarily the data plane

`genealogy-as-code` should not become a repository containing millions of OCR pages, database rows, embeddings, or graph edges.

Git is well suited to:

- schemas;
- provenance manifests;
- source descriptions;
- curation rules;
- entity-resolution rules;
- reference vocabularies;
- reviewed interpretations;
- small test fixtures;
- pipeline configuration;
- validation logic; and
- history of important decisions.

Large derived datasets may belong in:

- object storage;
- Parquet datasets;
- PostgreSQL;
- graph databases;
- search indexes;
- vector stores; or
- other reproducible external stores.

The Git repository describes and governs those resources without having to contain all of them.

---

# 5. A conceptual model

A minimal Historical Knowledge Fabric could contain the following concepts.

| Concept | Purpose |
|---|---|
| **Source** | Original archive, register, book, collection, database, image set, etc. |
| **Source Segment** | Specific page, act, image, spreadsheet row, or record within a source |
| **Extraction** | Text or structured values derived from a source segment |
| **Claim** | An assertion supported by one or more source segments |
| **Entity** | A person, place, organization, event, source, occupation, jurisdiction, etc. |
| **Identity Assertion** | Statement that two references represent the same or related entities |
| **Authority Reference** | Link to an external controlled identifier or authority system |
| **Interpretation** | Current synthesis of multiple claims |
| **Derivation Run** | Reproducible human or machine process that generated knowledge |
| **Review Decision** | Human approval, rejection, correction, or qualification |

Typed **relationships** between entities are not a separate storage type in the HKF 0.1 model. They are expressed as `Claim` records (subject–predicate–object + evidence); graph materialization is a provenance-preserving view of those claims. See [`HKF-SPEC.md`](/corpus/HKF-SPEC.md) §§20, 30, 73.

These concepts do not require one physical database schema.

They describe a logical architecture that different storage technologies can implement.

---

# 6. Example claim representation

The exact schema should be developed through a pilot rather than standardized prematurely, but a derived claim might conceptually resemble:

```yaml
claim_id: claim:przemyslany:register-1879:act-37:father
claim_type: parent-child

subject:
  mention: "Chaim Rosenberg"
  entity_ref: person:candidate:98431

predicate: parent_of

object:
  mention: "Sara Rosenberg"
  entity_ref: person:candidate:98432

evidence:
  source_ref: source:agad:example-register
  locator:
    act: 37
    page: 18

extraction:
  method: machine-assisted
  transcription_ref: extraction:abc123
  confidence: 0.94

status: reviewed

review:
  reviewer: curator-id
  reviewed_at: 2026-08-10

provenance:
  pipeline: genealogy-hkf-extract
  pipeline_version: 0.1
  model: example-model
  model_revision: example-revision
```

This object does **not** mean:

> Chaim Rosenberg definitely was Sara Rosenberg's father.

It means:

> This source contains evidence from which this parent-child claim was extracted and subsequently reviewed.

That distinction is foundational.

For the concrete HKF 0.1 shapes (`extraction_state`, OKF `verified`, `EvidenceLocator`), see [`HKF-SPEC.md`](/corpus/HKF-SPEC.md) §20 and [`corpus/schemas/`](./schemas/index.md). The sketch above remains illustrative.

---

# 7. How this maps to genealogy-as-code today

Much of the conceptual infrastructure already exists.

| Existing genealogy-as-code concept | Historical Knowledge Fabric role |
|---|---|
| Town bundle | Knowledge domain / bounded context |
| `sources/` | Source registry |
| `registers/` | Record-container descriptions |
| Place-name enrichment | Geographic entity-resolution rules |
| Naming conventions | Name interpretation / normalization rules |
| Data-quality reports | Source and extraction reliability signals |
| `index.md` | Progressive disclosure / concept navigation |
| `log.md` | Curation and knowledge-change history |
| PR review | Human validation gate |
| `TOWNS.md` maturity | Corpus maturity / readiness |
| Parked identity debt | Explicit unresolved-identity state |
| Reference CSVs | Controlled authorities / lookup resources |

The Historical Knowledge Fabric therefore does not require abandoning the current model.

It formalizes relationships that are already implicit in it.

---

# 8. Relationship to the repository boundaries

The existing separation among repositories remains valuable.

## genealogy-as-code

Acts as the **community knowledge and curation layer**.

It can contain:

- source descriptions;
- archive relationships;
- schemas;
- authority mappings;
- place identity;
- register knowledge;
- community-applicable interpretations;
- provenance standards;
- validation rules; and
- Historical Knowledge Fabric specifications.

It should continue to avoid becoming a bulk evidence warehouse.

---

## Private research vault

Acts as a **personal evidence and interpretation layer**.

It can consume Historical Knowledge Fabric concepts while retaining:

- person-level research conclusions;
- family hypotheses;
- private correspondence;
- DNA evidence;
- personal transcriptions; and
- researcher-specific interpretation.

A future fabric implementation could allow a personal vault to reference community entities without moving personal conclusions into the community repository.

---

## Research runtime

The `research/` directory acts as the **execution layer**.

It can contain reusable machinery that:

- locates sources;
- requests OCR;
- extracts candidate entities;
- generates claims;
- proposes identity matches;
- identifies contradictions;
- traverses linked datasets; and
- writes resulting artifacts into an appropriate knowledge store.

This creates a useful separation:

```text
                     COMMUNITY KNOWLEDGE
                    genealogy-as-code
                           │
             schemas / authorities / sources
                           │
                           ▼
SOURCE DATA ───────► RESEARCH MACHINERY ───────► DERIVED EVIDENCE
 archives                 research/             external stores
 OCR corpora                  │
 indexes                      │
                             ▼
                       PERSONAL KNOWLEDGE
                       private vault
```

---

# 9. The Historical Knowledge Fabric as layers

A practical implementation can be understood as seven layers.

## Layer 0 — Original evidence

Examples:

- archive scans;
- digitized books;
- microfilm images;
- database exports;
- cemetery images.

These normally remain in their authoritative repository or a dedicated evidence store.

---

## Layer 1 — Machine-readable representation

Examples:

- OCR;
- transcription;
- structured spreadsheet extraction;
- layout detection;
- record segmentation.

Every output should retain a pointer to Layer 0 and information about how it was generated.

---

## Layer 2 — Claims

Models or humans convert source segments into structured assertions.

Examples:

- person X appears in act Y;
- person X has occupation Z;
- place name P appears in record Y;
- source A cites source B;
- record Y describes a marriage on date D.

Claims remain independently addressable.

---

## Layer 3 — Entity resolution

Mentions are connected to candidate or established entities.

Examples:

```text
"Lemberg" ──same-place-as──► place:lviv
"Lwów"    ──same-place-as──► place:lviv
"Lvov"    ──same-place-as──► place:lviv
```

Person resolution should be much more conservative and evidence-driven.

---

## Layer 4 — Knowledge graph

Accepted relationships can now be traversed:

```text
Person
  └── appears_in ──► Record
                       └── contained_in ──► Register
                                             └── held_by ──► Archive

Person
  └── residence ──► Place
                      └── historical_jurisdiction ──► District

Register
  └── references_place ──► Place
```

Every important graph edge should remain traceable to the claims supporting it.

---

## Layer 5 — Interpretation

Multiple claims are synthesized into higher-level conclusions.

Examples:

- probable person identity;
- likely migration;
- register completeness;
- surname-variant relationship;
- changing administrative boundaries;
- probable archival succession.

Interpretation is explicitly versionable and revisable.

---

## Layer 6 — Retrieval and agents

Humans and agents can query the fabric without knowing where every underlying datum is physically stored.

A question such as:

> Which surname variants appear across Przemyślany registers between 1878 and 1890, and which variants appear to identify the same households?

might require the system to traverse:

1. the town bundle;
2. register metadata;
3. extracted record claims;
4. surname normalization guidance;
5. person-identity candidates;
6. household relationships; and
7. the supporting archive evidence.

The answer should return not only a conclusion but an **evidence path**.

---

# 10. Evidence-path retrieval

A defining property of the fabric should be:

> **No synthesized answer without a route back to evidence.**

A response should conceptually be able to provide:

```text
Conclusion
   │
   ├── supported by Claim A
   │      └── Register 1881, Act 14
   │             └── archive image / spreadsheet row
   │
   ├── supported by Claim B
   │      └── Register 1883, Act 82
   │
   └── challenged by Claim C
          └── Population Register, household 27
```

This turns explainability from an AI-interface feature into a property of the underlying knowledge architecture.

---

# 11. Contradiction should be preserved

A conventional database often tries to maintain one current value.

Historical research cannot always do that.

Suppose one source says:

```text
birth_year = 1858
```

and another says:

```text
birth_year = 1861
```

The fabric should not automatically choose one and delete the other.

Instead:

```text
Claim A
Person X → birth_year → 1858
Source: marriage act

Claim B
Person X → birth_year → 1861
Source: death record

Interpretation
Estimated birth: circa 1859–1861
Status: unresolved
```

A later birth record might resolve the discrepancy.

The claims remain part of the historical record even after the interpretation changes.

---

# 12. Knowledge updates should behave more like Git than Wikipedia

A powerful mental model is:

> **Git for historical understanding.**

New evidence should produce an interpretable change:

```text
Previous interpretation
Person A born approximately 1860.

New evidence
Birth register discovered containing probable match dated 1858.

Effect
Preferred birth year changed:
  1860? → 1858

Reason
Direct contemporary birth evidence now available.

Supporting evidence
  claim:...
  claim:...

Previous interpretation preserved
  yes
```

This makes changes explainable, reviewable, and reversible.

---

# 13. Storage architecture

The Historical Knowledge Fabric should be **storage-agnostic**.

Different representations solve different problems.

### Git / OKF

Best for:

- curated knowledge;
- schemas;
- manifests;
- provenance;
- governance;
- human-readable interpretations;
- configuration;
- small reference datasets.

### Relational / columnar storage

Best for:

- millions of source records;
- extracted claims;
- batch analytics;
- reproducible transformations.

Possible implementations include relational databases, DuckDB, and Parquet-based datasets.

### Graph representation

Best for:

- relationship traversal;
- entity networks;
- source lineage;
- historical jurisdiction;
- citation chains;
- multi-hop research.

The logical graph could be implemented using RDF, a property graph, or generated dynamically from relational data.

### Full-text search

Best for:

- exact historical wording;
- names;
- phrases;
- OCR corpus discovery.

### Vector retrieval

Best for:

- semantic similarity;
- discovering conceptually related passages;
- finding possible evidence when terminology differs.

Vector similarity should be treated as a **discovery mechanism**, not evidence by itself.

---

# 14. OKF alignment

The Historical Knowledge Fabric should continue to use OKF's core philosophy:

- plain files;
- human-readable knowledge;
- YAML frontmatter;
- stable concept identity;
- links between concepts;
- version control;
- progressive disclosure.

The project should also evaluate moving from its current OKF v0.1 basis to **OKF v0.2**.

That version is especially relevant because provenance, trust, freshness, lifecycle, and attestation are now first-class concerns.

Those concepts map directly to Historical Knowledge Fabric requirements:

| OKF concern | Historical Knowledge Fabric interpretation |
|---|---|
| Provenance | What source produced this knowledge? (`sources`, evidence locators) |
| Trust | Who checked this *representation*? (OKF `verified` → unverified / machine-confirmed / human-reviewed) |
| Freshness | When should this be revalidated? (`stale_after` — use selectively for historical evidence) |
| Lifecycle | Is this document current? (OKF `status`: draft / stable / deprecated only) |
| Attestation | Can a deterministic process verify how a result was produced? |

**Important refinement:** historical states such as disputed, superseded, parked, or candidate are **HKF domain fields**, not OKF `status` values. See [`HKF-SPEC.md`](/corpus/HKF-SPEC.md) §§8–9 and the [Relationship to HKF-SPEC](#relationship-to-hkf-spec) note above.

HKF certainty (identity `confidence`, extraction scores) MUST NOT be substituted for OKF trust.

The project should prefer adopting upstream conventions where they fit rather than inventing incompatible local equivalents.

---

# 15. Possible repository additions

The first stage does not require implementing a graph.

**Current layout** (as of HKF 0.1 draft):

```text
genealogy-as-code/
├── corpus/
│   ├── HKF-SPEC.md                      ← normative profile
│   ├── README.md
│   ├── architecture-proposal.md         ← this document
│   ├── schemas/
│   ├── predicates/core.md
│   ├── pipelines/przemyslany-pilot.md
│   ├── computations/validate-hkf.md
│   ├── examples/przemyslany/            ← bounded fixture
│   ├── okf-v02-migration.md
│   └── scripts/
│       ├── validate-hkf.py
│       └── hkf-evidence-path.py
└── research/                            ← personal research runtime
```

Town inventories live in a separate community corpus. Personal evidence stays in the researcher's vault.

These directories should only grow as corresponding concepts become concrete enough to justify them.

---

# 16. Type-system approach

The project should not immediately create many new OKF types.

The existing registry already instructs contributors to use the closest existing type with a `subtype` when a concept has not yet earned a canonical type.

That same discipline should apply here.

During experimentation, Historical Knowledge Fabric artifacts could use existing types plus explicit subtypes.

Only after repeated use demonstrates stable semantics should new types be proposed through the normal `okf-types.md` review process.

Possible eventual candidates might include:

- `Historical Claim`
- `Entity Resolution`
- `Authority Reference`
- `Historical Interpretation`
- `Provenance Manifest`

These are intentionally **candidate concepts**, not proposed registry additions yet.

---

# 17. A pilot using Przemyślany

Przemyślany is already the repository's canonical reference implementation for register-level enrichment, making it a natural Historical Knowledge Fabric pilot.

The pilot should remain deliberately small.

For example:

### Input

One well-understood register or representative subset.

### Produce

- source identifiers;
- record identifiers;
- extracted name/date/place mentions;
- candidate claims;
- candidate entity references;
- identity-resolution state;
- provenance metadata;
- a small traversable representation.

### Questions the pilot should answer

1. Can every extracted assertion be traced to its source location?
2. Can original spelling coexist with normalized identity?
3. Can two contradictory claims coexist?
4. Can unresolved identity remain unresolved?
5. Can a human reviewer approve or reject machine-generated assertions?
6. Can the same source be reprocessed by a newer model without destroying the previous extraction?
7. Can an answer generated from the graph show its complete evidence path?
8. Can the derived data live outside Git while its schema, provenance, and curation state remain in Git?

If these cannot be demonstrated on one controlled register, scaling the architecture would be premature.

---

# 18. Example research traversal

Imagine a future researcher asks:

> Did members of the same extended family appear in both Przemyślany and another nearby registration center between 1875 and 1900?

A fabric-aware agent might:

1. identify candidate surname variants using naming guidance;
2. find claims containing those variants;
3. resolve historical place names;
4. identify possible person matches;
5. compare parents, spouses, occupations, witnesses, addresses, and dates;
6. reject implausible matches;
7. traverse nearby town bundles;
8. consult additional digitized collections;
9. distinguish confirmed relationships from hypotheses; and
10. return both its proposed interpretation and the evidence supporting each step.

The important innovation is not that an LLM can write an answer.

The innovation is that the system can preserve the **research path** that made the answer defensible.

---

# 19. Reprocessing and continuous reinterpretation

Historical knowledge should be designed for repeated processing.

Suppose:

```text
2026:
OCR model A processes a register.
```

Later:

```text
2028:
OCR model B substantially improves handwritten-name recognition.
```

The fabric should permit both extraction runs to exist.

The second does not erase the first.

Instead the system can determine:

- which values changed;
- which claims changed;
- whether identity resolutions were affected;
- which interpretations depend upon those claims; and
- which conclusions should be reviewed.

This creates **knowledge dependency tracking**.

A corrected letter on one page might eventually cause:

```text
transcription
    ↓
name extraction
    ↓
person identity
    ↓
parent-child relationship
    ↓
household reconstruction
    ↓
migration hypothesis
```

to be reconsidered.

The system should be capable of discovering that dependency instead of relying upon a researcher to remember it manually.

---

# 20. Privacy, rights, and ethical boundaries

Greater technical ability to link historical information does not automatically mean every possible linkage should be published.

The fabric should retain the repository's existing boundaries around:

- living-person information;
- confidential exports;
- collaborator-restricted material;
- personal family conclusions;
- source licensing;
- archive terms of use; and
- data that should remain local.

Access and publication policies belong alongside technical provenance.

A graph edge can be technically derivable while still being inappropriate to publish.

---

# 21. Non-goals

The Historical Knowledge Fabric is **not** intended to:

- become a universal genealogy database;
- replace GEDCOM or other family-tree exchange formats;
- automatically merge people based on name similarity;
- declare AI-generated assertions to be facts;
- commit millions of records or scans to Git;
- duplicate source repositories;
- replace archival authority;
- eliminate human curation;
- move personal-family evidence into the community corpus;
- hide contradictions in pursuit of a clean graph; or
- require one graph database, vector database, or AI vendor.

The architecture is about **portable knowledge relationships**, not a mandatory technology stack.

---

# 22. Success criteria

A mature Historical Knowledge Fabric should make the following statements true:

### Evidence

Every significant historical assertion can be traced to its supporting source.

### Reproducibility

Machine-derived knowledge records how it was generated.

### Identity

Entity matches have explicit resolution state and justification.

### Uncertainty

Disagreement and ambiguity can be represented without data loss.

### Change

A new source can alter an interpretation without rewriting prior evidence.

### Traversal

Relationships can be followed across sources, registers, places, people, collections, and external authorities.

### Human review

Important assertions and identity decisions can pass through explicit curation gates.

### Portability

The logical model is independent of a particular model provider or database.

### Scale

Bulk evidence can live outside Git while Git remains the governance and knowledge control plane.

### Explainability

An agent-generated answer can show the chain of evidence used to reach it.

---

# 23. Suggested implementation phases

## Phase 0 — Define

Adopt this architecture document as a discussion artifact.

No storage technology decision is required.

---

## Phase 1 — Align

Review the repository against OKF v0.2, especially:

- provenance;
- trust;
- freshness;
- lifecycle;
- attestation.

Determine which local conventions can now use upstream OKF conventions.

---

## Phase 2 — Model

Define only the minimum schemas necessary for:

- source segment;
- claim;
- entity reference;
- identity assertion;
- provenance.

Create small synthetic examples and validation tests.

---

## Phase 3 — Pilot

Apply the model to one constrained Przemyślany dataset.

Measure curation burden as carefully as technical success.

---

## Phase 4 — Traverse

Demonstrate a research question requiring at least:

- two source types;
- identity resolution;
- multiple claims; and
- an evidence-backed conclusion.

---

## Phase 5 — Connect

Experiment with additional external corpora or authority systems without copying them wholesale into the repository.

---

## Phase 6 — Scale selectively

Only after the model proves useful should the project decide whether a dedicated relational store, graph representation, search index, or other infrastructure is justified.

---

# 24. The broader vision

The long-term opportunity is larger than genealogy.

Historical archives contain overlapping representations of:

- people;
- families;
- towns;
- institutions;
- businesses;
- occupations;
- migration;
- property;
- political boundaries;
- religions;
- communities;
- wars;
- epidemics;
- economic activity; and
- everyday life.

Historically, those relationships have been trapped inside documents.

OCR makes the documents readable.

Entity extraction makes references discoverable.

Identity resolution makes references connectable.

Claims make evidence computable.

Provenance makes the resulting knowledge defensible.

Versioning makes changing interpretations manageable.

Traversal makes the corpus researchable as a system.

That progression is the Historical Knowledge Fabric.

---

# 25. Proposed architectural position

`genealogy-as-code` should consider the Historical Knowledge Fabric an **architectural direction rather than an immediate platform initiative**.

The project already contains several of its foundational ideas:

- knowledge represented as code;
- distributed human curation;
- source-oriented organization;
- controlled vocabularies;
- progressive disclosure;
- explicit identity debt;
- Git-based provenance;
- community versus personal knowledge boundaries; and
- separation between knowledge and underlying bulk data.

The next question is therefore not:

> Should genealogy-as-code become a knowledge graph?

The more useful question is:

> **Can genealogy-as-code define the conventions that allow historical evidence to become a trustworthy, traversable knowledge graph when and where that is useful?**

That is a substantially smaller architectural commitment.

It may also be the more important one.

If successful, `genealogy-as-code` would provide not simply curated metadata around genealogical datasets, but a reproducible bridge between **historical evidence and evolving historical understanding**.

In that model, each source remains evidence.

Each extraction has provenance.

Each identity decision is explicit.

Each claim can be challenged.

Each interpretation can evolve.

And every conclusion can still lead a researcher back to the record from which it began.