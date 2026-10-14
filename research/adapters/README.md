# Cross Platform Adapters

Adapters keep one canonical backend while providing platform specific invocation wrappers.

## Files

- `adapters/claude.md`
- `adapters/codex.md`
- `adapters/gemini.md`

## Shared runtime pieces

- `routes.json`: machine readable route registry
- `scripts/run-route.py`: route validation and placeholder rendering
- `workflows/` and `prompts/`: canonical execution logic
