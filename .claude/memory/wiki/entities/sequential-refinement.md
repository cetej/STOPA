---
name: Sequential Refinement (SR)
type: concept
first_seen: 2026-04-08
last_updated: 2026-04-08
sources: [rethinking-thinking-tokens-pdr]
tags: [reasoning, inference, iteration, compute-efficiency]
---

# Sequential Refinement (SR)

> PDR special case (parallelism=1): iterative single-answer refinement that outperforms long chain-of-thought at matched sequential compute budgets.

## Key Facts

- Derived from PDR by setting parallelism to 1 — simplest form of the improvement-operator framing (ref: sources/rethinking-thinking-tokens-pdr.md)
- Outperforms long CoT at matched sequential budgets on AIME 2024/2025 benchmarks (ref: sources/rethinking-thinking-tokens-pdr.md)
- Avoids the context window growth problem of long CoT: each refinement step works on bounded context (ref: sources/rethinking-thinking-tokens-pdr.md)

## Relevance to STOPA

Validates `autoloop`'s core loop: iterate → refine → improve beats single long-context generation. Also validates critic-in-loop patterns: instead of one massive generation, run bounded refinements.

## Mentioned In

- [Rethinking Thinking Tokens: LLMs as Improvement Operators](../sources/rethinking-thinking-tokens-pdr.md)
