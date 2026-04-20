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

## Output protocol
- Hooks communicate via stdout JSON: `{"decision": "allow"|"block"|"skip", "reason": "..."}`
- Non-JSON stdout is treated as user-visible message
- Exit code 0 = success, non-zero = hook failure (logged but doesn't block)

## Conventions
- One hook per concern (single responsibility)
- `lib/` subdirectory for shared utilities
- Hook names should describe what they do: `panic-detector.py`, `cost-tracker.sh`
- Never modify API keys or secrets in hook scripts
