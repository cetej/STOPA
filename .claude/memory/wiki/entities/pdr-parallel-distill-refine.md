---
name: PDR (Parallel-Distill-Refine)
type: concept
first_seen: 2026-04-08
last_updated: 2026-04-08
sources: [rethinking-thinking-tokens-pdr]
tags: [orchestration, inference, reasoning, compute-efficiency]
---

# PDR (Parallel-Distill-Refine)

> Three-phase inference framework: generate diverse drafts in parallel, distill into bounded workspace, refine iteratively — decoupling context length from total token spend.

## Key Facts

- Three stages: (1) parallel generation of diverse solution drafts, (2) distillation into bounded textual workspace, (3) refinement using workspace (ref: sources/rethinking-thinking-tokens-pdr.md)
- Context length is controllable via degree of parallelism — not tied to total tokens generated (ref: sources/rethinking-thinking-tokens-pdr.md)
- Special case: parallelism=1 → Sequential Refinement (SR), which outperforms long CoT at matched compute (ref: sources/rethinking-thinking-tokens-pdr.md)
- RL training aligned with PDR inference on 8B model: +11% AIME 2024, +9% AIME 2025 (ref: sources/rethinking-thinking-tokens-pdr.md)

## Relevance to STOPA

Direct blueprint for `autoresearch` and `autoloop` patterns: generate diverse candidate solutions in parallel agents, distill findings, refine — without growing context. The parallelism-controls-quality insight validates STOPA's multi-agent farm tier over single long-context agents.

## Mentioned In

- [Rethinking Thinking Tokens: LLMs as Improvement Operators](../sources/rethinking-thinking-tokens-pdr.md)
