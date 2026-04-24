---
source: arxiv.org/abs/2604.02460
date: 2026-04-24
type: paper
title: "Single-Agent LLMs Outperform Multi-Agent Systems on Multi-Hop Reasoning Under Equal Thinking Token Budgets"
arxiv: "2604.02460"
wiki: concepts/single-vs-multi-agent-tokens.md
---

# Single-Agent LLMs Outperform Multi-Agent Systems (Equal Token Budgets)

## Authors
Dat Tran, Douwe Kiela

## Key Concepts
- Data Processing Inequality — splitting reasoning across agents destroys information
- Token budget fairness — controlling for total compute used
- Single-Agent Systems (SAS) vs Multi-Agent Systems (MAS)
- Multi-hop reasoning benchmark evaluation
- Information efficiency as architecture metric

## Main Claims
Multi-agent systems appear advantageous primarily due to greater computational resources, not inherent architecture. When token budgets are equal and context is used optimally, single-agent systems are more information-efficient. Standard MAS benchmarks contain methodological issues that inflate multi-agent advantages.

## Core Findings
- Single-agent consistently matched or exceeded MAS on multi-hop reasoning with controlled token budgets
- Tested across 3 model families: Qwen3, DeepSeek-R1-Distill-Llama, Gemini 2.5
- API-based budget controls showed artifacts (esp. Gemini 2.5)
- Standard benchmarks inflate MAS advantages through unequal compute allocation
- Theoretical grounding: Data Processing Inequality — information cannot increase through processing

## Entities
- arXiv: 2604.02460 (April 2026, cs.MA)
- Models: Qwen3, DeepSeek-R1, Gemini 2.5
- Benchmark: multi-hop reasoning tasks
