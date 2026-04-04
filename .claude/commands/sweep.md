---
name: sweep
description: Use when cleaning up repository entropy after a long session or multi-file changes. Trigger on 'sweep', 'cleanup', 'entropy', 'stale docs', 'dead code'. Do NOT use for code review (/critic) or refactoring (/simplify).
argument-hint: [--scope session|blast-radius|full] [--auto]
tags: [code-quality, post-edit, documentation]
phase: review
user-invocable: true
allowed-tools: [Read, Grep, Glob, Bash, Agent, Write, Edit]
model: sonnet
effort: medium
maxTurns: 20
handoffs:
  - skill: /critic
    when: "After sweep cleanup — verify sweep didn't introduce regressions"
    prompt: "Review sweep changes: documentation/dead-code cleanup"
  - skill: /scribe
    when: "Sweep discovered patterns worth recording"
    prompt: "Record learning: <pattern>"
---

# Sweep — Post-Session Entropy Cleanup

You are a dedicated cleanup agent. Your job is to reduce repository entropy after sessions that changed code behavior without updating surrounding context (docs, comments, tests, dead code).

**Core principle**: Code changes that modify behavior create entropy — documentation, comments, tests, and dependent code that still reference the old behavior. Left unchecked, this makes the repo progressively harder for agents and humans to navigate.

## Shared Memory

Read first:
- `.claude/memory/state.md` — understand what was recently changed
- `.claude/memory/checkpoint.md` — understand last session scope

## Input

Parse `$ARGUMENTS`:
- `--scope session` (default): analyze only files changed in the current/last session
- `--scope blast-radius`: analyze changed files + all their dependents
- `--scope full`: full repo scan (expensive — only on explicit request)
- `--auto`: non-interactive mode, fix everything without asking (for orchestrator auto-invocation)

<!-- CACHE_BOUNDARY -->

## Process

### Step 1: Identify Blast Radius

Determine what changed and what depends on it:

```
1. Get changed files:
   - git diff --name-only HEAD~5 (session scope — last 5 commits)
   - OR git diff --name-only <checkpoint-commit>..HEAD (if checkpoint has commit hash)

2. For each changed file, find dependents:
   - Python: grep -r "from <module> import\|import <module>" --include="*.py"
   - JS/TS: grep -r "from ['\"].*<module>['\"]|require.*<module>" --include="*.{js,ts,tsx}"
   - General: grep -r "<filename without ext>" to catch references

3. Build impact map:
   | Changed File | What Changed (summary) | Dependents |
   |-------------|----------------------|------------|
```

### Step 2: Detect Entropy (parallel agents)

Spawn up to 3 Haiku agents in parallel, each scanning for a specific entropy type:

#### Agent 1: Stale Documentation
```
Scan these files for documentation that contradicts the current code:
- README.md, docs/*.md — references to changed functions/APIs/behaviors
- Inline docstrings in dependents — do they describe old behavior?
- CLAUDE.md — does it reference patterns that changed?
- Code comments above/near changed lines — do they describe old logic?

Changed files and their diffs:
{git diff for changed files}

Dependent files:
{list of dependents}

Output JSON: [{"file": "...", "line": N, "issue": "...", "old_ref": "...", "current_behavior": "..."}]
```

#### Agent 2: Dead Code & Stale References
```
Scan for code that became dead or stale due to recent changes:
- Functions/classes that were renamed — old name still referenced?
- Imports that are no longer used after refactoring
- Config entries for removed features
- Test fixtures/mocks referencing old interfaces
- Commented-out code blocks (3+ lines) in changed files
- Variables assigned but never read in changed functions

Changed files:
{changed file list}

Dependent files:
{list of dependents}

Output JSON: [{"file": "...", "line": N, "type": "dead_import|dead_function|stale_reference|commented_code|unused_var", "description": "..."}]
```

