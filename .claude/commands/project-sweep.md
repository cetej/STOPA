---
name: project-sweep
description: Use when performing the same operation across all registered projects. Trigger on sweep all projects, project sweep. Not for single-project tasks.
argument-hint: [operation description] [--dry-run]
user-invocable: true
allowed-tools: ["Read", "Grep", "Glob", "Bash", "Agent", "Write", "Edit"]
effort: medium
---

# Project Sweep — Multi-Project Orchestration

Execute a batch operation across all registered projects in parallel.

## Instructions

### 1. Load Registry
Check if `~/.claude/memory/projects.json` exists — get list of projects with status "active". If not found, fall back to known project paths from CLAUDE.md (Cílové projekty section).

### 2. Parse Operation
Determine what to do from user input. Common sweep operations:

| Operation | Description |
|-----------|-------------|
| `health` | Git status, stale branches, uncommitted changes, CLAUDE.md presence |
| `update-deps` | Check for outdated dependencies (npm outdated, pip list --outdated) |
| `sync-learnings` | Push cross-project learnings to all project CLAUDE.md files |
| `lint-config` | Verify .claude/ config consistency across projects |
| `git-cleanup` | Prune merged branches, clean up stale remotes |
| `custom:<command>` | Run arbitrary command in each project directory |

If user doesn't specify, default to `health`.

### 3. Execute in Parallel
For each active project, spawn a sub-agent (model: haiku) that:

1. `cd` to project path
2. Verify path exists (`test -d <path>`)
3. Execute the operation
4. Return structured result: `{project, status, findings, actions_needed}`

Use Agent tool with `model: haiku` for each project. Run all in parallel.

**Important**: Sub-agents are READ-ONLY by default. Any modifications require explicit user confirmation per-project.

### 4. Aggregate Results

Compose a summary table:

```
## Project Sweep: {operation} ({date})

| Project | Status | Findings | Action Needed |
|---------|--------|----------|---------------|
| STOPA | OK | Clean, 2 branches | - |
| NG-ROBOT | WARN | 3 uncommitted files | Commit or stash |
| ADOBE-AUTOMAT | OK | Clean | - |

### Details
(expand per-project if findings are non-trivial)

### Cross-Project Insights
(patterns found across multiple projects)
```

### 5. Save Results
- Write sweep results to `.claude/memory/state.md` (overwrite "Last sweep" section)
- If critical findings: send Telegram notification via `bash ~/.claude/hooks/telegram-notify.sh`

### 6. Suggest Follow-ups
Based on findings, suggest concrete next actions:
- "NG-ROBOT has uncommitted changes — want me to commit them?"
- "3 projects have outdated dependencies — want me to update them one by one?"

## Health Check Details

When operation is `health`, check for each project:

1. **Git status**: `git -C <path> status --porcelain` — any uncommitted changes?
2. **Stale branches**: `git -C <path> branch --merged main | grep -v main` — branches to clean?
3. **Last commit**: `git -C <path> log -1 --format="%ar %s"` — how recent?
4. **CLAUDE.md**: Does `<path>/CLAUDE.md` exist? Is it up to date?
5. **Open issues**: `gh issue list -R <repo> --limit 3 --state open` (if gh available)
6. **Disk usage**: `du -sh <path>/.git` — repo size reasonable?

## Safety Rules

- NEVER auto-commit, push, or delete anything without user confirmation
- NEVER modify files in other projects without explicit approval
- If a project path doesn't exist, skip it and note in results
- If an operation fails for one project, continue with others
- Rate limit: max 8 parallel agents (one per project)

## Process

1. Load project registry (projects.json or CLAUDE.md fallback)
2. For each project, execute the requested operation
3. Collect results and report per-project status
4. If cross-project patterns found, tell user to record via `/scribe` (you may not have Write access in deep mode)

## Error Handling

- If a project fails: continue with remaining, report failures at end
- Never force-push or destructive operations without confirmation

## Output Format

```markdown
## Sweep Report: <operation>
| Project | Status | Notes |
|---------|--------|-------|
```
