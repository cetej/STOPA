---
name: HexMachina
type: paper
first_seen: 2026-04-07
last_updated: 2026-04-07
sources: [vertical-scaling-research]
tags: [multi-agent, orchestration, phase-separation, planning]
---

# HexMachina

> Multi-agent system demonstrating that 3-agent design (Orchestrator/Analyst/Coder) outperforms 5-agent designs due to "dilution from additional roles"; validates phase separation (discovery→improvement).

## Key Facts

- Paper: arXiv:2506.04651v2 (ref: sources/vertical-scaling-research.md)
- 3-agent core beats 5-agent: 54.1% vs 16.4% win rate against Reflexion-style (ref: sources/vertical-scaling-research.md)
- Phase separation is critical: Discovery (environment mapping) → Improvement (strategy). Without discovery, agents converge on "shallow 1-ply lookahead heuristics" (ref: sources/vertical-scaling-research.md)
- Compiled artifact: LLM proposes strategy → Python class encodes it → execution without re-querying LLM (ref: sources/vertical-scaling-research.md)
- Tested on game-playing — transferability to code tasks is inferred (ref: sources/vertical-scaling-research.md)

## Relevance to STOPA

Validates STOPA's orchestrate→scout→worker chain and budget tier limits (3-4 agents optimal). The compiled artifact pattern maps to orchestrator producing a plan JSON/YAML rather than per-step LLM calls.

## Mentioned In

- [Vertikální škálování Research](../sources/vertical-scaling-research.md)
