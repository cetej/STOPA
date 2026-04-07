---
name: Obsidian
type: tool
first_seen: 2026-04-07
last_updated: 2026-04-07
sources: [second-brain-gap-analysis]
tags: [knowledge-management, memory]
---

# Obsidian

> Markdown-based knowledge management tool s automatickou vizualizací backlinků jako graf — alternativní viewer pro STOPA wiki/learnings obsah.

## Key Facts

- Použití v STOPA kontextu: jednosměrný export (skript `export-to-obsidian.py`) — STOPA = source of truth, Obsidian = viewer (ref: sources/second-brain-gap-analysis.md)
- Výhody: okamžitě použitelné, zero custom code, graph view automaticky vizualizuje propojení přes `[[wiki links]]` (ref: sources/second-brain-gap-analysis.md)
- Nevýhody: duplicitní data, manuální re-export (ref: sources/second-brain-gap-analysis.md)
- Alternativa k HTML grafu (D3.js) — nevyžaduje vlastní vývoj (ref: sources/second-brain-gap-analysis.md)
- Export skript: ~150 řádků vs ~350 řádků pro D3.js variantu (ref: sources/second-brain-gap-analysis.md)

## Relevance to STOPA

Sekundární varianta (Cesta A) pro Knowledge Graph Visualization. Nižší effort než D3.js, ale méně integrovatelné. Doporučeno jako utility (ne core workflow).

## Mentioned In

- [Second Brain Gap Analysis](../sources/second-brain-gap-analysis.md)
