---
name: Improvement Operator
type: concept
first_seen: 2026-04-08
last_updated: 2026-04-08
sources: [rethinking-thinking-tokens-pdr]
tags: [reasoning, inference, orchestration, compute-efficiency]
---

# Improvement Operator

> Framing of LLMs as operators that take a (draft, context) pair and produce a better output — enabling operation across the accuracy-efficiency Pareto frontier.

## Key Facts

- Core reframing: model is not just a generator but a refiner — it improves existing drafts rather than producing from scratch (ref: sources/rethinking-thinking-tokens-pdr.md)
- Enables controllable compute: trade parallelism (draft diversity) vs latency (sequential refinements) (ref: sources/rethinking-thinking-tokens-pdr.md)
- Unifies sampling, self-critique, and iterative refinement under one framework (ref: sources/rethinking-thinking-tokens-pdr.md)

## Relevance to STOPA

Theoretical grounding for why STOPA's critic-in-loop and autoloop patterns work: the model is most effective when refining bounded drafts, not when extending a single long context. Informs model selection: iterative tasks → larger model (exploits refinement feedback better).

## Mentioned In

- [Rethinking Thinking Tokens: LLMs as Improvement Operators](../sources/rethinking-thinking-tokens-pdr.md)
