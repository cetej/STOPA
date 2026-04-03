---
date: 2026-04-01
status: DONE
component: memory
tags: [architecture, learnings, grep]
---

# 0001 — Memory architecture: stay markdown+grep

## Context
Evaluated whether to migrate from markdown+grep to LanceDB vector store for learnings retrieval as the system grew past 50 learnings files.

## Decision
Council verdict (5/5 unanimous): stay with markdown+grep. Implemented synonym fallback + confidence decay as improvements within current architecture.

## Alternatives Considered
- LanceDB vector store: rejected — added complexity without clear retrieval quality win at current scale

## Consequences
- Migration trigger defined: 500+ learnings OR 500ms grep OR 20% miss rate
- Full analysis: `research/council-verdict-memory-architecture-2026-04-01.md`
