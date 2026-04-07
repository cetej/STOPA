---
name: SKILLS-BENCH
type: concept
first_seen: 2026-04-07
last_updated: 2026-04-07
sources: [benchmarking-llm-skill-usage-realistic-settings]
tags: [skill, evaluation, benchmarking]
---

# SKILLS-BENCH

> 84-task benchmark evaluating whether LLM agents effectively leverage reusable skills under progressively realistic retrieval conditions.

## Key Facts

- 84 tasks across diverse agent skill scenarios (ref: sources/benchmarking-llm-skill-usage-realistic-settings.md)
- Tests 6 progressive conditions: curated+forced → curated → curated+distractors → retrieved(with curated) → retrieved(without curated) → no skills (ref: sources/benchmarking-llm-skill-usage-realistic-settings.md)
- Claude Opus 4.6 on SKILLS-BENCH with curated skills: 40.1% → 48.2% after query-specific refinement (ref: sources/benchmarking-llm-skill-usage-realistic-settings.md)
- Query-agnostic refinement on SKILLS-BENCH: modest gains (40.1% → 42.0%) confirming task awareness is critical (ref: sources/benchmarking-llm-skill-usage-realistic-settings.md)

## Relevance to STOPA

Provides a concrete eval framework for STOPA skill system — the 6-condition progression could be adopted for testing STOPA skill discovery quality.

## Mentioned In

- [Benchmarking LLM Skill Usage in Realistic Settings](../sources/benchmarking-llm-skill-usage-realistic-settings.md)
