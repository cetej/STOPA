---
date: 2026-04-04
type: architecture
severity: high
component: skill
tags: [verification, evaluation, cascade, schema-utility]
summary: "Tool-Genesis (arXiv:2603.05578) prokázal cascade failure — drobné L1 chyby zesilují do katastrofických L4 selhání. Schema compliance ≠ downstream utility (Schema-F1 0.964, SR 0.472). Iterativní oprava s execution feedback dává 2-5× lepší výsledky než one-shot. Aplikováno do /critic (cascade-aware verification), /verify a /harness (anti-schema-trap), /skill-generator (repair loop), CLAUDE.md (model selection)."
source: external_research
maturity: draft
uses: 2
harmful_uses: 0
confidence: 1.00
impact_score: 0.0
verify_check: "Grep('Schema-Utility Decoupling', path='.claude/skills/') → 3+ matches"
related: [2026-03-26-harness-simplification.md]
successful_uses: 0
---

## Tool-Genesis Cascade Evaluation Pattern

**Paper:** Tool-Genesis (arXiv:2603.05578, March 2026) — diagnostic benchmark pro autonomous tool creation.

**Klíčová zjištění aplikovaná do STOPA:**

1. **Cascade failure amplification**: Drobné chyby na L1 (surface compliance) se zesilují přes L2 (schema) → L3 (functional) → L4 (utility). Qwen3-8B: L1 68.6% → L4 1.2%.
   - **Aplikace**: /critic nyní verifikuje milestones v cascade pořadí (L1→L2→L3). Pokud L1 selže, neskoč na L3.

2. **Schema-utility decoupling**: Claude-Haiku-3.5 dosáhl Schema-F1 0.964 ale SR pouze 0.472. Povrchová shoda ≠ downstream úspěch.
   - **Aplikace**: Anti-schema-trap pravidlo v /verify, /harness, /critic — po format check VŽDY testovat na downstream datech.

3. **Execution feedback je rozhodující**: Code-Agent (iterativní oprava) dává 2-5× SR improvement nad Direct (one-shot).
   - **Aplikace**: Repair loop v /skill-generator (validate-and-repair, max 3 iterace).

4. **Scale reversal**: Menší modely mohou být lepší pro one-shot; větší modely lépe exploitují feedback.
   - **Aplikace**: Model selection tabulka v CLAUDE.md — silnější model pro iterativní smyčky, ne pro one-shot.
