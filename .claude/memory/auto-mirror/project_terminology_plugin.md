---
name: ngm-terminology v2.0
description: ngm-terminology v2.0.0 — NormalizedTermDB (244K terms, 6 domains), ChainTermDB, integrated into NG-ROBOT and ADOBE-AUTOMAT
type: project
---

ngm-terminology v2.0.0 nainstalován editable v `C:\Users\stock\Documents\000_NGM\terminology-db\`.

**Why:** BioLib rozšířil termdb.db o nové domény (geografie 19K, chemie 4K, medicína 2.8K, astronomie, geologie). Starý TermDB (flat schema) nemohl číst nové normalizované schema. NG-ROBOT a ADOBE-AUTOMAT potřebují přístup k 244K+ ověřeným překladům.

**How to apply:**

## Architektura (v2.0)
- **TermDB** (flat, `en/cz/lat` sloupce) — operační DB, read-write, 1665 termínů v NG-ROBOT/terminology.db
- **NormalizedTermDB** (normalized, `terms→translations→aliases`) — referenční DB, read-only, 244K+ termínů v BIOLIB/termdb.db
- **ChainTermDB** — řetězí více DB: dotaz na obě, zápis do flat
- Auto-discovery: `find_multi_domain_db()` hledá `NGM_MULTI_DOMAIN_DB`, `~/.ngm/termdb.db`, nebo known paths

## Napojení do projektů
- **NG-ROBOT**: `claude_processor.py` — `_chain_db` (TermDB + NormalizedTermDB), `detect_article_domains()` z 0_analysis.json témat, `format_termdb_for_prompt(article_domains=...)` injektuje doménově relevantní termíny do Phase 3 promptu
- **ADOBE-AUTOMAT**: `translation_service.py` — `_build_term_hints()` batch-překládá EN texty z elementů přes NormalizedTermDB, inject glosáře do Claude system promptu před překladem

## termdb.db domény (2026-03-20)
| Doména | Termínů | CZ pokrytí |
|--------|---------|------------|
| biology | 218,138 | 35% |
| geography | 19,735 | 96% |
| chemistry | 4,020 | 99% |
| medicine | 2,800 | 100% |
| astronomy | 126 | 89% |
| geology | 68 | 100% |

## Klíčové soubory
- `terminology-db/ngm_terminology/normalized_db.py` — NormalizedTermDB
- `terminology-db/ngm_terminology/chain.py` — ChainTermDB
- `terminology-db/ngm_terminology/config.py` — find_multi_domain_db()
- `NG-ROBOT/config.py` — MULTI_DOMAIN_DB_PATH
- `ADOBE-AUTOMAT/backend/config.py` — MULTI_DOMAIN_DB_PATH
- CLI: `python -m ngm_terminology.cli lookup/stats/enrich/add/export`
