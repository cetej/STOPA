---
date: 2026-03-27
type: bug_fix
severity: critical
component: general
tags: [playwright, mcp, chrome, downloads, claude-desktop, security]
---

# Playwright MCP v Claude Desktop unáší Chrome downloads

## Problém
Playwright MCP server (`@playwright/mcp@latest`) nakonfigurovaný v Claude Desktop
přesměruje VŠECHNY downloads z Chrome profilu, ke kterému se připojí, do své
temp složky `%LOCALAPPDATA%/Temp/playwright-artifacts-*/`. Soubory jsou uloženy
bez přípony s UUID názvy — uživatel je nemůže najít, otevřít ani identifikovat.

Chrome přitom ukazuje soubory v historii stahování, ale "Otevřít složku" nefunguje
a nastavení "vždy se ptát kam uložit" je ignorováno.

## Příčina
Playwright MCP se připojí k existující Chrome instanci a převezme kontrolu nad
download handlerem. Toto je **jiné chování** než Python Playwright knihovna
(`playwright` pip package), která spouští vlastní browser instanci.

## Řešení
1. Odstraněn Playwright MCP z `claude_desktop_config.json`
2. Zachráněno 11 souborů (178 MB) z temp složky do Downloads
3. "Claude in Chrome" MCP je lepší alternativa (neunáší downloads)

## Anti-pattern: NIKDY nedávat Playwright MCP do Claude Desktop
- Claude Desktop Playwright MCP = připojení k uživatelovu Chrome = side-effects
- Claude Code Playwright MCP v `settings.local.json` = vlastní instance = OK
- Python Playwright v projektech (cms_aqua_publisher.py) = vlastní instance = OK
