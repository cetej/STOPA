---
date: 2026-03-23
type: best_practice
severity: medium
component: skill
tags: [autoloop, optimization, llm-as-judge, structural-heuristic]
uses: 2
summary: "Karpathy optimization loop: edit → measure → score → iterate. Use structural heuristics + LLM-as-judge for scoring."
source: external_research
---

## Problém
Need for fast iteration loop for prompt/code optimization.

## Root Cause
Pure LLM-as-judge per iteration is too expensive and creates self-reinforcing bias.

## Reseni
Structural heuristic for fast iteration (grep-based, zero LLM cost) + single LLM-as-judge validation at end. One file, one metric, git rollback per iteration. M5 hybrid metric scores 22/25.

## Prevence
Don't use LLM to evaluate LLM output every iteration — self-reinforcing bias + cost explosion. Hybrid approach (structural fast loop + LLM final judge) is optimal.
