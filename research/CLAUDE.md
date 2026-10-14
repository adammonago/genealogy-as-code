# CLAUDE.md

Project instructions for autoresearch-genealogy.

## Configuration

Set `VAULT_PATH` to the local genealogy vault you want this repository to operate against.

Example:

`VAULT_PATH=/absolute/path/to/your/genealogy-vault`

## Project Structure

- `prompts/` — Autoresearch prompts for Claude Code. Each prompt is a self-contained research task.
- `vault-template/` — Genealogy notes starter kit. Copy into your repository workspace to begin.
- `reference/` — Methodology guides. Not meant to be modified per-project.
- `workflows/` — Step-by-step procedures for common tasks.

## Prompt Format

Every prompt in `prompts/` follows this structure:

- **Goal**: What the prompt is trying to accomplish
- **Metric**: A measurable quantity that indicates progress
- **Direction**: Whether to maximize or minimize the metric
- **Verify**: A command or check that measures current state
- **Guard**: Safety rails (what the prompt should NOT do)
- **Iterations**: How many autonomous loops to run
- **Protocol**: Step-by-step instructions for each iteration

Prompts use placeholder names: `[SURNAME]`, `[ANCESTOR]`, `[LOCATION]`, `[DATE]`, `[VAULT_PATH]`.

## Markdown Authoring Conventions

- All note files use YAML frontmatter with at minimum: `type`, `created`, `tags`
- Person files add: `name`, `born`, `died`, `family`, `confidence`, `sources`
- Transcription files add: `source`, `document_type`, `person`, `date`, `ocr_method`, `ocr_quality`
- Region files add: `confidence`
- Use standard Markdown links: `[Label](relative/path/to/file.md)`
- Never emit Obsidian wiki links (`[[...]]`) in GitHub output mode
- Always include `.md` in local note links
- File names use underscores, not spaces: `John_Smith.md`, not `John Smith.md`

## Style

- No hyphens as punctuation. Use commas, periods, colons, semicolons, or parentheses.
- No emojis.
- Source-first: every claim should cite its source. Unsourced claims should be flagged.
- Log negative results. "Searched X, found nothing" is valuable data.
- Use confidence tiers (Strong Signal / Moderate Signal / Speculative) for all claims.

## When Contributing

- All examples must use placeholder names. Zero real family names.
- Every prompt must include all 7 fields (Goal, Metric, Direction, Verify, Guard, Iterations, Protocol).
- Vault templates must have valid YAML frontmatter.
- Test that prompts work end-to-end before submitting.
