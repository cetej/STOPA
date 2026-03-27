---
name: Memory system upgrade ideas
description: Future ideas for upgrading STOPA memory — sabmemory patterns, FTS5 index, token budgeting. Low priority while grep suffices.
type: project
---

# Memory System — Nápady k budoucímu zvážení

**Zdroj**: Analýza sabmemory (2026-03-26), viz `outputs/sabmemory-analysis.md`
**Why:** Připravit se na moment kdy grep-first přestane stačit (500+ memory souborů).
**How to apply:** Neimplementovat dokud nenastane konkrétní problém (slow grep, missing results).

## Vzory k adopci (z sabmemory)

| Vzor | Implementace v STOPA | Effort | Kdy |
|------|---------------------|--------|-----|
| Token-budgeted search | Omezit grep output v memory-brief.sh na N tokenů | Nízký | Když kontext přetéká |
| Auto-forget/expiry | `expires: YYYY-MM-DD` v YAML frontmatter learnings | Nízký | Při maintenance |
| Importance scoring | `importance: 1-10` v YAML frontmatter | Střední | Při 200+ learnings |
| Memory versioning | `supersedes: <filename>` v frontmatter | Nízký | Při update conflicts |

## Fallback: Vlastní SQLite FTS5 index

Pokud grep přestane stačit, neadoptovat sabmemory (49 tools, Rust dep, SQLite-only).
Místo toho: Python script (~50 řádků) s `sqlite3` FTS5:
- Indexuje existující markdown memory soubory
- Markdown zůstává primary storage (git-friendly)
- SQLite jen jako search index (regenerovatelný)
- Zero new dependencies (sqlite3 built-in v Pythonu)

## Proč NE sabmemory/supermemory

- **sabmemory**: Git-unfriendly (SQLite), 49 tools = kontext bloat, Rust build na Windows, duplicitní systém
- **supermemory**: Cloud SaaS, placený Pro plan, vendor lock-in, privacy concern
- Naše file-based memory je git-tracked, human-readable, zero-overhead, pro ~50-200 memories plně stačí

## Trigger pro přehodnocení

- Memory soubory > 500 a grep je pomalý
- Potřeba cross-project memory search
- Potřeba entity relationships / knowledge graph
