# Contributing

## Corpus

Changes to the Historical Knowledge Fabric spec, schemas, predicates, or the Przemyślany fixture belong in `corpus/`.

Run this from the repository root before opening a pull request:

```bash
python3.11 corpus/scripts/validate-hkf.py
```

New OKF `type` values go in `corpus/okf-types.md`. Institution-specific codes stay in the community corpus that uses them.

Examples in `corpus/` must not include living-person private data or a family's conclusions.

## Research

Changes to prompts, workflows, archive guides, and the vault template belong in `research/`.

Examples must use placeholder names. Do not add real family data, local absolute paths, or secrets.

The Hebrew Headstone Helper prompt text is CC BY-NC 4.0. Keep its license notice with those files. See `research/NOTICE`.

## Licenses

`corpus/` documentation and schemas are CC BY 4.0. `research/` is MIT except for the Hebrew Headstone Helper materials named in `research/NOTICE`.
