---
date: 2026-04-12
type: architecture
severity: medium
component: orchestration
tags: [model-selection, rlhf, alignment, pre-training, post-training, instruction-following]
summary: "Pre-training = broad compression (knowledge, reasoning); post-training (RLHF/DPO) = alignment editing that increases preference info without significantly changing complexity. These are distinct: IFEval predicted by preference info (r=0.39), not compression (r=0.07)."
source: external_research
maturity: draft
uses: 0
successful_uses: 0
harmful_uses: 0
confidence: 0.6
impact_score: 0.0
verify_check: "manual"
skill_scope: [orchestrate, council]
---

## Detail

Conklin et al. (arXiv:2604.07569, ICLR 2026) show a clean dissociation:

**Pre-training compression predicts:**
- MMLU-Pro (knowledge), BBH (reasoning), MATH Level 5, GPQA, MuSR

**Post-training alignment (preference info) predicts:**
- IFEval (instruction following, verifiable constraint adherence)

Post-training consistently increases I(Z;preference) — representations learn to distinguish preferred from rejected — while complexity (I(X;Z)) barely changes.

**Implication for STOPA model selection:**
- For knowledge/reasoning tasks → optimize for compression optimality → base model quality matters
- For instruction-following tasks → post-trained/RLHF models necessary; base models insufficient regardless of size
- When mixing: instruction-tuned model with good base compression = best of both
- Sonnet vs Opus for instruction-following tasks: test alignment quality (preference info), not just benchmark scores
