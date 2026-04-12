---
name: Server restart policy
description: After editing server .py files, restart the server directly via taskkill+background start — don't ask user to do it
type: feedback
---

Po editaci .py souborů serveru VŽDY restartovat server sám: `taskkill //PID <pid> //F` + `python ngrobot_web.py &` na pozadí.

**Why:** Pro uživatele je komplikovanější najít správné okno a killnout server než pro Clauda spustit taskkill s PID. Přenášení této práce na uživatele je otravné.

**How to apply:**
- Po editaci serverových .py souborů: `netstat -ano | grep 5001` → `taskkill //PID <pid> //F` → `python ngrobot_web.py &` (background)
- Neříkat "prosím restartuj ručně" — prostě to udělat
- Syntaktickou validaci dělat přes `python -c "import modul"` PŘED restartem
