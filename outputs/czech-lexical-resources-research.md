# Czech Vocabulary Size and Open Lexical Resources — Research Brief

**Date:** 2026-03-30
**Question:** How large is Czech vocabulary? What open-source/freely downloadable Czech dictionaries and lexical resources exist?
**Scope:** survey
**Sources consulted:** 28

---

## Executive Summary

Czech vocabulary size estimates range widely depending on what is counted. The most comprehensive historical dictionary (PSJČ) recorded ~250,000 headwords, while the modern Slovník spisovné češtiny has ~197,200 entries. With inflected forms, the MorfFlex CZ 2.1 morphological dictionary expands this to **126.9 million lemma-tag-wordform triples**, reflecting Czech's rich morphology. [INFERRED] Czech has a significantly smaller total word count than English (est. 1M+ words) but comparable to German (~135,000 active words), though cross-language comparisons are methodologically problematic. [SINGLE-SOURCE]

For open data use: the most immediately useful **downloadable** resources are MorfFlex CZ (comprehensive morphology, CC BY-NC-SA 4.0), kaikki.org Czech Wiktionary extract (68,766 words, JSONL, Wiktionary license), the Czech Wiktionary XML dump (45 MB, CC BY-SA), and the DeriNet derivational network (1M+ lexemes, CC BY-NC-SA 4.0). All academic Czech NLP resources (LINDAT) are **non-commercial only**. Pure open commercial-use resources are scarce.

---

## Detailed Findings

### 1. Czech Vocabulary Size

Czech vocabulary size is contested and depends heavily on counting methodology:

- **PSJČ (Příruční slovník jazyka českého, 1935–1957):** ~250,000 headwords across 9 volumes [VERIFIED][1] — the most comprehensive historical inventory, but includes archaic terms
- **SSJČ (Slovník spisovné češtiny):** 197,200 entries [VERIFIED][2] — modern standard Czech dictionary (online at ssjc.ujc.cas.cz)
- **ASSČ (Akademický slovník současné češtiny, in progress):** projected 120–150,000 lexical units [VERIFIED][3], currently covers A–L
- **MorfFlex CZ 2.1 (all inflected forms):** 126,906,921 lemma-tag-wordform triples [VERIFIED][4] — this counts each inflected form separately, illustrating how Czech morphology multiplies the word form space
- **DeriNet 2.3 lexemes:** 1,040,126 lemmas [VERIFIED][5] — derived from MorfFlex, represents unique lexical items
- **Wiktionary Czech extract (kaikki.org):** 68,766 distinct words documented in English Wiktionary [VERIFIED][6]
- **Czech Wiktionary (cswiktionary) entry count:** [UNVERIFIED] — XML dump is 45 MB compressed, actual entry count not extracted
- **General estimate commonly cited:** ~350,000 total words (inc. technical/archaic), ~150,000 in active use [INFERRED][7]
- **Native speaker active vocabulary:** 3,000–10,000 words; passive: 3–6× larger [INFERRED][7]

**Comparison with other languages:** [INFERRED][8]
- English: 1,000,000+ total words estimated (Harvard/Google 2010 Books project)
- German: ~135,000 active words
- French: under 100,000 active words
- Czech: ~150,000 active, morphologically highly productive

Czech's inflectional morphology means one lexeme generates 10–20+ word forms. A count of "words" in Czech is fundamentally different from English word counting.

---

### 2. Czech Explanatory and Academic Dictionaries

#### PSJČ — Příruční slovník jazyka českého
- **Entries:** ~250,000 [VERIFIED][1]
- **URL:** https://bara.ujc.cas.cz/psjc/ (online search), https://lexiko.ujc.cas.cz/texts/psjc.html (info)
- **Publisher:** Ústav pro jazyk český (Czech Language Institute, Academy of Sciences)
- **License:** Online access only — **not available as open data download** [INFERRED from site structure]
- **Format:** Web interface only
- **Definitions:** Yes — full Czech explanatory dictionary with examples
- **Note:** Digitized and searchable online but no bulk data export confirmed

#### SSJČ — Slovník spisovné češtiny (Dictionary of Standard Czech)
- **Entries:** 197,200 [VERIFIED][2]
- **URL:** http://ssjc.ujc.cas.cz/
- **Publisher:** Ústav pro jazyk český
- **License:** Online access only — **no open data download found**
- **Format:** Web interface only
- **Definitions:** Yes — full explanatory dictionary

#### ASSČ — Akademický slovník současné češtiny
- **Projected entries:** 120,000–150,000 [VERIFIED][3]
- **Current status:** A–L published as of early 2026, ongoing
- **URL:** https://www.slovnikcestiny.cz/
- **License:** No API or bulk download found [VERIFIED from site]
- **Definitions:** Yes — comprehensive modern Czech

---

### 3. Czech Foreign Words Dictionary (Slovník cizích slov)

