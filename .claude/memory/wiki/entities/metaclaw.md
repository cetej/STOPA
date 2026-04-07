---
name: MetaClaw
type: concept
first_seen: 2026-04-07
last_updated: 2026-04-07
sources: [autoresearchclaw-research]
tags: [memory, orchestration, documentation]
---

# MetaClaw

> Cross-run learning systém v AutoResearchClaw: EvolutionStore ukládá lekce ve JSONL formátu, build_overlay() je injektuje jako prompt overlay do subsequent pipeline stages. Kombinuje intra-run a cross-run znalosti.

## Key Facts

- LessonCategory Enum: SYSTEM | EXPERIMENT | WRITING | ANALYSIS | LITERATURE | PIPELINE (ref: sources/autoresearchclaw-research.md)
- LessonEntry: stage_name, stage_num, category, severity, description, timestamp, run_id (ref: sources/autoresearchclaw-research.md)
- EvolutionStore: JSONL-backed append storage s staged queries (ref: sources/autoresearchclaw-research.md)
- Lesson capture sources: stage failures, blocked stages, PIVOT/REFINE decisions, stderr warnings, NaN/Inf anomalies (ref: sources/autoresearchclaw-research.md)
- build_overlay() generuje dvě části: intra-run lessons (time-weighted, severity-boosted) + cross-run SKILL.md files z `arc-*` directories (ref: sources/autoresearchclaw-research.md)
- SKILL.md formát: YAML frontmatter (name, description, metadata s category a trigger-keywords) + Markdown body (ref: sources/autoresearchclaw-research.md)

## Relevance to STOPA

Pokročilejší varianta STOPA learnings/ systému. Klíčový rozdíl: MetaClaw aktivně injektuje lekce jako prompt overlay do každé subsequent stage, STOPA learnings/ jsou retrieval-on-demand. Inspirace pro `/scribe` upgrade: auto-capture stage failures jako LessonEntry, ne jen explicit scribe volání.

## Mentioned In

- [AutoResearchClaw Architecture Research](../sources/autoresearchclaw-research.md)
