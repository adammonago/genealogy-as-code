# Gemini CLI Adapter

Use this adapter to execute packaged routes with Gemini CLI.

## Contract

- Agent entrypoint: `agents/genealogy-autoresearch-agent.md`
- Canonical route manifest: `routes.json`
- Canonical logic files: `workflows/` and `prompts/`
- Routing skill: `skills/genealogy-autoresearch/SKILL.md`
- Shared contracts: `prompts/_shared-output-contract.md`, `prompts/_shared-iteration-stop-rules.md`

## Recommended flow

1. Load `agents/genealogy-autoresearch-agent.md`.
2. Render a route payload:

```bash
python scripts/run-route.py --platform gemini --route-key prompt:11-immigration-search --vault-path "/path/to/vault" --ancestor "Example Person" --location "New York" --date "1880-1910" --print-only
```

3. Paste rendered content into Gemini CLI.
4. Ask Gemini to execute per the agent spec and emit the mandatory Run Summary.
5. Finalize the session: `python3 scripts/finalize-agent-run.py` (see [reference/post-run-hooks.md](../reference/post-run-hooks.md)).

## Example prompt wrapper

```text
Load agents/genealogy-autoresearch-agent.md and execute this packaged genealogy route.
Do not alter Goal, Metric, Direction, Verify, Guard, Iterations, or Protocol.
Apply prompts/_shared-output-contract.md and end with the mandatory Run Summary, then write-pending-agent-run.py or finalize-agent-run.py per reference/post-run-hooks.md.
```
