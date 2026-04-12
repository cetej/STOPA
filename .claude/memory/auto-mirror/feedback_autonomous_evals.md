---
name: feedback_autonomous_evals
description: User wants fully autonomous eval system — no manual commands, self-triggering, self-improving
type: feedback
---

Eval systém NESMÍ vyžadovat ruční příkazy. Uživatel nechce pamatovat `/harness eval-runner --skill critic`.

**Why:** User workflow je autonomní — agent má sám detekovat kdy běžet evals, sám interpretovat výsledky, sám navrhnout a aplikovat vylepšení. Ruční triggery jsou anti-pattern.

**How to apply:**
- Evals se triggurují automaticky (hooks po editaci SKILL.md, post-audit, post-autoloop)
- Výsledky se interpretují a actionují bez čekání na uživatele
- Self-improvement loop: eval fail → auto-diagnóza → návrh fixu → autoloop
- Uživatel vidí jen výsledky, ne proces
