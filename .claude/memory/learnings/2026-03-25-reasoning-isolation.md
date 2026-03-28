---
date: 2026-03-25
type: best_practice
severity: high
component: skill
tags: [reasoning, BOULDER, CARE, multi-turn, debiasing, arXiv]
summary: "BOULDER/CARE patterns: isolate reasoning from output generation to reduce bias. Apply in multi-turn skill prompts."
---

# Reasoning Isolation & Judge Debiasing in Skills

## Pattern

LLM reasoning accuracy degrades in multi-turn dialogue vs. single-shot (BOULDER, arXiv:2603.20133). LLM-as-judge scoring is biased by style/verbosity confounders (CARE, arXiv:2603.00039).

## Applied to STOPA skills

1. **`/critic`**: Added confounder-aware scoring (substance over style) + reasoning isolation guidance (evaluate milestones independently, re-read code before Judge phase)
2. **`/verify`**: Added reasoning isolation for complex milestones (fresh reasoning per milestone, isolated sub-agent context)
3. **`/scenario`**: Added semi-formal reasoning strategy (explicit premises → negate → trace consequences)
4. **`/systematic-debugging`**: Added structured premises to hypothesis formation (P1+P2+P3 → derive hypothesis)

## Key insight

Skills that evaluate/judge should actively counteract two failure modes:
- **Context accumulation bias**: Earlier assessments influence later ones within same conversation
- **Style-substance conflation**: Verbose/clean code gets higher scores regardless of correctness

## Mitigation

- Evaluate each item independently (don't let M1 outcome bias M2)
- Re-read evidence fresh before final judgment
- Sub-agents for evaluation should get minimal context (just milestone + code, not full history)
- Score based on what code does, not how it looks
