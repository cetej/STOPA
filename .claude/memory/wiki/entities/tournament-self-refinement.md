---
name: Tournament Self-Refinement
type: concept
first_seen: 2026-04-13
last_updated: 2026-04-13
sources: [autoreason-self-refinement-framework]
tags: [orchestration, iteration, review, evaluation]
---

# Tournament Self-Refinement

> Iterative improvement architecture that generates 3 competing variants per round (A=incumbent, B=adversarial revision, AB=synthesis), judged by a blind panel — replacing linear critique-and-revise with a tournament where "do nothing" always competes.

## Key Facts

- 3 variants per round: A (unchanged), B (fresh agent adversarial revision), AB (synthesis of A and B) (ref: sources/autoreason-self-refinement-framework.md)
- Fresh agents for B, AB, and all judges — no shared context prevents bias accumulation (ref: sources/autoreason-self-refinement-framework.md)
- Incumbent preservation: A always competes, so refinement must beat the original to proceed (ref: sources/autoreason-self-refinement-framework.md)
- Ablation: removing B OR AB alone collapses performance — all three roles are necessary (ref: sources/autoreason-self-refinement-framework.md)
- Convergence: k=2 consecutive incumbent wins → stop (ref: sources/autoreason-self-refinement-framework.md)

## Relevance to STOPA

Extends the Improvement Operator (PDR framing) with an explicit incumbent preservation mechanism. The A/B/AB structure maps to STOPA's critic-in-loop: instead of one critic, run parallel revision + synthesis, then vote. Directly applicable to `/autoreason` skill upgrade.

## Mentioned In

- [Autoreason: Self-Refinement That Knows When to Stop](../sources/autoreason-self-refinement-framework.md)
