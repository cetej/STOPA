---
name: project-sweep
description: "Use when performing the same operation across all registered projects (NG-ROBOT, ADOBE-AUTOMAT, ZACHVEV, POLYBOT, etc.) — bulk updates, config changes, dependency audits, skill syncs. Reads project registry from ~/.claude/memory/projects.json. Trigger on 'sweep all projects', 'project sweep', 'across all projects', 'všechny projekty'. Do NOT use for single-project tasks (/orchestrate), single-project cleanup (/sweep), or cross-project improvement routing (/improve)."
argument-hint: [operation description] [--dry-run]
tags: [orchestration, devops]
phase: meta
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

- Do not auto-commit, push, or delete anything without user confirmation — multi-project operations have amplified blast radius, and an unintended commit in the wrong project can be difficult to reverse
- Do not modify files in other projects without explicit approval — cross-project changes bypass per-project review gates and may violate project-specific constraints
- If a project path doesn't exist, skip it and note in results
- If an operation fails for one project, continue with others
- Rate limit: max 8 parallel agents (one per project)

<!-- CACHE_BOUNDARY -->

## Anti-Rationalization Defense

| Rationalization | Why Wrong | Do Instead |
|---|---|---|
| "I found uncommitted changes in NG-ROBOT — I'll commit them to keep things clean" | Committing without explicit per-project approval is forbidden; multi-project blast radius means one wrong commit can corrupt several repos | Report the uncommitted changes in the sweep table and propose the commit as a follow-up action for the user to approve |
| "The operation failed for one project so I'll stop the whole sweep" | Partial failure is expected in multi-project sweeps; aborting wastes results from successfully checked projects | Continue with remaining projects, collect all results, and report failures at the end with details |
| "8+ projects are registered so I'll run them sequentially to avoid overload" | Sequential execution is slower with no safety benefit; the 8-agent cap is already defined in Safety Rules | Run all active projects in parallel up to the 8-agent limit; batch if more than 8 |
| "I'll skip writing results to state.md since the output is already visible in the chat" | Chat output is ephemeral; state.md is the persistent record used by /status and future sessions | Always overwrite the "Last sweep" section of state.md with the current results, regardless of chat visibility |
| "The user didn't specify an operation so I'll ask what they want" | Default operation is explicitly defined as `health` — asking is unnecessary friction | Default to `health` sweep and note the default in the output header |

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
