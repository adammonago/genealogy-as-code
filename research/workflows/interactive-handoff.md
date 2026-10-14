# Interactive Handoff

Produce a structured handoff packet when research identifies the correct source but automation cannot finish (login wall, subscription database, image-only browse, archive request, or anti-bot gate).

## When to Use This Workflow

Use this when another route has already narrowed the problem but blocked before retrieval:

- A prompt exited with `interactive_wall` or handoff required
- Civil-record browse planning reached a blocked portal
- Web search found the collection but not the record image

Do not use this workflow for vague "search more" problems. The target source must be identifiable.

## Step 1: Capture Context

Record:

- Source `route_key` that triggered the handoff
- Related person, open question, or gap ID
- Evidence gathered so far (do not drop partial findings)
- `return_route` to resume after manual work

## Step 2: Fill the Handoff Template

Create a filled handoff file from `[VAULT_PATH]/templates/handoff-packet.md`. Every section is required:

| Section | Requirement |
|---|---|
| Context | Person or question, source route_key, date |
| Target source | Database, collection ID, blocked step, estimated effort |
| Search parameters | Query variants, date and place filters |
| Decisive record | What the record must prove |
| Prior negative searches | Table of attempts already made |
| Manual next steps | Smallest actionable steps for a human |
| Resume instructions | `return_route` set explicitly |

Save the file under the vault (for example `references/` or next to the person note).

## Step 3: Log and Hold State

1. Log the handoff in `[VAULT_PATH]/Research_Log.md` with source route, target source, and file path.
2. Keep related Open Questions as OPEN or BLOCKED; do not mark RESOLVED.
3. Do not update `Family_Tree.md` or canonical facts from a blocked handoff alone.

## Step 4: Recommend Resume Route

After manual work completes, the human (or agent) should:

1. Update transcription or person file with Strong Signal evidence first
2. Re-run the `return_route` named in the handoff packet
3. If manual work failed, log negatives and consider `workflow:phase-planning`

## Required Output Checklist

Every run must include:

1. Completed handoff file path
2. Research_Log entry
3. Explicit `return_route`
4. Mandatory Run Summary per `agents/genealogy-autoresearch-agent.md`
