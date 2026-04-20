---
source: https://arxiv.org/abs/2604.05096
fetched: 2026-04-20
type: arxiv-paper
authors: Hanbing Liu, Lang Cao, Yang Li
title: "RAG or Learning? Understanding the Limits of LLM Adaptation under Continuous Knowledge Drift"
---

# Raw: Knowledge Drift — Chronos

## Abstract Summary
LLMs are tied to fixed knowledge snapshots. Existing adaptation methods (continual finetuning, knowledge editing, RAG) fail under realistic continuous temporal knowledge drift. Most suffer from catastrophic forgetting and temporal inconsistency.

## Key Contributions
1. New benchmark: time-stamped real-world dynamic events showing chronological knowledge evolution
2. Chronos: time-aware retrieval baseline using Event Evolution Graph (no additional training)
3. Systematic evaluation framework for continuous knowledge drift

## Key Results
Vanilla RAG + learning-based approaches both struggle under continuous drift. Chronos (time-aware graph) outperforms without training.

## Concepts
- Event Evolution Graph
- Continuous knowledge drift
- Time-aware retrieval
- Catastrophic forgetting in continual learning
