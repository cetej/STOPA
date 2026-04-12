---
name: Preview Hub Fáze 3 — hlášené problémy
description: Uživatelem hlášené bugy z Fáze 3b — inline click neotevře zvětšení, save popisku chyba
type: feedback
---

## Problémy k opravě (hlášeno 2026-04-06)

1. **Inline click na obrázek v článku** — dříve otevíral zvětšení fotky, teď nefunguje (mousedown handler blokuje původní chování)
   **Why:** Fáze 3 přidala mousedown handler na `#pf-body figure.preview-image` který preventDefault+stopPropagation → zablokoval původní lightbox/zvětšení
   **How to apply:** Při opravách Fáze 3 — buď obnovit lightbox jako první akci editoru (velký náhled = zvětšení), nebo přidat zpět dedikovaný zvětšovací handler

2. **Uložení popisku článku skončilo chybou** — po úpravě popisku v editoru se zobrazila chyba
   **Why:** Pravděpodobně response format mismatch — `data.ok` vs `data.status` — částečně opraveno ale mohlo zůstat místo kde chyba přetrvává
   **How to apply:** Ověřit VŠECHNY API response checky v image-editor-modal.js, sjednotit na `data.ok || data.status === 'ok'`

3. **Dílčí chyby** — nespecifikované, vyčistit v pozdější fázi

## Rozhodnutí uživatele
Pokračovat v celkových úpravách a fázích, chyby čistit pak.
