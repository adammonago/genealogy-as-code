# Civil Record Browse Planning

How to plan an image-level civil-record browse when the problem is already narrow enough that generic web search is no longer the best tool.

## When to Use This Workflow

Use this when you already have a tight target such as:

- a known person, event type, place, and approximate year
- an indexed or derivative citation that still needs image confirmation
- an open question whose best next step is browsing a specific register rather than searching the open web

Typical examples:

- Italian civil-registration books on Antenati
- FamilySearch image-only catalog collections
- state-archive browse sets with year and volume structure

## Step 1: Define the Record Target

Write the target in one line:

- person
- event type
- date or date range
- jurisdiction
- why this record matters

Example:

- `Giuseppe Leone + Maria Elimena Trifia Di Vittorio`, marriage, `1854`, Pettorano sul Gizio, needed to confirm the direct-line couple bridge

## Step 2: Separate Collection Map From Working Surface

For the target record set, identify:

- **Collection map**: the catalog or finding aid that proves the records exist
- **Working surface**: the actual portal where images are likely to be browsed

Do not assume these are the same.

Examples:

- FamilySearch catalog as collection map, Antenati as working surface
- archive inventory page as collection map, local image viewer as working surface

## Step 3: Build a Browse Packet

Create a compact packet with:

- target person and event
- known date anchors
- exact place hierarchy
- likely register type (`nati`, `matrimoni`, `morti`, banns, processetti, supplements)
- candidate year books
- known film, DGS, item, archive unit, or volume identifiers
- expected naming variants

## Step 4: Define the Browse Order

Order the search from highest yield to lowest:

1. Exact year and exact event book
2. Neighboring years if the date may drift
3. Supplemental packets tied to the same event
4. Parent or child linked records that may confirm the same relationship indirectly

If the record predates civil registration, stop and reroute to parish or alternate archive research rather than pretending the same browse will work. Log the reroute in `Research_Log.md` with the target approach.

## Step 5: Set Stop Conditions

Before browsing, define what counts as:

- **Found**: image located and core facts extracted
- **Partial**: likely book or page range located but image not yet legible or not fully confirmed
- **Blocked**: images restricted, portal unavailable, or route requires membership / archive visit
- **Reroute**: wrong jurisdiction, wrong date range, or civil registration not yet in force

## Step 6: Produce One of Two Outputs

### If browsing is possible now

Produce a browse plan that lists:

- collection map
- working surface
- exact target books
- order of attack
- variant names to watch for
- what fields to extract if found

### If browsing is blocked

Create a filled handoff file from `[VAULT_PATH]/templates/handoff-packet.md`. Include:

- the exact collection or archive
- the blocked step
- the best manual next move
- the smallest set of screenshots, logins, or archive references needed to resume later
- `return_route` set to the workflow or prompt that should resume after manual work

Log the handoff in `Research_Log.md`.

## Step 7: Update the Vault Carefully

After the browse:

- update the person file or transcription note first
- then update Family_Tree.md, Timeline.md, and Open_Questions.md if the record changes shared facts
- if the record is not found, log the negative or blocked result explicitly

## Required Output Checklist

Every run of this workflow should explicitly include:

1. Target record statement
2. Collection map
3. Working surface
4. Target books / years
5. Browse order
6. Stop conditions
7. Manual handoff file from `[VAULT_PATH]/templates/handoff-packet.md` if blocked
