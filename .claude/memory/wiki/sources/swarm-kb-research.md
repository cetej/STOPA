---
title: "Swarm Knowledge Base — Karpathy Wiki Pattern, OpenClaw, Hermes"
slug: swarm-kb-research
source_type: research_output
date_ingested: 2026-04-07
entities_extracted: 9
claims_extracted: 5
---

# Swarm Knowledge Base — Karpathy Wiki Pattern, OpenClaw, Hermes

> **TL;DR**: Karpathy's LLM wiki pattern (raw/ → wiki/ with index.md, 4 phases: Ingest/Compile/Query/Lint) was extended by @jumperz into a 10-agent swarm with a quality pipeline (raw → drafts → Hermes gate → live) and per-agent briefings forming a compound loop. OpenClaw adds bootstrap injection (SOUL.md + AGENTS.md + MEMORY.md + yesterday's daily file) and pre-compaction flush. Hermes uses 3-axis scoring with fail-closed JSON contract.

## Key Claims

1. Karpathy's 3-layer wiki: raw/ (immutable dump) → wiki/ (LLM-maintained markdown with backlinks) → schema (CLAUDE.md/AGENTS.md); ~100 articles at ~400K words without RAG — `[verified]`
2. OpenClaw bootstrap injects 4 files at session start; hard limits 20K char/file, 150K total — `[verified]`
3. Pre-compaction flush: silent agent turn "Write any lasting notes to memory/YYYY-MM-DD.md; reply NO_REPLY if nothing to store" — mechanism STOPA currently lacks — `[verified]`
4. Hermes 3-axis scoring: procedure adherence × output correctness × token conciseness (0-1); fail-closed: `security_concerns || logic_errors` → `passed = false` — `[verified]`
5. Hermes quality gate architecture (issue #406) is a community proposal, not confirmed shipped code — `[verified]`

## Entities

| Entity | Type | Status |
|--------|------|--------|
| Karpathy Wiki Pattern | concept | new |
| OpenClaw | tool | new |
| Hermes Agent | tool | new |
| @jumperz | person | new |
| Pre-compaction Flush | concept | new |
| Hermes Quality Gate | concept | new |
| NousResearch | company | new |
| Andrej Karpathy | person | new |
| memsearch (Milvus) | tool | new |

## Relations

- Andrej Karpathy `invented` Karpathy Wiki Pattern
- @jumperz `extended` Karpathy Wiki Pattern (into 10-agent swarm)
- OpenClaw `implements` Karpathy Wiki Pattern (bootstrap injection)
- NousResearch `develops` Hermes Agent
- Hermes Agent `implements` Hermes Quality Gate
- memsearch (Milvus) `extracted_from` OpenClaw (open-sourced memory system)
