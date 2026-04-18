---
date: 2026-03-27
type: bug_fix
severity: critical
component: general
tags: [playwright, mcp, chrome, downloads, claude-desktop, claude-code, security]
summary: "Playwright MCP hijacks Chrome downloads to temp folder, breaking all browser downloads. NEVER add to Claude Desktop."
source: auto_pattern
maturity: draft
verify_check: "manual"
confidence: 1.0
uses: 1
successful_uses: 0
harmful_uses: 0
---

# Playwright MCP unáší Chrome downloads — post-mortem

## Co se stalo uživateli
Chrome stahoval soubory do neviditelné temp složky (`%LOCALAPPDATA%/Temp/playwright-artifacts-*/`)
místo do Downloads. Soubory bez přípony, s UUID názvy. "Otevřít složku" z historie stahování
nefungovalo. Nastavení "vždy se ptát kam uložit" bylo ignorováno. Trvalo 20+ hodin.

## Skutečná příčina (řetězec)

1. **2026-03-26 ~06:30** — Claude (já) při práci na dev-browser integraci přidal
   Playwright MCP do globálního `~/.claude/settings.json` pro Claude Code.
   Playwright MCP byl zároveň už v `claude_desktop_config.json` pro Claude Desktop.

2. **Playwright MCP při startu** se připojí k uživatelovu Chrome přes DevTools protocol
   a přebírá kontrolu nad download handlerem. Všechny downloads — i ty, které uživatel
   spustí ručně kliknutím — jdou do Playwright temp složky.

3. **Toto běželo nepřetržitě** protože Claude Code session (nebo Claude Desktop)
   drží Playwright MCP proces živý. Dokud běží JAKÁKOLI session s Playwright MCP,
   Chrome downloads jsou přesměrované.

4. **Chrome si drží download handler v paměti** — zabití Playwright procesu nepomůže,
   dokud se Chrome nerestartuje. Proto ani zabití procesů problém nevyřešilo.

## Proč diagnostika trvala tak dlouho

1. Nejdřív jsem myslel, že to způsobuje Azure AD WorkplaceJoined → špatně
2. Pak jsem odstranil Playwright z `claude_desktop_config.json` → nedostatečné
3. Pak jsem podezříval Claude in Chrome extension → červený herink
4. Až nakonec jsem našel Playwright MCP v **globálním** `~/.claude/settings.json`
5. I po odstranění z configu a zabití procesů to nefungovalo → Chrome musel být restartován

## Co bylo potřeba udělat (a co jsem měl udělat hned)

1. Odstranit Playwright MCP ze VŠECH configů najednou:
   - `~/.claude/settings.json` (globální Claude Code)
   - `claude_desktop_config.json` (Claude Desktop)
   - `settings.local.json` ve všech projektech (permissions)
2. Zabít VŠECHNY Playwright node procesy
3. **Restartovat Chrome** (force kill + znovu otevřít)
4. Smazat `playwright-artifacts-*` temp složky

## Collateral damage

- Vystavené tokeny v `claude_desktop_config.json` (GitHub PAT, Brave API key)
   — taky moje chyba z dřívějších sessions, zapsány přímo místo přes env vars
- 200+ MB souborů ztraceno v temp složce bez přípony
- 1+ hodina uživatelova času na diagnostiku problému, který jsem způsobil

## Anti-pattern: NIKDY Playwright MCP

- Playwright MCP (`@playwright/mcp`) = připojení k uživatelovu Chrome = přesměrování downloads
- NIKDY nepřidávat do žádného configu (settings.json, claude_desktop_config.json, settings.local.json)
- "Claude in Chrome" MCP = bezpečná alternativa (neinterceptuje downloads)
- Python Playwright v projektech (`pip install playwright`) = vlastní browser instance = OK
