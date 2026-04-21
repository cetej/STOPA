---
title: Process Reward Agents (PRA) — Knowledge-Intensive Reasoning
date: 2026-04-21
sources:
  - https://arxiv.org/abs/2604.09482
tags: [ai, process-reward-model, test-time-compute, knowledge-intensive-reasoning, medical-ai, frozen-policy]
related:
  - think-prm.md
  - cpmi-process-reward.md
  - rational-rewards.md
  - critical-step-optimization.md
---

# Process Reward Agents (PRA) — Knowledge-Intensive Reasoning

## Core Contribution

PRA = **test-time approach** that couples a **frozen policy model** with a **domain-specific reward module** providing online, step-wise rewards during generation.

Key distinction from existing PRMs: PRA works *during* generation (not post-hoc), enabling search-based trajectory ranking and pruning *before* completion. The policy model is never retrained.

## The Knowledge Problem

In knowledge-intensive domains (medicine, law, science), intermediate reasoning steps are "not locally verifiable" — you can't tell if step N is correct without domain knowledge. Standard PRMs struggle because they lack access to the domain's ground truth.

PRA solution: decouple the domain knowledge (reward module) from the reasoning engine (frozen LLM), letting each be specialized independently.

## Architecture

```
Frozen Policy LLM
      ↓ (generates candidate step)
Domain Reward Module ← retrieval augmentation
      ↓ (scores step quality)
Search-Based Decoder
      ↓ (prune low-scoring trajectories)
Final Answer
```

## Results

| Model | Benchmark | Accuracy | Notes |
|-------|-----------|----------|-------|
| Qwen3-4B + PRA | MedQA | **80.8%** | SOTA at 4B scale |
| Baseline Qwen3-4B | MedQA | ~55% | No PRA |
| Improvement | — | **+25.7%** | No retraining |

Generalizes across 0.5B to 8B parameter models.

## Relevance to STOPA

PRA is a test-time compute pattern applicable to STOPA's critic architecture:
- **Frozen policy + domain critic** = orchestrator + specialized critic agent
- `/critic` is currently post-hoc; PRA suggests an *inline* critic checking each agent step
- The 25.7% improvement without retraining suggests STOPA could improve quality without model upgrades — just better critic placement

Related to `/autoreason`: adversarial debate loop is a multi-step version of PRA's trajectory ranking.

## Connections

- [think-prm](think-prm.md): ThinkPRM = generative PRM with CoT; PRA = retrieval-augmented step-scorer — both address step-level verification
- [cpmi-process-reward](cpmi-process-reward.md): CPMI = efficient PRM labeling; PRA = PRM deployment — complementary contributions
- [critical-step-optimization](critical-step-optimization.md): CSO trains only on critical steps; PRA identifies and scores those steps at test time
