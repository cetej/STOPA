---
name: OpenClaw
type: tool
first_seen: 2026-04-07
last_updated: 2026-04-08
sources: [swarm-kb-research, idea-file-research, chief-of-staff-openclaw, karpathy-nopriors-autoagent-loopy-era]
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

- Real-world production deployment: VC with 100+ LP contacts uses it for full fundraise pipeline management (ref: sources/chief-of-staff-openclaw.md)
- Named AI: deployed as "Stella" with persistent identity and memory (ref: sources/chief-of-staff-openclaw.md)
- Two-layer memory in practice: daily log files + curated MEMORY.md synthesized by AI from daily notes (ref: sources/chief-of-staff-openclaw.md)
- Kaizen loop: Friday cron research + Sunday human review = weekly improvement cadence (ref: sources/chief-of-staff-openclaw.md)

- Created by Peter Steinberg; famous setup: 10 repos tiled on monitor, each Codex agent running 20-min tasks = "macro actions over repository" (ref: sources/karpathy-nopriors-autoagent-loopy-era.md)
- Karpathy's "Dobby the Elf" deployment: WhatsApp interface controlling Sonos, lights, HVAC, shades, pool, spa, security camera + Quinn vision model for visitor detection (ref: sources/karpathy-nopriors-autoagent-loopy-era.md)
- Five simultaneous innovations: SOUL.md personality, dialed-back sycophancy, memory system, single WhatsApp portal, home automation — all combined by Steinberg (ref: sources/karpathy-nopriors-autoagent-loopy-era.md)

## Mentioned In

- [Swarm KB Research](../sources/swarm-kb-research.md)
- [Idea File Research](../sources/idea-file-research.md)
- [How I Built a Chief of Staff on OpenClaw](../sources/chief-of-staff-openclaw.md)
- [No Priors: Code Agents, AutoResearch, and the Loopy Era](../sources/karpathy-nopriors-autoagent-loopy-era.md)
