---
date: 2026-04-13
type: best_practice
severity: high
component: orchestration
tags: [refinement, iteration, critic, convergence, anti-pattern]
summary: "In iterative improvement loops, 'do nothing' (incumbent preservation) must be a structurally first-class option — not just logically allowed — or the system will always produce changes regardless of quality."
source: external_research
uses: 2
successful_uses: 0
harmful_uses: 0
confidence: 0.70
verify_check: "manual"
skill_scope: [autoreason, autoloop, critic, self-evolve]
---

## Details

Critique-and-revise systems assume refinement is always desirable. The prompt structure ("find improvements") primes the model to produce changes even when none are needed. This causes:
- Hallucinated flaws in already-good outputs
- Quality degradation below single-pass baseline
- Infinite refinement without convergence

Fix: make A (unchanged) always a candidate in the judge panel. The model can only improve the incumbent by winning against it in a blind vote — not by default assumption.

Convergence criterion: incumbent wins k=2 consecutive rounds → stop. This gives structural exit.

**Application to STOPA**: all iterative skills (autoloop, self-evolve, autoreason) should have explicit convergence detection and incumbent preservation. Not just a loop counter.
