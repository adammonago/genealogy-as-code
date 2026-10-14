# Shared Iteration Stop Rules

All autoresearch prompts (`prompt:*` routes) apply these stop rules in addition to route-specific Guard clauses.

## Stop immediately

Stop the current loop and do not consume remaining iterations when any of these occur:

1. **Guard triggered**: A Guard clause fires (for example, fabrication risk, over-merge risk, or unauthorized RESOLVED status).
2. **Human handoff required**: The correct source is known but blocked by login, membership, image-only browsing, or archive access limits. Run `workflow:interactive-handoff` or produce a handoff packet using [handoff-packet.md](../vault-template/templates/handoff-packet.md) and stop.
3. **Reroute required**: The task shape matches a different route (identity bridge, civil-record browse, discrepancy resolution). Log the switch in `Research_Log.md`, name the target `route_key`, and exit the current prompt. Do not count the reroute as a failed iteration.

## Stop after reporting plateau

Stop early when progress stalls:

1. **Metric plateau**: The prompt metric is unchanged for two consecutive iterations. Report the plateau, summarize work done, and recommend the next `route_key` from [ROUTING_TABLE.md](../skills/genealogy-autoresearch/ROUTING_TABLE.md).
2. **Target exhausted**: No eligible work remains under the prompt's Goal (for example, all open questions attempted, all leaf nodes searched).

When stopping for plateau or exhaustion, still emit the mandatory [run summary](../agents/genealogy-autoresearch-agent.md#mandatory-run-summary).

## Do not stop prematurely

Continue iterating when:

- The metric improved on the latest iteration.
- A reroute was attempted but the sub-route returned actionable work for the current prompt.
- Partial progress was made and the Guard clauses still permit further search.

## Iteration boundary checklist

At the end of each iteration:

1. Run `python scripts/verify-metric.py --route-key <prompt> --vault-path <vault>` when the route is supported (`prompt:01`, `02`, `08`).
2. Record metric before and after.
3. Log negative results when searches found nothing.
4. Check reroute and handoff triggers before starting the next iteration.
