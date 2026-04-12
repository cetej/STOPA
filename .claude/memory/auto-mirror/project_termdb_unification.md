---
name: termdb_unification
description: termdb.db (246K) is the single lookup source for all terminology across NG-ROBOT, ADOBE-AUTOMAT; species_names.db keeps full taxonomy metadata
type: project
---

## Terminologická DB — sjednocení (2026-03-30)

**Před**: 4 zdroje (terminology.db, global_ledger.json, species_names.db, termdb.db) s chaotickým chain lookupem. Termíny se primárně ověřovaly proti malé 1.7K cache nebo rovnou na internetu.

**Po**: `termdb.db` (246,603 termínů) = JEDINÝ lookup zdroj. `species_names.db` = živá taxonomická DB s plnými metadaty (rank, wikidata, sources), enricher zapisuje do obou.

**Why:** Uživatel explicitně požadoval jednu fungující DB s lokálním lookup a web search až jako fallback.

**How to apply:**
- Všechny lookup operace jdou přes `NormalizedTermDB` (termdb.db)
- Nové termíny: `_main_db.add_term()` (normalized schema)
- Nové druhy: enricher → species_names.db (metadata) + termdb.db (flat)
- `terminology.db` a `global_ledger.json` jsou legacy — zachovány na disku ale ne v lookup chain
- ADOBE-AUTOMAT a NG-ROBOT sdílí stejný termdb.db přes BIOLIB cestu
- KARTOGRAF zatím nepoužívá term DB

**Dotčené soubory (klíčové):**
- `NG-ROBOT/claude_processor.py`: `_main_db` (NormalizedTermDB)
- `ADOBE-AUTOMAT/backend/services/text_pipeline/phases.py`: `_main_db`
- `terminology-db/ngm_terminology/normalized_db.py`: `add_term()`, canonical_name search
- `terminology-db/ngm_terminology/enricher.py`: dual-write
