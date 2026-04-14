---
id: T-YYYY-MM-DD-NNN
created: YYYY-MM-DD
priority: low | medium | high | critical
project: "project path (e.g., C:/Users/stock/Documents/000_NGM/NG-ROBOT)"
project_name: "short name (e.g., NG-ROBOT)"
status: pending | in_progress | done | failed | blocked
assigned_to: koder
created_by: stopa
---

# Task: <short title>

## What

<Clear description of what needs to be done. Be specific — file paths, function names, expected behavior.>

## Why

<Context: why this task exists. Bug report reference, user request, automated detection.>

## Acceptance Criteria

- [ ] <Specific, verifiable criterion>
- [ ] <Another criterion>
- [ ] Tests pass (or syntax check if no tests)
- [ ] No regressions in existing functionality

## Context

### Relevant Files
- `path/to/main/file.py` — <what's relevant about it>
- `path/to/test/file.py` — <existing tests>

### Prior Attempts (if any)
- <What was tried before and why it failed>

### Learnings to Apply
- <Reference to relevant .claude/memory/learnings/ files>

## Constraints

- Budget: <light | standard> (max agents: <N>)
- Don't change: <files or APIs that must not be modified>
- Dependencies: <don't install new deps | specific dep allowed>

## Outcome Location

Write outcome to: `.claude/memory/outcomes/<date>-koder-<result>-<slug>.md`
