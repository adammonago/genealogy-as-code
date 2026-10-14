# Open Question Resolution

Systematically attack every open question in your research using web sources.

## Shared Contracts

- Output contract: `prompts/_shared-output-contract.md`
- Iteration stop rules: `prompts/_shared-iteration-stop-rules.md`

Agents must apply both at startup per `agents/genealogy-autoresearch-agent.md`.

## Autoresearch Configuration

**Goal**: For every open question in `[VAULT_PATH]/Open_Questions.md`, execute the search strategy described and attempt resolution.

**Metric**: Number of open questions with status OPEN (not RESOLVED or PARTIALLY_RESOLVED)

**Direction**: Minimize (lower is better)

**Verify**: `python scripts/verify-metric.py --route-key prompt:08-open-question-resolution --vault-path [VAULT_PATH]` (counts questions with Status OPEN or BLOCKED in Open_Questions.md)

**Guard**:
- Respect the confidence tiers. Do not mark a question as RESOLVED unless the evidence meets the Strong Signal standard (two independent sources, or one authoritative primary source).
- Mark as PARTIALLY_RESOLVED when progress is made but the question is not definitively answered.
- Do not change an answer that is already marked RESOLVED unless new contradicting evidence is found.
- When an open question is really an identity-bridge problem or a narrow browse target, reroute accordingly instead of forcing generic web search.
- On reroute or handoff, log the switch in `Research_Log.md` with source and target `route_key`, then exit the loop for that question.

**Iterations**: 10

**Protocol**:

0. **Check reroute and handoff triggers** before executing generic web search on each question.

1. **Read all open questions**: Parse `[VAULT_PATH]/Open_Questions.md`. For each question with status OPEN, extract:
   - The exact question
   - The search strategy listed
   - The decisive records that would resolve it
   - Any partial evidence already gathered

2. **Prioritize**: Attack questions in this order:
   a. High priority with HIGH solvability
   b. High priority with MODERATE solvability
   c. Medium priority with HIGH solvability
   d. Everything else

3. **Choose the right route for each question**:
   - If the key issue is same-name collision, spouse split, alias handling, or household sorting, exit this prompt and run `workflow:identity-bridge-resolution`.
   - If the question already has an exact event/place/year target and the main need is image confirmation, exit this prompt and run `workflow:civil-record-browse-planning`.
   - If the search strategy already points to a known interactive or membership database, keep the question open and create a handoff from `[VAULT_PATH]/templates/handoff-packet.md`.

4. **For each question**:
   a. Execute the search strategy or routed workflow
   b. Evaluate results against the confidence tier framework
   c. Update Open_Questions.md with findings
   d. If resolved: mark RESOLVED with date, brief statement, and source
   e. If partially resolved: mark PARTIALLY_RESOLVED with what was found and what remains
   f. If blocked: record the exact archive, collection, or portal needed next
   g. If no progress: log the searches attempted as negative results in Research_Log.md

5. **Manual handoff packet**: When the route identifies the right source but cannot finish from the current environment, create a filled handoff file from `[VAULT_PATH]/templates/handoff-packet.md`. Include all template sections, set `return_route` to this prompt, and stop the loop for that question.

6. **Cascade updates**: When resolving a question changes facts in the tree:
   a. Update Family_Tree.md
   b. Update affected person files
   c. Update Timeline.md
   d. Check whether the resolution opens new questions (add to Open_Questions.md)

7. **Report**: After all iterations, summarize: questions resolved, questions partially resolved, blocked questions with handoff packets, questions with no progress, new questions discovered.
