---
name: termdb_consolidation_todo
description: DB consolidation needed — remove global_ledger.json dual-write, deprecate species_names.db and terminology.db across all connected projects
type: project
---

## Konsolidace terminologických databází — TODO

termdb.db (246K+) je jediný zdroj pravdy. Tyto legacy artefakty je třeba odstranit:

**Dual-write v NG-ROBOT:**
- `extract_terms_to_global_ledger()` v `utilities.py:1188-1189` zapisuje paralelně do global_ledger.json
- **Akce:** Odstranit zápis do global_ledger.json, ponechat jen termdb.db

**Deprecated DB soubory:**
- `species_names.db` (86.5 MB) — podmnožina termdb.db, 218K species
- `terminology.db` (pár MB) — importováno do termdb, jen merge skript odkazuje
- `global_ledger.json` (~100 KB, 1105 termínů) — paralelní kopie

**Why:** Paralelní zápis vytváří riziko rozjezdu dat (termdb OK + ledger fail nebo naopak).

**How to apply:** Při příští session v NG-ROBOT:
1. Odstranit dual-write z `extract_terms_to_global_ledger()`
2. Ověřit že žádný jiný kód nečte z global_ledger.json, species_names.db ani terminology.db
3. Zkontrolovat napojené projekty: **terminology-db**, **BIOLIB** — jestli nepoužívají legacy DB

**Napojené projekty k ověření:**
- `C:\Users\stock\Documents\000_NGM\terminology-db` — NormalizedTermDB definice, merge skripty
- `C:\Users\stock\Documents\000_NGM\BIOLIB` — fyzické umístění termdb.db a species_names.db
- Případně další projekty používající `ngm_terminology` package