#### ABZ.cz Slovník cizích slov — StarDict conversion
- **URL:** https://cihar.com/software/slovnik/ (Michal Čihař's conversion)
- **Download:** https://dl.cihar.com/slovnik/ (daily snapshots, ~665 KB StarDict format)
- **License:** Source ABZ.cz **prohibits redistribution** — Čihař provides a conversion script so users can generate their own copy [SINGLE-SOURCE][9]
- **Format:** StarDict (.tar.gz)
- **Entries:** Not specified; ABZ.cz has tens of thousands of foreign word entries [UNVERIFIED]
- **Definitions:** Yes — Czech explanations of foreign words
- **Bottom line:** You can download the conversion script and run it yourself, but cannot redistribute the resulting data

---

### 4. Wiktionary Czech Data

#### Czech Wiktionary (cswiktionary) XML Dump
- **URL:** https://dumps.wikimedia.org/cswiktionary/
- **Latest dump:** 2026-03-01 (`cswiktionary-20260301-pages-articles.xml.bz2`)
- **File size:** 45.0 MB compressed (bz2) [VERIFIED][10]
- **Format:** MediaWiki XML
- **License:** CC BY-SA 4.0 — freely usable with attribution, including commercial use [VERIFIED]
- **Definitions:** Yes — Czech Wiktionary entries include definitions, etymology, inflections
- **Update frequency:** Monthly

#### kaikki.org — Parsed Czech data from English Wiktionary
- **URL:** https://kaikki.org/dictionary/Czech/index.html
- **Download:** https://kaikki.org/dictionary/rawdata.html
  - Uncompressed: `cs-extract.jsonl` (260.6 MB) [VERIFIED][11]
  - Compressed: `cs-extract.jsonl.gz` (36.0 MB) [VERIFIED][11]
