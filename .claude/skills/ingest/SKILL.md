---
name: ingest
description: "Use when processing a raw source (URL, file, research output) into structured knowledge — entity pages, source summaries, learnings, concept-graph updates. Trigger on 'ingest', 'zpracuj zdroj', 'extract knowledge'. Do NOT use for recording a single decision (/scribe) or synthesizing existing learnings (/compile)."
argument-hint: "<URL or file path> [--batch outputs/] [--dry-run] [--no-learnings]"
tags: [memory, documentation, research, synthesis]
phase: meta
user-invocable: true
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Agent, WebFetch
model: sonnet
effort: high
maxTurns: 20
input-contract: "user or deepresearch → URL, file path, or directory → non-empty readable content"
output-contract: "source summary → wiki/sources/<slug>.md + entity pages → wiki/entities/<name>.md + optional learnings → learnings/"
preconditions: ["wiki/ directory exists in .claude/memory/"]
effects: ["source summary written to wiki/sources/", "entity pages created or updated in wiki/entities/", "concept-graph.json updated with new entities and edges", "wiki/INDEX.md updated"]
handoffs:
  - skill: /compile
    when: "After batch ingest (10+ sources) to regenerate wiki synthesis"
    prompt: "Compile --incremental to integrate newly ingested sources"
  - skill: /scribe
    when: "Ingest produced a high-severity learning that needs recording"
    prompt: "Record learning: <what was learned>"
---

# Ingest — Raw Source → Structured Knowledge

You are the Knowledge Ingestor. You take raw sources (URLs, files, research outputs) and extract structured knowledge into the STOPA memory system: entity pages, source summaries, cross-references, and concept-graph updates.

**Core principle**: Raw sources rot in `outputs/`. Structured knowledge compounds in `wiki/`.
Every ingested source should leave the memory system richer than it found it.

## Shared Memory

