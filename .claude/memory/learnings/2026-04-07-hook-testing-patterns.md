---
date: 2026-04-07
type: best_practice
severity: medium
component: hook
tags: [hook, testing, development, debugging]
summary: "Hook testing patterns: dry-run via env var, isolated testing with mock input JSON, production debugging via hook-errors.log and activity-log."
source: auto_pattern
uses: 1
harmful_uses: 0
successful_uses: 0
confidence: 0.9
verify_check: "Glob('.claude/hooks/*.py') → 1+ matches"
related: [2026-04-16-hook-cwd-anchor-pattern.md]
---

## Hook Testing Patterns

### 1. Isolated Hook Testing

Hooks receive context via stdin (JSON) and environment variables. Test individually:

```bash
# Simulate PostToolUse for a Write tool
echo '{"tool_name":"Write","tool_input":{"file_path":"test.py","content":"x=1"},"tool_output":"ok"}' | python .claude/hooks/acceptance-gate.py

# Simulate UserPromptSubmit
echo '{"prompt":"fix the bug in auth.py"}' | python .claude/hooks/skill-suggest.py
```

### 2. Dry-Run Mode

Some hooks support `DRY_RUN=1` or `--dry-run` to skip side effects:
- `tool-gate.py`: Set `STOPA_TOOL_GATE=log` (vs `enforce`) to log without blocking
- `permission-auto-approve.sh`: Always outputs decision to activity log
- Most memory hooks: check for file existence before write, safe to run on empty memory

### 3. Debugging Active Hooks

- **Activity log**: `.claude/hooks/lib/activity-log.jsonl` — every tool call logged
- **Hook errors**: Check stderr in Claude Code output (appears as system-reminder)
- **Trace files**: `.claude/traces/` — session traces from trace-capture.py and session-trace.py
- **Permission log**: permission-denied-logger.sh logs all denied permissions

### 4. Common Development Workflow

1. Edit hook in `.claude/hooks/`
2. Test with mock stdin JSON (see above)
3. Start new Claude Code session to trigger SessionStart hooks
4. Check activity log for expected entries
5. If hook writes to memory: verify with `python .claude/hooks/memory-integrity-check.py`

### 5. Hook vs Plugin Distribution

| Aspect | Local hooks (.claude/hooks/) | Plugin hooks (stopa-orchestration/hooks/) |
|--------|------------------------------|------------------------------------------|
| Count | 70+ hooks | 24 hooks (curated subset) |
| Testing | Direct, immediate | Requires plugin install |
| Updates | Edit and restart session | Re-sync via sync-orchestration.sh |
| Config | .claude/settings.json | hooks.json in plugin |

Plugin hooks are a curated subset — not all local hooks are distributed. Development hooks (autodream, auto-compound-agent, mid-session-extract) stay local.
