---
name: qmd
type: tool
first_seen: 2026-04-12
last_updated: 2026-04-12
sources: [claude-obsidian-llm-wiki-tutorial]
tags: [memory, knowledge-management, retrieval, search]
---

# qmd

> Lokální markdown search engine s hybridním BM25/vector rankingem a LLM re-rankingem — navržen jako wiki search layer pro Karpathy-style knowledge bases.

## Key Facts

- GitHub: `github.com/tobi/qmd` — open source, vše on-device (ref: sources/claude-obsidian-llm-wiki-tutorial.md)
- Dual interface: CLI (shell-out z agentů) + MCP server (native tool pro LLM) (ref: sources/claude-obsidian-llm-wiki-tutorial.md)
- Hybridní ranking: BM25 (keyword) + vector (semantic) + LLM re-ranking — kombinace tří signálů (ref: sources/claude-obsidian-llm-wiki-tutorial.md)
- Use case: wiki search při škálování nad ~100 zdrojů kde index.md přestává stačit (ref: sources/claude-obsidian-llm-wiki-tutorial.md)
- Alternativa k vlastnímu search scriptu — "LLM může pomoci vibe-code naivní search script" (ref: sources/claude-obsidian-llm-wiki-tutorial.md)

## Relevance to STOPA

Kandidát na replacement/rozšíření `scripts/hybrid-retrieve.py` pro wiki search. MCP interface by umožnil přímé tool volání z agentů bez shell-out. Vyhodnotit vs stávající BM25+graph approach v `memory-search.py`.

## Mentioned In

- [Claude + Obsidian Should Be Illegal](../sources/claude-obsidian-llm-wiki-tutorial.md)
