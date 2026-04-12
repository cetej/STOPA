---
name: Cross-project memory handoff
description: When preparing work for another project, save memory to TARGET project's auto-memory, not just current
type: feedback
---

Při přípravě handoffu do jiného projektu (např. STOPA → NG-ROBOT) uložit plán/memory do auto-memory CÍLOVÉHO projektu.

**Why:** Auto-memory je project-scoped (`C:\Users\stock\.claude\projects\C--<path>\memory\`). Session otevřená v NG-ROBOT nevidí STOPA memory a naopak. Checkpoint odkazoval na soubor, který v cílovém kontextu neexistoval.

**How to apply:** Při `/checkpoint` nebo `/handoff` s cross-project taskem:
1. Zjisti path cílového projektu (NG-ROBOT → `C--Users-stock-Documents-000-NGM-NG-ROBOT`)
2. Ulož memory soubor do `C:\Users\stock\.claude\projects\<target-path>\memory\`
3. Aktualizuj MEMORY.md indexu cílového projektu
4. Checkpoint reference musí uvádět, kde přesně soubor leží
