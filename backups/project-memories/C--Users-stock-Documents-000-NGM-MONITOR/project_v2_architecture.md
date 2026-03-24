---
name: MONITOR v2 Architecture
description: Signal-first redesign — cluster engine, brief/report generators, Záchvěv integration, new dashboard
type: project
---

MONITOR v2 přestavba z map-first na signal-first architekturu.

**Why:** Původní Crucix layout (mapy, letadla, 3D globe) je neužitečný pro analytika. Potřeba: přehledné signály, AI seskupování, on-demand analytické výstupy.

**How to apply:**
- Nové moduly: `lib/cluster/`, `lib/output/`, `lib/zachvev/`
- Dashboard: signal feed s clustery místo mapy
- API: `/api/brief/:id`, `/api/report/:id` pro on-demand výstupy
- Záchvěv: CRI + sentiment integrováno do sweep cycle
- Cost: ~$20-25/měsíc (Anthropic API)

**Stav (2026-03-22):** Backend kompletní, dashboard přepsán, integrace do server.mjs hotová. Testováno na reálných datech (4 clustery detekované).
