# Claude Adapter

Use this adapter to execute packaged routes with Claude.

## Contract

- Agent entrypoint: `agents/genealogy-autoresearch-agent.md`
- Canonical route manifest: `routes.json`
- Canonical logic files: `workflows/` and `prompts/`
- Routing skill: `skills/genealogy-autoresearch/SKILL.md`
- Shared contracts: `prompts/_shared-output-contract.md`, `prompts/_shared-iteration-stop-rules.md`

## Recommended flow

1. Load `agents/genealogy-autoresearch-agent.md` (role hats, autonomy matrix, run summary schema).
2. Render a route payload:

```bash
python scripts/run-route.py --platform claude --route-key workflow:discrepancy-resolution --vault-path "/path/to/vault" --print-only
```

3. Copy the rendered content into Claude.
4. Ask Claude to execute the route per the agent spec and emit the mandatory Run Summary.
5. Finalize: `python3 scripts/finalize-agent-run.py` (see [reference/post-run-hooks.md](../reference/post-run-hooks.md)).

## Example prompt wrapper

```text
Load agents/genealogy-autoresearch-agent.md and execute route_key=prompt:11-immigration-search using the rendered content.
Apply prompts/_shared-output-contract.md and shared iteration stop rules.
End with the mandatory Run Summary schema from the agent spec, then write-pending-agent-run.py or finalize-agent-run.py per reference/post-run-hooks.md.
```
