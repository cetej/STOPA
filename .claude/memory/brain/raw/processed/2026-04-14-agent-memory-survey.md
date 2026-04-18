---
title: "Memory for Autonomous LLM Agents: Survey 2022-2026"
source: https://arxiv.org/abs/2603.07670
date: 2026-04-14
type: academic-survey
tags: [memory, agent, survey, taxonomy, write-manage-read]
concepts: [agent-memory-taxonomy, second-brain, active-metacognitive-curation]
---

## Summary

Komplexní survey pokrývající vývoj agent memory systémů 2022–2026. Formalizuje write-manage-read loop jako unifikovaný rámec pro porozumění existujícím přístupům.

## Core Framework: Write-Manage-Read Loop

```
perception → WRITE → memory store → MANAGE → RETRIEVE → action
```

Třífa informačního toku v autonomním systému přes extended interakce. Každá fáze je semi-nezávislá a může být optimalizována odděleně.

## Třírozměrná taxonomie

1. **Temporal scope** — jak dlouho paměť přetrvává (session / cross-session / permanent)
2. **Representational substrate** — jak je informace uložena (text / vector / graph / structured)
3. **Control policy** — co řídí retenci/retrieval (rule-based / learned / hybrid)

## Pět rodin memory mechanismů

| Rodina | Popis | Příklady |
|--------|-------|---------|
| Context-resident compression | Vměstnání do token window | MemGPT, compression prompts |
| Retrieval-augmented stores | Externí databáze | RAG variants, vector DBs |
| Reflective self-improvement | Učení z minulých interakcí | Reflexion, self-critique |
| Hierarchical virtual context | Vrstvená organizace | hierarchical summarization |
| Policy-learned management | Neuronové řízení paměti | MemFactory, RL-based |

## Klíčový shift v evaluaci

Od "static recall benchmarks" → k "multi-session agentic tests that interleave memory with decision-making". Tento posun odhaluje výrazné limitace současných systémů.

## Aplikační domény

Personal assistants, coding agents, open-world gaming, scientific reasoning, multi-agent coordination.

## Nevyřešené výzvy

- Continual consolidation (bez zapomínání)
- Causally grounded retrieval
- Trustworthy reflection (hallucination v paměti)
- Learned forgetting
- Multimodal embodied memory

## Relevance pro 2BRAIN / STOPA

- Write-Manage-Read = formální základ pro 2BRAIN Ingest/Query/Lint cyklus
- 3D taxonomie pomáhá klasifikovat kde 2BRAIN sedí: cross-session, text+graph, hybrid control
- Hierarchical virtual context rodina = nejbližší analogie k 2BRAIN raw/wiki vrstvám
