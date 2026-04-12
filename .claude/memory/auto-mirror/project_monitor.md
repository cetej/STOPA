---
name: project_monitor
description: MONITOR project — Czech intelligence terminal, fork of Crucix OSINT dashboard with CZ data sources
type: project
---

MONITOR je český fork Crucix OSINT dashboardu — geopolitický a finanční intelligence terminal rozšířený o české zdroje.

**Why:** Crucix je zaměřený na US trhy a globální OSINT. Chybí český kontext (ČNB, ČHMÚ, české zprávy). MONITOR přidává české zdroje a lokalizaci.

**How to apply:**
- Repo: https://github.com/cetej/MONITOR (private), adresář `C:/Users/stock/Documents/000_NGM/MONITOR`
- Upstream: `calesthio/Crucix` (remote `upstream`)
- Stack: Node.js 22+, ESM only, Express, zero-dep philosophy
- České zdroje v `apis/sources-cz/` — oddělené od upstream
- Implementované CZ zdroje: ČNB (kurzy), ČHMÚ (výstrahy), CzechNews (ČTK/iROZHLAS/Novinky/ČT24)
- Plánované: NÚKIB, ČSÚ, OTE, Manipulátoři.cz, Reddit CZ, narativní vrstva z Záchvěv
- Default locale: cs (locales/cs.json)
- Server: `npm run dev` → http://localhost:3117
- Vazby: dodává kontext do ZÁCHVĚV (CRI) a NG-ROBOT (editorial)
- **Frontend tooling:** Pretext (`npm install @chenglou/pretext`, github.com/chenglou/pretext) — pure TypeScript text measurement bez DOM reflow. Canvas-based měření, layout čistou aritmetikou. Relevantní pro hustý dashboard text (news feed, tabulky) kde reflow způsobuje jank. Autor: chenglou (React core, Midjourney).
- **Možné rozšíření:** Web scraping modul pro čtení stránek bez JS renderingu — `trafilatura` (Python) nebo nativní fetch+parse (Node.js). Relevantní pro české zdroje které nemají RSS/API (Manipulátoři.cz, NÚKIB).
- **TODO — vyzkoušet Firecrawl** (`firecrawl.dev`): crawl celého webu + strukturovaný JSON extract + MCP server integrace. Use case: systematické sledování českých zpravodajských zdrojů bez API. Vyzkoušet free tier (500 stránek/měsíc) nejdřív. Kombinace Firecrawl MCP + `/deepresearch` skill = silný OSINT pipeline.
- Integrační specifikace: `STOPA/research/crucix-integration-specs.md`
