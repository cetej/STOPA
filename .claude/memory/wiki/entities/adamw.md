---
name: AdamW
type: concept
first_seen: 2026-04-07
last_updated: 2026-04-07
sources: [gradient-descent-research]
tags: [deep-learning, optimization]
---

# AdamW

> Adam with decoupled weight decay (arXiv:1711.05101, Loshchilov & Hutter); de facto standard for training transformer models.

## Key Facts

- Key insight: L2 regularization ≠ weight decay for adaptive optimizers like Adam; decoupling is necessary for correct behavior (ref: sources/gradient-descent-research.md)
- De facto standard for transformer training (ref: sources/gradient-descent-research.md)
- Absent from Ruder's survey (last revised June 2017; paper published November 2017) (ref: sources/gradient-descent-research.md)
- Default in Hugging Face Transformers, PyTorch (ref: sources/gradient-descent-research.md)

## Relevance to STOPA

Use AdamW (not Adam) for any fine-tuning tasks in STOPA-adjacent ML projects. Reference for `/dependency-audit` skill when checking optimizer choices.

## Mentioned In

- [Gradient Descent Research](../sources/gradient-descent-research.md)
