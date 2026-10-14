# Hebrew Headstone Extraction

Transcribe, translate, and interpret Hebrew or Yiddish tombstone inscriptions using the Hebrew Headstone Helper (H3) prompt, then write structured vault notes.

## Shared Contracts

- Output contract: `prompts/_shared-output-contract.md`
- Iteration stop rules: `prompts/_shared-iteration-stop-rules.md`

Agents must apply both at startup per `agents/genealogy-autoresearch-agent.md`.

## When to Use

- Tombstone or cemetery inscription photos with Hebrew, Yiddish, or mixed-script text
- Find a Grave memorials with headstone images needing Hebrew extraction
- Document triage or OCR pipeline routes a tombstone here instead of generic multimodal OCR

For non-Hebrew tombstones, use `workflow:ocr-pipeline` with standard multimodal transcription.

## H3 Analysis Core

Execute the canonical Hebrew Headstone Helper prompt in full:

`hebrew-headstone-helper/prompts/H3_v8_1_prompt.txt`

Do not paraphrase or shorten the H3 steps. Apply all sections: image intake, transcription, translation, date interpretation, physical description, symbols, cultural context, ethical guidelines, uncertainty handling, and response template.

H3 prompt text is licensed CC BY-NC 4.0. See `hebrew-headstone-helper/LICENSE`.

## Autoresearch Configuration

**Goal**: For the headstone image(s) supplied for `[ANCESTOR]` (or the person named in triage context), produce a complete H3 analysis and save it as a source-cited transcription note in the vault. Cross-reference extracted facts against existing person files without overwriting Strong Signal facts silently.

**Metric**: Number of required transcription sections completed with confidence scores (transcription, translation, date information, physical description, symbols, cultural context, overall uncertainty)

**Direction**: Maximize

**Verify**: Confirm a transcription note exists under `[VAULT_PATH]/` with `document_type` including tombstone or headstone, H3 sections present, and `ocr_method` set to `hebrew_headstone_helper`.

**Guard**:
- Do not invent inscription text. Mark illegible segments as `[unclear]` per H3 rules.
- Keep transcription (literal text) separate from translation and interpretation.
- Do not treat H3 translation or date conversion as Strong Signal for canonical tree facts without independent corroboration.
- If multiple stones appear in one image batch, label each stone A, B, C and process separately.
- If image quality blocks reliable reading, request additional images before guessing.
- If the person cannot be matched to an existing vault record, create a transcription note and log the ambiguity in `Open_Questions.md`; do not force a person-file merge.

**Iterations**: 2

**Protocol**:

0. **Check inputs**: Confirm image(s) are available. If none, stop and request images. Read `[ANCESTOR]` person file and related notes when `[ANCESTOR]` is provided.

1. **Run H3 analysis**: Load and execute `hebrew-headstone-helper/prompts/H3_v8_1_prompt.txt` against the supplied image(s). Preserve confidence scores and uncertainty notes from every H3 section.

2. **Create transcription note**: Copy `[VAULT_PATH]/templates/transcription.md` and fill:
   - `document_type`: `tombstone` or `headstone`
   - `person`: linked person name(s)
   - `ocr_method`: `hebrew_headstone_helper`
   - `ocr_quality`: from H3 image quality assessment
   - Transcription section: original script with line breaks preserved
   - Add subsections for Translation, Date Information (Hebrew and Gregorian), Symbols, and Cultural Context from the H3 output
   - Extracted Facts table with confidence per fact

3. **Cross-reference vault**:
   - Compare names, dates, and relationships against the person file and `Family_Tree.md`
   - Log contradictions in the transcription note and person file `## Data Discrepancies` when needed
   - Do not update canonical dates without Strong Signal or explicit discrepancy resolution

4. **Log the session**: Record the analysis in `[VAULT_PATH]/Research_Log.md` with image source, route_key, and any negative or blocked results (missing images, ambiguous person match).

5. **Report**: Summarize sections completed, confidence highlights, open ambiguities, and recommended next route (for example `workflow:discrepancy-resolution` if dates conflict, or `prompt:03-findagrave-sweep` if memorial link was the entry point).

## Vault Output Checklist

Every run should produce:

1. H3 analysis output (in transcription note or attached reference)
2. Transcription note with original script and English translation
3. Hebrew date conversion with confidence when dates appear
4. Research_Log entry
5. Mandatory Run Summary per `agents/genealogy-autoresearch-agent.md`
