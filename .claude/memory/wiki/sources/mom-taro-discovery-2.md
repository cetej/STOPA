---
title: "Adaptive Model Routing in LLM Agent Systems"
slug: mom-taro-discovery-2
source_type: research_output
date_ingested: 2026-04-07
entities_extracted: 8
claims_extracted: 5
---
# Adaptive Model Routing in LLM Agent Systems

> **TL;DR**: Survey of adaptive model routing patterns for LLM agents. Three main families: RouteLLM (preference-based, 2x cost reduction), Route-to-Reason (joint model+strategy, 40-60% budget), and xRouter (RL-based Pareto). Token-level optimization (prompt caching, deduplication) saves more than model routing alone. Step-level routing outperforms per-task routing — directly applicable to STOPA's orchestration budget tiers.

## Key Claims

1. RouteLLM achieves 2x cost reduction — using GPT-4 only 14% of the time while maintaining 95% quality — and routers generalize across model families without retraining — `[verified]`
2. Token-level optimization (caching, deduplication) saves 60-80% of costs vs 40-60% for model routing; combined approaches reach 2.5-3.5x savings — `[argued]`
3. Step-level Q-value routing outperforms per-task routing by assigning model based on learned success probability at each agent step — `[argued]`
4. xRouter (RL-based) avoids need for preference data and scales to >2 model tiers by optimizing cost-performance Pareto frontier directly — `[argued]`
5. Route-to-Reason unifies model AND reasoning strategy selection (CoT vs direct vs delegation) under a budget constraint, achieving 95%+ quality at 40-60% of baseline cost — `[argued]`

## Entities

| Entity | Type | Status |
|--------|------|--------|
| RouteLLM | tool | new |
| Route-to-Reason (RTR) | concept | new |
| xRouter | tool | new |
| MoMA (Mixture of Models & Agents) | concept | new |
| BEST-Route | concept | new |
| Step-Level Q-Value Models | concept | new |
| ZenML | tool | new |
| Software-Defined Agentic Serving | concept | new |

## Relations

- RouteLLM `enables` weak-to-strong transfer
- Route-to-Reason `extends` RouteLLM
- xRouter `replaces` RouteLLM (for >2 model scenarios)
- MoMA `combines` RouteLLM
- Step-Level Q-Value Models `improves` circuit-breaker logic
