---
name: Autoreason
type: tool
first_seen: 2026-04-13
last_updated: 2026-04-13
sources: [autoreason-self-refinement-framework]
tags: [orchestration, review, code-quality, iteration, evaluation]
---

# Autoreason

> Self-refinement framework from NousResearch that uses a tournament architecture (A/B/AB variants + blind Borda judge panel) to avoid prompt bias, scope creep, and lack of restraint in iterative improvement.

## Key Facts

- Tournament architecture: each iteration produces 3 competing versions — A (incumbent, unchanged), B (adversarial revision), AB (synthesis of A+B) (ref: sources/autoreason-self-refinement-framework.md)
- Judge panel: 3-7 fresh agents with no shared context vote via blind Borda count; "do nothing" is always a first-class option (ref: sources/autoreason-self-refinement-framework.md)
- Convergence: incumbent wins k=2 consecutive rounds → stop; avoids infinite refinement loops (ref: sources/autoreason-self-refinement-framework.md)
- Results: Haiku 3.5 + autoreason = 42/42 perfect sweep; Sonnet 4.6 77% vs 73% on 150 CodeContests; Haiku 3.5 40% vs 31% best-of-6 at matched compute (ref: sources/autoreason-self-refinement-framework.md)
- 7 judges converge 3× faster than 3 judges; removing either B or AB collapses performance (ref: sources/autoreason-self-refinement-framework.md)
- Narrowing returns at Haiku 4.5 (60% accuracy) — indicates generation-evaluation gap closing (ref: sources/autoreason-self-refinement-framework.md)
- Authors: SHL0MS and Hermes Agent (NousResearch, 2026) (ref: sources/autoreason-self-refinement-framework.md)

## Relevance to STOPA

Direct upgrade path for `/autoreason` skill: replace 2-variant debate with 3-variant tournament (A/B/AB), add Borda panel instead of single critic, add k=2 convergence detection. The "do nothing = valid option" principle maps to STOPA's circuit breaker logic.

## Mentioned In

- [Autoreason: Self-Refinement That Knows When to Stop](../sources/autoreason-self-refinement-framework.md)
