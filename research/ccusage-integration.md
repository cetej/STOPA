# ccusage MCP Server Integration

## What
[ccusage](https://github.com/ryoppippi/ccusage) — CLI + MCP server for tracking real $ costs from Claude Code JSONL logs.

## Setup

### 1. Install
```bash
npm install -g ccusage
# or use npx ccusage
```

### 2. MCP Server mode
Add to Claude Code settings (`~/.claude/settings.json`):
```json
{
  "mcpServers": {
    "ccusage": {
      "command": "npx",
      "args": ["-y", "@ccusage/mcp"]
    }
  }
}
```

### 3. CLI usage
```bash
npx ccusage daily     # Daily token usage + costs
npx ccusage monthly   # Monthly aggregated
npx ccusage session   # Per-conversation session
```

## Integration with STOPA /budget

The `/budget` skill tracks agent spawns and orchestration costs in `.claude/memory/budget.md`.
ccusage provides ground-truth $ costs from actual API usage.

Potential integration:
- `/budget` reads ccusage data (via MCP) to reconcile estimated vs actual costs
- Hook: periodic cost check could warn when daily spend exceeds threshold
- Dashboard: ccusage web UI at ccusage.com shows visual reports

## Status
- Documented as reference, not yet integrated into budget skill
- Decision: install when user wants real $ tracking, current budget.md is sufficient for agent orchestration cost control
