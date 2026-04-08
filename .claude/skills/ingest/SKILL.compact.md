---
name: ingest
variant: compact
description: Condensed ingest for repeat invocations within session. Use full SKILL.md for first invocation.
---

# Ingest — Compact (Session Re-invocation)

Raw source → structured knowledge: entity pages, source summaries, learnings, concept-graph.

## Input Flags

| Flag | Behavior |
|------|---------|
| (URL) | Fetch via Jina Reader (`https://r.jina.ai/{url}`) |
| (file path) | Read directly |
| `--batch <dir>` | Process all *.md in dir, largest-first, max 20 |
| `--backfill` | Process `outputs/*.md`, skip already-ingested |
| `--dry-run` | Show extraction plan, no writes |
| `--no-learnings` | Skip Phase 4c learning extraction |

## Pipeline

1. **Normalize** — get clean text (max 15K chars) + metadata. Generate slug (kebab, max 50 chars).
2. **Extract** — entities (max 12, skip generic), claims (3-8 with evidence levels), relations (max 8)
3. **Cross-reference** — entity resolution vs `wiki/entities/`, contradiction detection, concept-graph prep
4. **Store** — entity pages → source summary → optional learnings → concept-graph update → INDEX.md append

## Phase 4 Write Targets

| Artifact | Location | Size limit |
|---------|----------|-----------|
| Entity page (new/updated) | `wiki/entities/<name>.md` | 80 lines max |
| Source summary | `wiki/sources/<slug>.md` | 60 lines max |
| Learnings | `learnings/` | max 3 per source |
| concept-graph.json | root | add nodes + strengthen edges |

## Evidence Levels (claims)

`verified` | `argued` | `asserted` | `contradicts:<entity>`

## Entity Types

`tool` | `person` | `company` | `concept` | `paper`

## Circuit Breakers

- Skip files already in `wiki/sources/` (grep for slug — idempotent)
- Max 12 entities per source — force prioritization
- Max 20 files per batch run
- Skip generic entities (Python, GitHub, Google)
- If entity page exists and >30 lines with no new info → skip (add to Mentioned In only)
- Source summaries are append-only after creation

## Output on completion

Report: sources ingested, entities created/updated, learnings written, concept-graph nodes added.
For batch: table with per-file counts.
