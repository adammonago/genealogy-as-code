# genealogy-as-code

A toolkit for keeping genealogical knowledge in git: a community corpus of places and sources, plus a personal research runtime that can read that corpus while family conclusions stay in a private vault.

The format is a profile of Google's [Open Knowledge Format (OKF)](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md). Historical claims, extractions, and identity decisions use the [Historical Knowledge Fabric](corpus/HKF-SPEC.md) inside that envelope.

## Why this exists

Genealogical work produces two kinds of knowledge. A community accumulates notes about places, archives, and registers: which volumes exist, how names were written, and what an index covers. A researcher accumulates people, transcriptions, and conclusions about their own family.

[Adam Monago](https://github.com/adammonago) built this toolkit while doing both. Shared notes were written as OKF documents so people could review them in git, the same way code is reviewed. Claims about what a record says were given a path back to the evidence, which became the Historical Knowledge Fabric. Personal research ran from a separate vault, using repeatable workflows adapted from [Matt Prusak's autoresearch-genealogy](https://github.com/mattprusak/autoresearch-genealogy).

Those pieces are now split on purpose. This repository holds the format and the research runtime. A community's place inventories stay in that community's own repository. A family's evidence stays in a private vault. Another researcher can start from the [bundle template](corpus/template/README.md) without inheriting someone else's towns or family.

## Author

Adam Monago. Corpus documentation and schemas are [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). The research runtime is MIT, with the Hebrew Headstone Helper exception recorded in [`research/NOTICE`](research/NOTICE).

## Further reading

These essays on [Madam I'm Adam](https://www.adammonago.com/) are the argument this toolkit implements. The [knowledge as code series](https://www.adammonago.com/tag/knowledge-as-code/) has the rest.

| Essay | What it adds here |
|---|---|
| [Knowledge as Code](https://www.adammonago.com/knowledge-as-code/) | Treat durable knowledge as a reviewable file, not a row trapped in one application. |
| [Negative Knowledge](https://www.adammonago.com/negative-knowledge/) | Keep failed searches and retired claims, labeled, so the next session does not rediscover a dead end. |
| [Knowledge Priming](https://www.adammonago.com/knowledge-priming/) | Decide what an agent reads first. A place bundle's `index.md` is that budget. |
| [Historical Knowledge Fabric](https://www.adammonago.com/historical-knowledge-fabric/) | Keep what a source says, who it refers to, and what we currently believe as separate layers. |
| [The Merge Tax](https://www.adammonago.com/the-merge-tax/) | A clean family story that cannot be walked back to its sources has spent the evidence. |

## Two halves

| Directory | What it is | License |
|---|---|---|
| [`corpus/`](corpus/README.md) | Spec, schemas, validator, bundle template, and a small public fixture | [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) |
| [`research/`](research/README.md) | Vault template, prompts, workflows, and archive guides for AI-assisted research | MIT, with the Hebrew Headstone Helper prompts under [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/). See [`research/NOTICE`](research/NOTICE). |

```text
genealogy-as-code/
├── corpus/          ← format, schemas, validator, sample fixture, bundle template
└── research/        ← personal research runtime
```

A community corpus — one directory per place, with `index.md`, `sources/`, `registers/`, and `enrichment/` — lives in its own repository. Copy [`corpus/template/`](corpus/template/README.md) to start one. This toolkit does not ship place inventories or any one project's records.

## Validate the fixture

From this repository root:

```bash
python3.11 corpus/scripts/validate-hkf.py
python3.11 corpus/scripts/hkf-evidence-path.py interpretation:przemyslany:1899:act-412:birth-year
```

Requires PyYAML and jsonschema.

## Point research at a corpus

Copy `research/.env.local.example` to `research/.env.local` and set:

```bash
VAULT_PATH="/absolute/path/to/your-vault"
OKF_BUNDLE_PATH="/absolute/path/to/your-community-corpus"
OKF_TOWN="town-slug"
```

Agents then read `{OKF_BUNDLE_PATH}/{OKF_TOWN}/index.md` as read-only community context. Family conclusions stay in the vault. HKF rules live in `corpus/`, not in the town repository. See [`research/reference/hkf-consumer.md`](research/reference/hkf-consumer.md).

## Repository boundaries

| Kind of material | Where it belongs |
|---|---|
| Spec, schemas, generic types, validator, bundle template | `corpus/` in this repository |
| Prompts, vault template, archive guides, route runner | `research/` in this repository |
| Place bundles, archive finding aids, register curation shared with other researchers of that place | A community corpus repository |
| People, transcriptions, hypotheses, correspondence, DNA | The researcher's private vault |

Do not commit credentials, living-person private data, or bulk database exports.
