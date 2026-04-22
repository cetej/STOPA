---
title: ParaManager — Small Model as Master Orchestrator
category: concepts
tags: [multi-agent, orchestration, agent-as-tool, parallel-execution, planning]
sources: [raw/processed/2026-04-22-paramanager-small-model-orchestrator.md]
updated: 2026-04-22
---

# ParaManager — Small Model as Master Orchestrator

**Paper**: arXiv:2604.17009  
**Authors**: Wenzhen Yuan, Wutao Xiong, Fanchen Yu, et al. (April 2026)

## Core Principle

A lightweight orchestrator model (small model) can effectively coordinate large, diverse pools of specialized agents and tools — by abstracting all of them through a unified "Agent-as-Tool" interface.

## Agent-as-Tool Paradigm

Both agents and tools are represented as entries in a standardized, learnable action space. The orchestrator does not need to know whether it's calling a Python tool or a specialized LLM agent — the interface is identical.

**Result**: heterogeneous interface complexity eliminated; orchestrator generalizes to unseen agent pools.

## ParaManager Architecture

| Feature | Description |
|---------|-------------|
| Parallel subtask decomposition | Breaks tasks into concurrent subtasks |
| Asynchronous execution | Subtasks run simultaneously |
| Decoupled planning | Planning decisions separated from task execution |
| State feedback | Explicit state signals after each action |

## Training

1. **Supervised fine-tuning** with recovery mechanisms (handles partial failures)
2. **Reinforcement learning** optimizing 4 objectives: task success + protocol compliance + action diversity + reasoning efficiency

## Inversion of Conventional Wisdom

Conventional: orchestration needs the largest, most capable model.  
ParaManager: small model + good interface abstraction > large model + heterogeneous APIs.

## STOPA Relevance

STOPA's `/orchestrate` skill currently assumes Claude Sonnet/Opus for orchestration. The ParaManager pattern suggests Haiku-level model could orchestrate effectively IF the agent pool uses a standardized interface. Relevant to budget-tier optimization: light-tier orchestration with Haiku + standard worker agents.

The "Agent-as-Tool" paradigm already partially exists in STOPA (Agent() calls are uniform) but lacks the formal state feedback mechanism.

## Related Concepts

→ [agentforge.md](agentforge.md)  
→ [multi-agent-orchestration-protocols.md](multi-agent-orchestration-protocols.md)  
→ [gaama.md](gaama.md)  
→ [adaptive-orchestration-dmoe.md](adaptive-orchestration-dmoe.md)
