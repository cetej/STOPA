---
name: RTT PDF = source of truth pro text
description: RTT PDF je autoritativní zdroj textu, IDML je jen design/struktura — vždy začít RTT
type: feedback
---

**IDML** = design, struktura, formátování, umístění textových rámců.
**RTT PDF** = source of truth pro **textový obsah**. Autoritativní verze toho, co se překládá.

**Why:** IDML může mít Track Changes artefakty, fragmentovaný text v CharacterStyleRange, šablonové placeholdery. RTT PDF ukazuje čistý finální text tak, jak ho redakce schválila. U velkých reportáží RTT obsahuje i komentáře pro překlad, fakta a kontext.

**Workflow:**
1. RTT PDF přijde jako první referenční dokument
2. Mohou přijít aktualizace RTT (nová verze textu)
3. Ve finále přicházejí opravy k zapracování

**How to apply:**
- Při IDML extrakčním bugu: PRVNÍ krok = otevřít RTT/RELEASE PDF, porovnat s extrakcí
- Při validaci překladu: porovnat český text s RTT originálem
- RTT je ground truth — pokud se IDML a RTT liší, platí RTT
- Hledej RTT ve složce projektu: `*.pdf` (typicky "... RTT.pdf" nebo "... RELEASE *.pdf")
