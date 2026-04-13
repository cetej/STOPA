---
name: Pro-AI Bias
type: concept
first_seen: 2026-04-13
last_updated: 2026-04-13
sources: [pro-ai-bias-llms]
tags: [bias, recommendation, ai-safety, training-data, emergent]
---

# Pro-AI Bias

> Systematic preference of LLMs toward AI/ML solutions in recommendation tasks — emergent from training data, not injected via system prompt. Proprietary models show near-deterministic AI preference.

## Key Facts

- LLMs disproportionately recommend AI-related options across diverse advice-seeking queries (ref: sources/pro-ai-bias-llms.md)
- Proprietary models exhibit near-deterministic AI preference behavior (ref: sources/pro-ai-bias-llms.md)
- AI job salaries overestimated by ~10 percentage points vs matched non-AI jobs (ref: sources/pro-ai-bias-llms.md)
- "Artificial Intelligence" has highest cross-framing similarity in open-weight model embeddings (ref: sources/pro-ai-bias-llms.md)
- Detectable via controlled counterfactual testing: replace AI recommendation category and measure consistency (ref: sources/pro-ai-bias-llms.md)

## Why This Matters

This is the training-data analog of commercial persuasion. Princeton showed system-prompt injection creates asymmetric treatment. Pro-AI bias shows the same asymmetry emerges from training data alone — no injection needed. Together, they demonstrate AI recommendation bias has both structural (training) and operational (system prompt) sources.

## Relevance to STOPA

When STOPA agents recommend tools, libraries, or approaches, they may systematically favor AI/ML solutions. Counterfactual testing: ask the same question but swap the domain (AI → traditional) and check if recommendation quality/enthusiasm is symmetric.

## Mentioned In

- [Pro-AI Bias in LLMs](../sources/pro-ai-bias-llms.md)
