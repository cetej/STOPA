---
name: Daily Notes Memory Pattern
type: concept
first_seen: 2026-04-07
last_updated: 2026-04-07
sources: [chief-of-staff-openclaw]
tags: [memory, session]
---

# Daily Notes Memory Pattern

> Two-layer memory: raw daily log files (memory/YYYY-MM-DD.md) + AI-curated long-term MEMORY.md — all in flat markdown, no database.

## Key Facts

- Layer 1 (Daily): one file per day, raw log of meetings attended, decisions made, tasks added/completed, conversation context (ref: sources/chief-of-staff-openclaw.md)
- Layer 2 (Curated): MEMORY.md with key people, active projects, lessons learned, decisions — periodically synthesized from daily notes by the AI itself (ref: sources/chief-of-staff-openclaw.md)
- Bootstrap: AI reads curated MEMORY.md on startup to orient on what matters now (ref: sources/chief-of-staff-openclaw.md)
- Flat markdown > database: openable in any editor, git-backupable, no abstraction between human and AI's understanding of context (ref: sources/chief-of-staff-openclaw.md)
- "With this layer you have something closer to a person who's been working alongside you for months and never forgets anything" (ref: sources/chief-of-staff-openclaw.md)
- All meeting processing, email triage, and task tracking feeds back into this picture continuously (ref: sources/chief-of-staff-openclaw.md)

## Relevance to STOPA

STOPA has `checkpoint.md` (session snapshot) + `memory/` (learnings, state) but lacks the automatic daily log that captures raw context throughout the day. The two-layer split (raw daily + curated MEMORY.md) maps directly to STOPA's checkpoint + learnings split, validating the architecture.

## Mentioned In

- [How I Built a Chief of Staff on OpenClaw](../sources/chief-of-staff-openclaw.md)
