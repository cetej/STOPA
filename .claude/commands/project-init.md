---
name: project-init
description: "Use when setting up a new project with optimal Claude Code config, optionally with long-running multi-session harness scaffold (feature-list.json, progress.md, init.sh, docs/). Trigger on 'init project', 'new project', 'project setup', 'scaffold projekt', 'scaffold'. Do NOT use for existing projects with .claude/ already configured."
argument-hint: "[project-path] [--name 'Project Name'] [--force] [--skip-agents-md] [--harness]"
tags: [planning, devops, orchestration]
phase: plan
user-invocable: true
allowed-tools: Read, Write, Bash, Glob
model: haiku
effort: medium
maxTurns: 20
disallowedTools: Agent
output-contract: "project scaffold → .claude/ tree + CLAUDE.md + AGENTS.md (+ docs/ if --harness) → target project root"
effects:
  - ".claude/ directory structure created"
  - "memory templates written"
  - "CLAUDE.md and AGENTS.md initialized if absent"
  - "--harness: feature-list.json, progress.md, init.sh, docs/architecture.md created"
---

# Project Init — Optimal Claude Code Project Setup

You initialize new projects with the optimal `.claude/` structure for orchestration system integration. With `--harness`, you also create the long-running agent harness scaffold (feature-list.json as ground truth, progress.md for multi-session continuity, init.sh for reliable startup, docs/ as system of record).

## When Things Go Wrong

