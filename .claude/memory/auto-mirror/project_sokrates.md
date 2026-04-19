---
name: project_sokrates
description: SOKRATES — multi-agent Socratic dialogue analysis system for events/phenomena
type: project
originSessionId: 0657f990-5561-4f91-ba9e-6740211ba00d
---
SOKRATES je dialektický analytický systém inspirovaný Platónovými dialogy. Událost vstoupí → Sokrates ji rozloží na otázky → filosof-agenti debatují → syntéza s konsenzem, tenzemi a scénáři.

**Why:** Analýza událostí z více perspektiv současně — ne paralelní monology, ale skutečný dialog s protiargumenty.

**How to apply:**
- Projekt v `C:\Users\stock\Documents\000_NGM\SOKRATES\`
- Express 5.x na portu 3401, vanilla JS SPA
- 7 base filosofů: Sokrates (moderátor), Machiavelli, Locke, Sun-c', Smith, Arendtová, Marx
- Rozšiřitelné: nový filosof = nový .md soubor v `.claude/agents/philosophers/`
- 4 fáze: APORIE → ELENCHUS → ANTILOGIE → SYNTÉZA
- LLM backend: Anthropic API (Claude Sonnet), fallback na manuální mód bez klíče
- Integrace: MONITOR → event feed, ZACHVEV → sentiment data
- Spuštění: `node server.mjs` nebo přes launch.json "sokrates"
- Paleta: dark theme, warm gold/amber (#c9973f), Crimson Text serif + JetBrains Mono
