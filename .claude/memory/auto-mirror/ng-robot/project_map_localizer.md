---
name: Map Localizer — stav modulu
description: Modul map_localizer.py — lokalizace map EN→CZ. Session 8: plan_label_layout aktivován v pipeline, anchor-based positioning, force-directed anti-collision.
type: project
---

## Stav (2026-03-26, po session 8)

### Session 8: Layout planning v pipeline + force-directed anti-collision

**Implementováno:**
1. **`plan_label_layout()` aktivován v `localize()` flow** — byl mrtvý kód z NB Pro workflow. Nyní mezi krok 3b (residual cover) a krok 4 (render). Posílá DVA obrázky (originál + covered).
2. **Anchor-based positioning** — relativní pozice od anchor bodů místo absolutních souřadnic. Prompt: "15% severně od Yellowstone Lake" místo "x=27%, y=38%".
3. **Force-directed anti-collision** — nahradil greedy (3 iterace, posun od centra). Nový: 10 iterací, klesající damping (0.6×0.85^i), anchor constraint (point_* max 5% drift), simultánní síly.
4. **`_image_to_base64_safe()`** — komprimace obrázků pro API (base64 overhead × 4/3). PNG→JPEG s postupně klesající kvalitou.
5. **Originální Yellowstone mapa** nalezena v `articles/.../images/` (1759x3072), zkopírována do processed.

**Test výsledek (Yellowstone):**
- 41 prvků → 36 po filtraci → 34 umístěno, 5 anchor bodů
- Anti-collision: 51 posunů v 8 iteracích, 3 zbývající kolize
- Čas: 433s

### Zbývající problémy

| Problém | Root cause | Priorita |
|---------|-----------|----------|
| **Inpainting kvalita** | cv2.INPAINT_TELEA nedostatečný pro velké oblasti (YELLOWSTONE NATIONAL PARK) | Střední |
| **Zbytky EN textu** | 2-pass cover stále nechává fragmenty | Střední |
| **Truncation CZ názvů** | Dlouhé české názvy se nevejdou (návštěvnická centra) | Nízká |
| **3 zbývající kolize** | Force-directed konvergoval ale neodstranil vše | Nízká |

---

## Session 7 (předchozí): Grouping + Term Verification + NatGeo Specs

### Session 7: Grouping + Term Verification + NatGeo Specs

**Implementováno:**
1. **Fragment grouping** (`_group_related_elements()`)
   - Identifikuje textové fragmenty, které tvoří jeden logický název
   - Např. "YELLOWSTONE" (txt_20) + "NATIONAL PARK" (txt_22) → překlad jako celek
   - Přísná kritéria: x_diff<6%, y_diff 1-5%, stejný size+style+case
   - Po překladu split zpět na řádky pro rendering (`_split_group_translation()`)

2. **Term verification vylepšení** (`_verify_translations_web()`)
   - Deduplikace skupinových překladů — ověří jen primární element
   - Propagace oprav na všechny členy skupiny
   - Prompt: VŽDY hledat na cs.wikipedia.org (ne přeskakovat "obecně známé")
   - Zvýšený budget: thinking 6K, web_search max 15

3. **Font hierarchy cap**
   - `_FONT_BY_TYPE` definuje hierarchii: park(48) > country(36) > state(22) > forest(15)
   - `measured_size` (z width_pct/height_pct) NESMÍ přesáhnout 1.3× hierarchický základ
   - Řeší problém "les větší než park" z width_pct originálu

4. **NatGeo Name Placement Guide** v layout promptu
   - Pravidla pro města (NE>SE>NW>SW, vzdálenost 1/2-1 townspot)
   - Jezera (malá vedle, velká uvnitř, u nejširší části)
   - Řeky (paralelně s tokem, ne každý zákrut, zvětšit k ústí)
   - Pohoří (spread podél hřebene, rovnoběžné stackované linie)
   - Hierarchie velikostí (park > country > state > forest)

5. **NatGeo Resource Guide specs** zapsány do memory
   - `reference_natgeo_map_specs.md` — fonty, barvy, placement z "04 Maps 2022.pdf"

### Známé problémy (k řešení příště)

| Problém | Root cause | Návrh řešení |
|---------|-----------|--------------|
| **Pozicování stále nepřesné** | Claude Vision odhaduje pozice na čisté mapě, anti-collision greedy je slabý | Referencovat originální pozice relativně k anchor points |
| **NB Pro neodstraní text** | img2img stále nechává anglické nápisy | Lepší negative prompt, nebo dvou-průchodový inpainting |
| **Originální Yellowstone mapa smazána** | mapa.png je 3D infografika (2048x2048), ne originální vertikální mapa (1759x3072) | Stáhnout znovu z NG |
| **Inset mapa elementy** | Texty z inset mapky (IDAHO, MONTANA v malé mapce) se mísí s hlavní mapou | feature_type="inset" + filtrování |

### Architektura pipeline (6 kroků)
1. **Analyze** — Claude Vision: text elements + positions + anchor points + feature_type
2. **Translate** — grouping → TermDB batch → Claude (skupiny jako celek) → split zpět
3. **Verify** — web search: cs.wikipedia.org, propagace skupinových oprav
4. **Clean map** — NB Pro img2img (text removal) NEBO inpainting (cv2)
5. **Layout** — Claude Vision: pozice na čisté mapě dle kartografických pravidel
6. **Render** — Pillow: NG fonty, letter-spacing, halo, path_points, hierarchy cap

### Session plán (stav po session 8)
2. ~~Font metrics z originálu~~ → VYŘEŠENO hierarchickým capem (session 7)
3. ~~Referenční bod + relativní pozicování~~ → VYŘEŠENO anchor-based positioning (session 8)
4. NB Pro prompt / lepší inpainting — zbývá. cv2 inpainting nestačí pro velké textové oblasti.
