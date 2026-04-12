---
name: founding_conversation
description: Original design discussion that created the STOPA orchestration system — 6 roles, iterative loops, shared memory, separation of concerns
type: project
---

Orchestrační systém vznikl z uživatelovy úvahy o potřebě velitele/dirigenta pro řízení úkolů.

**Původních 6 rolí**: Dirigent, Průzkumník, Analytik, Exekutor, Kritik, Zapisovatel
**Klíčové principy**: dirigent nikdy nedělá práci sám, iterační smyčka (ne jednosměrný flow), scribe a critic oddělené role, sdílená paměť

**Why:** Toto je "zakládající dokument" systému. Všechny budoucí změny by měly být konzistentní s touto filozofií.
**How to apply:** Při refactoringu nebo rozšiřování systému ověřit, že nové skills/patterns neporušují tyto principy.
