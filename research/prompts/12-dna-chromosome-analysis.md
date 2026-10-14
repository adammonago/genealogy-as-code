# DNA Chromosome Analysis

Analyze per-chromosome ancestry data to separate parental contributions and map genetic segments to ancestor lines.

## Shared Contracts

- Output contract: `prompts/_shared-output-contract.md`
- Iteration stop rules: `prompts/_shared-iteration-stop-rules.md`

Agents must apply both at startup per `agents/genealogy-autoresearch-agent.md`.

## Autoresearch Configuration

**Goal**: Parse per-chromosome ancestry composition data (e.g., 23andMe's CSV export) to identify which chromosome copies are likely maternal vs paternal, and map ancestry segments to documented ancestor lines.

**Metric**: Number of chromosomes where the likely parental origin of each copy has been determined

**Direction**: Maximize

**Verify**: Count entries in `[VAULT_PATH]/chromosome_painting.md` where Copy 1 and Copy 2 have been assigned a likely parental origin.

**Guard**:
- Without a parent's DNA test, copy assignment is PROBABILISTIC, not definitive. Always note uncertainty.
- Do not over-interpret small segments (<5 cM). They may be noise.
- The X chromosome has special inheritance: males inherit X only from their mother. Use this as a calibration point.
- Do not conflate genetic ancestry with ethnic or national identity.
- If results contradict the documented tree in ways that suggest misattributed parentage or endogamy inflation, add hypotheses to `Open_Questions.md` and consult `reference/dna-interpretation-guardrails.md`; do not rewrite tree facts from DNA alone.

**Iterations**: 6

**Protocol**:

0. **Check guardrails** in `reference/dna-interpretation-guardrails.md` before mapping segments to named ancestors.

1. **Parse the data**: Read the ancestry composition CSV. For each chromosome (1 through 22, plus X), extract:
   - Copy 1 ancestry segments (start position, end position, ancestry label)
   - Copy 2 ancestry segments

2. **Analyze the X chromosome first** (if the subject is male):
   - Males inherit X only from their mother
   - Whatever ancestry appears on the X chromosome is 100% maternal
   - Use this as a calibration: if X is entirely [ANCESTRY-A], then [ANCESTRY-A] is at least partly maternal

3. **Identify clean separations**: Look for chromosomes where Copy 1 is predominantly one ancestry and Copy 2 is predominantly another. These are the most informative for parental assignment.

4. **Build the assignment table**: For each chromosome:
   - What ancestry dominates Copy 1?
   - What ancestry dominates Copy 2?
   - Which copy is likely maternal? (Cross-reference with X chromosome findings)
   - Confidence: High (clean separation) / Moderate (mixed) / Low (no clear pattern)

5. **Map to genealogy**: Using the parental assignments:
   - Which ancestry components are maternal? Compare against documented maternal ancestor lines.
   - Which are paternal? Compare against documented paternal ancestor lines.
   - Do the proportions make sense? (e.g., if the documented tree has 3 Scandinavian grandparents and 1 Eastern European, the genetic proportions should roughly reflect this)

6. **Analyze specific components**:
   - Count segments of each ancestry type
   - Many small segments = ancestry from many generations ago
   - Few large segments = ancestry from recent generations
   - A single large segment on one chromosome = likely from a specific recent ancestor

7. **Create the analysis file**: `[VAULT_PATH]/chromosome_painting.md` with:
   - Per-chromosome table (Copy 1 ancestry, Copy 2 ancestry, likely parent, confidence)
   - Summary of maternal vs paternal components
   - Mapping to documented ancestor lines
   - Open questions (unexpected segments, components that do not match the documented tree)