- **Entries:** 68,766 distinct Czech words (as documented in English Wiktionary) [VERIFIED][6]
- **Format:** JSONL — one JSON object per word, includes definitions, pronunciations, translations, inflections
- **License:** Wiktionary CC BY-SA (data origin) — cite Ylonen 2022 for academic use
- **Note:** This is Czech words **as documented in English Wiktionary**, not Czech Wiktionary itself. For Czech Wiktionary definitions, use the XML dump above.
- **Tool:** Extracted using wiktextract (https://github.com/tatuylonen/wiktextract)
- **Data freshness:** Based on 2026-03-25 enwiktionary dump [VERIFIED][11]

---

### 5. NLP Morphological and Lexical Resources (LINDAT/CLARIAH-CZ)

All resources below are hosted at https://lindat.mff.cuni.cz/repository/

#### MorfFlex CZ 2.1 — Czech Morphological Dictionary
- **Entries:** 126,906,921 lemma-tag-wordform triples [VERIFIED][4]
- **URL:** http://hdl.handle.net/11234/1-5833
- **Download:** `czech-morfflex-2.1.tsv.xz` — **238.88 MB compressed, 6 GB uncompressed** [VERIFIED][4]
- **Format:** TSV (tab-separated: lemma | positional-tag | wordform), UTF-8, XZ compressed
- **License:** CC BY-NC-SA 4.0 — **non-commercial only**
- **Publisher:** ÚFAL, Charles University (Jan Hajič et al.)
- **Released:** December 23, 2024
- **Definitions:** No — morphological data only (lemma + grammatical tag + all forms)
- **Use case:** Comprehensive morphological analysis, spell-checking, word form generation

#### DeriNet 2.3 — Czech Derivational Network
- **Entries:** 1,040,126 lexemes with 791,771 derivational + 7,598 compound relations [VERIFIED][5]
- **URL:** http://hdl.handle.net/11234/1-5846
- **Format:** TSV/custom text format
- **License:** CC BY-NC-SA 4.0 — **non-commercial only**
- **Publisher:** ÚFAL, Charles University
- **Released:** January 2025
- **Definitions:** No — derivational relationships only (e.g., "číst → čtenář → čtenářský")
- **Use case:** Word formation analysis, morphological family lookup

#### Czech WordNet 1.9 PDT
- **Entries:** 23,094 synsets (word senses), covering nouns, verbs, adjectives, adverbs [VERIFIED][12]
- **URL:** http://hdl.handle.net/11858/00-097C-0000-0001-4880-3
- **Download:** ZIP archive with XML files, **440 KB** [VERIFIED][12]
- **Format:** XML (VisDic/DEBVisDic format)
- **License:** CC BY-NC-SA 3.0 — **non-commercial only**
- **Publisher:** Masaryk University, Faculty of Informatics
- **Definitions:** Yes — synset definitions, semantic relations (hypernym/hyponym)
- **Note:** Older resource (2011); newer versions exist but licensing unclear

#### Czech Word Embeddings (SYN v9 corpus)
- **URL:** http://hdl.handle.net/11234/1-4920
- **Format:** Gzip-compressed text (word2vec format); also includes frequency files
- **Frequency vocabulary files:** word forms (71 MB uncompressed), lemmas (10 MB) [VERIFIED][13]
- **License:** CC BY-NC-SA 4.0 — **non-commercial only**
- **Use case:** Frequency lists are the practical resource here — contains all words with frequency ≥10 in SYN v9

---

### 6. Czech National Corpus (Český národní korpus / ČNK)

- **URL:** https://korpus.cz, https://ocnk.ff.cuni.cz/en/
- **Latest corpus:** SYN2025, SYN Release 14 (~5.5 billion words) [SINGLE-SOURCE][14]
- **Access model:** Free registration required — web interface (KonText) [VERIFIED][14]
- **Word frequency lists:** Accessible via KonText word list function, but **not directly downloadable as bulk files** [INFERRED from site structure]
- **License:** Custom CNC license (registration-based, non-commercial for most corpora)
- **Available for download:** Selected LINDAT-published subsets (e.g., SYN v4 on LINDAT at https://lindat.cz/repository/xmlui/handle/11234/1-1846)
- **Wiktionary frequency list:** 15,000 most-used Czech words from SYN2015 available at https://en.wiktionary.org/wiki/Wiktionary:Frequency_lists/Czech_wordlist [VERIFIED][15] — plaintext, Wiktionary CC BY-SA license

---

### 7. Spell-Checking Dictionaries

#### Czech Hunspell/LibreOffice Dictionary
- **URL:** https://github.com/LibreOffice/dictionaries/tree/master/cs_CZ
- **License:** GNU GPL
- **Format:** Hunspell format (.dic + .aff files) — word stems + affix rules
- **Use case:** Spell checking; not a semantic dictionary

#### Czech ispell dictionary for PostgreSQL
- **URL:** https://github.com/tvondra/ispell_czech
- **License:** GPL v3 [VERIFIED][16]
- **Format:** ispell (.affix + .hash)
- **Use case:** PostgreSQL full-text search in Czech

#### Svobodné slovníky (English-Czech)
- **URL:** https://www.svobodneslovniky.cz/
- **License:** GNU FDL 1.1+
- **Format:** Text/StarDict
- **Entries:** Not specified — English-Czech translation pairs, not explanatory
- **Note:** Community-maintained; working data in Git repo on their server

---

### 8. OpenStreetMap Czech Place Names

- **Download URL:** https://download.geofabrik.de/europe/czech-republic.html
- **File:** `czech-republic-latest.osm.pbf` — **882 MB** [VERIFIED][17]
- **Also available:** Shapefiles (`czech-republic-latest-free.shp.zip`), Geopackage
- **License:** ODbL 1.0 — **fully open, including commercial use** [VERIFIED][17]
- **Format:** PBF (Protobuf binary), Shapefile, or Geopackage
- **Place names:** All OSM place tags (city, town, village, hamlet, etc.) — extract with `place=*` filter using Osmium or osm2pgsql
- **Note:** To extract only place names (not full map data), use Overpass API at https://overpass-turbo.eu/ with query `[out:json]; area["ISO3166-1"="CZ"]; node[place](area); out;`

---

## Disagreements & Open Questions

1. **Total Czech vocabulary size:** Estimates range from 150,000 (active use) to 350,000+ (total including technical/archaic). DeriNet gives 1M+ lexemes if all derived forms are counted separately. No single authoritative source.

2. **ABZ.cz Slovník cizích slov license:** The redistribution prohibition creates a gray area — the data is publicly accessible online but legally cannot be repackaged. A scraping approach would violate ToS.

3. **ASSČ bulk download:** The most modern comprehensive explanatory dictionary has no published API or bulk download option. Presumably accessible only via web scraping (legally questionable).

4. **Czech WordNet newer versions:** Newer versions (2.x) exist but their licensing and download status is unclear — the 1.9 version on LINDAT is confirmed accessible.

5. **Czech National Corpus frequency lists:** The ČNK doesn't publish downloadable word frequency TSVs openly. The Wiktionary-hosted list (15,000 words from SYN2015) is the closest open alternative.

---

## Evidence Table

| # | Source | URL | Key Claim | Type | Confidence |
|---|--------|-----|-----------|------|------------|
| 1 | PSJČ info page | https://lexiko.ujc.cas.cz/texts/psjc.html | ~250,000 headwords | primary | high |
| 2 | SSJČ info page | https://ujc.cas.cz/en/elektronicke-slovniky-a-zdroje/dictionary-of-standard-czech-language/ | 197,200 entries | primary | high |
| 3 | ASSČ info page | https://www.slovnikcestiny.cz/o_slovniku.php | 120–150K projected, A–L done | primary | high |
| 4 | LINDAT MorfFlex CZ 2.1 | http://hdl.handle.net/11234/1-5833 | 126.9M triples, 238MB, CC BY-NC-SA 4.0 | primary | high |
| 5 | DeriNet ÚFAL page | https://ufal.mff.cuni.cz/derinet | 1,040,126 lexemes, Jan 2025, CC BY-NC-SA 4.0 | primary | high |
| 6 | kaikki.org Czech index | https://kaikki.org/dictionary/Czech/index.html | 68,766 distinct words | primary | high |
| 7 | Web synthesis | multiple | ~350K total, ~150K active, native 5K-65K | secondary | medium |
| 8 | Comparative vocab article | https://ititranslates.com/which-language-is-richest-in-words/ | English 1M+, German 135K | secondary | medium |
| 9 | Michal Čihař's site | https://cihar.com/software/slovnik/ | ABZ conversion script, no redistribution | primary | high |
| 10 | Wikimedia dumps | https://dumps.wikimedia.org/cswiktionary/20260301/ | 45MB bz2, 2026-03-01 | primary | high |
| 11 | kaikki.org raw data | https://kaikki.org/dictionary/rawdata.html | cs-extract.jsonl 260.6MB / 36MB gzip | primary | high |
| 12 | LINDAT Czech WordNet | http://hdl.handle.net/11858/00-097C-0000-0001-4880-3 | 23,094 synsets, 440KB ZIP, CC BY-NC-SA 3.0 | primary | high |
| 13 | LINDAT word embeddings | http://hdl.handle.net/11234/1-4920 | freq vocab files: 71MB forms, 10MB lemmas | primary | high |
| 14 | Czech NLC / CLARIN | https://ocnk.ff.cuni.cz/en/ | SYN2025, 5.5B words, registration-based | primary | high |
| 15 | Wiktionary freq list | https://en.wiktionary.org/wiki/Wiktionary:Frequency_lists/Czech_wordlist | 15,000 words from SYN2015, CC BY-SA | primary | high |
| 16 | ispell_czech GitHub | https://github.com/tvondra/ispell_czech | GPL v3, ispell format | primary | high |
| 17 | Geofabrik Czech OSM | https://download.geofabrik.de/europe/czech-republic.html | 882MB PBF, ODbL 1.0 | primary | high |

---

## Sources

1. Czech Language Institute — PSJČ info — https://lexiko.ujc.cas.cz/texts/psjc.html
2. Czech Language Institute — SSJČ info — https://ujc.cas.cz/en/elektronicke-slovniky-a-zdroje/dictionary-of-standard-czech-language/
3. ASSČ about page — https://www.slovnikcestiny.cz/o_slovniku.php
4. LINDAT MorfFlex CZ 2.1 — http://hdl.handle.net/11234/1-5833
5. ÚFAL DeriNet page — https://ufal.mff.cuni.cz/derinet
6. kaikki.org Czech dictionary index — https://kaikki.org/dictionary/Czech/index.html
7. Multiple web sources on Czech vocabulary estimates
8. Interpreters & Translators Inc — Language vocabulary comparison — https://ititranslates.com/which-language-is-richest-in-words/
9. Michal Čihař — Czech dictionary downloads — https://cihar.com/software/slovnik/
10. Wikimedia dumps — Czech Wiktionary — https://dumps.wikimedia.org/cswiktionary/
11. kaikki.org raw data downloads — https://kaikki.org/dictionary/rawdata.html
12. LINDAT Czech WordNet 1.9 — http://hdl.handle.net/11858/00-097C-0000-0001-4880-3
13. LINDAT Czech word embeddings — http://hdl.handle.net/11234/1-4920
14. Institute of Czech National Corpus — https://ocnk.ff.cuni.cz/en/
15. Wiktionary Czech frequency list (SYN2015) — https://en.wiktionary.org/wiki/Wiktionary:Frequency_lists/Czech_wordlist
16. tvondra/ispell_czech GitHub — https://github.com/tvondra/ispell_czech
17. Geofabrik Czech Republic OSM — https://download.geofabrik.de/europe/czech-republic.html

---

## Coverage Status

- **[VERIFIED]:** MorfFlex entry count and download details; kaikki.org Czech file sizes; Czech Wiktionary dump size and date; WordNet synset count and file size; OSM PBF size and license; SSJČ entry count; Wiktionary frequency list (15K words); ASSČ A–L status
- **[INFERRED]:** Total Czech vocabulary estimates (350K, 150K active); language comparisons; ČNK not providing bulk downloads; ABZ redistribution restriction
- **[SINGLE-SOURCE]:** SYN2025 reaching 5.5B words; language richness comparisons
- **[UNVERIFIED]:** Czech Wiktionary actual entry count; ABZ.cz foreign words entry count; ASSČ total published entries to date; newer Czech WordNet versions
