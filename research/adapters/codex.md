# Codex Adapter

Use this adapter to execute packaged routes with Codex or Cursor agents.

## Contract

- Canonical route manifest: `routes.json`
- Canonical logic files: `workflows/` and `prompts/`
- Routing skill: `skills/genealogy-autoresearch/SKILL.md`
- Agent entrypoint: `agents/genealogy-autoresearch-agent.md`
- Shared contracts: `prompts/_shared-output-contract.md`, `prompts/_shared-iteration-stop-rules.md`

## Recommended flow

1. Load `agents/genealogy-autoresearch-agent.md`.
2. Render a route payload:

```bash
python scripts/run-route.py --platform codex --route-key prompt:08-open-question-resolution --vault-path "/path/to/vault" --print-only
```

3. Paste output into Codex or Cursor chat.
4. Ask agent to run using `route_key`, shared contracts, and the mandatory Run Summary.
5. In Cursor, write pending manifest and let the stop hook finalize; elsewhere run `python3 scripts/finalize-agent-run.py` (see [reference/post-run-hooks.md](../reference/post-run-hooks.md)).

## Example prompt wrapper

```text
Load agents/genealogy-autoresearch-agent.md and run route_key=workflow:document-triage.
Use routes.json to resolve the source file.
Apply shared output and iteration stop contracts.
End with the mandatory Run Summary, then write-pending-agent-run.py or finalize-agent-run.py per reference/post-run-hooks.md.
```
