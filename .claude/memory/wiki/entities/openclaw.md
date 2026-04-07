---
name: OpenClaw
type: tool
first_seen: 2026-04-07
last_updated: 2026-04-07
sources: [swarm-kb-research, idea-file-research]
tags: [memory, orchestration, session]
---

# OpenClaw

> AI agent platform implementing "file system as memory" with 4-layer hierarchy (SOUL.md → AGENTS.md → MEMORY.md → daily files) and bootstrap injection at session start.

## Key Facts

- Bootstrap injection: SOUL.md + AGENTS.md + MEMORY.md + yesterday's daily file at session start (ref: sources/swarm-kb-research.md)
- Hard limits: 20K char/file, 150K total injected per session (ref: sources/swarm-kb-research.md)
- Pre-compaction flush: silent agent turn writes lasting notes to `memory/YYYY-MM-DD.md` before context compression (ref: sources/swarm-kb-research.md)
- Dreaming (consolidation) cycle exists in community extensions (`openclaw-auto-dream`) but may not be in base system (ref: sources/swarm-kb-research.md)
- Memory extracted and open-sourced by Milvus as `memsearch` (70% vector + 30% BM25) (ref: sources/swarm-kb-research.md)

## Relevance to STOPA

Pre-compaction flush is STOPA's P2 gap — extend `/compact` skill to extract key decisions to daily memory file before compaction. Bootstrap injection pattern validates STOPA's checkpoint.md approach.

## Mentioned In

- [Swarm KB Research](../sources/swarm-kb-research.md)
- [Idea File Research](../sources/idea-file-research.md)
