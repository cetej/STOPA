---
name: project_bonanza
description: BONANZA — Claude AI trading bot (trailing stop, copy trading, wheel strategy) at 000_NGM/BONANZA
type: project
---

BONANZA je automatizovaná obchodní platforma s Claude AI pro paper + live trading US akcií a opcí z EU/ČR.

**Repo:** `C:/Users/stock/Documents/000_NGM/BONANZA/`
**Stack:** Python 3.12, alpaca-py, Lumibot, httpx, pydantic-settings, SQLite, Rich
**MCP:** Alpaca MCP v2 (trading+options), Alpha Vantage (technikálie), Financial Datasets (fundamenty)
**Broker:** Alpaca (paper), Interactive Brokers (live EU)
**Smart money:** Lambda Finance API (congressional trades)

**Why:** Inspirováno tutoriálem Samin Yasar. Research brief v `STOPA/outputs/trading-bot-research.md`.

**How to apply:** Při práci na BONANZA čti CLAUDE.md a docs/ROADMAP.md v BONANZA projektu.

**Status (2026-04-13):** Fáze 0+1 hotové (scaffold + broker wrapper). Uživatel ještě nemá Alpaca účet.
**Next:** Uživatel založí Alpaca účet → test MCP connection → Sprint 2 (trailing stop).
