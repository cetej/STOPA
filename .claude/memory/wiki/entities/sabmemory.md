---
name: sabmemory
type: tool
first_seen: 2026-04-07
last_updated: 2026-04-07
sources: [sabmemory-analysis]
tags: [memory, mcp, knowledge-graph]
---
# sabmemory

> Lightweight MCP memory server v Rustu — 4.1 MB binary, ~6 MB RAM, SQLite FTS5, 49 MCP tools, knowledge graph s 3D WebGL dashboardem.

## Key Facts

- Repo: https://github.com/Sablinova/sabmemory (v0.1.0, Rust, MIT, 2026-03-09)
- Storage: jediný SQLite soubor s FTS5 virtual tables
- Search: FTS5 BM25 + importance score boosting, token-budgeted výstup (default 8000 tokens)
- 49 tools: memories, entities, projects, documents, code artifacts, relationships, profily, versioning
- Auto-linking: nové memories automaticky propojeny s podobnými přes FTS5 při zápisu
- Auto-forget: `forget_after` datum → soft-forget + audit trail
- Versioning chains: `updates`/`extends`/`derives` — jen latest verze v search results
- Cross-project support přes container tags a projects namespace
- NOT git-friendly (SQLite binary), NOT human-readable (ref: sources/sabmemory-analysis.md)

## Relevance to STOPA

STOPA verdict: **neadoptovat jako celek**. Adoptovat vzory: token-budgeted search, auto-forget/expiry, importance scoring, memory versioning chains. Sabmemory by duplikoval CC native auto-memory a přidal 49-tool context bloat. Zvažit znovu při >500 memory files nebo potřebě cross-project search.

## Mentioned In

- [sabmemory — Rozbor a doporučení pro STOPA](../sources/sabmemory-analysis.md)
