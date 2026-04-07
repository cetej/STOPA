---
title: "Claude Subconscious — Technical Architecture Deep Dive"
slug: claude-subconscious-research
source_type: research_output
date_ingested: 2026-04-07
entities_extracted: 5
claims_extracted: 4
---
# Claude Subconscious — Technical Architecture Deep Dive

> **TL;DR**: Claude Subconscious (Letta AI, MIT license) is a dual-agent plugin attaching a persistent Letta agent as a background brain to Claude Code sessions. Four hooks funnel session transcripts to the Letta agent, which maintains 8 typed memory blocks (~30 KB total) and "whispers" guidance back via stdout injection before each user prompt. The original CLAUDE.md-write approach caused 49K+ char token bloat and was replaced in v1.3.0 with stdout injection. Three open Linux/macOS bugs as of 2026-03-27.

## Key Claims

1. Claude Subconscious uses 4 Claude Code hooks (SessionStart, UserPromptSubmit, PreToolUse, Stop) with an async-detach pattern on Stop — worker spawned as separate OS process, hook exits immediately to avoid blocking — `[verified]`
2. The original CLAUDE.md write-back architecture caused 49K+ character token bloat and cross-project contamination; replaced in v1.3.0 with stdout injection — `[verified]`
3. The 8 memory blocks (~30 KB total) persist globally across all projects via a single Letta agent instance — creating cross-project contamination risk if not managed carefully — `[verified]`
4. One-step lag is fundamental: the agent always processes transcripts from the previous interaction and cannot respond in real-time to the current message — `[verified]`

## Entities

| Entity | Type | Status |
|--------|------|--------|
| Claude Subconscious | tool | new |
| Letta (formerly MemGPT) | company | new |
| GLM-5 | tool | new |
| Whispering Pattern | concept | new |
| Async-Detach Hook Pattern | concept | new |

## Relations

- Claude Subconscious `built_by` Letta
- Claude Subconscious `uses` Whispering Pattern
- Claude Subconscious `implements` Async-Detach Hook Pattern
- Letta `previously_known_as` MemGPT
- Claude Subconscious `default_model` GLM-5
