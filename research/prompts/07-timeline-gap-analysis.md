# Timeline Gap Analysis

Identify gaps in your family timeline where records should exist but have not been found.

## Shared Contracts

- Output contract: `prompts/_shared-output-contract.md`
- Iteration stop rules: `prompts/_shared-iteration-stop-rules.md`

Agents must apply both at startup per `agents/genealogy-autoresearch-agent.md`.

## Autoresearch Configuration

**Goal**: For every person in Family_Tree.md with known birth and death dates, identify time periods where records should exist but are missing. Search for those records.

**Metric**: Number of "expected record gaps" remaining (life events where a record probably exists but has not been found)

**Direction**: Minimize (lower is better)

**Verify**: Count entries in `[VAULT_PATH]/timeline_gaps.md` with status OPEN.

**Guard**:
- Not every gap has a findable record. Some records were destroyed, never created, or are not yet digitized.
- Do not fill gaps with speculative data. Only add records actually found.
- When a gap already has a narrow date, place, and event target, reroute to `workflow:civil-record-browse-planning` instead of broad web search.
- When the correct database is known but blocked, create a handoff from `[VAULT_PATH]/templates/handoff-packet.md` and exit the loop for that gap.

**Iterations**: 8

**Protocol**:

0. **Check reroute and handoff triggers** before searching each gap.

1. **Build expected events**: For every person in the tree, generate a list of life events that should have created records:
   - Birth (birth certificate, baptism record)
   - Marriage (marriage certificate, church record)
   - Census appearances (every 10 years they were alive during census years)
   - Military service (if applicable based on age and era)
   - Immigration/naturalization (if immigrant)
   - Death (death certificate, obituary, burial record)
   - Property ownership (deeds, tax records)

2. **Compare against what exists**: For each expected event, check whether a corresponding record exists in the vault (person file, transcription, or citation).

3. **Identify gaps**: Create `[VAULT_PATH]/timeline_gaps.md` listing:
   - Person, expected event, expected date range, expected jurisdiction, status (OPEN/FOUND/NOT_APPLICABLE)

4. **Prioritize gaps**: Rank by:
   - Records most likely to exist and be findable (census records, vital records in well-indexed jurisdictions)
   - Records that would resolve open questions
   - Records for ancestors with the fewest existing sources
   - Gaps already narrow enough for image-level browsing in a specific register set

5. **Choose search mode**: For each high-priority gap, decide which mode fits best:
   - **Browse-first**: reroute to `workflow:civil-record-browse-planning`
   - **Search-first**: date, place, or jurisdiction still too broad for effective browsing
   - **Interactive handoff**: the correct database is known but requires login, membership, or image-only access

6. **Search or browse for missing records**:
   - For browse-first targets, exit this prompt and run `workflow:civil-record-browse-planning`
   - For search-first targets, run targeted web searches:
   - Census: `[ANCESTOR NAME] [CENSUS YEAR] census [STATE/COUNTY]`
   - Vital records: `[ANCESTOR NAME] [EVENT] [YEAR] [JURISDICTION]`
   - Immigration: `[ANCESTOR NAME] passenger [YEAR RANGE] [PORT]`
   - For interactive handoff targets, create a filled handoff file from `[VAULT_PATH]/templates/handoff-packet.md`, set `return_route` to this prompt, log in `Research_Log.md`, and exit the loop for that gap

7. **Update**: When a record is found, update the person file, timeline, and gap tracker. When a search or browse yields nothing, log the negative or blocked result.
