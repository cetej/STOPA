---
title: SWE-Adept — Localization/Resolution Split for Repo-Level SWE
category: concepts
tags: [swe-agents, multi-agent, code-search, checkpoint-memory, version-control]
sources: [arXiv:2603.01327]
updated: 2026-04-25
---

# SWE-Adept — Localization/Resolution Split for Repo-Level SWE

**Paper**: arXiv:2603.01327
**Authors**: Kang He, Kaushik Roy

## Core Principle

Repo-level SWE tasks are bottlenecked by two distinct problems: (1) ineffective codebase navigation/context management, and (2) lack of systematic iterative test-driven modification. SWE-Adept splits these into specialized agents rather than letting a single agent juggle both.

## Architecture

| Component | Role |
|-----------|------|
| **Localization Agent** | Agent-directed depth-first search through codebase to find issue-relevant code while minimizing irrelevant context |
| **Resolution Agent** | Adaptive planning with Git-based version control, branching, reversion |
| **Step-Indexed Memory** | Each execution step is a checkpoint — precise retrieval and rollback |
| **Shared Working Memory** | Code-state checkpoints synced across agents |

## Key Results

- **+4.7%** end-to-end resolve rate over prior SOTA on SWE-Bench Lite and Pro
- Selective context traversal reduces token overhead vs full-file dumps
- Git-backed checkpoints enable safe exploration of alternative solutions

## STOPA Relevance

Validates two existing STOPA patterns:
1. **scout/orchestrate/critic split** — already separates localization (scout) from resolution (workers) from validation (critic). SWE-Adept adds explicit DFS-with-pruning for the localization step.
2. **Memory-backed checkpoint pattern** — STOPA's `checkpoint.md` + `state.md` + git ops mirror the step-indexed memory idea. Could formalize "execution step index" as retrieval key.

Direct applications:
- `/scout` could adopt agent-directed DFS pattern explicitly (current: heuristic exploration)
- `/orchestrate` farm tier could add per-subtask Git branch (currently shared working tree)
- Step-indexed memory pattern → useful for `/autoloop` and `/autoresearch` rollback

## Related Concepts

→ [swe-agents-survey.md](swe-agents-survey.md)
→ [analysis-bench-agents.md](analysis-bench-agents.md)
→ [semaclaw-harness-engineering.md](semaclaw-harness-engineering.md)
→ [paramanager-orchestrator.md](paramanager-orchestrator.md)
