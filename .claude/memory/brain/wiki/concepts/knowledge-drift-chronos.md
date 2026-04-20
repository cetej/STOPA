---
title: Knowledge Drift & Chronos — Time-Aware LLM Adaptation
date: 2026-04-20
sources:
  - https://arxiv.org/abs/2604.05096
tags: [rag, knowledge-drift, temporal-reasoning, event-evolution-graph, continual-learning]
related:
  - ecphory-rag.md
  - memory-augmented-routing.md
  - agent-memory-taxonomy.md
---

# Knowledge Drift & Chronos — Time-Aware LLM Adaptation

## Core Problem

LLMs are trained on fixed knowledge snapshots. Real-world knowledge **continuously drifts** — events update, facts change, contexts evolve. Standard adaptation methods all fail under realistic drift conditions:

| Method | Why It Fails |
|--------|-------------|
| Continual finetuning | Catastrophic forgetting of previous knowledge |
| Knowledge editing | Temporal inconsistency; cascading conflicts |
| Vanilla RAG | Retrieves stale or conflicting temporal evidence |

## The Benchmark

A dataset of **time-stamped real-world dynamic events** showing chronological knowledge evolution. Unlike existing static benchmarks, this captures genuine temporal drift patterns.

## Chronos: The Proposed Solution

**Time-aware retrieval** that organizes retrieved evidence into an **Event Evolution Graph**:
- Nodes = events at specific timestamps
- Edges = causal/temporal relationships between events
- No additional model training required
- Outperforms both vanilla RAG and learning-based approaches

## Key Insight

Temporal context isn't just *recency* — it's *trajectory*. A snapshot of a fact is less useful than understanding how that fact evolved. Chronos encodes the *direction of change*, not just its state.

## Relevance to STOPA

STOPA's learnings/ system has a similar problem: learnings can become stale or contradictory over time. The `valid_until:` field + confidence decay address this, but Chronos suggests a stronger solution: **event evolution tracking** for learnings that represent evolving best practices.

- `/evolve` could benefit from maintaining a change-trajectory per learning instead of just confidence decay
- The `supersedes:` chain in learnings is a primitive Event Evolution Graph

## Connections

- Extends [ecphory-rag](ecphory-rag.md): adds temporal dimension to entity-centric KG retrieval
- Complements [memory-augmented-routing](memory-augmented-routing.md): routing decides *what* to retrieve; Chronos structures *when/how facts changed*
- [agent-memory-taxonomy](agent-memory-taxonomy.md): Chronos implements temporally-aware read operation in write-manage-read loop
