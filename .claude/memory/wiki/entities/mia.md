---
name: MIA
type: paper
first_seen: 2026-04-08
last_updated: 2026-04-08
sources: [memory-intelligence-agent-mia]
tags: [memory, agent-memory, retrieval, rl-training, deep-research, test-time-learning]
---

# MIA (Memory Intelligence Agent)

> Three-component framework (Memory Manager + Planner + Executor) that treats memory as a living system — not a database — combining parametric and non-parametric memory with alternating RL and test-time learning.

## Key Facts

- Paper: arXiv:2604.04503 (Qiao et al., East China Normal University + Shanghai Innovation Institute) (ref: sources/memory-intelligence-agent-mia.md)
- Three components: Memory Manager (non-parametric, compressed trajectories), Planner (parametric, search strategies), Executor (search + analysis) (ref: sources/memory-intelligence-agent-mia.md)
- Key innovation: bidirectional conversion between parametric ↔ non-parametric memory (ref: sources/memory-intelligence-agent-mia.md)
- Training: alternating GRPO — Executor first, then Planner — enables synergistic cooperation (ref: sources/memory-intelligence-agent-mia.md)
- Test-time learning: Planner evolves continuously during inference without interrupting reasoning (ref: sources/memory-intelligence-agent-mia.md)
- Results: 7B Executor +31% avg across 11 benchmarks, outperforms 32B model by 18% (ref: sources/memory-intelligence-agent-mia.md)
- Frontier model boost: +9% on GPT-5.4 (LiveVQA), +6% on HotpotQA (ref: sources/memory-intelligence-agent-mia.md)
- Key finding: traditional long-context memory underperforms even no-memory baselines — static accumulation hurts (ref: sources/memory-intelligence-agent-mia.md)
- Code: github.com/ECNU-SII/MIA (ref: sources/memory-intelligence-agent-mia.md)

## Relevance to STOPA

MIA validates and extends STOPA's write-time gating approach: living memory (evolving + compressed) systematically beats static retrieval. The bidirectional parametric↔non-parametric bridge is directly applicable to STOPA's hybrid memory design (BM25 + file-backed learnings + critical-patterns).

## Mentioned In

- [Memory Intelligence Agent (MIA)](../sources/memory-intelligence-agent-mia.md)
