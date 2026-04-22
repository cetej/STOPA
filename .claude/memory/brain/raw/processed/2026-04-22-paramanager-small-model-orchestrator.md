---
title: Small Model as Master Orchestrator — ParaManager
source_url: https://arxiv.org/abs/2604.17009
fetched: 2026-04-22
type: arxiv-paper
authors: Wenzhen Yuan, Wutao Xiong, Fanchen Yu, et al.
---

# Small Model as Master Orchestrator: ParaManager

**Paper**: arXiv:2604.17009  
**Date**: April 18, 2026

## Abstract

Addresses multi-agent coordination challenges by proposing a unified orchestration framework that standardizes agent-tool interaction through normalized protocols and explicit state feedback.

## Key Innovations

### Agent-as-Tool Paradigm
Abstracts both agents and tools into a standardized, learnable action space. Removes heterogeneous interface complexity — orchestrator treats a specialized agent identically to a tool call.

### ParaManager
Lightweight orchestrator enabling:
- Parallel subtask decomposition
- Asynchronous execution
- Decoupled architecture: planning decisions separated from task execution

### Training
1. Supervised fine-tuning with recovery mechanisms
2. Reinforcement learning optimizing: task success + protocol compliance + diversity + reasoning efficiency

## Results

Strong performance across multiple benchmarks with robust generalization to previously unseen model pools — addresses extensibility limitations in static workflow systems.

## Significance

Enables small models to orchestrate large, diverse agent pools by abstracting capability interfaces. "Small model as orchestrator" inverts the assumption that orchestration requires the largest model.
