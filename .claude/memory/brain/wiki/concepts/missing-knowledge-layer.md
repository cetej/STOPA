---
title: The Missing Knowledge Layer in Cognitive Architectures
date: 2026-04-21
sources:
  - https://arxiv.org/abs/2604.11364
tags: [ai, cognitive-architecture, knowledge-layer, persistence-semantics, memory, coala]
related:
  - agent-memory-taxonomy.md
  - a-mem.md
  - agentic-memory-unified.md
  - knowledge-drift-chronos.md
---

# The Missing Knowledge Layer in Cognitive Architectures

## The Problem

Prominent frameworks (CoALA, JEPA) lack an **explicit Knowledge layer** with its own persistence semantics. The result: these systems incorrectly apply cognitive decay to factual information and use identical update mechanics for both facts and experiences.

**Facts don't decay like memories.** "Water boils at 100°C" doesn't become less true after 60 days of non-use. Applying Ebbinghaus decay to factual knowledge is an architectural error.

## Four-Layer Decomposition

| Layer | Persistence Semantics | Example |
|-------|----------------------|---------|
| **Knowledge** | Indefinite supersession | Facts, concepts — replaced only when contradicted by better evidence |
| **Memory** | Ebbinghaus decay | Episodic experiences — fade over time without reinforcement |
| **Wisdom** | Evidence-gated revision | Heuristics — only update when sufficient evidence accumulates |
| **Intelligence** | Ephemeral inference | Reasoning traces — valid only for the current context |

## Eight Convergence Points

Analysis of existing frameworks reveals 8 consistent gaps — systems conflate these four layers, leading to incorrect retrieval, inappropriate decay, and update collisions.

## Relevance to STOPA

STOPA's memory system partially separates these layers:
- `key-facts.md` = Knowledge (supersession only — "Updated when infrastructure changes")
- `memory/learnings/` = Memory (confidence decay for unused learnings — `uses == 0` after 60d: -0.1/30d)
- `critical-patterns.md` = Wisdom (evidence-gated: `uses >= 10 AND harmful_uses < 2`)
- Reasoning traces (current context) = Intelligence (ephemeral, not stored)

**Gap identified**: STOPA decays Knowledge alongside Memory (same `confidence` field). This paper suggests facts in `key-facts.md` should have NO decay — only supersession. Consider `valid_until: null` (explicit no-expiry) as a Knowledge marker.

## Connections

- [agent-memory-taxonomy](agent-memory-taxonomy.md): 3D taxonomy (temporal/substrate/control) maps partially to these 4 layers
- [knowledge-drift-chronos](knowledge-drift-chronos.md): Chronos addresses Knowledge layer specifically — temporal evolution of facts
- [a-mem](a-mem.md): Zettelkasten pattern treats notes as persistent — closer to Knowledge semantics than Memory
