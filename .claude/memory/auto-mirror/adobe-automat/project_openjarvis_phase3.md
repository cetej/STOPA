---
name: OpenJarvis Adopce — Fáze 3 zadání
description: Zadání pro další session — EventBus, Model Routing, Trace Dashboard (volitelné fáze z OpenJarvis adopce)
type: project
---

# OpenJarvis Adopce — Fáze 3: Rozšíření

**Stav:** Fáze 1+2 DONE (core/registry, engine, traces + refactor 3 modulů)
**Cíl:** Dotáhnout pokročilé patterns pro cost optimalizaci a observabilitu

## Úkoly (3 nezávislé bloky)

### 3A. Model Routing — Haiku/Sonnet podle náročnosti

**Proč:** Haiku je 4× levnější než Sonnet. Fáze pipeline jako "Úplnost" (phase 2) nepotřebují Sonnet.

**Co udělat:**
1. Přidat routing tabulku do `core/engine.py`:
   ```python
   MODEL_ROUTING = {
       "pipeline_phase_2": MODEL_HAIKU,      # Úplnost — jednoduchá kontrola
       "pipeline_phase_3": MODEL_SONNET,      # Termíny — potřebuje reasoning
       "pipeline_phase_4": MODEL_SONNET,      # Fakta — potřebuje reasoning
       "pipeline_phase_5": MODEL_HAIKU,       # Jazyk — pattern matching
       "pipeline_phase_6": MODEL_SONNET,      # Stylistika — kreativní
       "translation": MODEL_SONNET,           # Překlad — kvalita je klíčová
       "layout_planner": MODEL_SONNET,        # Layout — strukturovaný výstup
   }
   ```
2. `get_model_for_module(module: str) -> str` helper
3. Refaktorovat pipeline `phases.py` — každá fáze specifikuje svůj model přes routing
4. **Metriky:** Porovnat kvalitu Haiku vs Sonnet na 5 testovacích textech pro phase 2 a 5

**Odhad:** ~1h

### 3B. EventBus — Decoupling progress tracking

**Proč:** Aktuálně 3 různé callback patterns (pipeline progress_callback, translation progress_callback, layout WebSocket). EventBus je sjednotí.

**Co udělat:**
1. `core/events.py` — jednoduchý pub/sub:
   ```python
   class EventBus:
       def subscribe(self, event_type: str, handler: Callable)
       def publish(self, event_type: str, data: dict)
   ```
2. Event typy: `INFERENCE_START`, `INFERENCE_END`, `PHASE_START`, `PHASE_END`, `PROGRESS`
3. Refaktor pipeline `TextPipeline.run()` — publish events místo callback
4. WebSocket handler v `main.py` subscribuje EventBus → push do frontendu
5. **Bonus:** TraceCollector subscribuje automaticky → trace záznam bez wrapperu

**Odhad:** ~2h

### 3C. Trace Analytics Dashboard (Frontend)

**Proč:** API endpointy `/api/traces/summary` a `/api/traces/recent` existují, ale nemají UI.

**Co udělat:**
1. Nová Svelte stránka `TraceDashboard.svelte` (route: `#traces`)
2. Celkové statistiky: volání, tokeny, náklady za den/týden/měsíc
3. Breakdown: by model (kolik stojí Sonnet vs Haiku), by module (translation vs pipeline vs layout)
4. Posledních N volání — tabulka s trace_id, modul, model, tokeny, cena, latence
5. Jednoduchý graf (bar chart) — náklady za den pomocí `<canvas>` (ne knihovna)
6. Přidat odkaz na dashboard navigation

**Odhad:** ~1.5h

## Priorita

1. **3A Model Routing** — přímý cost saving (~40% na pipeline)
2. **3C Trace Dashboard** — viditelnost nákladů
3. **3B EventBus** — nice-to-have, hlavně pro budoucí rozšiřitelnost

## Kontext

- `backend/core/` — nové moduly z Fáze 1+2
- `docs/LEARNINGS.md` — rozhodnutí a poučení z implementace
- `memory/reference_openjarvis.md` — kompletní analýza OpenJarvis
- Pricing: Sonnet $3/$15 per 1M, Haiku $0.80/$4 per 1M (2026-03)