- **Directory already has `.claude/`**: Use `--force` to overwrite, or skip existing files. Never silently overwrite without flag.
- **Git not initialized**: Init git first (`git init`), then proceed with `.claude/` setup.
- **No write permissions**: Report the error clearly, suggest running with appropriate permissions.
- **--harness on existing project with docs/**: Do NOT overwrite docs/ content. Only add missing files (feature-list.json, architecture.md, progress.md) if they do not already exist.

## System Integration

This skill is part of the STOPA orchestration system. After initialization, the user installs the full orchestration via:
```bash
claude --plugin-dir /path/to/stopa-orchestration
```

<!-- CACHE_BOUNDARY -->

## Input

Parse `$ARGUMENTS`:
- **project-path**: Path to the project root (required). Can be `.` for current directory.
- **--name "Name"**: Project name for CLAUDE.md (optional, defaults to directory name)
- **--force**: Overwrite existing `.claude/` structure (optional, default: fail if exists)
- **--skip-agents-md**: Skip AGENTS.md generation (optional, default: always generate)
- **--harness**: Create long-running harness scaffold (feature-list.json, progress.md, init.sh, docs/). Use for multi-session projects.

If no arguments provided, use current working directory and ask user for project name.

## Step 1: Validate

1. Resolve project path to absolute path
2. Check the directory exists — if not, create it
3. Check if `.claude/` already exists:
   - If exists and no `--force` → STOP, tell user: "`.claude/` already exists. Use `--force` to overwrite."
   - If exists and `--force` → warn user, proceed (do NOT delete existing files, only overwrite templates)
4. Check if `CLAUDE.md` exists — if yes, skip CLAUDE.md creation (never overwrite project instructions)

## Step 2: Create Directory Structure

Create these directories:
```
.claude/
├── skills/          # Empty — skills come via STOPA plugin
├── memory/          # Shared memory for orchestration
├── hooks/           # Empty — hooks come via STOPA plugin
└── agents/          # For project-specific agents (optional)
```

Use `mkdir -p` for all directories.

## Step 3: Initialize Memory Files

Create each file with the exact templates below. These templates define the format that orchestration skills expect.

### `.claude/memory/state.md`

```markdown
# Active Task

No active task.

# Task History

| # | Task | Status | Date |
|---|------|--------|------|
```

### `.claude/memory/decisions.md`

```markdown
# Decision Log

Format for each entry:
## [Decision Title]
- **Context**: Why this decision was needed
- **Options**: What was considered
- **Decision**: What was chosen
- **Rationale**: Why
- **Date**: YYYY-MM-DD
```

### `.claude/memory/learnings.md`

```markdown
# Learnings

## Patterns
<!-- "When X, do Y" — proven approaches -->

## Anti-patterns
<!-- "Never do X, do Y instead" — things that failed -->

## Skill Gaps
<!-- "When doing X, we need skill for Y" — missing capabilities -->
```

### `.claude/memory/budget.md`

```markdown
# Budget Tracker

## Current Task

No active task.

## Tier Reference
| Tier | Agents | Critics | Scout | Use when |
|------|--------|---------|-------|----------|
| light | 0-1 | 1x end | surface | Single file fix |
| standard | 2-4 | 2x | deep | Multi-file change |
| deep | 5-8 | 3x | full | Cross-cutting feature |

## History

| # | Task | Tier | Agents | Critics | Verdict |
|---|------|------|--------|---------|---------|
```

### `.claude/memory/decisions-archive.md`

```markdown
# Decisions Archive

Old decisions moved here by /scribe maintenance. Read-only reference.
```

### `.claude/memory/budget-archive.md`

```markdown
# Budget Archive

Historical budget data moved here by /scribe maintenance.
```

## Step 4: Create CLAUDE.md (if not exists)

Only create if `CLAUDE.md` does not already exist in project root.

> **Why this matters**: Empirical study (arXiv:2601.20404, JAWs 2026, 10 repos, 124 PRs) shows repo-level instruction files reduce AI agent runtime by **28.64%** and output tokens by **16.58%** with zero loss in task completion. CLAUDE.md is not optional boilerplate — it's a direct performance lever.

Use this template — replace `{{PROJECT_NAME}}` with the project name:

```markdown
# {{PROJECT_NAME}}

## Popis

<!-- Krátký popis projektu — co dělá, k čemu slouží -->

## Struktura

<!-- Popis hlavních adresářů a souborů -->

## Orchestrace

Tento projekt používá orchestrační systém STOPA. Instalace:
\```bash
# Lokálně (z STOPA adresáře):
claude --plugin-dir /path/to/stopa-orchestration

# Nebo přímo ze STOPA:
./scripts/sync-orchestration.sh /path/to/this/project --commit
\```

Dostupné skills: `/orchestrate`, `/scout`, `/critic`, `/scribe`, `/budget`, `/checkpoint`, `/watch`, `/skill-generator`, `/dependency-audit`

## Konvence

### Kvalita kódu
- Preferuj jednoduché řešení — 3 řádky > předčasná abstrakce
- Nepřidávej features nad rámec zadání
- Error handling jen pro realistické scénáře

### Windows specifika
- Encoding: UTF-8 všude
- Cesty: `pathlib.Path()` nebo forward slashe

### Git
- Commit message: stručně, česky
- Staging: konkrétní soubory, ne `git add -A`
```

## Step 4b: Create AGENTS.md (if not exists and --skip-agents-md not set)

AGENTS.md is a cross-platform standard for repo-local agent instructions, read by OpenAI Codex, Cursor, Gemini CLI, Windsurf, and other AI tools alongside CLAUDE.md.

Only create if `AGENTS.md` does not already exist in project root AND `--skip-agents-md` was NOT passed.

When `--harness` is set, AGENTS.md MUST include the Startup Sequence section (5-step orient ritual).

Use this template — replace `{{PROJECT_NAME}}` with the project name:

```markdown
# {{PROJECT_NAME}} — Agent Instructions

## Project Overview

<!-- Short description of what this project does -->

## Repository Structure

<!-- Key directories and their purpose -->

## Startup Sequence (required for --harness projects)

Every coding session MUST begin with these steps before making changes:

1. `pwd` — confirm working directory
2. Read `docs/progress.md` to understand recent work
3. `git log --oneline -20` to see recent commits
4. Read `docs/feature-list.json` and pick highest-priority feature with `passes: false`
5. Run `./init.sh` to start the development environment
6. Run smoke test (defined in init.sh or docs/architecture.md) to verify working state

If smoke test fails: fix the existing breakage BEFORE touching any new feature.

## How to Run

<!-- Commands to build, test, and run the project -->

## Coding Conventions

- Keep changes minimal — implement only what was requested
- Prefer simple solutions over abstractions
- No error handling for impossible scenarios
- UTF-8 encoding everywhere; use forward slashes in paths

## Testing

<!-- How to run tests; what to verify before marking a task done -->

## Feature Completion Gate (required for --harness projects)

A feature is DONE only when:
1. All `steps` in `docs/feature-list.json` pass end-to-end (not just unit tests)
2. `passes: true` is set in feature-list.json for that feature
3. Change is committed with descriptive message
4. `docs/progress.md` updated with what was done

Never mark `passes: true` without end-to-end verification. JSON format resists casual editing — that is intentional.

## Important Files

<!-- List of files agents should check first for context -->

## Off-limits

<!-- Files or directories that should never be modified by agents -->
```

## Step 5: Create settings.json

Create `.claude/settings.json` with minimal config:

```json
{
  "permissions": {
    "allow": [],
    "deny": []
  }
}
```

## Step 6: Harness Scaffold (only when --harness flag is set)

This step implements the pattern from Anthropic's Claude Code harness engineering: repository-as-system-of-record, feature-list ground truth, reliable startup, and multi-session progress continuity.

Skip this step entirely if `--harness` was NOT passed.

### 6a: Create `docs/` directory

```
docs/
├── architecture.md      # Map pointing to deeper sources of truth
├── feature-list.json    # Enumerated features with passes:bool ground truth
├── progress.md          # Human-readable session log
└── decisions/           # Empty dir for future ADRs
```

Use `mkdir -p docs/decisions`.

### 6b: Create `docs/feature-list.json`

This is the project's ground truth for completeness. Stored as JSON (not Markdown) because models are empirically less likely to inappropriately modify JSON files.

Template:
```json
{
  "schema_version": "1.0",
  "project": "{{PROJECT_NAME}}",
  "last_updated": "{{TODAY}}",
  "features": [
    {
      "id": "F001",
      "category": "core",
      "description": "Short description of the user-visible behavior",
      "steps": [
        "Step 1: precondition",
        "Step 2: action",
        "Step 3: expected observation"
      ],
      "passes": false
    }
  ]
}
```

Substitute `{{TODAY}}` with current date (YYYY-MM-DD) and `{{PROJECT_NAME}}` with the project name. The single placeholder feature F001 is a template — instruct the user to replace it with real features.

### 6c: Create `docs/progress.md`

```markdown
# Progress Log

Append entries in reverse chronological order (newest first). Every coding session MUST end with an entry here.

## Session Template

```
### YYYY-MM-DD (session N)
- **Goal**: what was attempted
- **Features touched**: F001, F002
- **Status**: passes updated / blocked / in-progress
- **Next**: suggested next feature for next session
```

## Sessions

_(Add sessions above this line)_
```

### 6d: Create `init.sh`

Idempotent startup script. Must work on bash (Linux/macOS/Git-Bash on Windows).

```bash
#!/usr/bin/env bash
# init.sh — start development environment for {{PROJECT_NAME}}
# Idempotent: safe to run multiple times in one session.

set -euo pipefail

cd "$(dirname "$0")"

echo "==> Initializing {{PROJECT_NAME}} development environment"

# Step 1: verify prerequisites
# TODO: add commands to check required tools (node, python, etc.)
#   example: command -v node >/dev/null 2>&1 || { echo "node not found"; exit 1; }

# Step 2: install dependencies (idempotent)
# TODO: add install commands
#   example: [ -d node_modules ] || npm install

# Step 3: start background services if needed
# TODO: add service startup
#   example: docker-compose up -d db

# Step 4: smoke test — verifies environment is ready
# TODO: add a fast check (1-5 seconds) that proves the env works
#   example: curl -sf http://localhost:3000/health || exit 1

echo "==> Environment ready"
```

Make it executable: `chmod +x init.sh` (via Bash tool).

### 6e: Create `docs/architecture.md`

Short map (target: 100-150 lines) pointing to deeper sources of truth. This is the entry point for agents — not a comprehensive manual.

```markdown
# {{PROJECT_NAME}} — Architecture Map

This file is the entry point for agents working on this project. It points to deeper sources of truth. Keep it short (~100 lines). If a section grows large, extract it to its own file under `docs/` and link from here.

## What this project does

<!-- 2-3 sentences. What problem does it solve? Who is the user? -->

## Top-level structure

| Directory | Purpose | Key files |
|-----------|---------|-----------|
| `src/` | TODO | TODO |
| `tests/` | TODO | TODO |
| `docs/` | Agent-readable documentation | feature-list.json, progress.md |

## Core abstractions

<!-- List 3-7 main concepts/modules. One line each. Link to deeper docs if they exist. -->

## Invariants (mechanically enforced)

<!-- List architectural rules that are checked by linters/tests, not by human review. -->

## How to verify a feature works

1. Locate the feature in `docs/feature-list.json` by `id`
2. Follow the `steps` array end-to-end
3. If all steps observe expected behavior: set `passes: true`
4. Commit with message `feat(F###): <description>`

## Where to find things

- **Recent work**: `docs/progress.md`
- **Feature status**: `docs/feature-list.json`
- **Decisions**: `docs/decisions/` (ADR format)
- **Learnings**: `.claude/memory/learnings/`
```

### 6f: Update AGENTS.md for harness

If `--harness` was set AND AGENTS.md was created in Step 4b, the AGENTS.md template already includes the Startup Sequence and Feature Completion Gate sections. No additional edits needed.

If AGENTS.md already existed (created before this invocation): append the Startup Sequence and Feature Completion Gate sections to the existing file, with a comment marker for traceability:

```markdown
<!-- Added by /project-init --harness on YYYY-MM-DD -->
## Startup Sequence
...
## Feature Completion Gate
...
```

## Step 7: Output

Display to the user:

1. **Tree of created files** — show what was created (including docs/ if --harness)
2. **Next steps**:
   - "Uprav `CLAUDE.md` — doplň popis projektu a specifické konvence"
   - "Uprav `AGENTS.md` — doplň strukturu projektu a jak spustit testy (čtou to Codex, Cursor, Gemini CLI)"
   - If `--harness`: "Uprav `docs/feature-list.json` — nahraď placeholder F001 reálnými features projektu"
   - If `--harness`: "Vyplň `init.sh` — doplň commands pro start prostředí a smoke test"
   - If `--harness`: "Uprav `docs/architecture.md` — vyplň top-level strukturu a core abstractions"
   - "Nainstaluj orchestraci: `claude --plugin-dir /path/to/stopa-orchestration`"
3. **Quick start**: "Použij `/orchestrate` pro komplexní úkoly, `/scout` pro průzkum"

## Anti-Rationalization Defense

| Rationalization | Why Wrong | Do Instead |
|---|---|---|
| "The user didn't ask for --harness, I'll skip those files" | Correct — harness scaffold is opt-in by design | Respect the flag; only create docs/ when --harness is explicit |
| "I'll overwrite existing CLAUDE.md, the template is better" | CLAUDE.md contains accumulated project-specific instructions that cannot be reconstructed | Never overwrite — only create if absent |
| "feature-list.json in YAML would be cleaner" | Empirical finding: models edit Markdown/YAML casually, JSON resists casual editing — that rigidity is the point | Keep feature-list as JSON |
| "I'll pre-populate feature-list.json with guessed features from project name" | Guessed features are worse than a placeholder — they lock in wrong mental models | Create single F001 placeholder, instruct user to replace |

## Red Flags

STOP and re-evaluate if any of these occur:
- Overwriting existing files without --force flag
- Creating feature-list.json entries without user confirmation
- Generating init.sh with project-specific commands you cannot verify
- Proceeding when target directory is outside user's allowed paths

## Verification Checklist

- [ ] `.claude/` directory tree matches Step 2 exactly
- [ ] All memory templates written verbatim (orchestration skills parse these)
- [ ] CLAUDE.md and AGENTS.md either created OR explicitly skipped (with reason)
- [ ] If `--harness`: `docs/feature-list.json` is valid JSON (run `python -m json.tool docs/feature-list.json`)
- [ ] If `--harness`: `init.sh` is executable (`ls -l init.sh` shows `+x`)
- [ ] Output lists every file created, nothing silently written

## Rules

- Do not overwrite existing CLAUDE.md — it contains project-specific instructions and accumulated configuration that cannot be reconstructed from a template
- Do not overwrite existing AGENTS.md — it may contain custom agent configurations and team structures that would be lost
- Do not delete existing files in `.claude/` even with `--force` — these files represent accumulated project state (learnings, decisions, memory) that is irreplaceable once deleted
- Memory templates must match exactly — orchestration skills parse these formats
- Keep output in Czech for the user
- If project has `.git/`, mention that `.claude/memory/` should be in `.gitignore` (sensitive state)
- `--harness` scaffold is opt-in — never auto-apply to every project
