---
date: 2026-04-18
source: https://arxiv.org/abs/2604.13120
type: paper
title: "AgentForge: Execution-Grounded Multi-Agent LLM Framework for Autonomous Software Engineering"
authors: Rajesh Kumar, Waqar Ali, Junaid Ahmed, Najma Imtiaz Ali, Shaban Usman
tags: [multi-agent, software-engineering, execution-grounded, docker, swe-bench]
---

## Summary

AgentForge makes execution-grounded verification a core design principle: every code modification passes sandboxed execution before integration. Five specialized agents (Planner, Coder, Tester, Debugger, Critic) collaborate through shared memory in a Docker sandbox. Frames SE as iterative decision process over repository states where execution feedback > next-token likelihood. Achieves 40.0% on SWE-BENCH Lite, +26-28pp over single-agent baselines.

## Key Concepts

- Execution-grounded verification: run code before integrating changes
- Five agents: Planner, Coder, Tester, Debugger, Critic
- Shared memory architecture in Docker sandbox
- Repository state as decision process (RL framing)
- Execution feedback > next-token likelihood as supervision signal

## Claims

- 40.0% on SWE-BENCH Lite (26-28pp above single-agent baselines)
- Docker sandboxing enables safe execution-grounded verification
- Role decomposition enables parallel specialization

## Entities

Authors: Rajesh Kumar, Waqar Ali, Junaid Ahmed, Najma Imtiaz Ali, Shaban Usman
Benchmark: SWE-BENCH Lite
