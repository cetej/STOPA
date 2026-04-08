---
name: Instruction-Following Specialization
type: concept
first_seen: 2026-04-08
last_updated: 2026-04-08
sources: [llms-follow-instructions-skillful-coordination]
tags: [skill-design, orchestration, prompting, interpretability]
---

# Instruction-Following Specialization

> Instruction-following in LLMs uses diverse, task-specific neural representations rather than a single universal constraint-checking mechanism.

## Key Facts

- General probes underperform task-specific probes across all tested models (Llama 3.1 8B, Gemma 2 2B, Qwen2.5-0.5B) — minimal representational sharing between different instruction types (ref: sources/llms-follow-instructions-skillful-coordination.md)
- Cross-task transfer is weak and clusters by task *similarity*, not by task *category* — structural tasks don't generalize to semantic ones (ref: sources/llms-follow-instructions-skillful-coordination.md)
- Early model layers encode structural constraints (formatting, word counts); later layers encode semantic information (sentiment, topic) (ref: sources/llms-follow-instructions-skillful-coordination.md)
- Constraint satisfaction operates dynamically during generation (continuous monitoring), not via pre-generation planning (ref: sources/llms-follow-instructions-skillful-coordination.md)
- Model variation: Llama = constraint-specific signals; Qwen = relies on general LM features; Gemma = intermediate (ref: sources/llms-follow-instructions-skillful-coordination.md)

## Relevance to STOPA

Validates STOPA's specialized skill architecture: mixing constraint types in one prompt (format + content + semantic) is less effective than separate specialized skill invocations. Supports the principle of "one skill, one constraint domain."

## Mentioned In

- [How LLMs Follow Instructions: Skillful Coordination, Not a Universal Mechanism](../sources/llms-follow-instructions-skillful-coordination.md)
