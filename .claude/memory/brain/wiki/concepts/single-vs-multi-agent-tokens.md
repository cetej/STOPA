---
title: Single-Agent vs Multi-Agent Under Equal Token Budgets
category: concepts
tags: [multi-agent, single-agent, token-budget, reasoning, information-theory]
sources: [raw/processed/2026-04-24-single-vs-multi-agent-tokens.md]
updated: 2026-04-24
---

# Single-Agent vs Multi-Agent Under Equal Token Budgets

**Paper**: arXiv:2604.02460  
**Authors**: Dat Tran, Douwe Kiela (April 2026, cs.MA)

## Core Claim

Multi-agent systems appear superior primarily because benchmarks give them more compute. When token budgets are equalized, single-agent systems match or exceed MAS on multi-hop reasoning — because splitting reasoning across agents destroys information.

## Data Processing Inequality

The theoretical grounding: **information cannot increase through processing**. When Agent A processes context and passes a summary to Agent B, the summary contains *at most* as much information as Agent A's input. Every handoff is a lossy compression.

Single agents retain full context throughout the reasoning chain — no lossy handoffs.

## Experimental Results

| Architecture | Multi-hop Reasoning | Token Budget |
|---|---|---|
| Single-agent | Matched or exceeded MAS | Equal budget |
| Multi-agent | Conventional benchmarks show advantage | Typically higher budget |

Tested across 3 model families: Qwen3, DeepSeek-R1-Distill-Llama, Gemini 2.5

**Note**: API-based budget controls showed artifacts, especially with Gemini 2.5.

## Benchmark Methodology Issues

Standard MAS benchmarks:
- Allocate more total tokens to multi-agent systems
- Measure task completion without controlling for compute
- Conflate architectural advantage with resource advantage

## When Multi-Agent Still Makes Sense

This paper doesn't argue against MAS universally. Multi-agent is appropriate when:
- Tasks genuinely require parallel specialized processing (not just multi-hop reasoning)
- Context limits prevent single-agent from holding all information
- Different agents need access to different tools/environments

## STOPA Relevance

Important counterweight to STOPA's multi-agent bias. For **multi-hop reasoning tasks** (e.g., code analysis chains, research synthesis), a single well-resourced agent may outperform an orchestrated team. This validates the `light` budget tier: don't escalate to multi-agent unless the task genuinely requires it. The Data Processing Inequality is a useful mental model for `/orchestrate` budget tier decisions.

## Related Concepts

→ [paramanager-orchestrator.md](paramanager-orchestrator.md)  
→ [adaptive-orchestration-dmoe.md](adaptive-orchestration-dmoe.md)  
→ [gaama.md](gaama.md)
