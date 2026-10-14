---
type: handoff
status: ready_for_manual
return_route:
database_or_archive:
collection_id:
estimated_effort: browse
created: YYYY-MM-DD
tags: [genealogy, handoff]
---

# Handoff: [Short title]

Use this template when research identifies the right source but cannot finish in the current environment (login wall, subscription database, image-only browse, archive request, or anti-bot gate).

Copy this file into your vault (for example under `references/` or next to the person note) and fill every section before closing the agent run.

## Context

- **Related person or question**: [Person name or Open_Questions.md entry]
- **Route that produced this handoff**: [route_key]
- **Date**: YYYY-MM-DD

## Target source

| Field | Value |
|---|---|
| Database or archive | [Name and URL if known] |
| Collection ID / film / DGS / archive unit | [Identifier] |
| Blocked step | [What automation could not complete] |
| Estimated effort | browse \| login \| subscription \| archive_request |

## Search parameters

### Query variants

- [Variant 1]
- [Variant 2]

### Date and place filters

- [Date range or exact year]
- [Place, district, parish, or ED if applicable]

## What the decisive record must prove

State the fact or relationship this record needs to establish:

- [Decisive proof statement]

## Prior negative searches

Log what was already tried so manual work does not repeat dead ends:

| Query or browse target | Result |
|---|---|
| [Search or browse attempt] | [Nothing found / wrong person / blocked] |

## Manual next steps

1. [Smallest actionable step, for example open collection X and browse book Y for year Z]
2. [Optional: screenshots, logins, or archive references needed]
3. [Where to record findings when complete]

## Resume instructions

When manual work finishes:

1. Update the related person file or transcription note with evidence first.
2. Update `Open_Questions.md`, `Family_Tree.md`, or `Timeline.md` only if Strong Signal evidence supports the change.
3. Re-run the route in `return_route` with a note that the handoff is complete.

**return_route**: [route_key to resume, for example `prompt:08-open-question-resolution`]
