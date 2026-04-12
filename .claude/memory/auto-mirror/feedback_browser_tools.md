---
name: Browser tool selection guide
description: When to use agent-browser vs dev-browser vs Claude in Chrome vs WebFetch — decision matrix. agent-browser is the primary agent CLI tool.
type: feedback
---

## Browser tool rozhodovací matice

| Situace | Nejlepší nástroj | Proč |
|---|---|---|
| **AI agent ovládá browser (e2e testing, setup, scanning)** | **agent-browser** | CLI pro agenty: snapshot→refs→act, Rust daemon (nízká latence), Electron apps, 80+ příkazů, nízká tokenová zátěž |
| **Electron apps** (Discord, VSCode, Slack) | **agent-browser** | Jediný nástroj s CDP podporou pro Electron |
| **E2E testing aplikace** | **agent-browser** | Deterministic refs z accessibility tree, named sessions, domain allowlists |
| **Skenování/čtení přihlášené stránky** | **agent-browser** nebo **dev-browser --connect** | agent-browser: pokud máš nainstalovaný; dev-browser: pro připojení k existujícímu Chrome |
| Bulk akce přes víc tabů (mute, extract, check) | **dev-browser --connect** | Loop v kódu přes N tabů, session cookies |
| Scraping veřejné stránky (JS-rendered) | **dev-browser --headless** | Playwright API, levnější než MCP tool calls |
| Jednoduchý fetch veřejné stránky | **WebFetch** | Nejjednodušší, žádný browser |
| Interaktivní prohlížení s uživatelem (vizuální feedback) | **Claude in Chrome** | Uživatel vidí co se děje |
| Preview vlastní aplikace (localhost) | **Preview MCP** | Integrovaný, hot reload |
| Google Sheets data | **Google Sheets API / MCP** | Sheets renderuje canvas, ne DOM |

## Požadavky pro dev-browser --connect

Chrome musí běžet s `--remote-debugging-port=9222` nebo mít zapnutý remote debugging v `chrome://inspect/#remote-debugging`.

## Důležité poznatky z testování

- Persistent pages: stránka přežije mezi skripty (nemusí se re-navigovat)
- QuickJS sandbox: žádné `require()`, `fetch()`, `fs` — jen Playwright API + console
- Soubory jen do `~/.dev-browser/tmp/`
- Google Sheets nefunguje přes innerText (canvas rendering)
- YouTube: `video.pause()` zastaví obraz, ale pro zvuk nutné i `video.muted = true` + `volume = 0`

**Why:** Testováno 2026-03-26 (dev-browser). agent-browser přidán 2026-04-04 — uživatel potvrdil jako "nejlepší CLI tool pro agenty". Nízká tokenová zátěž, Electron support, snapshot→refs→act pattern.

**Radar update 2026-04-05:** agent-browser v0.24.1 (pre-1.0, 27K stars). Claim "82% fewer tokens" pochází od třetího testera (Pulumi blog), ne od Vercelu — platí jen pro jednoduché scénáře. **Showstopper: issue #1155 — nefunguje v CC sandboxu** (Unix socket blokovaný). Status: WATCH, neinstalovat dokud nebude 1.0 + sandbox fix. Naše sada (Claude in Chrome + WebFetch + dev-browser) plně pokrývá všechny use-cases.

**How to apply:** Pro agent-driven browser workflows (e2e testing, mass scanning, Electron apps) → agent-browser CLI jako default. dev-browser pro připojení k existujícímu uživatelskému Chrome. Claude in Chrome jen pro interaktivní scénáře s vizuálním feedbackem.

## Workflow pro zapnutí dev-browser --connect

1. Zkusit `dev-browser --connect` — pokud Chrome běží s debugging, funguje rovnou
2. Pokud port 9222 neodpovídá → požádat uživatele o souhlas a spustit `scripts/chrome-debug.bat`
3. Chrome se restartne s `--remote-debugging-port=9222` a obnoví taby (~3s)
4. Po práci volitelně spustit `scripts/chrome-normal.bat` pro návrat do normálu
5. NIKDY nerestartovat Chrome bez souhlasu uživatele
