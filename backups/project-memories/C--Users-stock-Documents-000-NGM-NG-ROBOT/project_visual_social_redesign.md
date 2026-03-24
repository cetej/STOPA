---
name: Visual/Social redesign plan
description: Plán na sloučení tabů Média+Poutáky+Vizuální editor do 2 tabů (Studio + Publikace). Detailní návrh v docs/REDESIGN_VISUAL_SOCIAL.md
type: project
---

Redesign vizuálního/social workflow — uživatel frustrovatelný z fragmentace.

**Hlavní problémy:**
- 3 taby zobrazují stejné obrázky (Média, Poutáky, Vizuální editor)
- 2 separátní úložiště (`images/` vs `social/`)
- Žádné propojení hero ↔ OG ↔ social selected image
- Export do MD je k ničemu, chybí copy-to-clipboard
- Carousel duplikace (Social tab vs Visual Editor)

**Navržené řešení:** Sloučit do 2 tabů:
1. **Studio** (rozšířený Visual Editor) — generování + galerie + QA
2. **Publikace** (nahrazuje Poutáky) — preview karty per platforma s copy tlačítky

**Why:** Uživatel potřebuje provázané prostředí: generovat → vybrat → kopírovat → postovat. Ne skákat mezi 3 taby.

**How to apply:** Detailní plán s fázemi migrace v `docs/REDESIGN_VISUAL_SOCIAL.md`. Začít fází 1 (sloučit úložiště), pak postupně UI.
