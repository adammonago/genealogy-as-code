# OCR Pipeline

How to convert scanned genealogical documents into structured, searchable Markdown notes.

## Overview

The pipeline follows four stages:

1. **Scan**: Digitize physical documents
2. **Classify**: Sort by document type and determine the best OCR method
3. **OCR and Transcribe**: Extract text from images
4. **Synthesize**: Create structured Markdown notes from the extracted text

## Tools

| Tool | Purpose | Install |
|---|---|---|
| Tesseract 5.x | Open-source OCR engine for printed text | `brew install tesseract` (macOS) or `apt install tesseract-ocr` (Linux) |
| ocrmypdf | Adds OCR text layer to PDFs | `pip install ocrmypdf` |
| ImageMagick | Image preprocessing (contrast, rotation, cropping) | `brew install imagemagick` |
| Claude (multimodal) | Reading handwritten text, old scripts, damaged documents | Built into Claude Code |
| hebrew-headstone-helper | Hebrew tombstone transcription + translation + date conversion | `prompt:13-hebrew-headstone` (uses H3 v8.1 via `hebrew-headstone-helper/prompts/`) |

## Stage 1: Scan

**For printed documents** (certificates, newspaper clippings):
- 300 DPI minimum, grayscale or color
- TIFF or PNG preferred (lossless); JPEG acceptable

**For photographs**:
- 600 DPI for prints, maximum resolution for negatives/slides
- Catalog only (no OCR needed); see Photo Cataloging below

**For handwritten documents** (letters, record books, postcards):
- Highest resolution available
- Color preferred (ink color can aid legibility)
- Photograph from directly above, evenly lit, no shadows

## Stage 2: Classify

Sort every scanned file into one of four categories:

| Category | Examples | OCR Method |
|---|---|---|
| **Printed text** | Certificates, diplomas, newspaper clippings, typed letters | Tesseract (ocrmypdf) |
| **Handwritten** | Record books, personal letters, funeral notes, genealogical charts | Claude multimodal |
| **Mixed** | Postcards (printed front, handwritten back), annotated documents | Layered: Tesseract for printed portions, Claude for handwritten |
| **Photo only** | Portraits, group photos, buildings, landscapes | No OCR; catalog metadata only |
| **Tombstone photos** | Cemetery headstones and grave markers | Claude multimodal for non-Hebrew; `hebrew-headstone-helper` for Hebrew/Yiddish inscriptions |

## Stage 3: OCR and Transcribe

### Printed Text (Tesseract)

**Basic OCR on a single image:**
```bash
tesseract input.jpg output_text
```

**OCR with language support** (for non-English documents):
```bash
tesseract input.jpg output_text -l deu    # German
tesseract input.jpg output_text -l nor    # Norwegian
tesseract input.jpg output_text -l pol    # Polish
```

**Batch OCR on a folder:**
```bash
for f in ~/Files/Genealogy/Collection/*.jpg; do
  tesseract "$f" "${f%.jpg}" -l eng
done
```

**Add OCR layer to a PDF:**
```bash
ocrmypdf input.pdf output.pdf -l eng --rotate-pages --deskew
```

**Preprocessing for difficult scans** (low contrast, skewed, stained):
```bash
# Increase contrast and convert to grayscale
convert input.jpg -colorspace Gray -normalize -sharpen 0x1 preprocessed.jpg
# Then OCR the preprocessed image
tesseract preprocessed.jpg output_text
```

### Handwritten Text (Claude Multimodal)

For handwritten documents, old scripts (German Kurrent, Fraktur), or damaged text that Tesseract cannot handle:

1. Open Claude Code
2. Ask Claude to read the image directly:
   ```
   Read the file at ~/Files/Genealogy/Collection/handwritten_record.jpg and transcribe
   all text you can see. Mark illegible portions with [unclear]. This is a [type of
   document] from approximately [date] in [language].
   ```

