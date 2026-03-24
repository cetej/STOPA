---
name: CZ Sources Expansion + LLM Polish
description: Session 2026-03-22 — přidání NÚKIB/ČSÚ/OTE zdrojů, GSAP fix, LLM polish, Záchvěv CRI integrace
type: project
---

## Session 2026-03-22 — Nové CZ zdroje + integrace

### Blok 1: 3 nové CZ zdroje (HOTOVO)
- **NÚKIB** (`apis/sources-cz/nukib.mjs`) — kybernetické hrozby, RSS feed + fallback scraping, severity klasifikace (critical/high/elevated/normal)
- **ČSÚ** (`apis/sources-cz/czso.mjs`) — makro data z RSS, kategorizace (gdp/inflace/nezaměstnanost/průmysl/obchod/mzdy), extrakce číselných hodnot
- **OTE** (`apis/sources-cz/ote.mjs`) — denní trh elektřina + plyn, JSON API + XML + summary page fallback, cenové prahy

Všechny registrovány v `briefing.mjs` (Tier 6), `inject.mjs`, `briefing-generator.mjs` (LLM kontext + rule-based fallback).
Boot animace rozšířena o řádek CZ zdrojů.
Celkový počet zdrojů: 34 (27 upstream + 7 CZ).

### Blok 2: GSAP Boot Animation Fix (HOTOVO)
- Race condition: SSE update během boot animace (0-5s) způsoboval DOM re-render a rozbíjel GSAP timeline
- Fix: `bootAnimating` flag, `pendingSSEData` buffer, `onComplete` callback na timeline
- Odstraněny `setTimeout` chains uvnitř `tl.call()` — nahrazeny přímými `tl.from()` na timeline
- GSAP availability guard pro případ, kdy CDN selže

### Blok 3: LLM Polish (HOTOVO)
- `cleanLLMText()` v `lib/llm/provider.mjs` — stripuje soft-hyphen, zero-width chars, NBSP
- Aplikováno ve všech LLM providerech + `parseBriefingResponse()`
- Prompt tuning: seniorní analytik ČR, české zdroje s vyšší váhou, kauzální řetězce místo korelací
- Model escalation: NÚKIB critical → Sonnet, multi-crisis detection (2+ simultánních krizí)
- Rule-based fallback rozšířen o NÚKIB kyber alerts a OTE energy price body

### Blok 4: Záchvěv CRI Integrace (HOTOVO)
- `apis/sources-cz/zachvev-cri.mjs` — optional cross-project source
- Dotazuje Záchvěv FastAPI na localhost:8000 (3s timeout)
- Graceful degradation: vrací `available: false` když Záchvěv offline
- CRI data předávána do LLM briefing kontextu

**Why:** Rozšíření o české datové zdroje je klíčové pro relevanci MONITOR pro CZ analytiky. Záchvěv integrace propojuje social media cascade detection s OSINT dashboardem.

**How to apply:** Při dalším rozšiřování CZ zdrojů dodržovat pattern v `apis/sources-cz/` — async `briefing()` export, `fetchText()` helper, graceful degradation, signals array.
