# Shared Output Contract

All genealogy autoresearch routes apply this contract. Agents must follow it even when a prompt or workflow file omits an Output Mode section.

## Markdown mode

- Output mode: GitHub Markdown.
- Use only standard Markdown links, never wiki links.
- For internal notes, generate links as `[Label](relative/path/to/file.md)` with `.md` extension.
- Resolve links against existing repo files; prefer canonical files in `people/`, `surnames/`, `transcriptions/`, and `references/`.
- If no target exists, write plain text (no link) unless instructed to create a stub note.
- Do not generate placeholder links like `Person/Name.md` or `REGION_NAME.md`.

## Evidence structure

Separate these layers in every write or report:

1. **Evidence**: What a source literally says, with citation.
2. **Interpretation**: What you infer from evidence, with confidence tier.
3. **Open questions**: What remains unresolved or blocked.

## Confidence tiers

Use exactly one tier per claim:

- **Strong Signal**: Two independent sources, or one authoritative primary source.
- **Moderate Signal**: One credible secondary source, or partial primary evidence.
- **Speculative**: Hypothesis only; not ready for canonical vault facts without review.

## Canonical file discipline

When updating shared vault files (`Family_Tree.md`, `Timeline.md`, `Research_Log.md`, `Open_Questions.md`):

- Log negative results, not only successes.
- Do not mark facts RESOLVED unless evidence meets Strong Signal standard.
- Propagate corrections to all affected canonical files when a route requires it.

## Related references

- Link authoring rules: [AUTHORING_GUIDELINES.md](../AUTHORING_GUIDELINES.md)
- Confidence framework: [reference/confidence-tiers.md](../reference/confidence-tiers.md)
- Source hierarchy: [reference/source-hierarchy.md](../reference/source-hierarchy.md)
