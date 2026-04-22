---
title: Adaptive Orchestration — Scalable Self-Evolving Multi-Agent Systems
source_url: https://arxiv.org/abs/2601.09742
fetched: 2026-04-22
type: arxiv-paper
authors: Sathish Sampath, Anuradha Baskaran
---

# Adaptive Orchestration: Scalable Self-Evolving Multi-Agent Systems

**Paper**: arXiv:2601.09742  
**Date**: January 10, 2026

## The Generalization-Specialization Dilemma

- **Monolithic agents** with large toolkits → context pollution → performance degradation
- **Static multi-agent configurations** → unnecessary latency and resource costs

Neither extreme works at scale.

## Solution: Dynamic Mixture of Experts (DMoE)

**Self-Evolving Concierge System** architecture:
- Dynamically restructures its runtime environment (no code rewriting)
- Recruits specialized sub-agents based on conversation/task analysis
- "Mixture of Experts" applied at the agent orchestration level

### Key Components

| Component | Role |
|-----------|------|
| **Meta-Cognition Engine** | Asynchronous mechanism detecting capability gaps in real-time |
| **LRU Eviction Policy** | Manages resource constraints by retiring least-recently-used agents |
| **Surgical History Pruning** | Addresses refusal bias without extensive model modifications |

## Results

"Maintains high task success rates while minimizing token consumption compared to static agent swarms."

## Key Insight

Agent pools should be dynamic, not static. The orchestrator continuously monitors what capabilities are needed and recruits/evicts agents accordingly — like an OS process scheduler for LLM agents.
