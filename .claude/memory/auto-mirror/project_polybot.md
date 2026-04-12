---
name: project_polybot
description: POLYBOT — MCP server pro paper trading na Polymarket prediction markets, Claude jako analytik + trader
type: project
---

POLYBOT je Python MCP server pro automatizovaný paper trading na Polymarket. Claude analyzuje markety, odhaduje pravděpodobnosti, paper-traduje a měří kalibraci.

**Why:** Prediction markets jako signálový zdroj + testbed pro kalibraci LLM predikcí. Phase 1 = paper trading, Phase 2 = real execution.

**How to apply:**
- Repo: `github.com/cetej/POLYBOT`, adresář `C:/Users/stock/Documents/000_NGM/POLYBOT`
- Stack: Python 3.12+, FastMCP, httpx, torch+transformers, SQLite, Pydantic
- Architektura: Claude → MCP Protocol → POLYBOT MCP Server → Polymarket Gamma/CLOB API
- Phase 1: read-only, paper trading; Phase 2: live execution
- Roadmap v docs/ROADMAP.md: 5 sprintů (Binance WS, divergence model, auto-loop, real execution, market making)
- Risk: Quarter-Kelly sizing, min edge 8%, circuit breakers (-5% daily, -20% drawdown)
- Integrace s ORAKULUM: přímý Python import pro encoding, correlation, prediction; markets adapter sdílený
- **Dev tooling:** MCporter (github.com/steipete/mcporter) — CLI MCP client pro testování/debug MCP serverů bez Claude Desktop. Headless, OAuth, JSON schema. Relevantní pro CI/CD a lokální vývoj POLYBOT MCP endpointů.
- **Možné rozšíření:** Web scraping modul pro standalone Python agenty — `trafilatura` nebo `jina.ai/reader` pro fetch čistého textu z URL bez závislosti na CC tools. Relevantní pro market news fetching mimo agentic loop.
