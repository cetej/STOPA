---
name: Pre-compaction Flush
type: concept
first_seen: 2026-04-07
last_updated: 2026-04-07
sources: [swarm-kb-research]
tags: [memory, session, orchestration]
---

# Pre-compaction Flush

> A silent agent turn executed before context compression that writes lasting insights to a daily memory file, preventing knowledge loss during compaction.

## Key Facts

- Prompt: "Write any lasting notes to memory/YYYY-MM-DD.md; reply NO_REPLY if nothing to store" (ref: sources/swarm-kb-research.md)
- Implemented in OpenClaw as part of its memory architecture (ref: sources/swarm-kb-research.md)
- Addresses the gap: compaction destroys in-context reasoning and decisions that were never persisted (ref: sources/swarm-kb-research.md)
- Two levels: agent-level (sub-agents write to raw/ before returning) + session-level (before /compact) (ref: sources/swarm-kb-research.md)

## Relevance to STOPA

STOPA P2 gap. Implement as extension to `/compact` skill: before compaction, run sub-agent with flush prompt. Also adoptable in `/orchestrate` agent prompt template as P1-A (raw/ output capture).

## Mentioned In

- [Swarm KB Research](../sources/swarm-kb-research.md)
