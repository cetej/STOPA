---
name: Two-Phase LLM Training
type: concept
first_seen: 2026-04-12
last_updated: 2026-04-12
sources: [learning-is-forgetting-llm-lossy-compression]
tags: [llm-training, theory, compression, scaling, information-theory]
---

# Two-Phase LLM Training

> IB-predicted training dynamic: Phase 1 (fitting) — model learns to predict output (I(Y;Z)↑); Phase 2 (compression) — model compresses irrelevant input (I(X;Z)↓), approaching the IB bound.

## Key Facts

- Confirmed at LLM scale for the first time in OLMo2 7B and 32B (150 training checkpoints, 4T tokens) (ref: sources/learning-is-forgetting-llm-lossy-compression.md)
- Phase transition occurs when next-token prediction loss saturates (ref: sources/learning-is-forgetting-llm-lossy-compression.md)
- Originally theorized by Tishby & Zaslavsky 2015, disputed by Saxe 2019, now empirically settled at transformer scale (ref: sources/learning-is-forgetting-llm-lossy-compression.md)
- **Capacity threshold**: models below parameter threshold fail to enter Phase 2 — OLMo2 1B oscillates, never compresses; same for SmolLM2 1.7B (despite 11T tokens) and Pythia 6.9B (undertrained) (ref: sources/learning-is-forgetting-llm-lossy-compression.md)
- N-gram decomposition: high-performing models show less token-level info and more bigram/trigram/quadgram info — representations encode context, not individual tokens (ref: sources/learning-is-forgetting-llm-lossy-compression.md)

## Relevance to STOPA

Confirms fundamental limit of small models (haiku tier) — they may not achieve compression phase and thus cannot fully represent complex contextual reasoning patterns regardless of context window size.

## Mentioned In

- [Learning is Forgetting: LLM Training As Lossy Compression](../sources/learning-is-forgetting-llm-lossy-compression.md)
