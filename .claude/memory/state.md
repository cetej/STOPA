# Shared Memory — Task State

Current task state shared across all agents and skills.

## Active Task

**Goal**: Czech Language Corrector — audit + průzkum + návrh architektury
**Type**: research + architecture proposal
**Status**: in_progress (awaiting user direction)

### Subtasks

| # | Subtask | Depends on | Method | Status |
|---|---------|-----------|--------|--------|
| 1 | Pipeline audit (NG-ROBOT Czech quality) | — | Agent:sonnet | done |
| 2 | Czech resources research (NLP tools, DBs) | — | Agent:sonnet | done |
| 3 | Overlap analysis (terminology vs corrector) | — | Agent:sonnet | done |
| 4 | Synthesis + architecture proposal | 1,2,3 | Direct | done |
| 5 | Implementation plan (user choice) | 4 | Pending user | pending |

### Key Findings

- Phase 1 (Translation) has NO Czech language guardrails — main injection point for anglicisms
- Phase 5 (LanguageContextOptimizer) is the main quality gate but overloaded (11 categories, Sonnet, thinking OFF)
- Phase 7 (SEO) generates new CZ text with no post-correction
- LanguageTool has NO Czech module — must build from scratch
- LINDAT/ÚFAL ecosystem (MorphoDiTa, UDPipe, Korektor) is the best foundation
- TermDB and corrector are complementary — need "protected terms" contract
- 3 variants proposed: A (prompt enhancement), B (hybrid corrector, recommended), C (full NLP stack)

## Task History

### 2026-03-19 — Karpathy AutoResearch
- **Goal**: Research Karpathy AutoResearch + create /autoloop skill
- **Result**: M5 hybrid metric, /autoloop skill created, baseline scores for all skills
- **Origin**: STOPA orchestration

### 2026-03-18 — Initial System Build
- **Goal**: Vytvořit orchestrační systém (skills, sdílená paměť, budget, session continuity)
- **Result**: 9 skills, sdílená paměť, budget tiers, circuit breakers, /watch, /checkpoint
- **Origin**: Vyvinut v test1 (Pyramid Flow), přenesen do STOPA jako source of truth
