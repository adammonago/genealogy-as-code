# Local History Extraction

Extract genealogical data from digitized local history books (bygdeboker, county histories, parish records).

## Shared Contracts

- Output contract: `prompts/_shared-output-contract.md`
- Iteration stop rules: `prompts/_shared-iteration-stop-rules.md`

Agents must apply both at startup per `agents/genealogy-autoresearch-agent.md`.

## Autoresearch Configuration

**Goal**: Search digitized local history sources for mentions of your ancestral families. Extract names, dates, relationships, farm and property information, and biographical details, then convert each passage into source-cited structured claims.

**Metric**: Number of new source-cited facts extracted and logged with confidence tier

**Direction**: Maximize

**Verify**: Count new claim entries added to person files, `Family_Tree.md`, `Research_Log.md`, `Open_Questions.md`, and `Unresolved_Persons.md` during this session.

**Guard**:

- Local histories are secondary sources. Cross-reference any extracted data with primary records before treating it as established.
- When extracting from non-English sources, note the original language text alongside the translation.
- Patronymic and farm name conventions vary by region and era. Do not assume modern surname conventions apply to historical records.
- Never overwrite an existing claim without preserving prior wording and source context.
- Log negative results. A documented failed search prevents duplicate effort later.
- If a contradiction may be a same-name collision, reroute to `workflow:identity-bridge-resolution`.
- If the source book is not digitized or access is blocked, create a handoff from `[VAULT_PATH]/templates/handoff-packet.md` and exit the loop for that source.

**Iterations**: 12

**Protocol**:

0. **Check reroute and handoff triggers** before extracting claims from a new source.

1. **Identify relevant local histories**: Based on your family's geographic origins, search for:
   - Digitized local history books (bygdeboker for Scandinavian families, county histories for American families, Ortsfamilienbucher for German families)
   - National library digital collections (nb.no for Norway, polona.pl for Poland, ANNO for Austria)
   - University and historical society publications
   - FamilySearch wiki pages for the relevant parish/county

2. **Search strategies by region**:

   **Scandinavian (bygdeboker)**:
   - Search the National Library (nb.no) for the parish name + "bygdebok" or "gard og slekt"
   - Search for farm names, not surnames (pre-1900 Scandinavian records use farm names and patronymics)
   - Check the Kvien database (kvien.net) for western Norway farm lineages

   **American (county histories)**:
   - Search for "[COUNTY] [STATE] history" on Google Books, HathiTrust, or Archive.org
   - Look for biographical sections (often at the back of 19th century county histories)
   - Check USGenWeb for the relevant county

   **Central European (Ortsfamilienbucher, parish records)**:
   - Search Matricula Online (data.matricula-online.eu) for Catholic parish records
   - Search GenTeam.at for indexed Austrian records
   - Search Archion.de for Protestant German records

3. **Extract data**: For each relevant passage found:
   a. Record exact source metadata:
      - Title, author, publication year
      - Repository or URL
      - Volume, page, and image number if available
   b. Transcribe the relevant text exactly as shown (OCR cleaned only where obvious)
   c. If non-English, add:
      - Original text
      - English translation
      - Translation uncertainty notes
   d. Extract structured claims in this format:

      `Claim`: [single fact statement]
      `People`: [normalized names plus observed variants]
      `Date`: [exact date or inferred range]
      `Place`: [parish, farm, county, region]
      `Relationship`: [parent, spouse, child, tenant, owner, witness, etc.]
      `Confidence`: [Strong Signal | Moderate Signal | Speculative]
      `Evidence Type`: [direct statement | compiled lineage | editorial summary]
      `Source`: [full citation]
      `Notes`: [ambiguities, spelling variants, OCR risk]

4. **Cross-reference each claim** against existing vault files:
   - Mark as `Confirmed`, `Potential Match`, `Contradiction`, or `New Person`.
   - For contradictions, create a short contradiction note with:
     - Existing claim and source
     - New claim and source
     - Plausible explanations (same-name collision, patronymic shift, farm move, date drift, OCR issue)
     - Next primary record to resolve conflict

5. **Update the vault**:
   - Add vetted claims to person files with citations and confidence tier.
   - Create new person files for newly discovered individuals.
   - Update `Family_Tree.md` for confirmed relationship changes.
   - Log every search in `Research_Log.md`, including negative results.
   - Add unresolved identity conflicts to `Unresolved_Persons.md`.
   - Add unresolved evidence conflicts to `Open_Questions.md`.

6. **Session output block**: End each run with:
   - `New Claims Added`: [count]
   - `People Files Created`: [count]
   - `Contradictions Flagged`: [count]
   - `Negative Searches Logged`: [count]
   - `Primary Records Needed Next`: [bullet list]

## Naming Convention Notes

### Scandinavian Patronymics

- Before ~1900, most Scandinavians did not use fixed surnames
- "Rasmusen" means "son of Rasmus," not a fixed family name
- The same person may appear as "[Name] [Patronymic]" in one record and "[Name] [Farm Name]" in another
- Example: "Paul Zacharias Antonsen Lillehaug" = Paul, middle name Zacharias, son of Anton, from the Lillehaug farm

### Farm Names

- Farm names function as location identifiers, not family names
- A family moving to a new farm would take the new farm's name
- Sub-farms (husmannsplasser) may not appear in standard farm name indexes
- The same farm name may exist in multiple parishes

### Americanization

- Immigrants often simplified or anglicized their names upon arrival
- Patronymics became fixed surnames (Johannesen → Johnson)
- Farm names were sometimes kept, sometimes dropped
- Spelling varied widely (Lillehaug / Lillehaugen / Lillehauge)

## Quality Checks Before Finishing

- Every claim has a full citation and confidence tier.
- Every translation includes original text plus uncertainty notes where relevant.
- Contradictions are logged, not silently merged.
- Negative searches are documented in `Research_Log.md`.
- New or updated people are reflected in linked vault files.
