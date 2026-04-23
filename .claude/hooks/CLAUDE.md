# Hooks Development Rules

## Python hooks
- Encoding: UTF-8 everywhere, `sys.stdout.reconfigure(encoding='utf-8', errors='replace')`
- Paths: `pathlib.Path()`, never hardcoded backslashes
- Windows: retry logic for file locking (antivirus), `errors='replace'` for I/O
- No `print()` for debugging in production — use `logging`

## Registration
Hooks must be registered in `.claude/settings.json` under the `hooks` key.
Format: event type -> array of hook configs with `command` and optional `timeout`.

## Hook events
- `SessionStart` — session initialization (memory brief, context injection, improvement notifications)
- `UserPromptSubmit` — after user sends a message (associative recall, auto-scribe)
- `PreToolUse` / `PostToolUse` — before/after tool execution
- `PermissionRequest` — before tool runs that need user permission (auto-approve/ask)
- `PermissionDenied` — fires when a permission prompt is denied (useful for `/less-permission-prompts` feedback loop; not yet wired)
- `PreCompact` / `PostCompact` — around context compaction (flush scratchpad, auto-checkpoint)
- `TaskCreated` — when a new sub-agent Task is spawned (budget gate, team tracking)
- `TeammateIdle` — when a named sub-agent has no pending work (cleanup, re-task)
- `Stop` — session end (normal completion)
- `StopFailure` — session stopped due to API error or unrecoverable failure (recovery guidance, notify)
- `Notification` — system notifications
- `CwdChanged` — fires when the working directory changes (reactive env mgmt: direnv reload, project detect)
- `FileChanged` — fires when a watched file changes (reactive env mgmt: reload config, re-index)
- `Elicitation` — intercepts structured input requests from the model (can inject defaults)
- `ElicitationResult` — fires after the user responds to an elicitation prompt

### CC v2.1.x new events — categorization

| Event | Category | STOPA status | Purpose |
|-------|----------|--------------|---------|
| `CwdChanged` | workflow | not wired | Reactive env (direnv, auto-profile) |
| `FileChanged` | workflow | not wired | Reactive reload on watched-file edits |
| `TaskCreated` | workflow | wired (`task-created-gate.sh`) | Budget gate on sub-agent spawn |
| `PostCompact` | memory | wired (`post-compact.sh`) | Checkpoint reminder post-compaction |
| `StopFailure` | safety+tracing | wired (`stop-failure.sh` + `stop-failure-logger.py`) | API error recovery + failure record |
| `PermissionDenied` | tracing | catalogued only | Feedback loop for `/less-permission-prompts` |
| `Elicitation` / `ElicitationResult` | workflow | not wired | Intercept/log structured input responses |

Categories: `safety` (block/deny), `memory` (persist/consolidate), `tracing` (observe), `workflow` (coordinate), `notification` (surface).

## Output protocol
- Hooks communicate via stdout JSON: `{"decision": "allow"|"block"|"skip", "reason": "..."}`
- Non-JSON stdout is treated as user-visible message
- Exit code 0 = success, non-zero = hook failure (logged but doesn't block)

## Conventions
- One hook per concern (single responsibility)
- `lib/` subdirectory for shared utilities
- Hook names should describe what they do: `panic-detector.py`, `cost-tracker.sh`
- Never modify API keys or secrets in hook scripts
