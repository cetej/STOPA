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

## 4. "Defer" PreToolUse option (CC v2.1.90)

**What it does:** A PreToolUse hook can return `{decision: "defer"}` instead of `allow`/`deny`. The pending permission is stored in the session. When the user later resumes with `--resume`, all deferred permissions are re-presented for approval.

**Use case:** Headless/overnight runs where destructive commands need human sign-off but shouldn't block the entire session. The agent continues working on other subtasks while the destructive one waits.

**Status:** Not implementing now — STOPA doesn't run headless yet. Adopt when remote triggers (`/schedule`) need semi-automated approval.

**Example — defer destructive Bash commands:**

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

**Example — defer external service mutations:**

```json
{
  "matcher": "mcp__github__*",
  "hooks": [
    {
      "type": "command",
      "if": "mcp__github__create_pull_request|mcp__github__merge_pull_request|mcp__github__push_files",
      "command": "echo '{\"decision\":\"defer\",\"reason\":\"GitHub mutation — deferred for review\"}'",
      "timeout": 1
    }
  ]
}
```

This would pause headless execution at destructive/external commands, letting a human resume with `--resume`.

## 5. Marketplace offline resilience (CC v2.1.90)

**New env var:** `CLAUDE_CODE_PLUGIN_KEEP_MARKETPLACE_ON_FAILURE=1`

When set, Claude Code preserves the marketplace plugin cache even if a fetch/install fails (network offline, GitHub down). Without this, a failed marketplace refresh can wipe the local cache, leaving skills unavailable until connectivity returns.

**When to use:**
- CI/CD environments with intermittent network access
- Offline development sessions with previously installed plugins
- Remote triggers running on flaky connections

**How to set (add to settings.json `env` section):**

```json
"env": {
  "CLAUDE_CODE_PLUGIN_KEEP_MARKETPLACE_ON_FAILURE": "1"
}
```

Or set as system environment variable before launching Claude Code.

## Impact summary (updated)

| Change | Effect | Estimated savings |
|--------|--------|-------------------|
| `if:` on learnings-sync | Skip bash spawn for ~95% of Write/Edit calls | ~50ms × N edits/session |
| `if:` on eval-trigger | Skip bash spawn for ~90% of Write/Edit calls | ~50ms × N edits/session |
| PermissionDenied hook | Log auto-mode denials + auto-retry read-only tools | Better autonomy in auto mode |
| TaskCreated hook | Budget + sprawl warnings on task creation | Prevents runaway orchestration |
| Defer PreToolUse | Pause headless runs at destructive commands | Enables overnight autonomous runs |
| Marketplace offline cache | Keep plugins available when network fails | Prevents skill loss in offline mode |
