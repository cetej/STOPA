---
name: Post-it State Protocol
type: concept
first_seen: 2026-04-07
last_updated: 2026-04-07
sources: [mbif-cpr-research, mbif-cpr-implementation-plan]
tags: [memory, session, orchestration]
---

# Post-it State Protocol

> Per-agent/skill state files limited to 30 lines, overwritten on each run — provides cross-invocation continuity without accumulating unbounded context.

## Key Facts

- Implemented in My-Brain-Is-Full-Crew as `Meta/states/{name}.md` (ref: sources/mbif-cpr-research.md)
- Max 30 lines — force summarization; larger state goes into intermediate/*.json (ref: sources/mbif-cpr-research.md)
- Overwrite semantics (not append): each run writes fresh state (ref: sources/mbif-cpr-research.md)
- Skills derived from an agent share its post-it space (e.g., /defrag reads architect post-it) (ref: sources/mbif-cpr-research.md)
- YAML frontmatter: skill, updated, phase, invocation (ref: sources/mbif-cpr-research.md)
- Delete after successful task completion; cleanup at /sweep for files older than 24h (ref: sources/mbif-cpr-research.md)

## Relevance to STOPA

Already adopted in STOPA as `.claude/memory/intermediate/{skill-name}-state.md` (see memory-files.md rules). This research confirms the pattern is validated in production use by MBIF-Crew.

## Mentioned In

- [MBIF vs CPR Research](../sources/mbif-cpr-research.md)
- [MBIF/CPR Implementation Plan](../sources/mbif-cpr-implementation-plan.md)
