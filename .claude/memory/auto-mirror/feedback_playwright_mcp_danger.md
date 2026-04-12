---
name: Playwright MCP hijacks Chrome downloads
description: Never add Playwright MCP to Claude Desktop — it hijacks user's Chrome downloads to a temp folder
type: feedback
---

NIKDY nepřidávat Playwright MCP (`@playwright/mcp`) do ŽÁDNÉHO configu — ani Claude Desktop, ani Claude Code globální/projektový.

**Why:** Playwright MCP se připojí k uživatelovu Chrome a přesměruje VŠECHNY downloads do temp složky bez přípony. Uživatel pak nemůže najít stažené soubory a Chrome ignoruje nastavení download cesty. Incident z 2026-03-27: stovky MB souborů uneseny, problém trval 20+ hodin než byl odhalen. Původní diagnostika byla chybná (identifikován jen Claude Desktop config, ale hlavní viník byl globální `~/.claude/settings.json` pro Claude Code).

**How to apply:**
- NIKDY Playwright MCP — ani do `settings.json`, ani do `settings.local.json`, ani do `claude_desktop_config.json`
- Pro browser automatizaci: použít "Claude in Chrome" MCP (neinterceptuje downloads)
- Python Playwright v projektech (pip package): OK — spouští vlastní browser instanci
