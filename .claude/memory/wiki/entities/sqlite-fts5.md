---
name: SQLite FTS5
type: concept
first_seen: 2026-04-07
last_updated: 2026-04-07
sources: [sabmemory-analysis]
tags: [memory, search]
---
# SQLite FTS5

> Full-text search extension built into SQLite — BM25 ranking, virtual tables, keyword-based (not semantic).

## Key Facts

- Built into Python's `sqlite3` stdlib — no additional dependency needed
- FTS5 virtual tables enable fast full-text search with BM25 ranking
- Keyword-based only — same semantic limitations as grep, but better ranking
- Auto-linking: sabmemory uses FTS5 similarity at write time to link related memories
- Fallback option for STOPA: Python script ~50 lines, SQLite as search index over markdown files (ref: sources/sabmemory-analysis.md)

## Relevance to STOPA

STOPA memory upgrade path: if grep becomes too slow (>500 files), SQLite FTS5 over existing markdown files is simpler than adopting sabmemory. SQLite stays regenerable — markdown remains primary storage. Pattern already partially implemented in `memory-search.py`.

## Mentioned In

- [sabmemory — Rozbor a doporučení pro STOPA](../sources/sabmemory-analysis.md)
