---
date: 2026-04-18
source: https://arxiv.org/abs/2601.01885
type: paper
title: "Agentic Memory: Learning Unified Long-Term and Short-Term Memory Management"
authors: Yi Yu, Liuyi Yao, Yuexiang Xie, Qingquan Tan, Jiaqi Feng, Yaliang Li, Libing Wu
tags: [memory, reinforcement-learning, grpo, long-short-term-memory, tool-based-memory]
---

## Summary

Proposes a unified framework treating memory operations (store, retrieve, update, summarize, discard) as actionable tools agents invoke autonomously. Unifies long-term and short-term memory within a single agent policy, enabling end-to-end optimization. Uses three-stage progressive RL with step-wise GRPO to handle sparse rewards from memory operations. Outperforms memory-augmented baselines on 5 long-horizon benchmarks on task performance, memory quality, and context efficiency.

## Key Concepts

- Memory operations as tools (store/retrieve/update/summarize/discard)
- Unified LT+ST memory management under single policy
- Progressive RL: 3-stage training with step-wise GRPO
- Sparse reward handling for discontinuous memory operations
- Context efficiency as explicit optimization target

## Claims

- Outperforms existing memory-augmented baselines on 5 long-horizon benchmarks
- Step-wise GRPO handles sparse, discontinuous memory rewards
- End-to-end optimization possible when memory ops are tool calls

## Entities

Authors: Yi Yu, Liuyi Yao, Yuexiang Xie, Qingquan Tan, Jiaqi Feng, Yaliang Li, Libing Wu
Benchmarks: 5 long-horizon tasks
