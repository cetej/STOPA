---
name: Reflexion
type: paper
first_seen: 2026-04-07
last_updated: 2026-04-07
sources: [egoa-prompt-techniques, agent-memory-problems]
tags: [memory, orchestration, self-improvement, verbal-rl]
---

# Reflexion

> Shinn et al. 2023 (arXiv:2303.11366) — verbal self-reflection jako substitut RL weight updates: agent analyzuje selhání v přirozeném jazyce a ukládá insight do episodic memory bufferu.

## Key Facts

- 91% pass@1 HumanEval vs 80% standard GPT-4 — +11% ze samotné verbální noty (ref: sources/egoa-prompt-techniques.md)
- Explicitní verbální nota "co příště udělám jinak" (ne pouze error log) je klíčový mechanismus
- Insight ukládán do episodic memory buffer — přetrvává přes pokusy
- Limitace: vyžaduje externí feedback signál (grader, environment reward)
- NeurIPS 2023

## Relevance to STOPA

STOPA 3-fix escalation je formálně Reflexion smyčka — ale generuje pouze error log, ne verbální notu. Přidání noty po každém FAIL je highest-priority low-effort improvement. Nota by měla být uložena do `core-invariants.md` pravidlo č. 7 (již zakomponováno).

## Mentioned In

- [EgoAlpha/prompt-in-context-learning Research Brief](../sources/egoa-prompt-techniques.md)
- [Agent Memory Problems Research](../sources/agent-memory-problems.md)
