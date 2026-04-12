---
name: Principia — On-Policy Judge Training
description: Meta FAIR paper proving on-policy LLM judges beat prompted/off-policy judges; rule-based verification is brittle; MC shortcuts = rationalization; cross-format transfer from harder outputs
type: reference
---

**Paper:** arXiv:2603.18886 (Meta FAIR + CMU, 2026-03-19)
**Title:** Reasoning over Mathematical Objects: On-Policy Reward Modeling and Test Time Aggregation
**Data:** [principia-collection](https://huggingface.co/datasets/facebook/principia-collection) | [principia-bench](https://huggingface.co/datasets/facebook/principia-bench)

## Key findings relevant to STOPA

1. **On-policy judge >> off-policy/prompted judge**: Judge trained on actual model outputs (on-policy) significantly outperforms prompted judges (even larger GPT-OSS-120B) and off-policy trained ones. Validates STOPA's `impact_score` mechanism measuring on real outputs.

2. **Rule-based verification is brittle**: SymPy/math-verify fails on equivalent but differently-formatted expressions (10-20% miss rate). Validates need for LLM critic alongside rule-based hooks (grep, ruff).

3. **MC shortcutting = rationalization**: Models backward-chain from easy options, collapse without them (10-20% drop across frontier models including o3). Quantitative evidence for Anti-Rationalization Defense tables in skills.

4. **Cross-format transfer**: Training on harder format (structured math objects) improves easier formats (numerical +7.5-17.5%, MCQA +12.31-25.47%). Argument for strict Verification Checklists — demanding structured output improves general reasoning.

5. **Test-time aggregation scales with on-policy training**: Multi-sample + judge aggregation improves quality. Academic validation for `/council` multi-persona pattern.

## How to apply

- Future critic/eval improvements: calibrate judges on actual workflow outputs (on-policy), not generic rubrics
- Keep dual verification: rule-based hooks + LLM critic (neither alone is sufficient)
- Maintain strict output format requirements in skills — cross-format transfer means harder format = better reasoning
