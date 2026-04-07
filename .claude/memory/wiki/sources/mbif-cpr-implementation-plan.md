---
title: "MBIF/CPR Implementation Plan for STOPA"
slug: mbif-cpr-implementation-plan
source_type: research_output
date_ingested: 2026-04-07
entities_extracted: 6
claims_extracted: 5
---

# MBIF/CPR Implementation Plan for STOPA

> **TL;DR**: Implementační plán 4 hlavních vzorů z MBIF-Crew a CPR systémů pro STOPA orchestraci. Prioritizuje call chain tracking (P1), truncation boundary v checkpoint.md (P1, ~60% token savings), confidence keywords (P2) a post-it state (P2). Sekundární vzory jsou PROTECTED/ARCHIVABLE sekce markery a compact ordering.

## Key Claims

1. Call chain tracking — přidání "EXECUTION CONTEXT" bloku do každého sub-agent promptu — eliminuje duplicitní práci agentů bez znalosti předchozích kroků — `[argued]`
2. Truncation boundary (`## Session Detail Log`) v checkpoint.md šetří ~60% tokenů při `/checkpoint resume` — identický vzor jako CPR's `## Raw Session Log` — `[verified]`
3. Confidence keywords v intermediate JSON (extrahované Haiku sub-agentem) umožňují grep-based search přes session artefakty bez full-text skenování — `[argued]`
4. Post-it state (`.claude/memory/intermediate/{skill-name}-state.md`, max 30 řádků) řeší resumption multi-turn skills bez kolize se sdíleným state.md — `[verified]` (MBIF production pattern)
5. PROTECTED/ARCHIVABLE inline markery v memory file headings umožňují selektivní archivaci bez mazání — triviální implementace (5 řádků do memory-files.md) — `[asserted]`

## Entities

| Entity | Type | Status |
|--------|------|--------|
| Call Chain Tracking | concept | new |
| Confidence Keywords | concept | new |
| My-Brain-Is-Full-Crew | tool | existing |
| CPR (Compress-Preserve-Resume) | tool | existing |
| Post-it State Protocol | concept | existing |
| Truncation Boundary Pattern | concept | existing |

## Relations

- Call Chain Tracking `extends` My-Brain-Is-Full-Crew
- Confidence Keywords `extends` CPR (Compress-Preserve-Resume)
- Call Chain Tracking `improves` STOPA orchestrate skill
- Truncation Boundary Pattern `reduces-tokens-in` STOPA checkpoint.md
- Post-it State Protocol `enables` skill resumption
