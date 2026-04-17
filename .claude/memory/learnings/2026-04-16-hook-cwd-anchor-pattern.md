---
date: 2026-04-16
type: bug_fix
severity: medium
component: hook
tags: [bash-hooks, cwd-dependency, path-anchoring, silent-failure]
summary: "Bash hooks must anchor paths via SCRIPT_DIR/PROJECT_ROOT, never use relative paths like '.claude/memory/'. CWD at hook invocation is unpredictable — STOPA's raw-capture.sh generated a nested anomaly tree (.claude/memory/learnings/.claude/memory/raw/) for 15+ days before detection because it used MEMORY_DIR='.claude/memory' with no anchor."
source: auto_pattern
uses: 2
harmful_uses: 0
successful_uses: 0
confidence: 1.0
maturity: draft
failure_class: assumption
failure_agent: hook
task_context: {task_class: bug_fix, complexity: low, tier: light}
verify_check: "Grep('SCRIPT_DIR.*pwd', path='.claude/hooks/', glob='*.sh') → 1+ matches"
skill_scope: []
related: [2026-04-15-msys-tmp-path-mismatch.md, 2026-04-07-hook-failure-modes.md, 2026-04-07-hook-testing-patterns.md]
---

## Situation

STOPA's `raw-capture.sh` Stop-hook used `MEMORY_DIR=".claude/memory"` — a relative path with no CWD anchor. When the hook fired from a shell whose CWD was not project root (e.g., a prior `cd .claude/memory/learnings/` left the shell there), the script wrote to `.claude/memory/learnings/.claude/memory/raw/` instead of `.claude/memory/raw/`.

## Detection

Discovered by STOPA audit (2026-04-16) when anomaly directory surfaced with 9 duplicate-but-truncated files:
- `.claude/memory/learnings/.claude/memory/activity-log.md` (423B vs real 7969B)
- `.claude/memory/learnings/.claude/memory/permission-log.md` (790B vs real 15890B)
- `.claude/memory/learnings/.claude/memory/sessions.jsonl` (174B vs real 17651B)
- Plus session captures, observations.jsonl, intermediate/ files

Anomaly tree had mtime 2026-04-16 07:00 — latest instance. Earlier bug invocations silently overwrote or skipped, no error logged.

## Fix Pattern

```bash
#!/usr/bin/env bash
# ALWAYS anchor bash hooks to project root via script location
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
MEMORY_DIR="$PROJECT_ROOT/.claude/memory"
# ... rest of script uses absolute $MEMORY_DIR
```

Applies to any hook that writes files using relative paths. Python hooks have same vulnerability — use `Path(__file__).resolve().parent.parent / "memory"` pattern.

## Why It Matters

1. **Silent failure mode** — hook exits 0, no error surface. Bug persists until someone notices anomaly filesystem
2. **Data fragmentation** — writes go to unexpected locations; legitimate consumers never find the data
3. **Memory pollution** — anomaly trees accumulate; evolve/sweep may accidentally count them as real data
4. **Cross-session amplification** — every Stop-hook invocation from wrong CWD worsens the mess

## Prevention

- Code review checklist: any `MEMORY_DIR=` or `Path(".claude/...")` without anchor = RED FLAG
- Hook sanity check: `find .claude/memory/learnings -type d -name '.claude'` should return 0
- Test hooks from multiple CWDs: project root, `.claude/`, subdirectory — all should write to same paths

## Related

- STOPA hooks use absolute paths in settings.json commands (`bash C:/.../hook.sh`) — this is correct. The bug is INSIDE the script, not in how it's invoked.
- 25+ other STOPA hooks should be audited for same pattern (grep `Path("\.claude` or `="\.claude`).
