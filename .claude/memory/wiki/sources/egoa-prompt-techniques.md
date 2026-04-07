---
title: "EgoAlpha/prompt-in-context-learning — Research Brief"
slug: egoa-prompt-techniques
source_type: research_output
date_ingested: 2026-04-07
entities_extracted: 10
claims_extracted: 5
---

# EgoAlpha/prompt-in-context-learning — Research Brief

> **TL;DR**: EgoAlpha je living paper tracker (v3.0.0, denní aktualizace) s 25+ paper listů. STOPA orchestrační architektura má silné akademické precedenty: /orchestrate ↔ Least-to-Most, Anti-Rationalization ↔ Contrastive CoT, 3-fix escalation ↔ Reflexion. Největší gap: Reflexion verbální nota "co příště jinak" zvyšuje HumanEval z 80% na 91% — STOPA ji negeneruje.

## Key Claims

1. Reflexion (Shinn et al. 2023) dosahuje 91% pass@1 HumanEval vs 80% standard GPT-4 přes verbální self-reflection uloženou do episodic memory — `[verified]`
2. LATS (MCTS + LLM reasoning + self-reflection) dosahuje 92.7% HumanEval na GPT-4 — nejvyšší v performance hierarchii — `[verified]`
3. Self-Consistency (+17.9% GSM8K) je nejefektivnější drop-in upgrade — zachová prompt strukturu, přidá latenci — `[verified]`
4. SPP (Solo Performance Prompting) kognitivní synergie nastává pouze na GPT-4/Opus tier, ne menších modelech — `[verified]`
5. Self-Discover (+32% vs CoT, 10-40× méně compute než Self-Consistency) — dynamický výběr reasoning modulů — `[verified]`

## Entities

| Entity | Type | Status |
|--------|------|--------|
| EgoAlpha | tool | new |
| Reflexion | paper | new |
| LATS | paper | new |
| Tree of Thoughts | paper | new |
| Graph of Thoughts | paper | new |
| ReAct | paper | new |
| Self-Refine | paper | new |
| MetaGPT SOPs | paper | new |
| Self-Discover | paper | new |
| Self-Consistency | concept | new |

## Relations

- Reflexion `implements` verbal RL loop (episodic memory buffer)
- LATS `combines` MCTS with LLM reasoning and Reflexion
- MetaGPT SOPs `defines` output contracts between agents
- Self-Discover `dynamically selects` reasoning modules per task
- STOPA 3-fix escalation `is formally` Reflexion loop (missing verbal note)
