# Background Monitors

Plugin monitors let `stopa-orchestration` watch files, logs, or polled
state in the background and notify Claude as events arrive. They use the
`monitors` manifest key introduced in Claude Code **v2.1.105** and share
the trust level of hooks (no sandbox, interactive CLI sessions only).

- Config: [`.claude-plugin/plugin.json`](../.claude-plugin/plugin.json) → `"monitors": "./monitors/monitors.json"`
- Catalogue: [`monitors/monitors.json`](../monitors/monitors.json)
- Spec: [code.claude.com/docs/en/plugins-reference#monitors](https://code.claude.com/docs/en/plugins-reference)

Each stdout line emitted by a monitor command becomes one notification in
the session, so monitor scripts keep output terse and action-oriented.

## Lifecycle

| `when` value                  | Starts                                         | Stops             |
| :---------------------------- | :--------------------------------------------- | :---------------- |
| `"always"` (default)          | Session start + on plugin reload               | Session end       |
| `"on-skill-invoke:<skill>"`   | First dispatch of the named skill this session | Session end       |

Disabling the plugin mid-session does **not** stop already-running
monitors; they stop when the session ends.

## Catalogue

| Monitor            | Status        | Trigger (`when`) | Purpose |
| :----------------- | :------------ | :--------------- | :------ |
| `memory-health`    | implemented   | always           | Flags memory files over 500 lines, `failures/` buildup, `learnings/` growth |
| `news-staleness`   | planned       | always           | Warn when `news.md` last scan is older than 7 days |
| `harness-adoption` | planned       | on-skill-invoke:watch | Track `/harness` adoption across target projects (1/8 as of 2026-04-23) |
| `watch-daily`      | planned       | always           | Replace `scheduled-tasks` cron with a session-local poll of `/watch` sources |
| `budget-health`    | planned       | on-skill-invoke:orchestrate | Daily spend indicator at orchestration start |

Planned monitors are design placeholders only — not wired into
`monitors.json` until they have a concrete use case proven against at
least two sessions of manual observation.

## `memory-health`

```json
{
  "name": "memory-health",
  "command": "python \"${CLAUDE_PLUGIN_ROOT}/hooks/monitor-memory-health.py\"",
  "description": "STOPA memory health (file sizes, failures/learnings buildup)"
}
```

### What it checks

| Check | Threshold | Remediation hint emitted |
| :---- | :-------- | :----------------------- |
| `*.md` file size (excluding `*-archive.md`) | > 500 lines | archive old entries to `<stem>-archive.md` |
| `failures/` buildup | > 40 files | `/sweep` to archive records older than 60 days |
| `learnings/` buildup | > 200 files | `/evolve` to prune low-confidence entries |

Thresholds mirror the hard limits in [`rules/memory-files.md`](../../.claude/rules/memory-files.md).
Archive files (`*-archive.md`) are intentionally skipped — they are the
destination for oversize content, not an issue themselves.

Output is capped at 5 notifications per session; overflow collapses into
a single summary line pointing to `/sweep` for a full audit.

### Script

- Path: [`hooks/monitor-memory-health.py`](../hooks/monitor-memory-health.py)
- Runtime: Python 3, stdlib only, Windows-safe (`pathlib`, UTF-8 reconfig)
- Exit: non-polling, runs once per session then exits
- Side effects: none (read-only filesystem scan)

### MemoryBackend abstraction (ADR 0016/0017)

The script reads the target directory from the `STOPA_MEMORY_DIR`
environment variable; it falls back to `.claude/memory` relative to the
session working directory. It does **not** touch backend-specific files
(`.sqlite`, `.index`, etc.) — it only relies on the filesystem view
(Markdown files + well-known subdirectories like `failures/` and
`learnings/`) that every `MemoryBackend` exposes. If the directory is
missing, the monitor exits silently, making it a no-op in projects that
do not use STOPA memory.

### Overlap with `memory-maintenance.sh`

The existing SessionStart hook [`hooks/memory-maintenance.sh`](../hooks/memory-maintenance.sh)
warns on a hard-coded list of five files at a lower (100-line)
threshold. The `memory-health` monitor is complementary:

| Aspect               | `memory-maintenance.sh` (hook) | `memory-health` (monitor) |
| :------------------- | :----------------------------- | :------------------------ |
| Scope                | 5 specific files               | Every `*.md` in the directory |
| Threshold            | 100 lines (warn) / 500 (crit)  | 500 lines (actionable only) |
| Subdirectories       | none                           | `failures/`, `learnings/` |
| Notification channel | SessionStart stdout            | Plugin monitor (per-line) |

## Adding a new monitor

1. Add a script under `hooks/` (Python stdlib only, UTF-8 stdout, silent
   no-op when targets are missing).
2. Register it in [`monitors/monitors.json`](../monitors/monitors.json)
   with `name`, `command`, `description`, and optional `when`.
3. Use `${CLAUDE_PLUGIN_ROOT}` for script paths — the plugin can be
   installed under arbitrary trees.
4. Update the **Catalogue** table above; promote the row from
   `planned` → `implemented` once a session has exercised it.
5. If the script depends on the memory directory, resolve it via
   `STOPA_MEMORY_DIR` (env var) → `.claude/memory` (cwd fallback); do
   not hard-code `.claude/memory` paths.

## Testing locally

Verify script behavior before enabling the plugin:

```bash
# Real memory (from STOPA repo root)
python stopa-orchestration/hooks/monitor-memory-health.py

# Override target dir
STOPA_MEMORY_DIR=/path/to/other/memory python stopa-orchestration/hooks/monitor-memory-health.py

# Non-STOPA project (should exit silently)
STOPA_MEMORY_DIR=/does/not/exist python stopa-orchestration/hooks/monitor-memory-health.py
```

Once the plugin is enabled in a Claude Code session (v2.1.105+), the
monitor arms automatically at session start and delivers any issue lines
as notifications in the task panel.
