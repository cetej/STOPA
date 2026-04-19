---
name: project_monitor
description: MONITOR project — Czech intelligence terminal, fork of Crucix OSINT dashboard with CZ data sources
type: project
originSessionId: 0d64be25-97b8-44dc-a7d7-8a726d816abf
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
- **WorldMonitor adoption (2026-04-19, Sprint 1 done, commit b5fdb60):** Clean-room adoption z koala73/worldmonitor (AGPL-3.0, 48.9k★). Tier A deliverables:
  - `apis/sources/_source-tiers.mjs` (83 klasifikovaných zdrojů, 4-tier system)
  - `apis/sources/_registry.mjs` (60 feedů, 14 CZ)
  - `scripts/validate-feeds.mjs` (health checker, 80% T1 OK, 86% CZ OK)
  - `scripts/check-unicode-safety.mjs` (Trojan Source + zero-width detector)
  - `docs/WORLDMONITOR-ADOPTION-PLAN.md` — roadmap Sprint 1-5 (Tier A done, B/C/D pending)
  - `NOTICE.md` — AGPL atribuce Elie Habib
- **Sprint 2 done (2026-04-19, commit 6b88583):** 3 core intelligence modules
  - `apis/sources/_cache.mjs` — LRU + failure cooldown (5min po 2 failech)
  - `apis/sources/_classifier.mjs` — CZ+EN regex classifier, 4 severity × 17 categories, Unicode-aware \p{L} lookaround pro české koncovky
  - `apis/sources/_cluster.mjs` — Jaccard + time window multi-source clustering
  - `scripts/smoke-test-sprint2.mjs` — E2E test, reálný výsledek: 215 článků → 32 klasifikovaných → 16 clusters (3 multi-source). Top: 6 zdrojů o Vystrčilovi
  - Bug fix learnings: \b ASCII boundary fails on Czech inflections (→ \p{L}), krátké keywords ("let") trigger false positives, bash inline template literals unreliable
- **Sprint 3 done (2026-04-19, commit f872fdb):** Core intelligence pro CZ
  - `apis/sources/_regions-cz.mjs` — 14 krajů, ČSÚ kódy, 157 stemmed aliasů, curated landmark allowlist, czechStem() helper pro flexe ("Pardubicích"/"Ostravě"/"Praze" → správný kraj)
  - `apis/sources/_region-index.mjs` — RegionCZ Index (unrest/security/info/cyber × 0.25 + baselineRisk), final 0-100 + severity label
  - `apis/sources/_hotspots-cz.mjs` — 16 hotspotů (2 jaderné, 3 energetické, 4 hraniční, 1 cyber, 2 politické, 2 transport, 2 průmyslové), combined score s trend detection
  - `apis/sources/_correlation.mjs` — extensible adapter framework, 2 builtin (disinfo, cyber-geopol), convergence alerts
  - `scripts/smoke-test-sprint3.mjs` — E2E: 215 článků → top region scores + hotspot trends + convergence
  - Reálný výsledek: Jihomoravský 32/moderate, Praha 30, Pardubický 30; Parlament ČR rising hotspot (38, 12 článků)
  - Learning: Czech stemming není triviální — "Karlovy Vary" locative "Karlových Varech" → EXTRA_STEMS hint, "Praha"/"Praze" (h→z) dtto. Landmark auto-extraction vypnuta (false positives "Škoda"/"Vláda").
- **Sprint 4 done (2026-04-19, commit b1a98f4):** Intel Layer + HTTP API
  - `apis/intel-layer.mjs` — integrační pipeline: registry → cache → classify → {regions, hotspots, correlation, clusters}, s getCachedIntel() 15min cache + sweepInFlight concurrent-dedupe
  - `server.mjs` — 4 nové endpointy: GET /api/intel, /api/intel/regions, /api/intel/hotspots, /api/intel/correlate + hourly intelMaintenance()
  - CLI: `npm run intel` (human), `npm run intel:json`
  - Shared parseFeedXml() — eliminace duplicit ze smoke-test skriptů
  - Benchmark: cold 520ms, warm 0ms, 5 concurrent calls = 49ms (shared sweep)
- **Refinement done (2026-04-19, commit cfcc9c6):** 8 security/perf/API fixes po code review — SSRF guard, ReDoS cap, Jaccard(∅,∅)=1, hotspot dedupe, pre-compile regex, pubDate future cap, tier API (tier vs tierExact), pruneExpired()
- **Sprint 5 done (2026-04-19, commit 1f54b0d):** Intel frontend visualization
  - `dashboard/public/intel.html` — standalone (~640 řádků), zero-dep kromě Google Fonts
  - SVG cartogram ČR (14 krajů, centroid-based 2D grid, barva podle severity)
  - Top regions table s 4-component breakdown, active hotspots s trend, correlation streams + alerts, multi-source clusters, feed health strip
  - MONITOR design tokens: IBM Plex Mono + Space Grotesk, `#0a0c10` bg, 1px borders, sharp corners (per DESIGN.md)
  - Auto-refresh 5 min + countdown footer + manual REFRESH
  - Route `GET /intel` v server.mjs
  - Verified HTTP: 200 OK, 20871 bytes HTML, JSON API response 215 articles / 14 regions / 3 hotspots
- **Dostupné:** http://localhost:3117/intel (dev) — plná vizualizace Sprint 1-4 intel layer output
- **Sprint 6 done (2026-04-19, commit b8de71e):** Digest formatter + Telegram delivery
  - `apis/intel-digest.mjs` — markdown + Telegram (< 4KB) + terminal formatters
  - Change detection 5 triggerů: critical-region / rising-hotspot / new-alert / new-cluster / score-jump
  - Idempotence přes `runs/digest-state.json` (gitignored) — `--only-on-change` pro cron
  - Telegram Bot API integration (TELEGRAM_BOT_TOKEN + CHAT_ID env vars)
  - Verified: first run 8 triggers, second run "no-change", telegram 391/4000 chars
  - Cron-ready: `*/30 * * * * npm run digest:send`
- **Sprint 7-9 done (2026-04-19, commit 3750c95):** Tests + 3D globe + i18n
  - `tests/intel-layer.test.mjs` — 53 testů, 10 suites, Node --test zero-dep, ~350ms
  - `tests/fixtures/sample-articles.mjs` — 12 deterministic articles pokrývajících všechny severity/categories/hotspoty
  - `dashboard/public/intel-globe.html` — 3D globe.gl (CDN, MIT), rings pro hotspoty, side panel, route /intel-globe, 2D↔3D toggle v /intel
  - `apis/intel-i18n.mjs` — XSS-safe locale injector, cached load, fr→cs fallback
  - `locales/cs.json` + `locales/en.json` — nová `intel:` sekce s headings/cols/severity/empty states
  - `server.mjs` — /intel + /intel-globe routes injectují locale z ?lang= nebo currentLanguage
  - Npm: `npm test`, `npm run test:watch`
- **MONITOR kompletní stav:** 10 commitů, 8 sprintů + 1 refinement, ~6300 řádků, plný pipeline registry→cache→classify→cluster→scoring→API→2D+3D viz→digest→tests, 53/53 unit testy
- **Roadmap dokončen** (Discord přeskočen per user) mapy
- **TODO zbývající feed URL opravy:** State Department (state.gov/press-releases/feed INVALID), NATO (natohq URL 404), AFP/Reuters/AP via Google News proxy (EMPTY pro AFP), Hospodářské noviny (hn.cz/rss INVALID), Demagog.cz (rss 404)
