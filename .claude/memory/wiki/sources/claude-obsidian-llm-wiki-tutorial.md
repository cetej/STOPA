---
title: "Claude + Obsidian Should Be Illegal — LLM Wiki Tutorial"
slug: claude-obsidian-llm-wiki-tutorial
source_type: social_post
url: ""
date_ingested: 2026-04-12
date_published: "~2026-04"
entities_extracted: 6
claims_extracted: 6
---

# Claude + Obsidian Should Be Illegal — LLM Wiki Tutorial

> **TL;DR**: Praktický návod na Karpathy LLM Wiki pattern s Claude Code + Obsidian. Klíčové: Obsidian = IDE/viewer, CC = programmer, wiki = codebase. Přidává 4 operační vzory (ingest, query, lint, morning briefing) + qmd jako search tool. Původní idea file Karpathy zahrnuta jako součást postu.

## Key Claims

1. LLM wiki jako "compounding artifact" — odpovědi na dotazy by měly být uloženy zpět do wiki jako nové stránky, jinak zmizí do chat history — `[argued]`
2. Obsidian-as-IDE / CC-as-programmer / wiki-as-codebase mental model: CC provádí změny, Obsidian zobrazuje výsledky v real-time — `[asserted]`
3. Morning briefing cron (`claude -p "..."` na 7:30am) čte Memory.md + nové raw soubory za 24h + tiskne briefing — nastavit jednou, běží navždy — `[asserted]`
4. Call transcript → multi-file update: jeden příkaz extrahuje rozhodnutí, akce, summary; aktualizuje Action-Tracker.md, Decision-Log.md, vytvoří client note — `[asserted]`
5. Lint operace (weekly): vyhledá kontradikce, orphan pages, pojmy bez stránky, zastaralé claimy — wiki zůstane zdravá automaticky — `[argued]`
6. qmd (`github.com/tobi/qmd`): hybrid BM25/vector search pro lokální markdown soubory, CLI + MCP server, vhodný pro wiki search při škálování nad ~100 zdrojů — `[asserted]`

## Entities

| Entity | Type | Status |
|--------|------|--------|
| [Karpathy Wiki Pattern](../entities/karpathy-wiki-pattern.md) | concept | updated |
| [Obsidian](../entities/obsidian.md) | tool | updated |
| [qmd](../entities/qmd.md) | tool | new |
| [Vannevar Bush Memex](../entities/vannevar-bush-memex.md) | concept | new |
| Obsidian Web Clipper | tool | mentioned |
| Marp | tool | mentioned |

## Relations

- Obsidian `used_with` Claude Code — real-time wiki viewer během CC edits
- qmd `extends` Karpathy Wiki Pattern — search layer pro scale >100 zdrojů
- Karpathy Wiki Pattern `inspired_by` Vannevar Bush Memex — personal curated knowledge + associative trails
- Morning Briefing Pattern `extends` Karpathy Wiki Pattern — operační cron varianta

## Cross-References

- Related learnings: `2026-04-07-ingest-pipeline-architecture.md` (pokud existuje), memory-architecture wiki článek
- Related wiki articles: [memory-architecture](../memory-architecture.md), [karpathy-nopriors-autoagent-loopy-era](karpathy-nopriors-autoagent-loopy-era.md)
- Contradictions: none
