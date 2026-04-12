---
name: Inbox články — chybějící pozice obrázků a infoboxů v CMS
description: Články zpracované z inbox/dokumentů nemají správné pozice obrázků a infoboxů v CMS Aqua exportu, na rozdíl od RSS článků
type: project
---

Články z inbox (document_processor.py) nemají v CMS Aqua správné pozice obrázků a infoboxů — obrázky nejsou na správných místech v těle článku.

**Why:** RSS a inbox pipeline generují odlišnou strukturu výstupu. Na konci pipeline (9_final.md) by měl být výstup identický bez ohledu na zdroj, ale evidentně není.

**Stav (2026-03-15): IMPLEMENTOVÁNO**

Řešení ve dvou vrstvách:
1. **Náhled + Save** (`ngrobot_web.py`): Auto-placement obrázků → editor přetáhne (DnD) → save konvertuje `preview-suggested` na `![IMAGE:](images/file)` + `[Popisek:]` → CMS publisher najde inline markery
2. **CMS fallback** (`cms_aqua_publisher.py`): `_find_best_positions_for_body_images()` + `_inject_image_placeholders_into_html()` — keyword-overlap auto-placement přímo v publisheru

Infografiky (`type=infographic`) jsou vyloučeny z auto-placementu (obě místa).
