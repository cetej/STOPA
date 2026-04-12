---
name: feedback_checkpoints
description: Checkpoint quality rules — never mix completed work with new tasks, keep context minimal and unambiguous
type: feedback
---

Checkpointy pro novou session nesmí obsahovat detaily hotové práce z předchozích sessions.

**Why:** Uživatel byl opakovaně frustrovaný, protože checkpoint pro Session 6 obsahoval seznamy hotových modulů z Session 5, což nová session interpretovala jako "vše hotovo". Také jsem opakovaně ztrácel kontext o tom, co Záchvěv vlastně je a jak funguje flow.

**How to apply:**
- Checkpoint pro session N obsahuje POUZE úkoly session N
- Hotovou práci z předchozích sessions popsat jednou větou ("CLI pipeline existuje, viz CLAUDE.md") — ne enumerovat moduly
- Žádné checklisty s [x] pro práci z minulých sessions
- Verzuj checkpointy číslem session + minor verzí (v6.0, v6.1...)
- Konceptuální popis flow patří do checkpointu — je to kritický kontext
- Pokud něco iteruješ s uživatelem, zapiš opravu do feedback memory IHNED
- Testuj checkpoint mentálně: "kdyby si toto přečetla fresh session, pochopí co dělat a co NEdělat?"
