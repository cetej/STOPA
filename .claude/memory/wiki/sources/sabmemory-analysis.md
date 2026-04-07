---
title: "sabmemory — Rozbor a doporučení pro STOPA"
slug: sabmemory-analysis
source_type: research_output
date_ingested: 2026-04-07
entities_extracted: 5
claims_extracted: 4
---
# sabmemory — Rozbor a doporučení pro STOPA

> **TL;DR**: sabmemory je lightweight MCP memory server v Rustu (4.1 MB, ~6 MB RAM) s SQLite FTS5, knowledge graph a 49 MCP tools. Pro STOPA je overkill — adoptovat vzory (token budget, expiry, importance), ne nástroj samotný.

## Key Claims

1. SQLite FTS5 + BM25 ranking překonává plain grep pro memory retrieval v rankingu, ale sémanticky je stejně omezený (keyword-only) — `[verified]`
2. 49 MCP tools = ~3000–5000 tokenů overhead per session vs. 0 tokenů overhead pro file-based memory — `[argued]`
3. Duplicitní memory systém (sabmemory + CC auto-memory) vede ke split-brain problému kde obě memory vidí různá data — `[argued]`
4. Token-budgeted search (default 8000 tokens) zabraňuje context overflow při memory retrieval — `[verified]`

## Entities

| Entity | Type | Status |
|--------|------|--------|
| sabmemory | tool | new |
| SQLite FTS5 | concept | new |
| BM25 ranking | concept | new |
| Knowledge Graph (sabmemory) | concept | existing (graphrag) |
| Three.js WebGL dashboard | tool | skip (generic) |

## Relations

- sabmemory `implements` SQLite FTS5
- sabmemory `uses` BM25 ranking
- sabmemory `exposes` 49 MCP tools
- sabmemory `alternative-to` STOPA file-based memory
- Token-budgeted search `pattern-of` sabmemory
