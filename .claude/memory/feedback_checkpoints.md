---
name: feedback_checkpoints
description: Checkpoint management rules — frequent saves, versioning, never lose session context
type: feedback
---

Dělej checkpointy s feedbackem ČASTĚJI a VERZUJ je.

**Why:** Předchozí konverzace údajně vyčistila checkpoint Session 5 a ztratil se kontext pro Session 6. Uživatel byl frustrovaný, že se točíme v kruhu.

**How to apply:**
- Na začátku každé nové session: ihned zapiš checkpoint s aktuálním stavem (co je hotové, co se dělá)
- Po každém dokončeném bloku práce (ne jen na konci session): aktualizuj checkpoint
- Verzuj checkpointy: `checkpoint.md` = aktuální, `checkpoint_v5.md`, `checkpoint_v6.md` = archiv
- Checkpoint NIKDY nemazat — přepsat jen aktuální, staré archivovat
- Checkpoint musí obsahovat: task list s pending/done statusy, technické poznatky, resume prompt
