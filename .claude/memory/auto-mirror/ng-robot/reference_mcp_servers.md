---
name: MCP servery v Claude Code
description: Přehled nainstalovaných MCP serverů a jejich účel v NG-ROBOT workflow
type: reference
---

## Nainstalované MCP servery (~/.claude/settings.json)

| Server | Balíček | Účel |
|--------|---------|------|
| brave-search | `@modelcontextprotocol/server-brave-search` | Web search (fáze 3, 8) |
| playwright | `@playwright/mcp@latest` | Browser automation, video stahování |
| context7 | `@upstash/context7-mcp` | Aktuální dokumentace knihoven/API |
| github | `@modelcontextprotocol/server-github` | GitHub integrace |
| Windows-MCP | `@modelcontextprotocol/server-windows` | Windows systémové operace |
| scheduled-tasks | `@modelcontextprotocol/server-scheduled-tasks` | Plánované úlohy |
| sequential-thinking | `@modelcontextprotocol/server-sequential-thinking` | Strukturované krokové uvažování pro lepší plánování a brainstorm (přidáno 2026-03-16) |

## Status line

Konfigurováno v `~/.claude/statusline-command.sh` — zobrazuje model, git branch, % kontextu.
