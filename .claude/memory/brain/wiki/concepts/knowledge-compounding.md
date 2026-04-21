---
title: Knowledge Compounding — Agentic ROI Framework
date: 2026-04-21
sources:
  - https://arxiv.org/abs/2604.11243
tags: [ai, knowledge-compounding, token-efficiency, llm-wiki, agentic-roi, persistent-memory]
related:
  - llm-wiki.md
  - byterover.md
  - memory-augmented-routing.md
---

# Knowledge Compounding — Agentic ROI Framework

## Core Insight

LLM tokens should be treated as **capital goods** (appreciate through use) rather than consumables (burned per query). A persistent knowledge base makes each query cheaper over time — this is **knowledge compounding**.

## The Agentic ROI Model

Standard ROI model assumes task costs are **mutually independent** — each query costs roughly the same. This breaks down when you introduce a persistent KB.

Revised model: **Cost(t)** is a time-varying function governed by knowledge-base coverage rate **H(t)**:
- As H(t) increases, retrieval hit rate improves → fewer tokens per query
- Ingestion cost is amortized across all future queries that hit the cache

## Empirical Results

| Scenario | Compounding | RAG Baseline | Savings |
|----------|-------------|--------------|---------|
| 4 sequential queries | 47K tokens | 305K tokens | **84.6%** |
| 30-day medium concentration | — | — | **53.7%** |
| 30-day high concentration | — | — | **81.3%** |

## Three Compounding Mechanisms

1. **Amortized ingestion costs** — pay once, retrieve many times
2. **Auto-feedback loops** — KB improves its own coverage from usage signals
3. **External result write-back** — successful retrieval enriches KB for future queries

## Relevance to STOPA

This paper formally justifies STOPA's investment in:
- `memory/learnings/` system: each learning amortizes across future uses (tracked via `uses` counter)
- `critical-patterns.md`: top-10 always-loaded patterns = zero marginal retrieval cost
- `/compile` skill: synthesis increases H(t) coverage for complex queries
- 2BRAIN itself: this very wiki is the compounding knowledge base that reduces per-session token cost

The maturity tier system (draft → validated → core) is a direct implementation of H(t) optimization: core patterns have H(t) ≈ 1.0 for their domain.

## Connections

- [llm-wiki](llm-wiki.md): Karpathy's LLM Wiki pattern is the practical implementation; this paper provides the economic theory
- [memory-augmented-routing](memory-augmented-routing.md): 47% semantic similarity → compounding means those queries get cheaper over time
- [byterover](byterover.md): ByteRover's hierarchical Context Tree is an architecture for maximizing H(t)
