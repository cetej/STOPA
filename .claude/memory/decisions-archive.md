# Archived Decisions

Decisions older than 10 tasks, moved here by `/scribe maintenance`.

<!-- Archived 2026-03-30 — resolved/stable/foundational decisions -->

### 2026-03-27 — Cloud Auto-Fix integration: 3-layer approach
- **Decision**: `/autofix` skill (DONE) + `/fix-issue` Phase 7 (DONE) + Scheduled cloud tasks (PLANNED)
- **Status**: DONE (skill + integration), PLANNED (scheduled tasks need Claude GitHub App)

### 2026-03-26 — AutoDream vs STOPA memory: KOEXISTENCE
- **Decision**: Dream jako "janitor" (čištění, dedup), STOPA `/scribe` jako "architekt" (YAML, grep-first, archivace)
- **Ochrana**: HTML komentář v MEMORY.md, monitorovat, eskalace: `autoDreamEnabled: false`
- **Status**: STABLE — rozhodnutí platí, PR #39299 stále nemerged

### 2026-03-24 — Server pro 24/7 agent infrastrukturu
- **Decision**: PENDING — uživatel plánuje server
- **Požadavky**: CC CLI + scheduled tasks + Telegram + Git SSH + Python 3.11+
- **Sync**: SyncThing (P2P, $0/měsíc)
- **Možnosti**: (A) VPS €5-10/měsíc, (B) Anthropic hosted, (C) RPi, (D) Mac Mini
- **Status**: PENDING — rozhodnutí na uživateli

### 2026-03-24 — Voting Pattern: Known Gap, Future Option
- **Decision**: Neimplementovat, zapsat jako nápad. Flag `--voting` pro `/critic` až bude evidence potřeby.
- **Status**: PARKED

### 2026-03-24 — /fix-issue workflow: Direct main commits (solo project)
- **Decision**: Commitovat přímo na main bez feature branch/PR workflow
- **Status**: DONE — foundational convention

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
