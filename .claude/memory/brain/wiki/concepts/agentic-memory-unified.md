---
title: Agentic Memory — Unified RL-Trained Memory Management
category: concepts
tags: [memory, reinforcement-learning, grpo, long-short-term-memory, tool-based-memory]
sources: [raw/2026-04-18-agentic-memory-unified-rl.md]
updated: 2026-04-18
---

# Agentic Memory — Unified RL-Trained Memory Management

**Paper**: arXiv:2601.01885  
**Authors**: Yi Yu, Liuyi Yao, Yuexiang Xie, Qingquan Tan, Jiaqi Feng, Yaliang Li, Libing Wu

## Core Idea

Memory operations as tools. Instead of long-term and short-term memory being separate system components, this framework makes them tools the agent can invoke:

- `store` — add to persistent memory
- `retrieve` — query memory
- `update` — modify existing entry
- `summarize` — compress older entries
- `discard` — remove stale entries

This enables **end-to-end optimization**: the agent learns when and how to use memory through reinforcement learning, not hand-coded logic.

## Training Approach

Three-stage progressive RL using **step-wise GRPO** (Group Relative Policy Optimization):
1. Train on simple memory tasks (single operation)
2. Extend to multi-operation sequences
3. Full long-horizon tasks with sparse rewards

GRPO handles the key challenge: memory operations have sparse, discontinuous rewards (a retrieve now affects success 10 steps later).

## Why It Matters

Context window efficiency is an explicit optimization target. The agent learns to:
- Summarize and discard proactively (not just when context is full)
- Retrieve selectively (not retrieve everything)
- Update rather than duplicate

## Results

Outperforms memory-augmented baselines on 5 long-horizon benchmarks across:
- Task completion rate
- Memory quality (relevance, freshness)
- Context efficiency (tokens used)

## STOPA Relevance

STOPA's memory access is currently reactive (hook reads learnings at session start). This paper suggests the next evolution: **agents should decide when to store, retrieve, and discard** — not just consume a pre-loaded set.

## Related Concepts

→ [agent-memory-taxonomy.md](agent-memory-taxonomy.md)  
→ [a-mem.md](a-mem.md) — Zettelkasten memory evolution  
→ [memory-augmented-routing.md](memory-augmented-routing.md) — routing applications
