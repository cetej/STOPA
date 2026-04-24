---
name: Žádné iterativní hádání u UI tasků
description: U UI/workflow tasků udělej kompletní analýzu existujícího vzoru PŘED implementací — zákaz "implementuju a uvidím"
type: feedback
originSessionId: a4e2ce98-63c4-420e-813f-3ec89a6f16e5
---
U UI/workflow tasků (přidání media-toggle, preview komponenty atd.) NEpiš kód, dokud není jisté, kam se to napojuje a jaký je analogický existující vzor. Iterativní pokusy s "implementuju a uvidím, jak to vypadá" jsou pro uživatele nesnesitelné.

**Why:** Při tasku „přidat videa do náhledu jako u obrázků" jsem nejdřív vytvořil plovoucí `+🎬` tlačítko + modál (wrong UX). Uživatel očekával **📄 toggle na karty v Media tabu** (jako u obrázků mají ⭐ hero a 📄 in-article). Iteroval jsem 3× než jsem našel `in_article` flag, který už existoval pro obrázky. Kromě UX chyby jsem ještě missnul, že pages_bp merguje `videos/captions.json` PŘES `images/captions.json` — takže můj zápis do images/captions.json se neprojevil. Pak ještě missnul, že `parse_final_article` načítá jen images/captions.json. Kaskáda chyb z neúplné analýzy.

**How to apply:**
1. **Krok 1 (povinný):** Najdi existující analogický feature v kódu. Pokud user řekne "jako u X", spusť Explore/Grep pro X a NAJDI:
   - Kde je UI komponenta (template, JS, CSS)
   - Kde je perzistence (file, db field)
   - Jaké API endpointy používá
   - Jak data tečou (page load → display → action → save → reload)
2. **Krok 2 (povinný):** Napiš jednovětý popis ZAMÝŠLENÉ implementace a teprve pak kóduj. Pokud popis obsahuje "asi", "možná", "zkusíme" → STOP, vrať se ke kroku 1.
3. **Když user odmítne implementaci:** STOP a přečti si jeho zprávu pomalu. Nejde o detail, jde o úplně špatný směr → revertuj a zeptej se NEBO udělej hlubší analýzu.
4. Tato pravidla NEPOUŽIJ pro: čistě algoritmické úpravy, debugging známých chyb, refactoring jednoho souboru.
