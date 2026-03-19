# Shared Memory — Task State

Current task state shared across all agents and skills.

## Active Task

**Goal**: Karpathy AutoResearch — research + /autoloop skill creation
**Type**: research + implementation
**Status**: complete

### Subtasks

| # | Subtask | Depends on | Method | Status |
|---|---------|-----------|--------|--------|
| 1 | Research Karpathy AutoResearch (3 agents) | — | Agent:research ×3 | done |
| 2 | Analyze STOPA applications | 1 | Direct | done |
| 3 | Select metric (M5 hybrid) | 2 | Direct | done |
| 4 | Create /autoloop skill | 3 | Direct | done |
| 5 | Baseline scoring all skills | 4 | Bash | done |

## Task History

### 2026-03-18 — Initial System Build
- **Goal**: Vytvořit orchestrační systém (skills, sdílená paměť, budget, session continuity)
- **Result**: 9 skills, sdílená paměť, budget tiers, circuit breakers, /watch, /checkpoint
- **Origin**: Vyvinut v test1 (Pyramid Flow), přenesen do STOPA jako source of truth
