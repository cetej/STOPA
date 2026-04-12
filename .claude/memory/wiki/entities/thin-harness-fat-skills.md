---
name: Thin Harness Fat Skills
type: concept
first_seen: 2026-04-12
last_updated: 2026-04-12
sources: [garry-tan-thin-harness-fat-skills]
tags: [skill-design, orchestration, harness]
---

# Thin Harness, Fat Skills

> Architectural principle: encode intelligence in markdown skill files (fat), keep the execution harness minimal (~200 lines of code, thin).

## Key Facts

- "Fat skills" = markdown procedures encoding judgment, process, and constraints — "90% of the value lives here" (ref: sources/garry-tan-thin-harness-fat-skills.md)
- "Thin harness" = ~200 lines: JSON in, text out, read-only by default, runs model in loop, manages context (ref: sources/garry-tan-thin-harness-fat-skills.md)
- Anti-pattern: fat harness with 40+ tool definitions eating half the context window + 2-5s MCP round-trips (ref: sources/garry-tan-thin-harness-fat-skills.md)
- Every model improvement automatically improves every skill when intelligence is in skills, not harness (ref: sources/garry-tan-thin-harness-fat-skills.md)
- Three-layer stack: Fat Skills → Thin Harness → Deterministic Application (QueryDB, ReadDoc, Search) (ref: sources/garry-tan-thin-harness-fat-skills.md)

## Relevance to STOPA

This is the explicit theoretical backing for STOPA's design: SKILL.md files hold the intelligence, `.claude/settings.json` hooks are the thin harness layer, and Python scripts are the deterministic application layer.

## Mentioned In

- [Key Concepts for AI Agentic Skills Design — Thin Harness Fat Skills](../sources/garry-tan-thin-harness-fat-skills.md)
