---
source: arxiv.org/abs/2604.10029
date: 2026-04-24
type: paper
title: "Self-Distilled Reinforcement Learning for Co-Evolving Agentic Recommender Systems"
arxiv: "2604.10029"
wiki: concepts/coars-agentic-recommenders.md
---

# Self-Distilled RL for Co-Evolving Agentic Recommender Systems (CoARS)

## Authors
Zongwei Wang, Min Gao, Hongzhi Yin, Junliang Yu, Tong Chen, Quoc Viet Hung Nguyen, Shazia Sadiq, Tianrui Li

## Key Concepts
- Agentic Recommender Systems (ARS) — LLM-powered multi-turn recommendation
- Co-evolution of recommender + user agents through shared trajectories
- Self-distilled credit assignment — converting historical data to token-level signals
- Interaction reward: coupled supervision from shared multi-turn trajectories
- Parameter internalization (vs external textual memory)

## Main Claims
Existing ARS rely on external memory rather than internalizing learning into parameters. Current RL approaches for ARS overlook two things: interactive co-evolution between agents, and dense supervision available throughout multi-turn trajectories. CoARS addresses both simultaneously.

## Core Findings
- Two mechanisms: interaction reward (coupled supervision) + self-distilled credit assignment (token-level signals from history)
- Outperforms representative ARS baselines on recommendation performance and user alignment
- First RL framework treating ARS as co-evolution problem

## Entities
- CoARS framework
- Agentic Recommender Systems (ARS)
- arXiv: 2604.10029 (April 2026, cs.IR)
