---
name: NSA (Native Sparse Attention)
type: concept
first_seen: 2026-04-07
last_updated: 2026-04-07
sources: [attention-research]
tags: [attention, llm-architecture, deepseek, sparse-attention]
---

# NSA (Native Sparse Attention)

> DeepSeek's sub-quadratic sparse attention mechanism achieving O(Lk) complexity instead of O(L²); ACL 2025 Best Paper; first deployed in DeepSeek V3.2-Exp.

## Key Facts

- Paper: arXiv:2502.11089 (DeepSeek-AI, ACL 2025 Best Paper) (ref: sources/attention-research.md)
- Complexity: O(Lk) instead of O(L²) — enables much longer contexts efficiently (ref: sources/attention-research.md)
- DeepSeek V3.2-Exp (Sep 2025): first deployment of sub-quadratic sparse attention in a frontier model (ref: sources/attention-research.md)
- Built on top of MLA in V3.2-Exp (ref: sources/attention-research.md)
- Also called DSA (Dynamic Sparse Attention) in V3.2-Exp context (ref: sources/attention-research.md)

## Relevance to STOPA

Signals direction of frontier model attention architecture. When selecting models for long-context STOPA tasks, DeepSeek models with NSA offer better scaling efficiency.

## Mentioned In

- [Attention Mechanism Innovations](../sources/attention-research.md)
