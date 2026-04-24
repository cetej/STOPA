---
title: SAGE — RL-Based Self-Improving Agent with Skill Library
category: concepts
tags: [reinforcement-learning, skill-library, self-improvement, agent-evolution, grpo]
sources: [raw/processed/2026-04-24-sage-skill-library.md]
updated: 2026-04-24
---

# SAGE — RL-Based Self-Improving Agent with Skill Library

**Paper**: arXiv:2512.17102  
**Authors**: Jiongxiao Wang, Qiaojing Yan, Yawei Wang et al. (December 2025, revised March 2026)

## Core Principle

Skill libraries as persistent knowledge stores require RL integration — not just prompting — for genuine agent self-improvement. Accumulated skills must be reward-integrated, not merely appended as external memory.

## SAGE Framework

| Component | Description |
|-----------|-------------|
| **Skill Augmented GRPO** | RL on top of Group Relative Policy Optimization with skill access |
| **Sequential Rollout** | Iterative task chain deployment enabling cross-task skill transfer |
| **Skill-integrated reward** | Reward considers skill usage quality, not just final outcomes |
| **AppWorld evaluation** | Validated on complex multi-step app interaction benchmark |

## Key Results

- **+8.9%** Scenario Goal Completion over baseline
- **−26%** interaction steps required
- **−59%** token generation (via learned skill reuse)
- Validated on AppWorld benchmark (realistic multi-app tasks)

## Why Prompting Alone Fails

Existing approaches add skills as memory/context but don't teach the agent *when and how* to use them. Without reward signal tied to skill usage, agents default to re-solving problems from scratch even when relevant skills exist.

## STOPA Relevance

Directly validates the STOPA skill library architecture: skills need both storage (SKILL.md) AND reinforcement of when/how to use them. The 59% token reduction from skill reuse is strong evidence for investing in skill quality and routing. Sequential Rollout ≈ STOPA's `/autoloop` pattern: iterative task chains that build on previous outputs.

## Related Concepts

→ [memfactory.md](memfactory.md)  
→ [knowledge-compounding.md](knowledge-compounding.md)  
→ [byterover.md](byterover.md)  
→ [agentic-memory-unified.md](agentic-memory-unified.md)
