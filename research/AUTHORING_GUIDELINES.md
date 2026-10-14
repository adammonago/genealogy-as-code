# Authoring Guidance for GitHub-Compatible Links

Use this policy for all authoring tools that generate Markdown for this repository.

## Core Rules

- Always emit standard Markdown links: `[Label](relative/path/to/file.md)`
- Never emit Obsidian wiki links (`[[...]]`) in GitHub output mode
- Always include `.md` extension for local note links
- Use repo-relative canonical targets, then compute the correct relative path from the current file
- Keep links case-accurate with actual filenames

## Unknown Targets

If a target is unknown:

- either emit plain text (no link), or
- emit a link to an agreed stub path and create that stub

For templates, use backticked placeholders (for example, `Person_Name`), not real links.

## Suggested Link Format Contract (for tools)

- Input intent: `entity_type`, `entity_name`, `current_file_path`
- Resolver output: `relative_markdown_path_with_md_extension`
- Renderer output: `[entity_name](resolved_relative_path.md)`

## Shared Output Contract

Genealogy autoresearch routes share one output contract. Do not duplicate it in individual prompts.

- Canonical contract: [prompts/_shared-output-contract.md](prompts/_shared-output-contract.md)
- Iteration stop rules (prompt routes): [prompts/_shared-iteration-stop-rules.md](prompts/_shared-iteration-stop-rules.md)

## Practical Prompt Snippet for Authoring Agents/Tools

When authoring or editing a route, reference the shared contract instead of pasting Output Mode text:

```text
Apply prompts/_shared-output-contract.md. For prompt routes, also apply prompts/_shared-iteration-stop-rules.md.
```
