---
name: Self-Discover
type: paper
first_seen: 2026-04-07
last_updated: 2026-04-07
sources: [egoa-prompt-techniques]
tags: [reasoning, planning, orchestration]
---

# Self-Discover

> Zhou et al. 2024 (arXiv:2402.03620) — LLM dynamicky vybírá atomické reasoning moduly a skládá task-specific strukturu před řešením.

## Key Facts

- +32% vs standard CoT, 10-40× méně compute než Self-Consistency (ref: sources/egoa-prompt-techniques.md)
- Model vybere z menu reasoning modulů (CoT? Search? Verification? Tool-use? Decomposition?)
- Task-specific struktura = lepší než single fixed reasoning strategy
- Nejsilnější eficiency gain v EgoAlpha přehledu

## Relevance to STOPA

Inspirace pro /triage skill: dynamický výběr reasoning modulů pro každý task. Místo fixního "vždy orchestruj" nebo "vždy jednoduché" — STOPA triage by měl vybrat z menu: CoT only / Scout + implement / Orchestrate + critic / Deep research. Odpovídá STOPA tier systému ale s explicitní modul selekcí.

## Mentioned In

- [EgoAlpha/prompt-in-context-learning Research Brief](../sources/egoa-prompt-techniques.md)
