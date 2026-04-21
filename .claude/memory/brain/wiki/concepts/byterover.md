---
title: ByteRover — Agent-Native Hierarchical Memory
date: 2026-04-21
sources:
  - https://arxiv.org/abs/2604.01599
tags: [ai, agent-memory, hierarchical-context, memory-augmented-generation, maturity-tiers, rag, file-based-memory]
related:
  - agent-memory-taxonomy.md
  - a-mem.md
  - gaama.md
  - knowledge-compounding.md
  - missing-knowledge-layer.md
---

# ByteRover — Agent-Native Hierarchical Memory

## Core Innovation

ByteRover inverts the traditional memory system design: **the same LLM that reasons about tasks also curates and structures knowledge.** No separate storage system with different semantics — agent-native means the reasoner and the curator are one.

Traditional problem: "the system that stores knowledge does not understand it" → semantic misalignment between stored and queried representations.

## Context Tree Architecture

```
Domain
  └── Topic
        └── Subtopic
              └── Entry (atomic knowledge unit)
```

Each node has explicit relations and provenance tracking. Human-readable markdown on local filesystem — zero external infrastructure.

## 5-Tier Progressive Retrieval

| Tier | Method | Speed | Cost |
|------|--------|-------|------|
| 1 | Exact keyword match | Sub-10ms | Zero LLM |
| 2 | BM25 sparse retrieval | Sub-50ms | Zero LLM |
| 3 | Hierarchical navigation | Sub-100ms | Zero LLM |
| 4 | Graph walk | ~200ms | Zero LLM |
| 5 | LLM-curated synthesis | Seconds | LLM call |

**Most queries resolve at Tier 1-3** — the LLM is the last resort, not the first.

## Adaptive Knowledge Lifecycle (AKL)

- **Importance scoring**: not all knowledge is equal; entries scored by relevance and usage
- **Maturity tiers**: draft → validated → core (identical to STOPA's learning maturity system)
- **Recency decay**: unused entries decay; frequently accessed entries promoted

## Results

- SOTA on LoCoMo benchmark
- Competitive on LongMemEval
- No vector database, no embedding service, no graph server

## Relevance to STOPA

ByteRover is the closest external architecture to STOPA's learning system:
- Maturity tiers: STOPA adopted draft/validated/core before seeing this paper — independent validation
- File-based markdown: same principle as STOPA's `memory/learnings/`
- 5-tier retrieval: STOPA's grep-first → synonym fallback → hybrid (BM25+graph) = tiers 1→3→5
- Context Tree: 2BRAIN's wiki/concepts/ hierarchy mirrors this

**Key difference**: ByteRover is single-agent; STOPA extends to multi-agent with farm tier and shared ledgers.

## Connections

- [agent-memory-taxonomy](agent-memory-taxonomy.md): ByteRover implements Write-Manage-Read loop with LLM-curated management
- [gaama](gaama.md): GAAMA uses graph-based retrieval (PPR); ByteRover uses hierarchical tree — complementary approaches
- [knowledge-compounding](knowledge-compounding.md): ByteRover's AKL is the mechanism behind knowledge compounding's H(t)
