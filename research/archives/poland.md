# Poland

Polish genealogical records are extensive but access varies significantly by region and record type.

## Key Databases

### Geneteka
- **URL**: https://geneteka.genealodzy.pl/
- **Coverage**: Indexed parish records (births, marriages, deaths) across Poland. Coverage varies by voivodeship.
- **Cost**: Free
- **Searchable**: Yes (by surname, parish, event type, date range)
- **AI accessibility**: AI-searchable. Results are structured HTML tables.
- **Languages**: Polish (some English interface elements)

**Search tips:**
- Search by surname across all voivodeships first to see where the name concentrates
- For common surnames (Kowalski, Nowak), filter by specific parish or voivodeship
- Cross-reference both spouses' surnames to narrow results
- Search both masculine and feminine adjective surname forms (`Kowalski` / `Kowalska`)
- Try Latin church-name equivalents (`Joannes` / `Jan`, `Josephus` / `Jozef`, `Jacobus` / `Jakub`)
- Watch for hereditary nicknames (`przydomki`) and `vel`, `alias`, or `vulgo` style alternate-name patterns

### Szukaj w Archiwach (Search in Archives)
- **URL**: https://www.szukajwarchiwach.gov.pl/
- **Coverage**: Digitized parish register images from Polish state archives
- **Cost**: Free
- **Searchable**: Browse-only (images organized by parish, year, and record type)
- **AI accessibility**: AI-readable for navigation pages; actual records are scanned images requiring Claude multimodal for reading

### Metryki.genealodzy.pl
- **URL**: https://metryki.genealodzy.pl/
- **Coverage**: Scanned parish records, complementary to Szukaj w Archiwach
- **Cost**: Free
- **Searchable**: Yes for many indexed entry points, with linked images depending on collection
- **AI accessibility**: Index pages are AI-readable; record images still require image review

### JRI-Poland
- **URL**: https://jri-poland.org/
- **Coverage**: Jewish vital-record index across thousands of Polish towns
- **Cost**: Free search (some linked scans or follow-up access may depend on partner sites)
- **Searchable**: Yes
- **AI accessibility**: Search result tables are AI-readable

**Search tips:**
- Try town-name variants in Polish, German, Russian, and Yiddish-influenced forms
- Search surname-only first when given-name spelling is unstable
- Treat indexed year/town hits as a bridge to the underlying record, not the end of the research

### Mapa Nazwisk (Surname Map)
- **URL**: https://www.mapanazwisk.eu/en/
- **Coverage**: Modern distribution of Polish surnames
- **Cost**: Free
- **AI accessibility**: AI-searchable
- **Use**: Identifies which regions a surname concentrates in, narrowing your search area

### Gesher Galicia
- **URL**: https://www.geshergalicia.org/
- **Coverage**: Records from the former Galicia region (now split between Poland and Ukraine). Includes the Galician Town Locator for Jewish civil-register centers.
- **Cost**: Free (some collections) / Membership for full access
- **AI accessibility**: Partially AI-readable

**Galicia depth:** Austrian Galicia Jewish research (Jewish center vs. residence village, AGAD browse patterns, OKF town bundles) is covered in [galicia-jewish.md](galicia-jewish.md).

## Naming Conventions

### Przydomki (Hereditary Nicknames)
A uniquely Polish naming phenomenon. When a common surname (like Kowalski, the 2nd most common in Poland) could not distinguish families in a village, hereditary nicknames (przydomki) were used. A family might be known as "Kowalski called Prusak." Upon emigration, some families adopted the przydomek as their American surname because it was more distinctive.

### Patronymics and Regional Variations
- "-ski/-ska" suffix indicates origin from a place or manor
- "-wicz/-owicz" suffix means "son of"
- "-ek/-ak" suffix is diminutive or descriptive
- Married or daughter forms may appear as `-owa`, `-ina`, `-owna`, or `-anka`
- Church records may Latinize given names even when the family used Polish forms in daily life

### Polish Matching Rules Worth Applying

- Normalize diacritics when searching, but preserve original spellings in citations
- Search both `ł` and `l`, `ó` and `o`, `ś` and `s`, `ż/ź` and `z`
- Try historical German-influenced spellings such as `sz/sch`, `cz/tsch`, `w/v`, and `j/y`
- If a female surname appears in a married or daughter form, infer the likely base surname and search both
- Normalize place names carefully: strip archive abbreviations like `woj.`, `pow.`, `gm.`, `par.` before comparing places

## Partition-Era Complications

Poland was partitioned among Russia, Prussia, and Austria from 1795 to 1918. Records from this period are in three different languages and administrative systems:

| Partition | Records Language | Archives |
|---|---|---|
| Russian (Congress Poland) | Russian, Polish, Latin | Polish state archives |
| Prussian (Greater Poland, Silesia) | German | Polish state archives, some in German archives |
| Austrian (Galicia) | Latin, German, Polish | AGAD Warsaw (Szukaj w Archiwach), Gesher Galicia, JRI-Poland; see [galicia-jewish.md](galicia-jewish.md) |

## Belarusian Connection

If your family came from the eastern borderlands (Kresy), records may be in Belarusian, Lithuanian, or Ukrainian archives. The Brest Region of Belarus has its own genealogical resources (separate from the Polish databases listed above).

## Search Strategy

1. Start with Geneteka surname search across all voivodeships
2. Identify the voivodeship(s) where your surname concentrates
3. Use Mapa Nazwisk to confirm modern distribution
4. Search JRI-Poland for Jewish-record coverage and Metryki for parish/civil index coverage where relevant
5. Search Szukaj w Archiwach or Metryki image collections for the specific parish(es)
6. If the family was from Austrian Galicia, read [galicia-jewish.md](galicia-jewish.md): use the Gesher Town Locator, search JRI-Poland by Jewish center (not only residence village), and load per-town archive metadata from `OKF_BUNDLE_PATH` when configured
7. For immigration records, cross-reference with US naturalization records (which list exact birthplace for post-1906 applications)
