---
name: Input sanitization before pipeline
description: Inbox files from previous Claude sessions contain processing artifacts that must be stripped before pipeline runs
type: feedback
---

Vstupní soubory v inbox/ mohou být výstupem z předchozí Claude session a obsahovat procesní komentáře ("Všechny fáze proběhly", checklisty s ✓, "Výsledný článek:"). Pipeline je prožene všemi fázemi beze změny.

**Why:** Bug v článku "Přežití v temnotě" — artefakty se propsaly do 9_final.md a odtamtud do CMS Aqua.

**How to apply:** document_processor.py nyní má `_sanitize_input_content()` volanou PŘED pipeline. phases.py `_remove_phase_notes()` rozšířen o nové vzory + preferování skutečného H1 před generickým názvem dokumentu. Při budoucích podobných problémech: vždy přidat vzor do OBOU míst (vstupní sanitizace + výstupní čištění).
