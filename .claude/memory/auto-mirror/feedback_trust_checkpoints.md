---
name: feedback_trust_checkpoints
description: When re-verifying completed work, acknowledge the checkpoint context instead of appearing to discover it fresh
type: feedback
---

Ověřování hotové práce je OK — ale dělej to vědomě, ne jako bys o ní nevěděl.

**Why:** Uživatel si všiml, že Claude čte checkpoint, pak ověřuje completed items, ale prezentuje to jako "discovery" místo "verification". Vypadá to jako by systém dokumentace nefungoval — jako by Claude zapomněl co už bylo uděláno. Problém není ověřování samotné, ale nedostatek transparence kolem něj.

**How to apply:**
1. Když checkpoint říká X je DONE a chceš to ověřit → řekni "Checkpoint říká X je hotové, ověřím stav" (ne "podívám se co je potřeba")
2. Rozlišuj "verification" (vím co hledám, kontroluji) vs "exploration" (nevím co tam je)
3. Netvař se, že objevuješ něco nového, když to checkpoint už popsal
