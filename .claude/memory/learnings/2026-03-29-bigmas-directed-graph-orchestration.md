---
date: 2026-03-29
type: architecture
severity: medium
component: orchestration
tags: [orchestration-graph, shared-workspace, dynamic-structure, global-workspace-theory]
summary: "Dynamic agent graph orchestration: GraphDesigner analyzes task → generates task-specific directed graph (3-node for simple, 9-node for complex). Agents coordinate via centralized shared workspace. Graph complexity scales with task demands."
source: external_research
uses: 0
harmful_uses: 0
related: []
verify_check: "manual"
---

## Situace
BIGMAS (arxiv:2603.15371) organizes specialized LLM agents as nodes in dynamically constructed directed graphs. Central insight: different tasks need different agent configurations. Instead of fixed workflow, GraphDesigner agent:
1. Analyzes problem complexity
2. Builds task-specific agent graph (variable #nodes, connectivity)
3. Defines shared workspace contract (what data agents exchange)
4. Agents communicate exclusively via workspace (no peer-to-peer)

Outperforms fixed multi-agent setups on reasoning + planning.

## Mapping to STOPA

Current STOPA orchestrate is mostly **sequential/fixed**:
- Tier-1 agents run in order (scout → plan → work → assess)
- All agents share global memory (state.md, budget.md, learnings/)
- No task-specific graph construction

BIGMAS offers **dynamic/adaptive approach**:
- Generate graph for each task (simple task = 2 agents, complex = 5-7)
- Centralized workspace = STOPA memory files (already doing this!)
- Agent roles emerge from task structure, not hardcoded

## Vzor: Task Complexity → Graph Template

| Task Complexity | Graph Shape | Agent Nodes | Workspace Items |
|---|---|---|---|
| Trivial (single edit) | Linear 1-2 | [executor] | none |
| Simple (3-5 files) | Linear 2-3 | [scout, worker] | findings.json |
| Standard (refactor) | DAG 3-4 | [scout, plan, worker, critic] | plan.json, trace.json, findings.json |
| Complex (cross-cutting) | Cyclic 5-7 | [scout, architect, worker×2, critic, reviewer] | architecture.json, trace.json, findings.json, decisions.json |

## Aplikace na STOPA

**Opportunity 1: Adaptive orchestrate**
- Instead of fixed [scout → plan → work → assess], `/orchestrate` generates graph based on file count + scope
- Simple edit → skip scout, jump to worker
- Cross-cutting → add architect node before worker

**Opportunity 2: Task-specific workspace contract**
- Current: all agents write to same files (learnings/, decisions.md, etc.)
- Proposed: each task-graph defines which files it touches (reduces contention)
- Example: code-only task ignores research.md, skips deepresearch agent

**Opportunity 3: Cyclic orchestration**
- Some complex tasks benefit from feedback loops (worker → critic → worker)
- BIGMAS framework models this naturally (cyclic edges allowed)
- Current STOPA is mostly acyclic (one-pass)

## Prevence
- Don't use dynamic graphs for trivial tasks (overhead > benefit)
- Workspace contract must be explicit (document what each agent writes/reads)
- Cyclic graphs need exit condition (depth limit or convergence check)

## Kdy aplikovat
- Multi-step complex tasks (>10 files, >3 modules)
- When task scope is uncertain (scout can determine graph complexity)
- When different agents need parallel work (worker×2 in DAG)
- NOT for quick one-off edits (overhead not justified)
