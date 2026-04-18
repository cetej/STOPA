---
date: 2026-04-07
type: best_practice
severity: medium
component: general
tags: [rl-training, multi-reward, optimization, reward-shaping]
summary: "When optimizing against multiple metrics simultaneously, normalize each metric independently before aggregating — direct sum-then-normalize collapses distinct metric combinations to identical advantage values, destroying signal resolution."
source: external_research
maturity: draft
uses: 0
successful_uses: 0
harmful_uses: 0
confidence: 0.6
verify_check: "manual"
failure_class: logic
task_context: {task_class: pipeline, complexity: medium, tier: standard}
---

## Multi-reward Normalization Collapse (GDPO pattern)

**Problem:** Applying group normalization to the *sum* of multiple rewards (GRPO-style) collapses distinct reward combinations to identical normalized values. Example: (0,1) and (0,2) reward pairs both normalize to (-0.7071, +0.7071), erasing the distinction between "partially achieved" and "strongly achieved."

**Fix (GDPO):** Three-step decoupled normalization:
1. Normalize each reward independently (group-wise mean/std per reward dimension)
2. Sum the normalized advantages
3. Apply batch-level normalization for numerical stability

**Priority ordering:** When objectives have different difficulty levels, weight tuning alone fails — model still optimizes the easier objective. Use conditional gating: `R_secondary = R_secondary if R_primary achieved else 0`.

**Evidence:** +2–7% improvements across tool calling, AIME, and coding benchmarks (arXiv:2601.05242, Liu et al. 2026).

**STOPA applicability:** Relevant if /autoloop or /autoresearch runs optimization loops against multiple metrics (e.g., correctness + format + length). The conditional reward pattern maps directly to STOPA's critic scoring: gate style/length metrics on correctness threshold.
