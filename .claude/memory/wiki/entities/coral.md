---
name: CORAL
type: tool
first_seen: 2026-04-08
last_updated: 2026-04-08
sources: [coral-autonomous-multi-agent-evolution]
tags: [multi-agent, self-evolution, autoresearch, open-ended, orchestration]
---

# CORAL

> Lightweight framework enabling organizations of autonomous LLM agents to run experiments, evaluate solutions, and iteratively improve codebases via sustained exploration and shared knowledge.

## Key Facts

- Each agent runs in its own git worktree branch — complete isolation, zero conflicts (ref: sources/coral-autonomous-multi-agent-evolution.md)
- Shared state via `.coral/public/` directory; agents access via symlinks with zero sync overhead (ref: sources/coral-autonomous-multi-agent-evolution.md)
- Manager can send heartbeat-triggered prompts (reflection, skill consolidation) to interrupt running agents (ref: sources/coral-autonomous-multi-agent-evolution.md)
- Warm-start mode: agents do literature review (web search) before implementation (ref: sources/coral-autonomous-multi-agent-evolution.md)
- Results: 3-10× improvement rate vs evolutionary baselines across 10 diverse task types (ref: sources/coral-autonomous-multi-agent-evolution.md)
- Kernel optimization task: improved best score from 1363 to 1103 cycles using 4 co-evolving agents (ref: sources/coral-autonomous-multi-agent-evolution.md)
- Supports Claude Code, OpenCode, Codex as agent backends; 17+ CLI commands; web dashboard
- Grading via `TaskGrader` base class: `uv run coral eval` stages changes, commits, and grades in one operation

## Relevance to STOPA

CORAL's git-worktree-per-agent isolation pattern and `.coral/public/` shared state are directly applicable to STOPA's `--group N` orchestration mode; heartbeat-triggered skill consolidation maps to STOPA's critic/checkpoint insertion during long runs.

## Mentioned In

- [CORAL: Autonomous Multi-Agent Evolution for Open-Ended Discovery](../sources/coral-autonomous-multi-agent-evolution.md)
