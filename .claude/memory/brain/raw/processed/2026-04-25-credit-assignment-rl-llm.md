---
source: arxiv.org/abs/2604.09459
date: 2026-04-25
type: paper
title: "From Reasoning to Agentic: Credit Assignment in Reinforcement Learning for Large Language Models"
arxiv: "2604.09459"
wiki: concepts/credit-assignment-rl-llm.md
---

# Credit Assignment in RL for LLMs (Survey)

## Author
Chenchen Zhang

## Key Concepts
- Two regimes: reasoning RL (500-30k tokens) vs agentic RL (100k-1M tokens)
- 47 credit assignment methods organized in 2D taxonomy:
  - Granularity: token / segment / step / turn / multi-agent
  - Methodology: Monte Carlo / temporal difference / model-based / game-theoretic / information-theoretic
- Reasoning side relies on Process Reward Models + critic-free group comparison
- Agentic side adds: hindsight counterfactuals, asymmetric privileged critics, turn-level MDP

## Main Claims
Sparse outcome rewards become exponentially harder as trajectory length grows. Agentic RL methods diverge from reasoning RL — they invent new techniques rather than reusing PRM/GRPO.

## Core Findings
- Inventory of 47 methods with taxonomy labels
- Reporting checklist for systematic methodological gaps
- Benchmark protocol with method-selection decision tree
- Identifies hindsight counterfactual + asymmetric critics as agentic-RL frontier

## Entities
- arXiv: 2604.09459
- PRM (Process Reward Models), GRPO
- Subject: ML / NLP
