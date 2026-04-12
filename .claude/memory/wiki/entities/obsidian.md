---
name: Obsidian
type: tool
first_seen: 2026-04-07
last_updated: 2026-04-12
sources: [second-brain-gap-analysis, claude-obsidian-llm-wiki-tutorial]
tags: [knowledge-management, memory]
---

# Obsidian

> Markdown-based knowledge management tool s automatickou vizualizací backlinků jako graf — alternativní viewer pro STOPA wiki/learnings obsah.

## Key Facts

- Použití v STOPA kontextu: jednosměrný export (skript `export-to-obsidian.py`) — STOPA = source of truth, Obsidian = viewer (ref: sources/second-brain-gap-analysis.md)
- Výhody: okamžitě použitelné, zero custom code, graph view automaticky vizualizuje propojení přes `[[wiki links]]` (ref: sources/second-brain-gap-analysis.md)
- Nevýhody: duplicitní data, manuální re-export (ref: sources/second-brain-gap-analysis.md)
- Alternativa k HTML grafu (D3.js) — nevyžaduje vlastní vývoj (ref: sources/second-brain-gap-analysis.md)
- **Obsidian-as-IDE mental model**: CC provádí edity wiki, Obsidian zobrazuje výsledky v real-time — "Obsidian is the IDE; the LLM is the programmer; the wiki is the codebase" (ref: sources/claude-obsidian-llm-wiki-tutorial.md)
- **Obsidian Web Clipper**: browser extension — převádí web články na markdown pro okamžitý ingest do raw/ (ref: sources/claude-obsidian-llm-wiki-tutorial.md)
- **Dataview plugin**: queries přes YAML frontmatter — generuje dynamické tabulky pokud LLM přidává frontmatter do stránek (ref: sources/claude-obsidian-llm-wiki-tutorial.md)
- **Marp plugin**: markdown → slide deck format — generovatelné z wiki obsahu (ref: sources/claude-obsidian-llm-wiki-tutorial.md)
- **Image download hotkey**: Settings → Files → Attachment folder path (`raw/assets/`) + hotkey "Download attachments for current file" (Ctrl+Shift+D) — images lokálně pro LLM vision access (ref: sources/claude-obsidian-llm-wiki-tutorial.md)
- Graph view = nejlepší způsob vizualizace shape wiki — co je propojeno, hubs, orphans (ref: sources/claude-obsidian-llm-wiki-tutorial.md)

## Relevance to STOPA

Sekundární varianta (Cesta A) pro Knowledge Graph Visualization. Nižší effort než D3.js, ale méně integrovatelné. Doporučeno jako utility (ne core workflow). Obsidian-as-IDE model validuje přístup: STOPA wiki = codebase, CC = programmer.

## Mentioned In

- [Second Brain Gap Analysis](../sources/second-brain-gap-analysis.md)
- [Claude + Obsidian Should Be Illegal](../sources/claude-obsidian-llm-wiki-tutorial.md)
