---
name: RouteLLM
type: tool
first_seen: 2026-04-07
last_updated: 2026-04-07
sources: [mom-taro-discovery-2, mom-taro-research]
tags: [routing, cost-optimization, orchestration, model-selection]
---
# RouteLLM

> Open-source framework (lm-sys) that trains a lightweight router classifier on human preference data to route queries between strong/weak LLM models at inference time, achieving 2x cost reduction.

## Key Facts

- Achieves 2x cost reduction on MT Bench — uses GPT-4 only 14% of the time while maintaining 95% GPT-4 quality (ref: sources/mom-taro-discovery-2.md)
- Router trained on (Claude 3 Opus, Llama 3 8B) generalizes to (GPT-4, Mistral 7B) without retraining — learns abstract hardness features not model-specific artifacts (ref: sources/mom-taro-discovery-2.md)
- Paper: arXiv:2406.18665; GitHub: github.com/lm-sys/RouteLLM (ref: sources/mom-taro-discovery-2.md)
- Requires preference training data; threshold classifier runs on edge (ref: sources/mom-taro-discovery-2.md)
- Limitation for STOPA: preference data for Haiku/Sonnet/Opus may not exist (ref: sources/mom-taro-discovery-2.md)

## Relevance to STOPA

Direct replacement candidate for fixed `light/standard/deep/farm` tier assignment. Could route per-subtask instead of per-task, reducing wasted budget on easy steps within complex workflows.

## Mentioned In

- [Adaptive Model Routing in LLM Agent Systems](../sources/mom-taro-discovery-2.md)
- [MoM + TARo Research Brief](../sources/mom-taro-research.md)
