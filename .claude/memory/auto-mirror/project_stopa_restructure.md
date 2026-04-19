---
name: STOPA Restructure Plan
description: 3-phase plan to fix STOPA — sensors, STOPA/KODER split, measurable feedback loop. Full plan in outputs/stopa-restructure-plan.md
type: project
originSessionId: a93b40e9-4ff0-451c-a713-4d435ed2d724
---
STOPA restructure rozhodnuto 2026-04-14. Tři fáze:

**Fáze 1 (tento týden):** Opravit senzory
- skill-usage-tracker nefunguje (sessions.jsonl: skills=0)
- failure-recorder nefunguje (failures/ prázdné)
- Ořezat hooks z ~70 na ~30
- Archivovat 20 mrtvých skills
- Zpracovat 778 raw captures

**Fáze 2 (příští týden):** Rozdělit STOPA a KODER
- STOPA = meta-agent (orchestrace, memory, komunikace, rozhodování)
- KODER = execution agent (kód, testy, quality, iterativní optimalizace)
- Handoff přes task queue + outcomes

**Fáze 3 (za 2 týdny):** Jeden měřitelný feedback loop
- watch → ingest → actionable learnings pipeline
- Baseline ~10% actionable rate, cíl 50%

**Why:** Systém má 65 skills a 70 hooks ale 1 outcome a 0 failures — běží naprázdno.
**How to apply:** Každá session v STOPA by měla odkazovat na tento plán. Plán v outputs/stopa-restructure-plan.md.
