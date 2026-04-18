---
title: Memory-Augmented Routing — Knowledge Access Beats Model Size
category: concepts
tags: [memory, routing, retrieval, hybrid-retrieval, cost-reduction, persistent-agents]
sources: [raw/2026-04-18-memory-augmented-routing.md]
updated: 2026-04-18
---

# Memory-Augmented Routing — Knowledge Access Beats Model Size

**Paper**: arXiv:2603.23013  
**Authors**: Xunzhuo Liu, Bowei He, Xue Liu, Andy Luo, Haichen Zhang, Huamin Chen

## Core Finding

**47% of production queries** are semantically similar to prior interactions.

An 8B model with retrieved conversational context can recover **69% of a 235B model's performance** at **4% of the cost** (96% cost reduction).

The implication: for user-specific repetitive queries, knowledge access > raw model scale.

## Architecture

```
Incoming query
     ↓
[Memory Retrieval] — BM25 + cosine similarity hybrid
     ↓
  Hit?  →  YES: route to 8B model + context (96% of queries)
     ↓
   NO:  route to 235B model (4% of queries)
```

## Hybrid Retrieval

BM25 + cosine similarity achieves **+7.7 F1** over either method alone.
- BM25: exact keyword match, fast, good for specific terminology
- Cosine similarity: semantic match, handles paraphrase
- Hybrid: covers both failure modes

## Numbers

| Metric | Value |
|--------|-------|
| Queries routed to cheap path | 96% |
| Cost reduction | 96% |
| Performance recovery vs 235B | 69% |
| Hybrid retrieval gain | +7.7 F1 |
| Semantically similar queries | 47% of production |

## Benchmarks

- LoCoMo: 152 questions (conversational memory)
- LongMemEval: 500 questions (long-horizon memory)

## STOPA Relevance

STOPA's hybrid-retrieve.py (BM25 + grep + graph walk) is already aligned with this paper's retrieval approach. The routing insight is new: instead of always calling the strongest model, STOPA orchestrate could route simple/repetitive tasks to Haiku when memory retrieval hits a high-confidence match.

## Related Concepts

→ [agent-memory-taxonomy.md](agent-memory-taxonomy.md)  
→ [agentic-memory-unified.md](agentic-memory-unified.md)