Read first (silently, don't list contents):
- `.claude/memory/wiki/INDEX.md` — current wiki state
- `.claude/memory/learnings/critical-patterns.md` — top patterns (for cross-reference)
- `.claude/memory/concept-graph.json` — current entity/edge graph (READ STRUCTURE ONLY — entity keys + edge keys, not full file)

## Input

Parse `$ARGUMENTS`:
- **URL** (https://...) → fetch via Jina Reader (`https://r.jina.ai/{url}`), fallback to WebFetch
- **File path** → Read directly (supports .md, .txt, .pdf)
- **`--batch <dir>`** → Glob `<dir>/*.md`, process each file sequentially (max 20 per run)
- **`--dry-run`** → Show extraction plan without writing files
- **`--no-learnings`** → Skip learning extraction (only entities + source summary)
- **`--backfill`** → Batch mode for `outputs/` research reports (skip already-ingested)
- No arguments → prompt user for source

For `--batch` and `--backfill`: process files largest-first (most knowledge-dense).
Skip files already ingested: grep `wiki/sources/` for matching slug.

<!-- CACHE_BOUNDARY -->

## Pipeline (4 Phases)

### Phase 1: Normalize

**Goal:** Get clean text + metadata from any source type.

| Source type | Method | Metadata extracted |
|------------|--------|-------------------|
| URL | Jina Reader via WebFetch | title, author, date, URL |
| Local .md file | Read | filename, first H1 as title, date from frontmatter |
| Research output (`outputs/*.md`) | Read | title from H1, date from provenance file if exists |
| PDF | Read (built-in PDF support) | title, page count |

**Output:** `source_text` (string, max 15K chars — truncate with `[TRUNCATED]` marker) + `metadata` dict.

**Slug generation:** Kebab-case from title, max 50 chars. Example: "Agent Memory Problems Research" → `agent-memory-problems-research`.

### Phase 2: Extract (core intelligence)

Extract three types of structured data from the source text. Be selective — quality over quantity.

#### 2a. Entity Extraction

Identify the most important entities mentioned in the source:

| Entity type | What to extract | Examples |
|------------|----------------|---------|
| `tool` | Software, libraries, frameworks, APIs | LlamaFirewall, MemCollab, Jina Reader |
| `person` | Researchers, developers, thought leaders | Karpathy, Simon Willison |
| `company` | Organizations, labs, institutions | Anthropic, DeepMind, Virginia Tech |
| `concept` | Frameworks, methods, theories, patterns | spreading activation, RLHF, salience gate |
| `paper` | Academic papers, arXiv preprints | arXiv:2604.00901 (HERA) |

**Rules:**
- Max **12 entities** per source (force prioritization)
- Skip generic entities everyone knows (Python, JavaScript, GitHub, Google)
- Skip entities already well-covered: grep `wiki/entities/` for name — if exists and >30 lines, skip unless source adds NEW info
- Each entity: `{name, type, description (1 sentence), relevance_to_stopa (1 sentence)}`

#### 2b. Claim Extraction

Extract the 3-8 most important factual claims:

```
{claim, evidence_level, source_section}
```

Evidence levels:
- `verified` — source provides data/benchmarks/measurements
- `argued` — source makes a reasoned argument with supporting logic
- `asserted` — source states it without evidence
- `contradicts:<entity>` — claim contradicts something in existing memory

**Rules:**
- Every claim must be falsifiable and specific (not "AI is important")
- Include numbers/metrics when available ("reduces latency by 40%")
- Flag claims that contradict existing learnings or wiki articles

#### 2c. Relation Extraction

Identify relationships between extracted entities:

```
{entity_a, relation, entity_b, evidence}
```

Relations: `uses`, `extends`, `competes_with`, `contradicts`, `part_of`, `created_by`, `inspired_by`, `supersedes`

**Rules:**
- Max **8 relations** per source
- Only relations supported by the source text — no inference
- Prefer relations involving STOPA-relevant entities

### Phase 3: Cross-Reference

**Goal:** Connect new knowledge to existing memory.

#### 3a. Entity Resolution
For each extracted entity:
1. Grep `wiki/entities/` for entity name (case-insensitive)
2. Grep `learnings/` for entity name in tags/summary
3. Grep `wiki/sources/` for entity mentions

Decision:
- **New entity** (no matches) → will create entity page in Phase 4
- **Update existing** (matches, source adds new info) → will append to entity page
- **Skip** (matches, no new info) → log in source summary, don't update

#### 3b. Contradiction Detection
For each extracted claim:
1. Grep existing learnings for related keywords
2. If claim conflicts with existing learning → flag as `WARNING:` in source summary
3. Don't auto-resolve — human judgment needed

#### 3c. Concept-Graph Preparation
Prepare updates for `concept-graph.json`:
- New entities → new nodes
- Co-occurring entities (same source) → new or strengthened edges
- Existing entities with new learning file reference → update `learning_files` array

### Phase 4: Store

Write all artifacts. Order matters — entity pages first, then source summary (which references them).

#### 4a. Entity Pages

Location: `.claude/memory/wiki/entities/<name>.md`

For **new entities:**
```markdown
---
name: <Entity Name>
type: tool | person | company | concept | paper
first_seen: YYYY-MM-DD
last_updated: YYYY-MM-DD
sources: [<source-slug>]
tags: [<relevant tags>]
---

# <Entity Name>

> <1-sentence description>

## Key Facts

- <Fact 1 from source> (ref: sources/<source-slug>.md)
- <Fact 2> (ref: sources/<source-slug>.md)

## Relevance to STOPA

<1-2 sentences on why this matters for the orchestration system>

## Mentioned In

- [<Source Title>](../sources/<source-slug>.md)
```

For **existing entities** — append new facts and source reference:
- Add new facts under `## Key Facts`
- Add source to `sources:` frontmatter array
- Update `last_updated:` date
- Add to `## Mentioned In` list

**Rules:**
- Max 80 lines per entity page
- If entity page would exceed 80 lines: summarize older facts, keep most recent + most important
- Entity name in filename: lowercase, hyphens for spaces (e.g., `llamafirewall.md`, `spreading-activation.md`)

#### 4b. Source Summary

Location: `.claude/memory/wiki/sources/<slug>.md`

```markdown
---
title: "<Source Title>"
slug: <slug>
source_type: url | file | research_output
url: "<URL if applicable>"
date_ingested: YYYY-MM-DD
date_published: "<if known>"
entities_extracted: N
claims_extracted: N
---

# <Source Title>

> **TL;DR**: <2-3 sentence summary of the source>

## Key Claims

1. <Claim> — `[evidence_level]`
2. <Claim> — `[evidence_level]`

## Entities

| Entity | Type | Status |
|--------|------|--------|
| [Name](../entities/<name>.md) | tool/concept/... | new / updated / existing |

## Relations

- <Entity A> `relation` <Entity B> — <evidence>

## Cross-References

- Related learnings: <list of matched learning files>
- Related wiki articles: <list of matched wiki articles>
- Contradictions: <if any, with WARNING: prefix>
```

**Rules:**
- Max 60 lines per source summary
- Source summaries are append-only — never edit after creation (provenance)

#### 4c. Learnings (optional, skip with `--no-learnings`)

If the source contains actionable patterns for STOPA development:
- Max **3 learnings** per source (force highest-value selection)
- Use standard learning format (YAML frontmatter per memory-files.md rules)
- Set `source: external_research`
- Apply salience gate: skip if similar learning already exists (grep tags+component)

#### 4d. Concept-Graph Update

Run: `python scripts/update-concept-graph.py` if it exists.

If script doesn't exist, update manually:
1. Read `concept-graph.json`
2. For each new entity: add to `entities` with `mentions: 1`, `last_seen: today`, `learning_files: []`
3. For each entity pair co-occurring in this source: add/strengthen edge in `edges`
   - New edge: `weight: 1.0, count: 1`
   - Existing edge: `count += 1`, recalculate weight
4. Write back `concept-graph.json`

**Rules:**
- Don't add entities that already exist with same name (case-insensitive)
- Edge key format: `entity_a|entity_b` (alphabetical order)

#### 4e. INDEX.md Update

Append new source to wiki/INDEX.md:
- Add to sources section (create if doesn't exist)
- Update entity count
- Don't regenerate full INDEX — that's `/compile`'s job

### Batch Mode (`--batch` / `--backfill`)

For processing multiple files:

1. Glob target directory, sort by file size descending
2. Check `wiki/sources/` for already-ingested slugs — skip those
3. Process each file through Phase 1-4
4. **Between files:** brief status update (N/total, entities created, claims extracted)
5. After all files: summary table

**Backfill mode** (`--backfill`): targets `outputs/*.md` specifically:
- Skip `outputs/.research/` sub-files (only process final reports)
- Skip provenance files (`*-provenance.md`)
- Max 20 files per run (budget control)
- After backfill: suggest running `/compile --incremental`

## Anti-Rationalization Defense

| Rationalization | Why Wrong | Do Instead |
|---|---|---|
| "This source has too many entities, I'll extract them all" | Bloat kills retrieval quality — 50 shallow entities < 10 deep ones | Cap at 12, prioritize STOPA-relevant |
| "I'll skip cross-referencing, it takes too long" | Cross-refs are the compounding mechanism — without them ingest is just filing | Always run Phase 3, even if brief |
| "This source doesn't have learnings, so I'll skip Phase 4c entirely" | Source summary + entities alone are still valuable | Write source + entities even with `--no-learnings` |
| "The existing entity page is fine, no need to update" | New source = new perspective, even small additions compound | At minimum add to `Mentioned In` list |
| "I'll just save the raw text instead of extracting" | Raw text doesn't compound — structured knowledge does | Extract claims + entities, always |

## Red Flags

STOP and re-evaluate if any of these occur:
- Extracting more than 12 entities from a single source
- Creating entity pages with less than 3 facts
- Writing source summaries longer than 60 lines
- Skipping Phase 3 (cross-reference) for any reason
- Processing more than 20 sources in a single batch without pause

## Verification Checklist

- [ ] Source summary exists in `wiki/sources/<slug>.md` with correct frontmatter
- [ ] All entity pages reference the source in `Mentioned In`
- [ ] Entity pages have `relevance_to_stopa` section (not generic descriptions)
- [ ] Claims have evidence levels (not all marked `verified`)
- [ ] Cross-references found and listed (or explicitly noted as "no matches")
- [ ] Concept-graph.json updated with new entities (verify with grep)
- [ ] No duplicate entity pages created (check case-insensitive)

## Rules

1. **Quality over quantity.** 5 well-connected entities > 15 shallow stubs.
2. **STOPA relevance filter.** Skip entities irrelevant to orchestration, AI agents, or knowledge management.
3. **Idempotent.** Re-ingesting the same source should not create duplicates (check slug in sources/).
4. **Provenance.** Every fact in entity pages cites its source. No orphan claims.
5. **Budget awareness.** Batch mode: ~$0.02 per source (Haiku extraction). Report total at end.
6. **Don't block on imperfection.** Missing metadata, unknown dates, partial extraction — all OK. Write what you have, mark gaps.
