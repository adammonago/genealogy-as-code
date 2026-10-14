# Galicia (Jewish Records)

Galicia was the Austrian crown land (1772 to 1918) that now spans southeastern Poland and western Ukraine. Jewish civil vital registration there follows Austrian administrative geography, not modern country borders. Researchers working Galician lines need three layers at once: **where the family lived**, **which Jewish center held their civil register**, and **which archive fond holds the surviving images**.

For Poland-wide tools and naming rules, see [poland.md](poland.md). For cross-national Jewish methodology, see [jewish-genealogy.md](jewish-genealogy.md).

## Key Databases

### JRI-Poland
- **URL**: https://jri-poland.org/
- **Coverage**: Indexed Jewish vital records across Galician towns. Coverage varies by town and register type.
- **Cost**: Free search (linked images and archive access depend on the source)
- **Searchable**: Yes (surname, town, record type, year range)
- **AI accessibility**: Partially AI-searchable

**Search tips:**
- Search surname-only across a JRI research area when given-name spelling is unstable.
- Treat index hits as pointers to underlying acts, not as finished genealogical proof.
- When a residence village returns no hits, look up its **Jewish center** before concluding the family was not registered (see Geographic Concepts below).

### Gesher Galicia
- **URL**: https://www.geshergalicia.org/
- **Coverage**: Galician cadastral maps, tax records, vital indexes, town histories, and the **Galician Town Locator**.
- **Cost**: Free (some collections require membership)
- **AI accessibility**: AI-searchable for indexed collections

### Gesher Galicia Town Locator
- **URL**: https://www.geshergalicia.org/galician-town-locator/
- **Coverage**: Circa 1900 mapping of every Galician settlement to administrative district, judicial district, and religious record centers (Roman Catholic, Jewish, Greek Catholic).
- **Cost**: Free (members may see extended content)
- **AI accessibility**: AI-readable for navigation; full table is large

| Locator column | Meaning |
|---|---|
| Galician Town | Village or town name |
| Administrative District | Bezirkshauptmannschaft / powiat seat |
| Judicial District | Court district (Bezirkgericht) |
| Roman Catholic Center | Parish where RC records were kept |
| Jewish Center | Kehilla / town of civil register for Jewish vitals |
| Greek Catholic Center | GC parish |

**Notation:** `BH.Town` means *Bethaus* (prayer house) subsidiary to the named center. Vitals may still route through the parent Jewish center per the locator.

### Szukaj w Archiwach (AGAD, Warsaw)
- **URL**: https://www.szukajwarchiwach.gov.pl/
- **Coverage**: Digitized images for many Galician Jewish civil registers held at AGAD (Archiwum Główne Akt Dawnych), Warsaw. Browse by fond and signature.
- **Cost**: Free
- **Searchable**: Browse-only within fond inventories
- **AI accessibility**: AI-readable for catalog pages; record images require multimodal review

### FamilySearch (Galicia collections)
- **URL**: https://www.familysearch.org/
- **Coverage**: Selected Galician Jewish metric books and census forms on microfilm. Coverage is town-specific.
- **Cost**: Free (account required)
- **Searchable**: Mostly browse-only by film and item
- **AI accessibility**: Browser-only for images

## Geographic Concepts

### Residence village ≠ Jewish civil register

A `residence` field in a vital act may name a small village while the act was **registered through a different Jewish center**. This is normal in Galicia: families lived in outlying villages but their births, marriages, and deaths were recorded at the kehilla seat named in the Gesher locator.

**Rule:** When an act names Village A in Powiat X, check which **Jewish center** held its register. The indexed act may appear under Town B, not Village A.

### Administrative vs. judicial district

Powiat (administrative) seats and judicial district seats do not always coincide. A family can appear in records filed under one district while living in another's hinterland. Use the locator's **both** columns before narrowing JRI searches to a single town filter.

### Generic locator patterns

These patterns recur across Galician towns. They are illustrative; your town's mappings live in an OKF bundle or the live Gesher locator.

| Pattern | Illustration | Research action |
|---|---|---|
| Powiat seat is Jewish center for adjacent villages | Villages near the administrative seat | Search the seat town in JRI, not only the residence hamlet |
| Same powiat, multiple Jewish centers | Outlying villages routed through a nearby kehilla | Look up the Jewish center column before abandoning the search |
| Paired towns in adjacent uyezds | Two register towns roughly 10 to 20 km apart | Search both when either town returns no hits; check marriage alegata `origin_town` both ways |
| Cross-district edge case | RC parish center and Jewish center point to different towns | Do not assume one town filter covers all record types |
| Prayer-house notation | `BH.Town` in locator | Treat as subsidiary to the named center; confirm which center received vitals |

### Cross-register searches

