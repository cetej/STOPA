---
name: Local data first
description: Always use D:/GEODATA local data, never download from internet when local copy exists
type: feedback
---

Vždy preferuj lokální data z D:/GEODATA před stahováním z internetu. Online stahování povrchu kolabuje.

**Why:** Uživatel má 45GB COP30 tiles + ETOPO1 na D:. Online stahování je pomalé a nespolehlivé. Vektorové dlaždice by se měly cachovat lokálně.

**How to apply:** Jakýkoli nový datový zdroj (tiles, vektory, fonty) musí mít lokální cache na D:/GEODATA s fallbackem na internet. Nikdy nenavrhuj řešení, které závisí čistě na online zdrojích.
