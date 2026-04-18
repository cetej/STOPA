---
title: "Using Claude Code: Session Management & 1M Context"
slug: cc-session-management-1m-context
source_type: text
url: ""
date_ingested: 2026-04-18
date_published: "2026-04 (Anthropic internal)"
author: Anthropic
entities_extracted: 3
claims_extracted: 6
---

# Using Claude Code: Session Management & 1M Context

> **TL;DR**: Anthropic's official guidance on session management with 1M context. Key message: context rot starts at ~300-400k (not 95%), rewind is better than correction, and bad compacts happen when model can't predict next task direction.

## Key Claims

1. Context rot begins at ~300-400k tokens on 1M context model — `asserted` (task-dependent)
2. Model is at its LEAST intelligent point when compacting (due to context rot) — `argued`
3. Bad compact root cause: model can't predict session direction → drops off-axis content — `argued`
4. Rewind (Esc×2) drops messages after branch point — cleaner than appending correction — `argued`
5. "New task = new session" rule of thumb, 1M context doesn't override it — `asserted`
6. Subagent mental test: "will I need this tool output again, or just the conclusion?" — `argued`

## Entities

| Entity | Type | Status |
|--------|------|--------|
| [context-rot](../entities/context-rot.md) | concept | new |
| [rewind](../entities/rewind.md) | tool | new |
| [session-branching-point](../entities/session-branching-point.md) | concept | new |

## Relations

- `rewind` `competes_with` `correction` — rewind is cleaner: drops context vs. appends noise
- `context-rot` `causes` `bad-compact` — degraded model quality at compaction point
- `compact` `competes_with` `clear` — lossy auto-summary vs. curated hand-written brief
- `subagent` `part_of` `session management` — context isolation mechanism

## Cross-References

- Related learnings: `2026-04-01-autocompact-threshold.md`, `2026-04-14-compact-timing-60pct.md`, `2026-04-18-cc-graduated-compaction-5layer.md`
- Related wiki articles: [orchestration-infrastructure](../orchestration-infrastructure.md) (context/session section)
- Contradictions: none (complements existing compact guidance; adds absolute threshold + rewind pattern)
