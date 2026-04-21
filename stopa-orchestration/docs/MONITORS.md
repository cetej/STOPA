# Background Monitors

The `stopa-orchestration` plugin ships background monitors via the CC v2.1.105+
`monitors/monitors.json` manifest. Each monitor runs a persistent shell command
for the lifetime of the session and delivers every stdout line to Claude as a
notification.

Reference: [Plugins reference → Monitors](https://code.claude.com/docs/en/plugins-reference#monitors)

## How monitors differ from hooks

| Aspect | Hooks | Monitors |
|---|---|---|
| Trigger | Event (SessionStart, PostToolUse, …) | Continuous / skill-invoke |
| Process | Runs to completion per event | Long-running (until session end) |
| Output | stdout parsed by CC per-event | Each stdout line = notification |
| Disable mid-session | Hook stops firing | **Monitor keeps running** |

Monitors run unsandboxed at the same trust level as hooks. They require an
interactive CLI session — headless mode and unsupported hosts skip them.

## Registered monitors

### 1. `memory-health` — implemented

- **Trigger**: `always` (session start + plugin reload)
- **Lifecycle**: persistent, 30-minute poll interval
- **Command**: `python "${CLAUDE_PLUGIN_ROOT}/hooks/monitor-memory-health.py"`
- **Use case**: nudges `/sweep` when `.claude/memory/` files or directories
  exceed maintenance thresholds.

**Thresholds** (from `.claude/rules/memory-files.md` + `core-invariants.md`):

| Target | Warn at | Hard ceiling |
|---|---|---|
| `.claude/memory/*.md` line count | 500 | — (invariant, must archive) |
| `.claude/memory/failures/` file count | 40 | 50 |
| `.claude/memory/outcomes/` file count | 80 | 100 |

**Dedup**: hashes the set of findings; re-emits only when the set changes.
Exits silently (code 0, no output) when `.claude/memory/` is not found —
target projects without STOPA memory layout stay quiet.

**Test mode**: `python hooks/monitor-memory-health.py --once` runs a single
check and exits. Used for development; no sleep loop.

---

## Planned monitors (not yet implemented)

### 2. `news-staleness` — planned

- **Trigger**: `always`
- **Lifecycle**: persistent, 6-hour poll
- **Use case**: emit a nudge when the most recent `/watch` scan in
  `.claude/memory/news.md` is older than 7 days.
- **Implementation sketch**: grep last `**Scan log**: ` header date, compare
  to today, emit line if delta > 7 days. Dedupe on delta-bucket (emit once
  per 7→8→9… day transition).

### 3. `harness-adoption-tracker` — planned

- **Trigger**: `always`
- **Lifecycle**: persistent, 24-hour poll
- **Use case**: notify when multi-session harnesses in target projects
  stagnate (no progress marker updates in 72h while harness is active).
- **Implementation sketch**: scan registered project directories for
  `progress.md` + check mtime + last completed feature. Requires project
  registry pointer via `${user_config.project_registry_path}`.

### 4. `budget-daily-limit` — planned

- **Trigger**: `always`
- **Lifecycle**: persistent, hourly poll
- **Use case**: emit a warning when daily budget consumption in
  `.claude/memory/budget.md` crosses configurable thresholds (75%, 90%).
- **Implementation sketch**: parse current-day subtotal from budget.md,
  compare to `${user_config.daily_budget_limit}`, emit on threshold
  crossings. One-shot per threshold (don't spam once crossed).

### 5. `failures-accumulation` — planned

- **Trigger**: `on-skill-invoke:orchestrate`
- **Lifecycle**: activates only once `/orchestrate` is dispatched
- **Use case**: tail `.claude/memory/failures/` for new files during
  orchestration and surface them to the orchestrator immediately (without
  waiting for the next session).
- **Implementation sketch**: Python watchdog-style loop on
  `failures/` directory; emit filename + failure_class on each new file.

### 6. `recipe-completion` — planned

- **Trigger**: `on-skill-invoke:orchestrate`
- **Lifecycle**: persistent after trigger
- **Use case**: when a YAML recipe writes `recipes/run-<id>/status.json`,
  stream `complete`/`failed` states to Claude in real time.
- **Implementation sketch**: inotify-like poll on `recipes/run-*/status.json`
  mtime changes.

---

## Authoring new monitors

1. Create `stopa-orchestration/hooks/monitor-<name>.py` (Python 3, UTF-8, stdlib only).
2. **Emission rule**: print ONE line per actionable event. Dedupe aggressively —
   every stdout line becomes a notification in Claude's session.
3. **Silent exit**: when preconditions are missing (e.g., no memory dir, no
   registry), exit 0 with no output. Do not print warnings to stderr that would
   show up in plugin load diagnostics as errors.
4. **Poll interval**: for non-event-driven monitors, sleep ≥ 5 min between
   checks. Shorter intervals consume CPU without user benefit.
5. Register in `monitors/monitors.json` with `name`, `command`, `description`,
   and optionally `when` (default `always`, alternatives: `on-skill-invoke:<skill>`).
6. Test with `--once` flag locally, then install the plugin and verify the
   monitor appears in the session task panel.
7. Document here under "Registered monitors" with trigger, lifecycle, thresholds.

## Limitations

- **Disabling plugin mid-session does not stop running monitors.** They exit
  only at session end.
- **Non-interactive sessions skip monitors.** Do not rely on monitors for
  CI/scheduled-task paths.
- **Version gate**: requires Claude Code v2.1.105 or later. Older versions
  silently ignore the `monitors` manifest key.
- **Notifications are opaque**: Claude sees each line as a notification but
  there is no structured event channel — format your output for human
  readability.
