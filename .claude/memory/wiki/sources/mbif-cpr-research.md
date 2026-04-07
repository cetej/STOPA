---
title: "My-Brain-Is-Full-Crew vs CPR — Claude Code Orchestration Patterns"
slug: mbif-cpr-research
source_type: research_output
date_ingested: 2026-04-07
entities_extracted: 7
claims_extracted: 5
---

# My-Brain-Is-Full-Crew vs CPR — Claude Code Orchestration Patterns

> **TL;DR**: MBIF-Crew (gnekt) is a multi-agent Obsidian orchestration system with pull-based agent chaining, post-it state (30-line per-agent files), and a pure dispatcher CLAUDE.md. CPR (EliaAlberti) is a 3-command session persistence system with a hard truncation boundary (`## Raw Session Log`), inline section markers, and confidence keywords for grep-first retrieval. The two systems solve orthogonal problems: MBIF handles runtime orchestration, CPR handles cross-session persistence.

## Key Claims

1. MBIF's CLAUDE.md opens with "NEVER RESPOND DIRECTLY" — acts as a pure router, never the responder — `[verified]`
2. Pull-based agent chaining: agents write `### Suggested next agent` in output; dispatcher decides; max depth 3, no agent repeated — `[verified]`
3. CPR's hard truncation boundary (`## Raw Session Log`) enables `/resume` to load only text above the heading (~60% token savings) — `[verified]`
4. CPR requires `claude config set --global autoCompact false` — without it CC silently deletes context before saving — `[verified]`
5. Post-it state: 30-line per-agent files in `Meta/states/{name}.md`, overwritten each run, shared between skill and its parent agent — `[verified]`

## Entities

| Entity | Type | Status |
|--------|------|--------|
| My-Brain-Is-Full-Crew | tool | new |
| CPR (Compress-Preserve-Resume) | tool | new |
| gnekt | person | new |
| EliaAlberti | person | new |
| Post-it State Protocol | concept | new |
| Pull-based Agent Chaining | concept | new |
| Truncation Boundary Pattern | concept | new |

## Relations

- gnekt `created` My-Brain-Is-Full-Crew
- EliaAlberti `created` CPR (Compress-Preserve-Resume)
- My-Brain-Is-Full-Crew `implements` Pull-based Agent Chaining
- My-Brain-Is-Full-Crew `implements` Post-it State Protocol
- CPR (Compress-Preserve-Resume) `implements` Truncation Boundary Pattern
