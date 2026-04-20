---
source: https://arxiv.org/abs/2604.03826
fetched: 2026-04-20
type: arxiv-paper
authors: Aviral Gupta, Rudra Dhar, Daniel Feitosa, Karthik Vaidhyanathan
title: "Context Matters: Evaluating Context Strategies for Automated ADR Generation Using LLMs"
accepted: EASE Conference 2026
---

# Raw: ADR Generation Context Strategies

## Abstract Summary
ADR creation is underutilized despite importance due to authoring overhead. LLMs can help. Context presentation strategy fundamentally shapes output quality.

## Dataset
750 open-source repositories with sequential ADRs.

## Five Context Strategies Evaluated
1. No context (baseline)
2. All-history (complete previous records)
3. First-K (earliest records)
4. Last-K (recent records)
5. RAFG (retrieval-based context)

## Key Results
- Small recency window (3-5 prior records) = best balance quality/efficiency
- Retrieval-based selection = marginal gains in typical sequential workflows
- Context engineering > model scale alone

## Practical Contribution
Recommended defaults for tool builders + targeted retrieval fallbacks for complex scenarios.
