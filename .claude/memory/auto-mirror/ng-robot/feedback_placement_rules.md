---
name: Placement rules v render smyčce nefungují
description: Pixelové placement posuny (anchor_ne, avoid_water, inside_area) v render_czech_text() degradují výstup — kaskádové kolize. Placement řešit ve fázi plánování, ne renderu.
type: feedback
---

Pixelové placement posuny v render smyčce map_localizer.py DEGRADUJÍ výstup.

**Why:** Session 4 test ukázal, že anchor_ne + avoid_water + inside_area + cover_residual_text vytvářejí kaskádové kolize. Claude Vision (plan_label_layout) + anti-collision (_resolve_collisions) řeší pozicování dostatečně. Přidání dalšího posunu v renderu to rozbíjí. cover_residual_text navíc ničí terénní detaily na čisté NB Pro mapě.

**How to apply:** Placement rules implementovat ve fázi plan_label_layout (jako instrukce pro Vision), ne v render smyčce. Helper metody (_is_water_color, _check_water_overlap) ponechat pro budoucí integraci do plánování. Nikdy nemanipulovat pozice v render_czech_text() — ta metoda jen vykresluje na zadané souřadnice.
