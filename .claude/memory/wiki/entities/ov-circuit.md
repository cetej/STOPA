---
name: OV Circuit (Output-Value)
type: concept
first_seen: 2026-04-12
last_updated: 2026-04-12
sources: [mechanistic-steering-refusal-circuits]
tags: [interpretability, attention, mechanistic, steering]
---

# OV Circuit (Output-Value)

> The output-projection × value component of transformer attention heads; the primary mechanistic pathway through which representation steering modifies model behavior.

## Key Facts

- Refusal steering interacts almost exclusively through OV circuit — freezing attention scores (QK) drops performance by only 8.75% — ref: sources/mechanistic-steering-refusal-circuits.md
- Top circuit edges predominantly connect to attention values, MLPs, and output head — nearly excluding query/key pathways — ref: sources/mechanistic-steering-refusal-circuits.md
- Mathematical decomposition of steered OV circuit reveals semantically interpretable concepts even when original steering vector lacks interpretability — ref: sources/mechanistic-steering-refusal-circuits.md

## Relevance to STOPA

Understanding that steering bypasses QK means STOPA's behavioral hooks (calm-steering, panic-detector) operate at the output/value level — they don't fight against the model's attention routing, making them efficient.

## Mentioned In

- [What Drives Representation Steering?](../sources/mechanistic-steering-refusal-circuits.md)
