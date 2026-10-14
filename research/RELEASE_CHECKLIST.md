# Public Release Checklist

Use this checklist before creating a public tag or GitHub release.

## License and Attribution

- [ ] Confirm all bundled dependencies and assets are license compatible.
- [ ] Confirm `LICENSE`, `NOTICE`, and `THIRD_PARTY_LICENSES.md` are present and accurate.
- [ ] Confirm README provenance links are current.

## Sensitive Data and Content Review

- [ ] Verify no private or proprietary data is present in tracked files.
- [ ] Perform a history review for accidentally committed secrets or credentials.
- [ ] Remove or rotate any exposed secret before release.

## Release Metadata

- [ ] Update `CHANGELOG.md` with upstream base reference and local deltas.
- [ ] Create an annotated tag (example: `v0.1.0`).
- [ ] Push branch and tags, then draft a GitHub release from the tag.

## Recommended Commands

```bash
git status -sb
git log --oneline --decorate -n 20
git tag -a v0.1.0 -m "Release v0.1.0"
git push origin main --tags
```
