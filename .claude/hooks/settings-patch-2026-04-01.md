# Settings.json Patch — CC v2.1.89 Hook Improvements

Apply manually to `.claude/settings.json` (config-protection blocks automated edits).

## 1. Add `if:` guards to Write|Edit PostToolUse hooks

Find this block in PostToolUse → matcher `Write|Edit|MultiEdit`:

```json
{
  "type": "command",
  "command": "bash .claude/hooks/learnings-sync.sh",
  "timeout": 5,
  "statusMessage": ""
}
```

Replace with:

```json
{
  "type": "command",
  "if": "Write(**/learnings/**)|Edit(**/learnings/**)",
  "command": "bash .claude/hooks/learnings-sync.sh",
  "timeout": 5,
  "statusMessage": ""
}
```

---

Find:

```json
{
  "type": "command",
  "command": "bash .claude/hooks/eval-trigger.sh",
  "timeout": 3,
  "statusMessage": ""
}
```

Replace with:

```json
{
  "type": "command",
  "if": "Write(**SKILL.md)|Edit(**SKILL.md)|Write(**/skills/**)|Edit(**/skills/**)",
  "command": "bash .claude/hooks/eval-trigger.sh",
  "timeout": 3,
  "statusMessage": ""
}
```

## 2. Add PermissionDenied hook (new in v2.1.89)

Add this new top-level section after `StopFailure`:

```json
"PermissionDenied": [
  {
    "matcher": "",
    "hooks": [
      {
        "type": "command",
        "command": "bash .claude/hooks/permission-denied-logger.sh",
        "timeout": 3,
        "statusMessage": ""
      }
    ]
  }
]
```

## 3. Add TaskCreated hook (new in v2.1.89)

Add this new top-level section after `TaskCompleted`:

```json
"TaskCreated": [
  {
    "matcher": "",
    "hooks": [
      {
        "type": "command",
        "command": "bash .claude/hooks/task-created-gate.sh",
        "timeout": 5,
        "statusMessage": "Checking task budget..."
      }
    ]
  }
]
```

## Impact summary

| Change | Effect | Estimated savings |
|--------|--------|-------------------|
| `if:` on learnings-sync | Skip bash spawn for ~95% of Write/Edit calls | ~50ms × N edits/session |
| `if:` on eval-trigger | Skip bash spawn for ~90% of Write/Edit calls | ~50ms × N edits/session |
| PermissionDenied hook | Log auto-mode denials + auto-retry read-only tools | Better autonomy in auto mode |
| TaskCreated hook | Budget + sprawl warnings on task creation | Prevents runaway orchestration |

## Notes on `defer` (PreToolUse)

The `defer` permission is for headless mode (`-p --resume`). Not implementing now because STOPA doesn't run headless yet. When remote triggers need semi-automated approval:

```json
{
  "matcher": "Bash",
  "hooks": [
    {
      "type": "command",
      "if": "Bash(rm *)|Bash(git push*)|Bash(git reset*)",
      "command": "echo '{\"decision\":\"defer\",\"reason\":\"Destructive command — waiting for human approval\"}'",
      "timeout": 1
    }
  ]
}
```

This would pause headless execution at destructive commands, letting a human resume with `-p --resume`.
