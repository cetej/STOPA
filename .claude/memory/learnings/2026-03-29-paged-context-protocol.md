---
date: 2026-03-29
type: architecture
severity: medium
component: orchestration
tags: [context, memory, retrieval, budget, lazy-allocation, block-manifest]
summary: "Paged context protocol: read block-manifest.json (metadata) first, fetch only top-scored blocks by budget — prevents loading irrelevant learnings into agent context."
source: external_research
uses: 1
harmful_uses: 0
related: [gsd-patterns.md, 2026-03-26-harness-simplification.md]
verify_check: "Glob('.claude/memory/learnings/block-manifest.json') → 1+ matches"
confidence: 0.95
successful_uses: 0
---

## Pattern

Inspired by Paged Attention in LLMs (vLLM): instead of pre-allocating a large memory block for each request, allocate in small pages on demand.

Applied to STOPA context loading:
- **Before**: grep full files, read all matching learnings (pre-allocation)
- **After**: read `block-manifest.json` (lightweight metadata), score each block, fetch only top-N within token budget (lazy allocation)

## Analogie

| LLM Paged Attention | STOPA Context Protocol |
|--------------------|----------------------|
| KV Cache page | individual learning file |
| Page table | block-manifest.json |
| Memory capacity | context token budget |
| Page replacement policy | retrieval_score (severity × recency) |
| Shared prefix caching | critical-patterns.md (always-read, stable) |
| Internal waste (unused slots) | loading low-relevance learnings |

## Implementace

1. `block-manifest.json` generován skriptem `scripts/build-component-indexes.py`
2. Každý blok má `retrieval_score`, `token_estimate`, `active` flag
3. Orchestrate Context Bootstrap: score → sort → greedy fill do token budgetu
4. Agenti dostávají inline context — nečtou memory sami

## Token budgety

| Tier | Learning budget | Note |
|------|----------------|------|
| light | 0 (skip) | critical-patterns.md stačí |
| standard | ~2 000 tokens | top 3-5 learnings |
| deep | ~4 000 tokens | top 8-10 learnings + related expansion |

## Kdy použít

- Při každém `/orchestrate` volání (Context Bootstrap fáze)
- Při maintenance: rebuild manifest po přidání nových learnings
- Při hlídání kontextového bloatu: pokud agent dostává >5 000 tokenů learnings → snížit tier
