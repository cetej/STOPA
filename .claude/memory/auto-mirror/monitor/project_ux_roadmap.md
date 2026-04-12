---
name: UX Roadmap Progress
description: Stav implementace UX roadmapu MONITOR dashboardu — co je hotové, co zbývá, kde navázat
type: project
---

## UX Roadmap — Stav k 2026-03-21

Roadmap v `docs/ROADMAP-UX.md` definuje 10 features. Sessions 1-4 implementovaly #1-7, #9:

### HOTOVO
1. **Signal Context** — `lib/signal-context.mjs` (14 metrik, prahy, CZ dopad)
2. **Situation Briefing** — `lib/briefing-generator.mjs` (LLM + rule-based)
3. **Detail Drawer** — klikatelné metriky → pravý slide-out panel s interpretací
4. **OSINT Feed Filtering** — 7 kategorií, severity, filter bar + sort
5. **Cross-Signal Stories** — `lib/story-detector.mjs` (4 story templates)
6. **CZ Overview Widget** — left rail: ČNB kurzy, ČHMÚ výstrahy, české zprávy
7. **Map Interactivity** — 2 sessions kompletní:
   - S1: enriched popups (severity, source, context), 13 layer toggles, ACLED ring click, marker metadata
   - S2: grid-based clustering (flat mód), cluster popup drill-down, region filter pro OSINT feed, localStorage persistence layer stavu, enriched hover tooltips (globe), hidden count indicator
9. **Watchlist + Browser Notifications** — localStorage, push notifikace

8. **Timeline Slider** — S1: snapshot storage v `runs/memory/snapshots/`, `/api/history` + `/api/snapshot/:timestamp` endpointy, slider UI pod mapou s live/history přepínáním, debounced loading, viewing indikátor

10. **Daily Digest** — `lib/digest-generator.mjs` (LLM + rule-based), scheduled send v configovatelný čas (UTC), `/digest` příkaz pro Telegram + Discord

### ZBÝVÁ
Nic — všech 10 features z UX roadmapu je implementováno.

**Why:** Celý UX roadmap dokončen. Dashboard přešel z "hezký" na "použitelný" — interpretace signálů, interaktivita, české rozšíření, timeline, watchlist, daily digest.

**How to apply:** Pro budoucí práci: roadmap je vyčerpaný, další features by měly vycházet z reálného používání a zpětné vazby.
