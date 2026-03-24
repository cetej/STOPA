---
name: restart-servers-after-changes
description: Po editaci Python modulů VŽDY restartovat běžící web server a zabít staré instance — jinak Python cachuje starou verzi v sys.modules
type: feedback
---

Po každé editaci Python souborů, které jsou importované běžícím serverem (claude_processor.py, ngrobot.py, ng_agent.py, export_formats.py, atd.), MUSÍM:

1. Najít běžící instance web serveru (`ngrobot_web.py`) a dalších long-running procesů
2. Ukončit je (kill)
3. Restartovat čistě

**Why:** 18. března 2026 noční batch zpracování 5 článků kompletně selhal, protože web server běžel se starou verzí `claude_processor.py` v paměti (chyběla nově přidaná funkce `pre_resolve_species`). Všech 5 článků prošlo překladem (fáze 0-1), ale spadly na fázi 2 s ImportError. Práce za hodiny ztracena, uživatel oprávněně naštvaný.

**How to apply:**
- Po KAŽDÉ editaci .py souboru v projektu: zkontrolovat `tasklist | grep python` / `ps aux | grep python`
- Pokud běží `ngrobot_web.py` nebo jiný server → zabít a restartovat
- Platí i pro `auto_agent.py`, `run_pipeline.py` a jakýkoliv long-running proces
- Python lazy importy (uvnitř funkcí) NEPOMÁHAJÍ — `sys.modules` cache platí per-proces
- Tohle je NENEGOCIABILNÍ — žádná editace serveru bez restartu
