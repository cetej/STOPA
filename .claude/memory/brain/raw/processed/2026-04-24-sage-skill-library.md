---
source: arxiv.org/abs/2512.17102
date: 2026-04-24
type: paper
title: "Reinforcement Learning for Self-Improving Agent with Skill Library"
arxiv: "2512.17102"
wiki: concepts/sage-skill-library.md
---

# Reinforcement Learning for Self-Improving Agent with Skill Library

## Authors
Jiongxiao Wang, Qiaojing Yan, Yawei Wang, Yijun Tian, Soumya Smruti Mishra, Zhichao Xu, Megha Gandhi, Panpan Xu, Lin Lee Cheong

## Key Concepts
- SAGE: Skill Augmented GRPO for self-Evolution
- Skill libraries as persistent knowledge stores for LLM agents
- Sequential Rollout — iterative task chain deployment
- Skill-integrated reward mechanisms (beyond outcome-based)
- AppWorld benchmark evaluation

## Main Claims
LLM agents struggle to continuously improve and adapt in new environments. Skill library implementations addressing this require more than prompting — RL is necessary for genuine self-improvement. The key insight: skill accumulation must be reward-integrated, not just appended as memory.

## Core Findings
- 8.9% improvement in Scenario Goal Completion
- 26% reduction in interaction steps required
- 59% decrease in token generation
- Validated on AppWorld benchmarks
- Sequential Rollout enables cross-task skill transfer

## Entities
- SAGE framework (Skill Augmented GRPO for self-Evolution)
- AppWorld benchmark
- GRPO (Group Relative Policy Optimization)
- arXiv: 2512.17102 (December 2025, revised March 2026)
