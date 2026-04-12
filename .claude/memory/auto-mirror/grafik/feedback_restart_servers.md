---
name: always-restart-both-servers
description: After any code change, always restart BOTH API and UI servers without being asked
type: feedback
---

Po každé změně kódu vždy restartuj OBA servery (API i UI) automaticky, bez čekání na pokyn.

**Why:** Uživatel nechce opakovaně říkat "restartuj server" — je to samozřejmost po editaci.

**How to apply:** Po jakékoliv editaci v grafik/ nebo ui/ ihned zastavit a znovu spustit oba preview servery (grafik-api + grafik-ui).
