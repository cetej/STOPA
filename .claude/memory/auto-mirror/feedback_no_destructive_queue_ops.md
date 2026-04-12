---
name: Never clear queue or restart server without asking
description: CRITICAL — queue/clear deletes user's RSS article selection, soft cancel is unreliable, don't chain destructive ops
type: feedback
---

NIKDY nepoužívej `queue/clear` nebo restart serveru bez explicitního souhlasu uživatele.

**Why:** queue/clear smazal uživateli stažené RSS články připravené k výběru. Soft cancel (cancel-running) nefunguje spolehlivě — opakované pokusy nic neřeší. Řetězení destruktivních operací (clear → restart → re-download) situaci jen zhoršilo.

**How to apply:**
- Pokud cancel nefunguje: řekni to uživateli a nech HO rozhodnout co dál
- Nikdy nemaz frontu — obsahuje uživatelova data (RSS výběr, rozpracované úkoly)
- Restart serveru = ztráta stavu — jen na explicitní pokyn
- Nový článek ke zpracování přidej do fronty a NECH ho čekat, nemaž ostatní
