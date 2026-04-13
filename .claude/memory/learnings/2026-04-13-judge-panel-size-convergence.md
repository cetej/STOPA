---
date: 2026-04-13
type: best_practice
severity: medium
component: orchestration
tags: [evaluation, critic, review, convergence]
summary: "7 fresh judges converge 3× faster than 3 judges in blind Borda voting; each judge must have independent context (no shared prior from previous rounds)."
source: external_research
uses: 0
successful_uses: 0
harmful_uses: 0
confidence: 0.6
verify_check: "manual"
skill_scope: [autoreason, critic]
---

## Details

From autoreason ablations:
- 3 judges: correct winner selected, but slow convergence (more rounds needed)
- 7 judges: 3× faster convergence to correct winner
- Judge independence is critical: shared context = bias from previous rounds bleeds in

For STOPA applications (budget constraint): 3 judges is the minimum practical; 5 is a good tradeoff. 7 only when quality is worth the cost.

**Implication for `/critic` in loops**: a single critic in a loop accumulates bias. Panel of 3+ fresh critics per round significantly improves reliability without infinite iteration.
