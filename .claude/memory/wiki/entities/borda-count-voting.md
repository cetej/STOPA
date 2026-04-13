---
name: Borda Count Voting
type: concept
first_seen: 2026-04-13
last_updated: 2026-04-13
sources: [autoreason-self-refinement-framework]
tags: [evaluation, orchestration, review]
---

# Borda Count Voting

> Rank-aggregation method where each judge ranks all candidates, and points are assigned by rank position — used in autoreason's judge panel for blind multi-agent voting on refinement outcomes.

## Key Facts

- Each judge ranks A, B, AB independently with no shared context — eliminates verbosity bias and positional bias (ref: sources/autoreason-self-refinement-framework.md)
- 7 judges converge 3× faster to correct winner than 3 judges (ref: sources/autoreason-self-refinement-framework.md)
- "Do nothing" (incumbent A) is always a ranked candidate — unlike critique-and-revise where revision is assumed necessary (ref: sources/autoreason-self-refinement-framework.md)
- Blind: judges receive outputs without labels (A/B/AB) (ref: sources/autoreason-self-refinement-framework.md)

## Relevance to STOPA

Replaces single-critic verdict in STOPA with a panel vote — reduces individual judge hallucination and verbosity inflation. 7-judge configuration is practical minimum for fast convergence. Can be implemented as parallel agent spawns with structured ranking output.

## Mentioned In

- [Autoreason: Self-Refinement That Knows When to Stop](../sources/autoreason-self-refinement-framework.md)
