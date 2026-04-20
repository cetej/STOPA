---
title: ADR Generation with LLMs — Context Strategies
date: 2026-04-20
sources:
  - https://arxiv.org/abs/2604.03826
tags: [ai, architecture-decision-records, context-engineering, rag, documentation, prompt-engineering]
related:
  - context-engineering.md
  - architecture-descriptors-ai-agents.md
  - knowledge-drift-chronos.md
---

# ADR Generation with LLMs — Context Strategies

## Core Finding

When using LLMs to generate Architecture Decision Records (ADRs), how you present historical context matters more than which model you use. **Context engineering > model scale** as the dominant performance driver.

## Background: The ADR Problem

ADRs document the rationale behind architectural decisions. Despite their value, they're consistently underwritten because the authoring overhead is high. LLMs can reduce this overhead — if given the right context.

## Dataset

750 open-source repositories with sequential ADRs. Real project histories, not synthetic data.

## Five Strategies Evaluated

| Strategy | Description | Result |
|----------|-------------|--------|
| No context | Baseline — prompt only | Lowest quality |
| All-history | All previous ADRs | High token cost, diminishing returns |
| First-K | Earliest records | Context often stale/irrelevant |
| **Last-K (3-5)** | Most recent records | **Best balance: quality + efficiency** |
| RAFG | Retrieval-based selection | Marginal gains in typical workflows |

## Key Numbers

- **Optimal window**: 3-5 prior ADRs
- **Retrieval fallback**: useful for non-sequential/cross-cutting decisions, not routine sequential ADRs
- Context engineering contribution > model parameter scaling

## Broader Principle

This paper empirically confirms what context-engineering theory predicts: **the right context at the right scale beats more compute**. For sequential structured artifacts (ADRs, changelogs, decision logs), recent history is almost always the most relevant context.

## Relevance to STOPA

STOPA's decisions.md is a sequence of architectural decisions — analogous to ADRs. The optimal context window finding suggests:

- When `/scribe` writes a new decision, load the last 3-5 entries as context, not the full history
- `/evolve` generating learning revisions: use recent learning history (last 3-5 from same component), not full corpus

Also relevant for `/checkpoint`: session resume should prioritize the most recent context window over full history (already partially implemented via `## Session Detail Log` truncation boundary).

## Connections

- [context-engineering](context-engineering.md): empirical proof that deliberate context selection outperforms "more = better"
- [architecture-descriptors-ai-agents](architecture-descriptors-ai-agents.md): both address structured documentation for AI coding agents — descriptors at navigation level, ADR strategies at decision level
- [knowledge-drift-chronos](knowledge-drift-chronos.md): Chronos solves temporal drift in factual retrieval; ADR strategies solve temporal relevance in structured document retrieval — same underlying principle
