---
date: 2026-04-12
type: best_practice
severity: high
component: orchestration
tags: [model-selection, information-bottleneck, compression, evaluation, tier-selection]
summary: "LLM optimality I(Y;Z)/I(X;Z) predicts benchmark performance (r=0.52) from a single forward pass on C4 — cheaper than benchmark eval suites. Preference info I(Z;pref) is stronger (r=0.76) and predicts alignment/instruction-following quality."
source: external_research
uses: 0
successful_uses: 0
harmful_uses: 0
confidence: 0.6
impact_score: 0.0
verify_check: "manual"
---

## Detail

Conklin et al. (arXiv:2604.07569, ICLR 2026) show that the Information Bottleneck optimality ratio — I(Y;Z)/I(X;Z), expressivity per bit of complexity — predicts aggregate benchmark performance across MMLU-Pro, BBH, MATH, GPQA, MuSR at Spearman r=0.52 (p<0.001). Preference information I(Z;preference) reaches r=0.76.

Both can be computed from internal model representations in a single forward pass using the soft entropy estimator (github.com/hcoxec/soft_h), without decoding or running behavioral evals.

**Practical implication:** When selecting between model tiers (haiku vs sonnet vs opus), optimality provides a principled information-theoretic signal beyond benchmark tables. Post-training (RLHF/DPO) shifts preference info without much changing complexity — base vs instruction-tuned choice matters for instruction following specifically.

**Key dissociation:** IFEval (instruction following) NOT predicted by compression optimality (r=0.07) — needs preference info (r=0.39). Other benchmarks predicted by compression. This means: pre-training compression ≠ alignment.
