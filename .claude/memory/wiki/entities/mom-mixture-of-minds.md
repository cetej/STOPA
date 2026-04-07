---
name: MoM (Mixture-of-Minds)
type: paper
first_seen: 2026-04-07
last_updated: 2026-04-07
sources: [mom-taro-research]
tags: [orchestration, multi-agent, reinforcement-learning]
---

# MoM (Mixture-of-Minds)

> Zhou et al. (arXiv:2510.20176) — multi-agent GRPO systém pro table understanding s role-specific reward funkcemi a sequential training (planner → coder → answerer).

## Key Facts

- 62.13% na TableBench — role-specific rewards přináší +5-17% kvalitu (ref: sources/mom-taro-research.md)
- Sequential training (planner first, then coder) překonává simultánní trénink — upstream quality je bottleneck
- Role-specific rewards: BLEU pro planner, execution success pro coder, exact match pro answerer
- Best-of-N parallel rollouts: 8x rollouts přidávají +3.65% kvalitu
- Removing any role degrades celkový výsledek

## Relevance to STOPA

Validuje navrhovaný role-specific critic scoring: scout (coverage/relevance), worker (correctness/tests), verifier (evidence grounding). Potvrzuje STOPA upstream-first quality design — scout quality gate PŘED plan fází.

## Mentioned In

- [MoM + TARo Research Brief](../sources/mom-taro-research.md)
