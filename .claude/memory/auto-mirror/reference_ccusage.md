---
name: ccusage token tracking
description: ccusage CLI and MCP server for real-time Claude Code token usage tracking — integrated into /budget skill
type: reference
---

## ccusage — Token Usage Tracker

**CLI**: `npx ccusage@latest` — reads local JSONL logs, zero config
**MCP**: `@ccusage/mcp@latest` — added to global `~/.claude/settings.json` as MCP server

### Key Commands
```bash
npx ccusage@latest daily --json          # Daily totals + model breakdown
npx ccusage@latest blocks --json         # 5-hour billing windows + burn rate
npx ccusage@latest session --json        # Per-project session costs
npx ccusage@latest monthly --json        # Monthly aggregates
npx ccusage@latest daily --since YYYYMMDD --until YYYYMMDD --json  # Date range
```

### MCP Tools (6 total)
`daily`, `session`, `monthly`, `blocks`, `codex-daily`, `codex-monthly`

### Integration
- `/budget` skill uses ccusage CLI via Bash for real data
- MCP server available for other tools/sessions via `~/.claude/settings.json`

### Companion Tool
**claude-monitor** (`pip install claude-monitor`) — real-time terminal monitor with burn rate, progress bars. Heavier (numpy, pydantic). Good for split-terminal watching during expensive sessions.
