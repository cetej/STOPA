---
title: A-MEM — Zettelkasten-Inspired Agentic Memory
category: concepts
tags: [memory, zettelkasten, agent-memory, dynamic-indexing, knowledge-network]
sources: [raw/2026-04-18-a-mem-zettelkasten-agent-memory.md]
updated: 2026-04-18
---

# A-MEM — Zettelkasten-Inspired Agentic Memory

**Paper**: arXiv:2502.12110 (NeurIPS 2025)  
**Authors**: Wujiang Xu, Zujie Liang, Kai Mei, Hang Gao, Juntao Tan, Yongfeng Zhang

## Core Idea

A-MEM treats agent memory as an interconnected knowledge network — not a flat key-value store. Inspired by the Zettelkasten method (atomic notes linked by context), every memory note carries:
- Contextual description
- Keywords and tags
- Links to related historical notes

When a new memory is added, the system finds relevant existing notes and establishes bidirectional links. Crucially, new memories can trigger **updates to existing entries** — memory evolves rather than just accumulates.

## Why It Matters for STOPA

The A-MEM approach directly maps to STOPA's learnings/ system:
- Each learning file is an atomic note with tags/components
- `related:` field (max 3) is the link mechanism
- `supersedes:` field is Zettelkasten's "replacement" pattern
- Hybrid retrieval + graph walk = A-MEM's network traversal

The key A-MEM insight STOPA doesn't yet fully exploit: **new learnings should trigger review/update of related existing learnings** (not just append).

## Results

- Evaluated on 6 foundation models
- Outperforms SOTA baselines across diverse tasks
- Architecture generalizes across model families

## Key Contrast

| Approach | Structure | Evolution |
|----------|-----------|-----------|
| Flat memory store | Key-value lookup | No evolution |
| RAG/vector store | Similarity search | No evolution |
| A-MEM | Interconnected network | New memories update existing |

## Related Concepts

→ [agent-memory-taxonomy.md](agent-memory-taxonomy.md) — broader taxonomy  
→ [zettelkasten.md](zettelkasten.md) — source methodology  
→ [memfactory.md](memfactory.md) — complementary memory architecture
