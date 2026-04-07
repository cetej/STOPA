---
name: query-specific-refinement
type: concept
first_seen: 2026-04-07
last_updated: 2026-04-07
sources: [benchmarking-llm-skill-usage-realistic-settings]
tags: [skill, evaluation, retrieval, optimization]
---

# Query-Specific Refinement

> Agent-driven skill improvement: explores the task, evaluates retrieved skills, then synthesizes a refined version tailored to the specific query.

## Key Facts

- Recovers substantial performance lost under realistic conditions: 40.1% → 48.2% on SKILLS-BENCH, 57.7% → 65.5% on Terminal-Bench 2.0 for Claude Opus 4.6 (ref: sources/benchmarking-llm-skill-usage-realistic-settings.md)
- Acts as "multiplier on existing skill quality, not generator of new knowledge" — requires relevant skill to already be in retrieved set (ref: sources/benchmarking-llm-skill-usage-realistic-settings.md)
- Coverage score threshold: ≥3.83 = refinement succeeds; ≤3.49 = refinement fails (ref: sources/benchmarking-llm-skill-usage-realistic-settings.md)
- Substantially outperforms query-agnostic refinement (offline improvement without task context) (ref: sources/benchmarking-llm-skill-usage-realistic-settings.md)

## Relevance to STOPA

Maps directly to STOPA's `/self-evolve` pattern. Validates that task-aware skill improvement beats offline refinement. The coverage threshold (≥3.83) is a usable signal for when to trigger self-evolve vs fall back to no-skill baseline.

## Mentioned In

- [Benchmarking LLM Skill Usage in Realistic Settings](../sources/benchmarking-llm-skill-usage-realistic-settings.md)
