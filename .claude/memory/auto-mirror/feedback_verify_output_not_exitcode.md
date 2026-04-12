---
name: Verify output content, not just exit code
description: Never claim "done" based on pipeline exit code — always check actual output size and content
type: feedback
---

Nikdy neříkej "hotovo" jen proto, že pipeline prošel bez erroru. VŽDY zkontroluj skutečný výstup — velikost souboru, obsah, kompletnost.

**Why:** User zpracoval článek, pipeline hlásil "Článek zpracován!" ale finální soubor měl 3K místo 25K — jen seznam souvisejících článků místo celého článku. Prohlásil jsem "všech 9 fází prošlo, článek je hotový" bez kontroly.

**How to apply:** Po pipeline/build/processu vždy: (1) zkontroluj velikost výstupních souborů, (2) podívej se na prvních pár řádků, (3) porovnej s očekávaným výstupem. Teprve pak říkej "hotovo".
