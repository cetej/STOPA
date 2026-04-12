---
name: Karpathy Wiki Pattern
type: concept
first_seen: 2026-04-07
last_updated: 2026-04-12
sources: [swarm-kb-research, idea-file-research, second-brain-gap-analysis, claude-obsidian-llm-wiki-tutorial]
tags: [memory, knowledge-management, orchestration]
---

# Karpathy Wiki Pattern

> LLM-maintained knowledge base architecture: raw/ (immutable source dump) → wiki/ (LLM-maintained markdown with backlinks + index.md) → schema (CLAUDE.md/AGENTS.md). 4 operations: Ingest, Query, Lint, Morning Briefing.

## Key Facts

- Published by Andrej Karpathy ~April 2, 2026 as GitHub Gist (ref: sources/swarm-kb-research.md)
- Scale: ~100 articles, ~400K words on a research topic without RAG pipeline (ref: sources/swarm-kb-research.md)
- Extended by @jumperz into 10-agent swarm: raw/ → drafts/ → Hermes gate → live/ → per-agent briefings (ref: sources/swarm-kb-research.md)
- STOPA already partially implements this via `outputs/.research/` staging area (ref: sources/swarm-kb-research.md)
- **Queries-back-to-wiki**: odpovědi na dotazy by měly být uloženy zpět jako nové wiki stránky — kompound efekt, insights nesmizí do chat history (ref: sources/claude-obsidian-llm-wiki-tutorial.md)
- **Lint operace**: týdenní health-check — kontradikce, orphan pages, pojmy bez stránky, zastaralé claimy → `lint-report.md` (ref: sources/claude-obsidian-llm-wiki-tutorial.md)
- **Morning briefing cron**: `claude -p "Read Memory.md + new raw sources + print briefing"` na cron 7:30am — nastavit jednou, běží navždy (ref: sources/claude-obsidian-llm-wiki-tutorial.md)
- **Call transcript workflow**: jeden příkaz → dekompozice na rozhodnutí/akce/summary → Action-Tracker.md + Decision-Log.md + client note (ref: sources/claude-obsidian-llm-wiki-tutorial.md)
- **Division of labor**: LLM = summarizing, cross-referencing, filing, bookkeeping; Human = curating sources, asking questions, thinking (ref: sources/claude-obsidian-llm-wiki-tutorial.md)
- **qmd**: při škálování nad ~100 zdrojů, index.md nestačí → `github.com/tobi/qmd` jako search layer (ref: sources/claude-obsidian-llm-wiki-tutorial.md)
- Inspirováno Vannevar Bush Memex (1945) — asociativní stopy jako wiki backlinks (ref: sources/claude-obsidian-llm-wiki-tutorial.md)

## Relevance to STOPA

Direct model pro STOPA's `/compile`, `/ingest`, a wiki/ adresář. Nové: queries-back-to-wiki principle validuje přístup ukládání research výstupů. Morning briefing cron = direct pattern pro scheduled task (autodream.py). Lint operace = basis pro `/sweep` wiki maintenance.

## Mentioned In

- [Swarm KB Research](../sources/swarm-kb-research.md)
- [Idea File Research](../sources/idea-file-research.md)
- [Second Brain Gap Analysis](../sources/second-brain-gap-analysis.md)
- [Claude + Obsidian Should Be Illegal](../sources/claude-obsidian-llm-wiki-tutorial.md)
