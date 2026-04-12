---
name: Agent-friendly CLI patterns
description: Design patterns for building CLIs that AI agents can use effectively — applies to skill design, MCP tools, and any CLI we build
type: reference
---

## Core patterns for agent-consumable CLIs

### Non-interactive by default
- Every input as a flag, interactive mode only as fallback for missing flags
- `--yes` / `--force` to skip confirmations
- Agents can't press arrow keys or answer prompts mid-execution

### Discoverability via progressive --help
- Top-level shows subcommands only, each subcommand has own `--help`
- Every `--help` includes concrete examples (agents pattern-match off examples faster than descriptions)

### Structured output
- `--output json` / `--format json` on every data-returning command
- Auto-detect `isatty()` — strip ANSI colors/spinners when piped
- Stable output schemas — don't rename fields between releases

### Predictable structure
- Consistent pattern: `resource + verb` (e.g., `service list`, `deploy list`, `config list`)
- Return data on success: IDs, URLs, durations — not just "done"

### Error handling
- Fail fast with actionable errors: show correct invocation + available values
- Distinct exit codes: 0=success, 1=error, 2=invalid args, 3=partial
- Don't exit 0 on failure with "Error:" in stdout

### Safety & idempotency
- `--dry-run` for destructive actions (preview what would happen)
- Commands idempotent by default (retry-safe)
- `--timeout` flag — agents can't Ctrl+C, built-in timeout with clean exit

### Composability
- Accept flags AND stdin (`--stdin`, pipes)
- `--limit`/`--offset` or `--cursor` for pagination (don't dump 10K results)
- Output parseable for chaining: `--tag $(mycli build --output tag-only)`

## How to apply in STOPA

1. **Skill output standardization**: Skills are "CLIs for agents" — consider structured exit signals (SUCCESS/FAIL/PARTIAL) and machine-readable output sections
2. **Dry-run for destructive skills**: `/compact`, `/scribe maintenance`, memory archivace could benefit from preview mode
3. **skill-generator**: When creating new skills, check these patterns as a checklist
4. **Any new CLI tool** in STOPA projects: use this as design reference
