---
title: "Memory Intelligence Agent"
slug: memory-intelligence-agent-mia
source_type: url
url: "https://arxiv.org/abs/2604.04503"
date_ingested: 2026-04-08
date_published: "2026-04-07"
entities_extracted: 3
claims_extracted: 7
---

# Memory Intelligence Agent

> **TL;DR**: MIA combines a non-parametric Memory Manager (compressed trajectories), a parametric Planner (RL-trained search strategies), and an Executor into a living memory system. Bidirectional parametric↔non-parametric conversion + test-time learning enables continuous evolution. 7B MIA outperforms 32B baseline by 18%; +9% on GPT-5.4.

## Key Claims

1. Living memory (evolving + compressed) outperforms static retrieval by +31% avg across 11 benchmarks with 7B model — `verified`
2. Traditional long-context memory underperforms no-memory baselines — static accumulation actively hurts — `argued`
3. Bidirectional parametric↔non-parametric memory conversion is the structural key to evolution without full retraining — `argued`
4. Alternating GRPO (Executor first → Planner) produces synergistic cooperation better than joint or simultaneous training — `argued`
5. Test-time learning enables Planner to adapt to new distributions during inference without interrupting reasoning — `argued`
6. 7B Executor outperforms 32B model by 18% when equipped with effective memory — `verified`
7. +9% boost on GPT-5.4 on LiveVQA; +6% on HotpotQA — memory augments even frontier models — `verified`

## Entities

| Entity | Type | Status |
|--------|------|--------|
| [MIA](../entities/mia.md) | paper/concept | new |
| [Test-Time Learning](../entities/test-time-learning.md) | concept | new |
| [GRPO](../entities/grpo.md) | concept | updated |

## Relations

- MIA `uses` GRPO — Executor + Planner trained via GRPO alternately
- MIA `extends` RAG — addresses static retrieval limitations
- Test-Time Learning `part_of` MIA — Planner evolution mechanism
- MIA `competes_with` ByteRover — both tackle memory-augmented deep research
- MIA `inspired_by` Contrastive Distillation — bidirectional parametric↔non-parametric conversion

## Cross-References

- Related learnings: 2026-04-08-recency-beats-complex-memory.md (complementary: recency bias), 2026-03-30-write-time-gating-salience.md (write-time gating), 2026-03-29-memcollab-agent-agnostic-memory.md (agent-agnostic memory)
- Related wiki articles: [memory-architecture](../memory-architecture.md), [orchestration-multi-agent](../orchestration-multi-agent.md)
- Contradictions: none detected
