---
date: 2026-03-25
type: best_practice
severity: high
component: workflow
tags: [autoloop, batch-edit, approval-fatigue, python]
summary: "Editing 30+ files via Read/Edit causes approval fatigue. Use Python batch scripts with --dry-run for bulk mechanical changes."
source: auto_pattern
---

## Problém
Editing 30+ files via Read→Edit tool cycle requires 60+ permission approvals. User finds this extremely annoying ("approval fatigue").

## Root Cause
Edit tool requires Read first, each call needs user approval in non-auto mode. For bulk mechanical changes this is wasteful.

## Reseni
Use single Python script via Bash tool for batch edits:
- One permission for the whole batch
- Explicit UTF-8 handling (`sys.stdout.reconfigure`, `encoding='utf-8'`)
- Use `re.sub` for regex replacements (not sed — fails on smart quotes on Windows)
- File-level atomicity (read all → modify in memory → write all)

## Prevence
For multi-file mechanical changes (>5 files): always Python batch script, never iterative Edit tool.
For single-file or content-sensitive changes: Edit tool is fine.
