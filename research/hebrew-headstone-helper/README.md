# Hebrew Headstone Helper (H3) Prompts

A collection of carefully‑crafted **AI prompts** for analysing Hebrew and Jewish headstones.

The prompts guide large‑language‑model assistants to deliver accurate transcriptions, translations, date conversions, symbol interpretations, and cultural context—helping genealogists and family historians unlock the information carved in stone.

| Prompt file | Version | Release date | Highlights |
|-------------|---------|--------------|------------|
| `H3_v7_prompt.md` | v7 | 2025‑01‑?? | Original “Hebrew Headstone Helper” prompt. |
| `H3_v8_1_prompt.md` | v8.1 | 2025‑04‑22 | Better date logic, confidence scores, multi‑image handling, formatting fixes. |

## Repository structure

```
prompts/               → all released prompt files  
README.md              → overview & usage  
CHANGELOG.md           → version‑by‑version notes  
CONTRIBUTING.md        → how to propose improvements  
LICENSE                → MIT License (for prompt text)  
examples/              → sample inputs & outputs (optional)  
```

## Quick start

1. **Packaged route (recommended)**: Run `route_key=prompt:13-hebrew-headstone` from the autoresearch-genealogy repository. The wrapper at `prompts/13-hebrew-headstone.md` loads this prompt and writes vault transcription notes.
2. **Direct use**: Pick the prompt version you need (v8.1 recommended). Copy the text **as-is** into your LLM chat.
3. Provide a headstone image or details.
4. Receive a structured, culturally sensitive report.

## Why multiple versions?

Prompts evolve. Older versions remain for replication or comparison.  
Use **v8.1** for the most accurate date conversion and clearer uncertainty reporting.

## Contributing

Feedback is welcome—see `CONTRIBUTING.md`.

## License

Prompt text is released under a Creative Commons Attribution-NonCommercial 4.0 International CC BY-NC 4.0 Public License (see `LICENSE`).  
Images in `examples/` may have separate credits.
