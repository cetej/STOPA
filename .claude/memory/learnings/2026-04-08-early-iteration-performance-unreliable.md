---
date: 2026-04-08
type: anti_pattern
severity: high
component: skill
tags: [autoloop, autoresearch, self-evolve, optimization, scaling-laws, iteration-strategy]
summary: "ScaleRL (400K GPU-hours): early small-compute performance is unreliable predictor of scale. Approach winning first 2-3 iterations may lose at scale. Different recipes reach DIFFERENT asymptotes — more iterations don't fix a bad approach. STOPA autoloop/autoresearch must give each approach enough iterations before judging, and predict ceiling early."
source: external_research
uses: 0
successful_uses: 0
harmful_uses: 0
confidence: 0.7
verify_check: "manual"
---

## Detail

ScaleRL (arXiv:2510.13786, Meta, 400K GPU-hours) establishes three principles validated at massive scale:

**1. Not all approaches reach the same ceiling.**
Performance follows a sigmoidal curve: R = R0 + (A-R0) / (1+(Cmid/C)^B). Each recipe has its own asymptote A. More compute NEVER fixes a low A — it just approaches it faster.

**STOPA impact:** In /autoloop and /autoresearch, if an approach plateaus, switching approaches is the right move — more iterations won't break past the ceiling. Currently these skills don't distinguish "still climbing" from "at ceiling."

**2. Early performance is unreliable.**
Method X beating Y at iteration 3 doesn't predict which wins at iteration 30. The sigmoidal curve has an inflection point — early gains can be misleading.

**STOPA impact:** /autoloop currently picks "best so far" after a few iterations. This biases toward fast-start approaches that may have low ceilings. Give each approach at minimum 5 iterations before comparing (currently: 3-fix rule kicks in too early for approach selection, though it's fine for error escalation).

**3. Most design choices affect efficiency (B), not ceiling (A).**
Changing normalization, curriculum, etc. makes you reach the ceiling faster, but the ceiling stays the same. Only loss type and batch size shift A.

**STOPA impact:** When optimizing a skill's performance, focus on what actually shifts the asymptote (the core algorithm/approach), not on prompt tweaks that only change speed of convergence.

**Actionable for /autoloop:** Consider fitting a 3-parameter sigmoidal curve to score trajectory after 5+ iterations. If predicted A is below target, switch approach instead of burning more iterations. Code: devvrit.com/scalerl_curve_fitting.
