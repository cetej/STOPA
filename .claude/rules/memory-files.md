---
globs: ".claude/memory/**"
---

# Pravidla pro memory soubory

- Max 500 řádků per soubor — při překročení archivuj staré záznamy do `*-archive.md`
- Formát: markdown s jasnou strukturou (headings, tabulky, seznamy)
- Nikdy nemazat historii — přesouvej do archivu
- Datum ve formátu YYYY-MM-DD (absolutní, ne relativní)
- Checkpoint: vždy obsahuje resume prompt pro další session
- Budget: vždy obsahuje aktuální zůstatek a tier
- Learnings: každý záznam má datum, kontext, a poučení
