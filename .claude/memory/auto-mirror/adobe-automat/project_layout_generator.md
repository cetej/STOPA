---
name: Layout Generator — nová funkcionalita
description: Plán pro modul generování IDML layoutů z fotek a textu podle NG vzorů — 8 sessions
type: project
---

Layout Generator — nový modul NGM Localizeru pro tvorbu unikátních IDML layoutů.

**Why:** Uživatel chce obrácený workflow — nejen lokalizovat, ale i vytvářet nové layouty podle NG stylu z nahraných fotek a textu.

**How to apply:**
- Detailní plán: `docs/PLAN_LAYOUT_GENERATOR.md` (8 sessions)
- Session 1: Template Analyzer (reverse-engineering IDML) — DONE
- Session 2: Pattern Library (katalog spread typů) — DONE
- Session 3: IDML Builder (programatická tvorba IDML) — DONE
- Session 4: Layout Planner (AI kompozice) — DONE
- Session 5: Backend API — DONE
- Session 6: Frontend — nový Dashboard + Layout Wizard — DONE
- Session 7: Preview & Polish
- Session 8: Pokročilé funkce (volitelná)
- Dashboard se předělá na dual-mode hub (Lokalizace | Layout Generator)
- Klíčové nové adresáře: `backend/services/layout/`, `data/templates/`

**Session 3 výstup (2026-03-22):**
- `backend/services/layout/idml_builder.py` — IDMLBuilder class
- Skeleton IDML přístup — kopíruje Resources/Fonts/Styles/MasterSpreads z reálného NG IDML
- Generuje nové Spread XML + Story XML z layout specifikace
- Podpora všech 9 spread patterns, threaded text frames, image links
- Validováno: XML validace, ZIP packaging, Frame→Story linkage

**Session 4 výstup (2026-03-22):**
- `backend/services/layout/image_analyzer.py` — Pillow analýza fotek, EXIF, klasifikace priority
- `backend/services/layout/text_parser.py` — parsování článku (strukturovaný i plain), odhad prostoru
- `backend/services/layout/layout_planner.py` — rule-based + AI-assisted plánování sekvence spreadů
- Nové modely v `models_layout.py`: `ImageInfo`, `ArticleText`, `TextEstimate`, `ImagePriority`, `ImageOrientation`
- E2E testováno: 6 fotek + článek → opening + body + closing, validace OK

**Session 6 výstup (2026-03-22):**
- Dashboard redesign: dvousloupcový hub (Lokalizace | Layout Generator) + záložky projektů
- `LayoutWizard.svelte` — 6-krokový wizard s auto-detekcí fáze projektu
- `api.js` rozšířen o 12 layout API metod
- `router.js` — podpora query params v hash routeru
- Routing: `#layout-wizard`, `#layout-wizard/{projectId}?style=xxx`
- Ověřeno: nový projekt, existující projekt (e2e-test-article), plán preview, navigace
