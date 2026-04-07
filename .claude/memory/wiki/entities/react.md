---
name: ReAct
type: paper
first_seen: 2026-04-07
last_updated: 2026-04-07
sources: [egoa-prompt-techniques]
tags: [orchestration, tool-use, reasoning]
---

# ReAct

> Yao et al. 2022 (arXiv:2210.03629) — interleaved Thought→Action→Observation loop pro LLM agenty s tool use. 672 citací — nejcitovanější agent paper v EgoAlpha repu.

## Key Facts

- +34% ALFWorld, +10% WebShop vs baseline (ref: sources/egoa-prompt-techniques.md)
- Klíčový insight: samotný CoT bez externího pozorování vede k halucinacím
- Thought krok = reasoning, Action = tool call, Observation = tool output
- Základní architektura pro většinu moderních agent frameworků

## Relevance to STOPA

STOPA agent execution loop (agent thinks → calls tool → processes output → next step) je přímá implementace ReAct vzoru. STOPA orchestrate skill rozšiřuje ReAct o budget tiering, circuit breakers a memory persistence.

## Mentioned In

- [EgoAlpha/prompt-in-context-learning Research Brief](../sources/egoa-prompt-techniques.md)
