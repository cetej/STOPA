---
name: dreams
variant: compact
description: Condensed dreams for repeat invocations within session. Use full SKILL.md for first invocation.
---

# Dreams — Compact (Session Re-invocation)

Offline memory consolidation: cross-link learnings, backward-update contexts, detect patterns.

## Smart Skip

Skip if: last dream < 3 days ago AND no new learnings AND no new outcomes. Log skip to `dreams/YYYY-MM-DD-skip.md`.

## Process

```
Phase 0: Smart Skip Check (dates, counts)
Phase 1: Collect — recent learnings (14d), outcomes, checkpoint, autodream-report, concept-graph
Phase 2: Consolidate
  2a: Cross-link (max 3 related: per learning, prefer cross-component)
  2b: Backward-update (append-only, max 1 per learning per cycle)
  2c: Pattern detection (3+ occurrences → critical-patterns candidate)
  2d: Concept graph edges (max 200 nodes)
  2e: Replay queue check (stale pending >14d, ready items)
Phase 3: Dream log → .claude/memory/dreams/YYYY-MM-DD.md
Phase 4: Abbreviated cycle if < 3 new items
```

## Circuit Breakers

- > 5 links per cycle → over-connecting, stop
- > 3 backward-updates per cycle → too aggressive
- Dream log > 100 lines → too verbose
- Phase 1 > 10 minutes → narrow scope

## Critical Rules

- NEVER delete/modify core learning content — only add `related:` and append context
- NEVER create new learnings — that's /scribe's job
- NEVER skip Smart Skip check
- All `related:` links must be bidirectional (A→B and B→A)
- Backward updates are append-only (original unchanged)
