---
name: Karpathy Wiki Pattern
type: concept
first_seen: 2026-04-07
last_updated: 2026-04-07
sources: [swarm-kb-research]
tags: [memory, knowledge-management, orchestration]
---

# Karpathy Wiki Pattern

> LLM-maintained knowledge base architecture: raw/ (immutable source dump) → wiki/ (LLM-maintained markdown with backlinks + index.md) → schema (CLAUDE.md/AGENTS.md). 4 phases: Ingest, Compile, Query, Lint.

## Key Facts

- Published by Andrej Karpathy ~April 2, 2026 as GitHub Gist (ref: sources/swarm-kb-research.md)
- Scale: ~100 articles, ~400K words on a research topic without RAG pipeline (ref: sources/swarm-kb-research.md)
- Extended by @jumperz into 10-agent swarm: raw/ → drafts/ → Hermes gate → live/ → per-agent briefings (ref: sources/swarm-kb-research.md)
- Script names (`wiki-compile.py`, `wiki-briefing.py`) are informal labels — no confirmed published code (ref: sources/swarm-kb-research.md)
- STOPA already partially implements this via `outputs/.research/` staging area (ref: sources/swarm-kb-research.md)

## Relevance to STOPA

Direct model for STOPA's `/compile` skill and wiki/ directory. P1 gap: unify agent output capture to `raw/` as staging area. P1 gap: add Hermes-style quality gate in `/compile` Phase 3.5.

## Mentioned In

- [Swarm KB Research](../sources/swarm-kb-research.md)
