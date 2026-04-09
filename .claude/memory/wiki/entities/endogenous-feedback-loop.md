---
name: Endogenous Feedback Loop
type: concept
first_seen: 2026-04-09
last_updated: 2026-04-09
sources: [acemoglu-ai-aggregation-knowledge]
tags: [memory, aggregation, bias, learning-pipeline]
---

# Endogenous Feedback Loop

> When an AI aggregator trains on beliefs that were themselves shaped by the aggregator's previous output, creating a self-reinforcing cycle that amplifies existing biases rather than correcting them.

## Key Facts

- Formalized in Acemoglu et al. (arXiv:2604.04906) via extended DeGroot social learning model (ref: sources/acemoglu-ai-aggregation-knowledge.md)
- Fast update speed (low ρ) tightly couples aggregator to current biased beliefs — slow updates allow independent signal to accumulate (ref: sources/acemoglu-ai-aggregation-knowledge.md)
- Parallels model collapse (training on AI-generated data) but operates on beliefs/rules, not model weights (ref: sources/acemoglu-ai-aggregation-knowledge.md)

## Relevance to STOPA

STOPA's learning pipeline exhibits this exact loop: behavioral-genome guides agent behavior → agents generate learnings → /evolve promotes learnings back to behavioral-genome. Mitigated via: (1) circular validation detection in learning-admission.py, (2) slow graduation threshold (uses >= 10), (3) skill_scope field for local vs global graduation.

## Mentioned In

- [How AI Aggregation Affects Knowledge](../sources/acemoglu-ai-aggregation-knowledge.md)