Claude's multimodal capabilities are often better than Tesseract for:
- Handwritten text in any language
- Faded or damaged documents
- Old printing styles (blackletter, Fraktur)
- Mixed-format documents (printed forms filled in by hand)

### Mixed Documents (Layered Approach)

For postcards and annotated documents:
1. Run Tesseract on the full image to capture printed text
2. Use Claude multimodal to read the handwritten portions
3. Combine the results in the transcription note

### Tombstone Photos (Special Route)

Most photos are catalog-only, but tombstone images are genealogical evidence and should be extracted.

1. If the inscription is Hebrew (or partly Hebrew/Yiddish), run `route_key=prompt:13-hebrew-headstone` (canonical wrapper; H3 v8.1 core at `hebrew-headstone-helper/prompts/H3_v8_1_prompt.txt`).
2. Ask for:
   - line-by-line transcription (original script)
   - English translation
   - Hebrew date conversion (if present)
   - uncertainty/confidence notes per line
3. If the inscription is non-Hebrew, use Claude multimodal directly with the standard transcription workflow.
4. Save both raw model output and cleaned transcription note for auditability.

## Stage 4: Synthesize

After OCR, create a structured note using the transcription template:

1. Copy `templates/transcription.md`
2. Fill in the YAML frontmatter (source path, document type, persons mentioned, date)
3. Paste the OCR text into the Transcription section
4. Extract facts into the Extracted Facts table
5. Add any notes about document condition or OCR quality

### OCR Quality Grading

Grade every OCR result:

| Grade | Meaning | Action |
|---|---|---|
| **Good** | Text is fully readable and extractable | Proceed to fact extraction |
| **Partial** | Some text readable, gaps or errors present | Note gaps with [unclear]; extract what is available |
| **Bad** | Most text unreadable or garbled | Re-OCR with Claude multimodal; if still bad, flag for human review |
| **Photo-Only** | No text to OCR | Catalog metadata (who, when, where) in a note |
| **Tombstone-Extracted** | Tombstone text extracted and translated | Add transcription note, extracted facts, and confidence markers |

### Quality Audit

After processing a batch of documents, create an audit file:

```markdown
| File | Category | OCR Method | Quality | Note |
|---|---|---|---|---|
| certificate_001.jpg | printed | tesseract | Good | [Transcription_Certificate_001](transcriptions/Transcription_Certificate_001.md) |
| letter_002.jpg | handwritten | claude | Partial | [Transcription_Letter_002](transcriptions/Transcription_Letter_002.md) |
| photo_003.jpg | photo_only | none | N/A | cataloged in photo index |
```

## Photo Cataloging

Photos do not need OCR but should be cataloged:

```markdown
| File | Person(s) | Approximate Date | Location | Category | Notes |
|---|---|---|---|---|---|
| portrait_001.jpg | [ANCESTOR] | ~1920 | [Studio, City] | portrait | Formal studio portrait |
| group_002.jpg | [ANCESTOR-1], [ANCESTOR-2] | ~1935 | [Location] | group | Wedding or reunion |
```

## Tips

- **Batch processing**: Process documents in groups by family line or document type, not one at a time
- **Save raw OCR output**: Keep the raw text files even after creating vault notes; they are useful for searching
- **Foreign language documents**: Install Tesseract language packs for the languages in your family's records. For languages Tesseract does not support well (e.g., old Norwegian, Polish with diacritics), use Claude multimodal
- **Parallel processing with AI**: If using Claude Code, you can ask it to process multiple documents concurrently using agents. For a large batch, this is significantly faster than sequential processing
- **When in doubt, use Claude**: If Tesseract produces garbage, do not spend time tweaking parameters. Send the image to Claude multimodal instead. The quality difference on handwritten and historical documents is usually dramatic.
- **Tombstone exception**: Do not treat tombstone photos as "photo-only." Route Hebrew inscriptions through `prompt:13-hebrew-headstone` and preserve both transcription and translation in your vault.
