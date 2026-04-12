---
name: task_termdb_lookup_optimization
description: Zadání pro novou session — optimalizace DB lookup v NG-ROBOT fázi 3 (30s → <5s)
type: project
---

## Úkol: Optimalizace termdb.db lookup pro NG-ROBOT Phase 3

### Kontext

Fáze 3 NG-ROBOT pipeline (`claude_processor/term_verifier.py`, třída `TermVerifierV2`) ověřuje odborné termíny v přeložených článcích. Byla přepsána z LLM-based (ořezávala články) na Python-first (MorphoDiTa + termdb.db). Funguje správně — články se neořezávají. Ale DB lookup je pomalý.

### Problém

- termdb.db: **747 MB SQLite**, 246K+ termínů (tabulky: `terms`, `translations`, `aliases`, `sources`, `domains`)
- Na 60 KB článku (Grand Canyon, NG): 1079 extrahovaných substantiv → 460 po filtraci → **30s DB lookup**
- Každý kandidát = 1-2 SQL dotazy (`translations.name = ? COLLATE NOCASE` + `terms.canonical_name = ? COLLATE NOCASE`)
- Indexy existují (`idx_translations_name`, `idx_terms_canonical`) ale 460 dotazů × 747 MB = pomalé

### Cíl

Snížit DB lookup z **30s na <5s** bez ztráty accuracy.

### Soubory k práci

- `C:\Users\stock\Documents\000_NGM\NG-ROBOT\claude_processor\term_verifier.py` — nová fáze 3 (funkce `lookup_terms_in_db`, `_fast_lookup`, `_prefilter_terms`)
- `C:\Users\stock\Documents\000_NGM\terminology-db\ngm_terminology\normalized_db.py` — `NormalizedTermDB` třída, schema, lookup metody
- `C:\Users\stock\Documents\000_NGM\BIOLIB\termdb.db` — fyzická DB (747 MB)

### Možné přístupy (prozkoumat a vybrat)

**A. In-memory cache při startu:**
- Při prvním volání načíst všechny `translations.name` + `term_id` do Python dict
- Lookup = dict.get() = O(1) místo SQLite query
- Paměťová cena: ~246K entries × ~50B = ~12 MB
- Pro: nejrychlejší lookup. Proti: startup penalty (~2-5s), memory footprint

**B. Batch SQL query:**
- Místo 460 jednotlivých dotazů: jeden `WHERE tr.name IN (?, ?, ?, ...)` s 460 parametry
- SQLite zvládne IN clause do ~1000 parametrů
- Pro: minimální změna kódu. Proti: stále I/O bound na 747 MB DB

**C. SQLite FTS5:**
- Přidat FTS5 virtual table pro `translations.name`
- `unicode61` tokenizer s `remove_diacritics=2` pro český text
- Pro: fuzzy matching zdarma, rychlý. Proti: zvětší DB, potřebuje rebuild

**D. Zmenšit DB:**
- 747 MB je hodně. Zkontrolovat co zabírá místo — pravděpodobně `sources` tabulka nebo duplicity
- VACUUM, případně oddělit metadata od lookup dat
- Pro: zrychlí všechno. Proti: vyžaduje analýzu struktury

**E. Preload domény:**
- Phase 0 detekuje domény článku (biology, geography...)
- Načíst jen relevantní domény do paměti místo celé DB
- Pro: menší working set. Proti: složitější logika

### Metriky pro ověření

1. Čas DB lookup na Grand Canyon článku (nyní 30s, cíl <5s)
2. Přesnost — nesmí se ztratit žádné korekce (porovnat výstup s originálem)
3. Memory footprint — rozumný (pod 100 MB pro cache)

### Vedlejší úkol (volitelné)

Při práci s DB zkontrolovat:
- Proč je 747 MB — co zabírá místo? `SELECT name, SUM(pgsize) FROM dbstat GROUP BY name`
- Jsou tam duplicity v `translations`?
- Poznámka v `project_termdb_consolidation.md` — global_ledger.json dual-write k odstranění
