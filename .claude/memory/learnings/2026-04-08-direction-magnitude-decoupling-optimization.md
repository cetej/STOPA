---
date: 2026-04-08
type: best_practice
severity: medium
component: skill
tags: [optimization, self-evolution, credit-assignment, autoloop, self-evolve]
summary: "RLSD paper proves decoupling update direction (what to change) from magnitude (how much) avoids information leakage and gives 2× convergence. Apply to STOPA iterative skills: critic gives direction (pass/fail), diff analysis gives per-change magnitude."
source: external_research
uses: 1
successful_uses: 0
harmful_uses: 0
confidence: 1.0
verify_check: "manual"
---

## Detail

RLSD (arXiv:2604.03128) identifies that when a teacher signal has privileged access to ground truth, directly using it for gradient direction causes information leakage — performance peaks early then degrades (the OPSD failure mode).

**Fix:** Environment reward controls direction (reinforce/penalize), teacher evidence controls per-token magnitude only. Clipping bounds the influence.

**STOPA parallel:** In /autoloop and /self-evolve, the critic (which sees eval results) provides direction (PASS/FAIL, better/worse). But currently all edits within a change are treated uniformly. RLSD suggests analyzing which specific changes contributed most to the outcome and weighting future iterations accordingly.

**Concrete application:**
- After critic evaluates an autoloop iteration: diff the changed lines
- Lines where the change aligns with improvement → high weight (keep/expand)
- Lines where the change doesn't affect outcome → low weight (neutral)
- Lines where the change correlates with regression → negative weight (revert)

This is essentially per-line credit assignment instead of whole-file pass/fail — the same insight RLSD applies at token level.

**Also:** The impossibility trilemma warns that you can't simultaneously have stability + improvement + leakage-free in distribution-matching frameworks. STOPA's self-evolve should not try to match a "reference skill" distribution — instead, optimize toward environment outcomes (test results, critic scores) directly.
