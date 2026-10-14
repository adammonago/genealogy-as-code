# Bundle template

Copy this directory to `{your-corpus}/{place-slug}/` and replace the placeholders in `index.md` and `log.md`.

```text
{place-slug}/
├── index.md         ← place overview
├── log.md           ← curation history
├── sources/         ← archives, microfilm, digital collections
├── registers/       ← one document per register or record group
├── enrichment/      ← naming, place names, data quality
└── playbooks/       ← local contributor guides
```

The knowledge documents describe the records. Bulk spreadsheets, scans, and database exports stay outside git.

Point a research vault at the corpus with `OKF_BUNDLE_PATH` and `OKF_TOWN`. See the repository [README](../../README.md).
