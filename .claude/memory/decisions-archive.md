# Archived Decisions

Decisions older than 10 tasks, moved here by `/scribe maintenance`.

<!-- Archived 2026-03-27 — resolved/foundational decisions -->

### 2026-03-22 — Skill Audit Findings: Integration Gaps in Utility Skills
- **Context**: skill-audit harness ran across all 15 skills, revealing 4 skills with integration score 2/5
- **Decision**: Utility skills (youtube-transcript, verify) should add "After Completion" sections writing to learnings.md/state.md; scout should add explicit disallowedTools
- **Status**: PARTIALLY DONE — audit ongoing (11/30 skills evaluated, cross-cutting fixes applied)

### 2026-03-18 — Add Budget Controller to Orchestration System
- **Decision**: Full budget skill with 3 complexity tiers (light/standard/deep)
- **Status**: DONE — `/budget` skill implemented and operational

### 2026-03-18 — Soften "Never Do Work Yourself" Rule
- **Decision**: Light tier allows direct work, standard/deep still delegate
- **Status**: DONE — implemented in orchestrator

### 2026-03-18 — Remove Bash and Agent from skill-generator
- **Decision**: Restricted to Read, Write, Edit, Glob, Grep
- **Status**: DONE — least-privilege applied

### 2026-03-18 — STOPA as Source of Truth
- **Decision**: STOPA as standalone meta-project for orchestration
- **Status**: DONE — foundational, operational since creation