Families moving between neighboring register offices may leave traces in **more than one** town bundle. When alegata or index rows cite an `origin_town` outside the town you searched, pivot to that town's JRI page and OKF bundle before merging identities.

## AGAD Browse Concepts (Generic)

Many Galician Jewish civil registers at AGAD follow recurring structures. This guide documents **patterns**, not per-town signature inventories. For fond numbers, year ranges, and image sequences, use an OKF town bundle (see External OKF Context).

### Marriage registers and alegata

Marriage fonds often contain:

1. **Marriage registers** — sequential civil acts for the town or district period.
2. **Marriage alegata** — supporting documents filed with marriages: birth extracts from other towns, parental consent, military discharge, widowhood proofs.

Alegata are genealogically rich because they may name an **`origin_town`** where a spouse was born or where a supporting certificate was issued. That field can bridge families across towns that otherwise look unrelated.

### Continuation volumes

When a physical register book filled, archives sometimes opened a **continuation volume** with a new signature under the same fond. Later acts and overflow alegata may sit in the continuation, not the primary volume.

### Image sequence resets

Image numbering typically **restarts at 1** when a new signature begins. Do not carry image numbers across signatures or continuation volumes when logging browse progress or building source citations.

### Under-indexed alegata

Legacy JRI indexes sometimes emphasize register acts over alegata rows. A negative JRI search does not prove alegata were never filed. Browse planning may still be warranted when marriage acts exist but birth proof from another town is missing.

For browse handoffs, use `workflow:civil-record-browse-planning` with OKF-sourced fond metadata rather than guessing signatures from town name alone.

## External OKF Context

Per-town AGAD inventories, place-name enrichment, and register curation notes are **community corpus** data. They belong in an external OKF bundle repository, not in this archive guide.

When `OKF_BUNDLE_PATH` and `OKF_TOWN` are configured (in `.env.local` or your vault `Data_Inventory.md`), load:

```
{OKF_BUNDLE_PATH}/{OKF_TOWN}/index.md
{OKF_BUNDLE_PATH}/{OKF_TOWN}/enrichment/place-names.md
{OKF_BUNDLE_PATH}/{OKF_TOWN}/sources/
corpus/HKF-SPEC.md
corpus/README.md
```

Use OKF for signature-level browse targets, coordinator contacts, and town-specific naming clusters observed in indexes. Use HKF materials for claim/evidence/identity conventions when reasoning about register extractions — see `reference/hkf-consumer.md` in this repo. Keep person conclusions, transcriptions, and merge decisions in your vault under `VAULT_PATH`.

Repository boundaries: [toolkit README](../../README.md#repository-boundaries).

## Search Strategy

1. Identify the shtetl or village of residence using JewishGen Communities Database and Gesher Galicia resources.
2. Look up the settlement in the **Gesher Galicia Town Locator** and record its Jewish center, administrative district, and judicial district.
3. Search JRI-Poland for each relevant surname across the Jewish center town, the residence village (if indexed), and any paired register town suggested by locator patterns.
4. When `OKF_BUNDLE_PATH` is set, read the matching town bundle for archive signatures and place-name disambiguation before broad web searching.
5. Follow JRI hits to Szukaj w Archiwach or FamilySearch images; log page-level negatives when browse fails.
6. For marriage acts, scan adjacent alegata images for `origin_town` values that point to other towns.
7. Cross-check immigration and naturalization records for town-of-origin spellings in multiple languages (Polish, German, Yiddish, Ukrainian).

## Common Pitfalls

- **Filtering JRI to the residence village only.** Many acts are filed under the Jewish center, not the hamlet of residence.
- **Treating one negative town search as proof of absence.** Paired register towns and alegata `origin_town` values routinely contradict a single-town filter.
- **Assuming modern country borders match record jurisdiction.** Pre-1918 Galician acts may now sit in Polish or Ukrainian catalogs; the locator and OKF bundle clarify which archive system applies.
- **Duplicating OKF signature inventories here.** Fond lists go stale; maintain them in OKF bundles and load at runtime via `OKF_BUNDLE_PATH`.
- **Merging on surname match across towns without alegata or witness corroboration.** Galician surname concentration and patronymic naming reward slow, source-first linking.

## Related Guides

| Guide | Use when |
|---|---|
| [poland.md](poland.md) | Geneteka, Szukaj w Archiwach navigation, Polish naming rules, partition overview |
| [jewish-genealogy.md](jewish-genealogy.md) | Holocaust records, DNA endogamy, Daitch-Mokotoff, immigration ports |
| [austria.md](austria.md) | Vienna and post-migration Austrian records for Galician emigrants |
| [russia-ukraine.md](russia-ukraine.md) | Modern Ukrainian archive access for towns now in Ukraine |
