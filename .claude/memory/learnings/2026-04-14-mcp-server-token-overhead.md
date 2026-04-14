---
date: 2026-04-14
type: best_practice
severity: high
component: orchestration
tags: [tokens, mcp, cost-optimization]
summary: Each connected MCP server loads ~18K tokens per message into context. Disconnect unused servers per session. Prefer CLI tools over MCP where equivalent.
source: external_research
uses: 0
successful_uses: 0
harmful_uses: 0
confidence: 0.7
maturity: draft
verify_check: "manual"
---

## MCP Server Token Overhead

Every connected MCP server loads ALL its tool definitions into context on EVERY message. A single server can cost ~18,000 tokens per message — invisible overhead.

**Rule**: Audit MCP connections at session start. Disconnect servers not needed for current task.

**Principle**: Where a CLI equivalent exists, prefer CLI over MCP. CLI outputs go through RTK filtering (60-90% savings). MCP tool definitions are uncompressible overhead.

**Example**: Google Calendar CLI vs Google Calendar MCP — CLI is faster and cheaper.

**STOPA context**: We already have many MCP servers (GitHub, Gmail, Calendar, Brave, Playwright, Chrome, Context7, filesystem, Telegram, scheduled-tasks, YouTube). Not all are needed every session. A per-session audit could save 50-100K tokens over a long session.

**Source**: Token management vlog (2026-04-14).
