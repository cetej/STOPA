---
name: After ruff autofix always verify removed imports are truly unused
description: Ruff F401 removed REQUESTS_AVAILABLE try/except blocks — broke runtime. Always grep for usages before accepting removals.
type: feedback
---

Po ruff autofix VŽDY ověř že odstraněné importy nejsou používané jinde v souboru.

**Why:** Ruff F401 smazal `REQUESTS_AVAILABLE = True` z try/except bloků v phases.py a utilities.py, ale proměnná se používala o tisíce řádků níže. Způsobilo NameError při zpracování článků.

**How to apply:**
- Po `ruff --fix`: grep každý odstraněný symbol v celém souboru
- Zvlášť pozor na try/except import bloky s flag proměnnými (AVAILABLE, HAS_X)
- Zvlášť pozor na velké soubory (1000+ řádků) kde usage je daleko od definice
