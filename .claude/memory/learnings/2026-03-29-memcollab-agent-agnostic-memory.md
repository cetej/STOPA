---
date: 2026-03-29
type: architecture
severity: high
component: memory
tags: [memory-sharing, contrastive-learning, multi-model, claude-tiers, trajectory-distillation]
summary: "Agent-agnostic memory via contrastive trajectory distillation: run multiple agents (Haiku/Sonnet/Opus) on same task, contrast their reasoning paths, distill shared constraints. Memory then improves all agents, not just one."
source: external_research
uses: 1
harmful_uses: 0
related: []
confidence: 0.75
verify_check: "manual"
---

## Situace
MemCollab (arxiv:2603.23234) constructs collaborative memory that transfers across different LLM agents. Key insight: naive memory transfer between agents fails because memory entangles task-level knowledge with agent-specific biases. Solution: contrast reasoning trajectories from different agents solving the same problem.

## Problem s aktuálním STOPA approach
Currently, each agent (Haiku, Sonnet, Opus) builds its own learnings in parallel. When one agent discovers a pattern, other agents don't benefit unless we manually transfer + verify. This is:
- Labor-intensive (human reviews transfers)
- Lossy (agent-specific tricks don't generalize)
- Slow (patterns emerge independently across agents)

## Řešení: Contrastive Trajectory Distillation
1. **Task set**: Collect same 10-20 problems/scenarios
2. **Multi-agent solve**: Run Haiku, Sonnet, Opus on each → 30-60 trajectories
3. **Contrast**: Compare solution paths pairwise → what's common? what's model-specific?
4. **Distill**: Extract shared reasoning constraints (abstract rules that ALL agents benefit from)
5. **Task-aware retrieval**: At inference, condition memory access on task category (coding vs reasoning vs research)

## Aplikace na STOPA

**Phase 1 (v26-03-30)**: Design contrastive loop
- Pick 5 representative tasks from state.md completed tasks
- Run Haiku `/orchestrate` + Sonnet `/scout` on each → compare reasoning traces
- Identify shared decision points (when do both agents choose same branch?)

**Phase 2 (later)**: Implement memory inference
- Extend `/scribe` to detect contrastive patterns in agent outputs
- Tag memory entries as "cross-tier validated" vs "single-agent"
- Cross-tier entries get higher weight in retrieval

## Prevence
- Don't merge memory blindly (degrades specific agent optimizations)
- Require minimum 2-agent agreement before marking as "shared"
- Include task category in memory entries so retrieval is context-aware

## Kdy aplikovat
- When 3+ agents independently discover same pattern → strong signal
- When Sonnet solves differently than Haiku → contrastive gold mine
- NOT when only one agent succeeds (keep agent-specific knowledge)
