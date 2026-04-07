---
name: MemGPT
type: paper
first_seen: 2026-04-07
last_updated: 2026-04-07
sources: [agent-memory-problems]
tags: [memory, context-management, paging]
---

# MemGPT

> Packer et al. 2023 (arXiv:2310.08560) — OS-inspired virtual context management pro LLM agenty s 3-tier paging (main/recall/archival).

## Key Facts

- 3-tier: main context (aktívní), recall storage (searchable), archival storage (long-term) (ref: sources/agent-memory-problems.md)
- Automatický page-in/page-out mezi tiers — agent sám rozhoduje co přesunout
- 93.4% na DMR benchmark (Zep dosahuje 94.8%)
- Landmark paper pro UMG řešení — paging = bounded growth

## Relevance to STOPA

STOPA memory systém (working memory v kontextu / learnings/ / archiv) je analogický 3-tier MemGPT struktuře. Max 500 řádků + archivace pravidlo odpovídá paging principu. Rozdíl: STOPA používá file-based storage místo programatického paging API.

## Mentioned In

- [Agent Memory Problems Research](../sources/agent-memory-problems.md)
