---
name: PREKLAD
description: PREKLAD — translation pipeline EN→CZ pro NG-ROBOT RTT files (PDF/DOCX → strukturovaný CZ DOCX), FastAPI+HTMX UI, fork z NG-ROBOT/ADOBE-AUTOMAT s critic-revise loopem
type: project
originSessionId: 57ea8e53-fe72-44e8-a188-0332b9f12df0
---
PREKLAD je standalone překladatelský klon NG-ROBOT pipeline, založen 2026-04-27.

**Cesta:** `C:/Users/stock/Documents/000_NGM/PREKLAD`
**Repo:** cetej/PREKLAD (zatím jen lokálně)
**Stack:** Python 3.11+, FastAPI, HTMX, Alpine.js, Tailwind (CDN), pdfplumber + pdf2docx, python-docx, anthropic SDK
**Termdb:** sdílená `C:/Users/stock/Documents/000_NGM/BIOLIB/termdb.db` (z ngm-terminology, single source of truth)

**Architektura:** 8-phase adaptive pipeline:
- Phase 0: RTT analyzer (deterministic, doména/komplexita)
- Phase 1: Translator (Claude API + master prompt v1, port z NG-ROBOT v42.2.6)
- Phase 1.6: Glossary enforcer (termdb hard binding, port z ADOBE-AUTOMAT)
- Phase 5: Czech context (false friends, anglicismy, port z ADOBE-AUTOMAT)
- CzechCorrector (deterministic typografie)
- Phase 6: Critic agent (3-5 suspect spans, JSON)
- Phase 7: Targeted revision (max 2 iterace)
- Phase 8 optional: Domain critic (biology/geo/history)

**Adaptive depth:** Krátký RTT (<500w) skipuje Phase 5/6/7. Dlouhý jede full pipeline + critic loop.

**RTT input:** PDF (přes pdf2docx hybrid: pdfplumber pro body + pdf2docx pro sidebar text frames) nebo přímo DOCX. Line-numbered structure jako primary join key (`^\d+(-\d+)?:`). Translator letter ("Dear Editors and Translators:") = METADATA, NEPŘEKLÁDAT.

**Outputs:** strukturovaný CZ DOCX, side-by-side EN|CZ DOCX, audit JSON s line mapping.

**UI:** http://127.0.0.1:8000/ — drag&drop upload, SSE live progress, dark mode toggle, IBM Plex Serif/Sans typografie, sage/terracotta paleta (anti-slop compliant — žádný Inter/Roboto, žádný violet gradient).

**Live test ověřen:** Rainbow Lizards (225 slov) projel Phase 0+1+1.6+CzechCorrector, vyprodukoval validní CZ DOCX (38KB) + side-by-side (40KB). Sample: "MOHOU NÁS TYTO DUHOVÉ JEŠTĚRKY NAUČIT NĚCO O EVOLUCI?". Critic loop ještě neověřen na long-format (Okavango).

**Tests:** 109/109 pass (parser 45 + pipeline 31 + exporter 24 + api 9).

**Open issues:**
- Job queue in-memory only (restart = ztráta historie)
- Phase 6/7 critic loop neověřený na dlouhý format
- PDF sidebar extraction je hybridní/fragilní
- Žádná autentizace (open localhost-only)

**2026-04-28 fix — Species genus consensus (cross-project, NG-ROBOT + ADOBE-AUTOMAT + PREKLAD):**
- Phase 1.6 + lookup_terms_for_article rozšířen o genus-level fallback. Ceratogyrus
  attonitifer (nový druh, není v termdb) → "nový druh sklípkana" namísto halucinace
  "tarantule"; Microctenopoma → "ostnovec"; Breviceps → "otylka"; bull elephant →
  "samec slona". Sdílená metoda v `ngm_terminology.NormalizedTermDB.lookup_genus_consensus`.
- Orchestrator: opraven TODO `termdb_misses=[]` — Phase 3 web_search nyní reálně
  spustí pro nedohledatelné druhy s genus consensus jako prompt hint.
- Master prompt v3 (PREKLAD/NG-ROBOT/ADOBE-AUTOMAT): zákaz halucinace pro druhy mimo
  termdb + collocation guard pro pohlavní dimorfismy ("bull elephant" → "samec X").
- Detail: `.claude/memory/learnings/2026-04-28-genus-consensus-cross-project.md`