#### Agent 3: Test & Type Coherence
```
Scan for tests and type annotations that are inconsistent with current code:
- Test assertions checking old behavior/return values
- Test names that describe old behavior (test_returns_string when function now returns dict)
- Mock setups with outdated signatures
- Type annotations in dependents that don't match changed function signatures

Changed files and their diffs:
{git diff}

Test files in scope:
{test files that import changed modules}

Output JSON: [{"file": "...", "line": N, "type": "stale_test|wrong_mock|outdated_type", "description": "...", "expected": "...", "actual": "..."}]
```

### Step 3: Triage Findings

Merge results from all agents. Classify by severity:

| Severity | Criteria | Action |
|----------|---------|--------|
| **high** | Contradicts current behavior — will cause wrong decisions | Fix immediately |
| **medium** | Stale but not contradictory — misleading but not dangerous | Fix in this session |
| **low** | Cosmetic entropy — dead imports, commented code | Fix if time allows |

Sort by severity (high first), then by number of dependents affected.

### Step 4: Fix Entropy

For each finding (high and medium severity):

1. **Documentation fixes**: Update docs/comments to reflect current behavior
2. **Dead code removal**: Remove unused imports, functions, commented-out blocks
3. **Test updates**: Fix assertions, mock signatures, test names
4. **Type fixes**: Update type annotations in dependents

**Rules for fixing:**
- ONLY fix entropy — do NOT improve, refactor, or add features
- Keep fixes minimal — change the minimum needed for accuracy
- If a fix is ambiguous (unclear what the correct state should be), skip and report
- Never delete test files entirely — only update assertions/mocks
- If `--auto` flag is NOT set, present the fix plan and wait for approval before applying

### Step 5: Verify Fixes

After applying fixes:

1. Run applicable checks on fixed files:
   - Python: `python -c "import <module>"` for each fixed .py
   - Lint: `ruff check <fixed-files>` (if available)
   - Tests: `pytest <fixed-test-files> --no-header -q` (if test files were fixed)

2. Ensure no new issues were introduced:
   - `git diff --stat` — review scope of changes
   - No unrelated files should be modified

### Step 6: Report

```markdown
## Sweep Report

**Scope**: {session|blast-radius|full}
**Files analyzed**: {N changed} + {M dependents}
**Findings**: {X high} / {Y medium} / {Z low}

### Fixed
| # | File:Line | Type | What was wrong | What was fixed |
|---|-----------|------|---------------|---------------|
| 1 | docs/api.md:42 | stale_doc | Referenced old `get_user()` signature | Updated to match new `get_user(include_profile=False)` |
| 2 | src/utils.py:15 | dead_import | `from auth import old_validator` (removed) | Deleted import |

### Skipped (low severity)
| # | File:Line | Type | Description |
|---|-----------|------|------------|

### Needs Manual Review
| # | File:Line | Issue | Why automated fix is unsafe |
|---|-----------|-------|---------------------------|
```

## Auto-Invocation

This skill can be auto-invoked by `/orchestrate` at the end of deep/standard tier sessions.
Add to orchestrate Phase 6 after critic pass:

```
If tier is standard or deep AND git diff --stat shows 5+ files changed:
  → spawn sweep with --scope blast-radius --auto
```

## Safety Rules

- Do not delete test files or test functions — removing tests eliminates regression coverage and makes it impossible to verify that future changes don't reintroduce the bug the test was catching
- Do not change function signatures or behavior — changing them breaks all callers and dependents, creating cascading failures outside the blast radius
- Do not modify files outside the blast radius — out-of-scope changes bypass the review gate and create untracked side effects that no verification step covers
- If in doubt, skip the fix and report it as "Needs Manual Review"
- All fixes must be reversible via `git checkout`

## Cost

- 3 × Haiku agents (parallel detection) + 1 × Sonnet (fixing) ≈ light-to-standard cost
- Typically 5-10 minutes for session scope, 15-20 for blast-radius
