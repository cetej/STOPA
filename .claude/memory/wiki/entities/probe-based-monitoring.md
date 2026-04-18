---
name: Probe-based Monitoring
type: tool
first_seen: 2026-04-18
last_updated: 2026-04-18
sources: [cognitive-companion-parallel-monitoring]
tags: [monitoring, mechanistic-interpretability, hidden-states, zero-overhead]
---

# Probe-based Monitoring

> Linear probe trained on LLM hidden states to detect reasoning degradation with zero inference overhead.

## Key Facts

- Trained on hidden states from layer 28 (in the tested models) (ref: sources/cognitive-companion-parallel-monitoring.md)
- AUROC 0.840 cross-validated on proxy-labeled dataset; mean effect size +0.471 (ref: sources/cognitive-companion-parallel-monitoring.md)
- Zero measured inference overhead — probe runs on cached activations, no extra forward pass
- Alternative to LLM-as-judge (~10-15% overhead per step) and LLM-based Companion (~11% overhead)
- Requires hidden-state access — not available via proprietary API (Claude, GPT); only applicable to self-hosted/open models

## Relevance to STOPA

Not directly applicable to STOPA (Claude API exposes no hidden states). Architecturally useful as reference: when we eventually need monitoring for self-hosted worker models (e.g., local Ollama for bulk tasks), probe-based is the cheapest option. Current STOPA approach (edit→fail pattern matching in panic-detector.py) is analogous at the behavioral level — pattern-match observable outputs instead of hidden states.

## Mentioned In

- [Cognitive Companion: Parallel Monitoring](../sources/cognitive-companion-parallel-monitoring.md)
