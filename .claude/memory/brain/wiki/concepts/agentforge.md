---
title: AgentForge — Execution-Grounded Multi-Agent Software Engineering
category: concepts
tags: [multi-agent, software-engineering, execution-grounded, docker, swe-bench]
sources: [raw/2026-04-18-agentforge-execution-grounded.md]
updated: 2026-04-18
---

# AgentForge — Execution-Grounded Multi-Agent Software Engineering

**Paper**: arXiv:2604.13120  
**Authors**: Rajesh Kumar, Waqar Ali, Junaid Ahmed, Najma Imtiaz Ali, Shaban Usman

## Core Principle

**Execution-grounded verification**: every code modification must pass sandboxed execution before integration. Verification is not optional — it is structurally enforced.

Execution feedback > next-token likelihood as supervision signal. The agent learns from running code, not from predicting tokens.

## Agent Roles

| Agent | Responsibility |
|-------|---------------|
| Planner | Decomposes issue into subtasks |
| Coder | Implements changes |
| Tester | Writes/runs tests |
| Debugger | Analyzes failures |
| Critic | Reviews before integration |

Communication: shared memory in Docker sandbox.

## Repository State as Decision Process

The framework frames software engineering as an **iterative decision process over repository states** (RL framing). Each state = snapshot of the repo. Each action = file modification. Reward = execution success.

This enables systematic search: instead of one-shot generation, agents explore the state space guided by execution feedback.

## Results

- **40.0% on SWE-BENCH Lite** (+26-28pp over single-agent baselines)
- Docker sandboxing enables safe code execution
- Role decomposition enables parallel specialization

## STOPA Relevance

AgentForge's execution-grounded principle maps to STOPA's "verify before done" invariant. The 5-agent decomposition (Planner/Coder/Tester/Debugger/Critic) is a natural pattern for orchestrate skill — currently STOPA uses Scout/Worker/Critic but lacks a dedicated Tester and Debugger role.

## Related Concepts

→ [multi-agent-hpc.md](multi-agent-hpc.md)  
→ [gaama.md](gaama.md)
