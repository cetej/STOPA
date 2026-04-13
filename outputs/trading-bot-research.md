# Claude AI Trading Bot — Research Brief

**Date:** 2026-04-13
**Question:** Nejlepší stack pro automatizovanou obchodní platformu s Claude AI (z EU/ČR)
**Scope:** broad (6 domén)
**Sources consulted:** 22

## Executive Summary

Postavit Claude-powered trading bota z EU/ČR je reálné, ale vyžaduje jiný stack než v tutoriálu (Samin Yasar používá Alpaca z USA). Klíčové zjištění:

1. **Alpaca je pro EU zatím nedostupný pro individuální tradery** [VERIFIED][1,2] — akvizice WealthKernel (červenec 2025) otevírá cestu do EU, ale retail API účty pro ČR zatím neexistují. **Doporučení: Interactive Brokers** jako primární broker (dostupný v ČR, plná options podpora, Python API) + Alpaca paper trading pro vývoj.

2. **Alpaca MCP Server v2 je production-ready** [VERIFIED][3] — 61 nástrojů včetně options (Greeks, IV, multi-leg), paper trading defaultně zapnutý, přímá integrace s Claude Desktop/Code.

3. **Congressional copy trading má 45denní zpoždění** [INFERRED][4,5] — STOCK Act povoluje 45 dní na disclosure. Strategie stále funguje (kongresmani drží pozice měsíce/roky), ale není to day trading. Nejlepší API: **Lambda Finance** (free tier 50 calls/měsíc) nebo **Quiver Quantitative** (free delayed, $25/měsíc pro real-time).

4. **Lumibot je nejlepší framework pro wheel strategy** [VERIFIED][6] — nativní Alpaca + IBKR integrace, options backtesting přes ThetaData, stejný kód pro backtest i live. AI agent runtime zabudovaný.

5. **MiFID II se na retail tradery s boty pravděpodobně nevztahuje** [INFERRED][7] — Article 17 cílí na investment firms, ne na individuální investory. Ale pozor: pokud bot obchoduje agresivně, může ČNB klasifikovat aktivitu jako "dealing on own account".

---

## Detailed Findings

### 1. Brokeráže s API — EU/ČR dostupnost

| Broker | EU/ČR | Options | Paper Trading | API kvalita | Cena |
|--------|-------|---------|--------------|-------------|------|
| **Interactive Brokers** | ANO [VERIFIED] | Plná (US + EU opce) | ANO | Komplexní (TWS/Gateway) | Komise od $0.65/kontrakt |
| **Alpaca** | NE (zatím) [VERIFIED][1] | ANO (US only) | ANO | Výborná (REST, MCP) | $0 komise, data $99/měsíc |
| **Tradier** | NE [INFERRED] | ANO (US) | ANO | Dobrá (REST, OAuth) | $0 stocks, $0.35/opce |
| **Tastytrade** | Omezené [UNVERIFIED] | Výborná | ANO | Základní | Nízké poplatky |

**Doporučení pro ČR:**
- **Vývoj + paper trading:** Alpaca (free, nejlepší MCP integrace s Claude)
- **Live trading:** Interactive Brokers (jediný plně funkční v ČR s options + API)
- **Přechod:** Lumibot umožňuje switch brokerů bez přepisu strategie [VERIFIED][6]

**Alpaca EU timeline:** Akvizice WealthKernel [VERIFIED][2] přináší UK/EU licenci. Alpaca v 2025 review zmiňuje expanzi do EU jako prioritu pro 2026 [SINGLE-SOURCE][2]. Pro individuální API účty z ČR zatím žádný potvrzený termín.

### 2. MCP servery pro Claude — finanční data

| MCP Server | Typ | Nástroje | Options | Cena |
|-----------|-----|----------|---------|------|
| **Alpaca MCP v2** [VERIFIED][3] | Trading + data | 61 tools (8 toolsetů) | ANO (Greeks, IV, chains) | Free (paper), data plány |
| **Alpha Vantage MCP** [SINGLE-SOURCE][8] | Data only | 100+ finančních API | Omezená | Free tier 25 calls/den |
| **Financial Datasets MCP** [VERIFIED][9] | Fundamentals | Statements, prices, news | NE | API key required |
| **EODHD MCP** [SINGLE-SOURCE][10] | Data + technikálie | 77 read-only tools | Omezená | Placený |
| **LSEG MCP** [SINGLE-SOURCE][11] | Institutional | Yield curves, FX, bonds | NE | Enterprise |

**Doporučený stack:**
```
Claude Desktop/Code
  ├── Alpaca MCP v2 (trading + market data + options)
  ├── Alpha Vantage MCP (doplňkové fundamenty, technická analýza)
  └── Financial Datasets MCP (financial statements pro analýzu)
```

**Alpaca MCP v2 detaily** [VERIFIED][3]:
- Instalace: `claude mcp add alpaca -- uvx alpaca-mcp-server`
- Env vars: `ALPACA_API_KEY`, `ALPACA_SECRET_KEY`, `ALPACA_PAPER_TRADE=true`
- Toolsety: account, trading, watchlists, assets, stock-data, crypto-data, options-data, corporate-actions
- Paper trading defaultně ON
- V2 je kompletní přepis (FastMCP + OpenAPI) — V1 nekompatibilní

### 3. Smart Money — Congressional Trades

| Služba | API | Free tier | Data freshness | Coverage |
|--------|-----|-----------|---------------|----------|
| **Lambda Finance** [VERIFIED][4] | REST API | 50 calls/měsíc | Hodiny po STOCK Act filing | Senate + House |
| **Quiver Quantitative** [VERIFIED][5] | REST + Python pkg | Delayed data | Near real-time (placený) | Congress + lobbying + contracts |
| **Capitol Trades** [VERIFIED][4] | Žádné veřejné API | Free web | Aktuální | Senate + House od 2012 |
| **Unusual Whales** [INFERRED][12] | Žádné veřejné API | — | Real-time | Congress + options flow |
| **Senate Stock Watcher** [SINGLE-SOURCE][4] | JSON endpoints | Zcela free | Variabilní | Pouze Senate |

**Klíčový insight:** STOCK Act povoluje **45 dní** na zveřejnění obchodu [INFERRED][4,5]. Copy trading proto funguje jen pro **pozice držené měsíce/roky** (což kongresmani typicky dělají — nekupují na day trading). Backtest McCaula ukazuje +34.8% vs 15% S&P za rok, ale s inherentním zpožděním.

**Doporučení:**
- **Pro vývoj:** Capitol Trades (free web scraping) + Senate Stock Watcher (free JSON)
- **Pro produkci:** Lambda Finance API ($0 free tier) nebo Quiver Quantitative ($25/měsíc)
- **Alternativní data:** n8n workflow template existuje pro Firecrawl + OpenAI + Gmail monitoring kongresmanů [SINGLE-SOURCE][13]

### 4. Backtesting Frameworky

| Framework | Options | Alpaca | Aktivní | Rychlost | Use case |
|-----------|---------|--------|---------|----------|----------|
| **Lumibot** [VERIFIED][6] | ANO (ThetaData) | Nativní | ANO (4.7K commitů) | Střední | Wheel strategy, live + backtest |
| **VectorBT** [INFERRED][14] | Omezená | Ne nativně | Nejasné | Nejrychlejší | Research, parameter sweep |
| **Backtrader** [INFERRED][14] | Základní | Komunitní | Stagnuje (od 2018) | Střední | Event-based strategie |
| **QuantConnect (LEAN)** [INFERRED][14] | ANO | ANO | ANO (486K uživatelů) | Dobrá | Cloud, plná infrastruktura |
| **NautilusTrader** [SINGLE-SOURCE][14] | ANO | Ne | ANO | Velmi rychlý | Institutional-grade |

**Doporučení pro wheel strategy:**
- **#1 Lumibot** — jediný framework s nativní podporou options lifecycle (CSP → assignment → covered call), ThetaData backtesting s NBBO cenami, a přímou Alpaca/IBKR integrací. Stejný kód pro backtest i live.
- **#2 QuantConnect** — pokud potřebuješ cloud execution a rozsáhlejší historická data. Ale vendor lock-in.
- **VectorBT** — jen pro equity research, ne pro options execution

### 5. Regulatorní aspekty EU/ČR

**MiFID II Article 17 — Algorithmic Trading** [VERIFIED][7]:
- Cílí na **investment firms**, ne retail investory
- Požadavky: testování algoritmů, pre-trade kontroly, governance, dokumentace
- **Retail trader s Claude botem pravděpodobně nespadá** pod Article 17 [INFERRED][7]
- ALE: pokud obchoduješ přes regulovaného brokera (IBKR), broker sám zajišťuje compliance

**ČNB (Česká národní banka)** [INFERRED][15]:
- ČNB potvrdila, že prop trading firmy "mohou spadat pod MiFID" [SINGLE-SOURCE][15]
- Pro individuálního retail tradera s paper/live účtem u regulovaného brokera: standardní režim
- Klíčové: neporaduj jiným lidem za peníze (to vyžaduje licenci)

**Daňové implikace ČR** [UNVERIFIED]:
- Kapitálové zisky z akcií/opcí: 15% daň z příjmu (nebo 23% nad ~1.6M Kč ročně)
- Osvobození: držení > 3 roky NEBO roční příjem z prodeje < 100 000 Kč
- US akcie přes IBKR: W-8BEN formulář pro snížení US withholding tax (30% → 15%)
- **Doporučení:** Konzultovat s daňovým poradcem — specifika závisí na objemu a frekvenci

**ESMA product intervention** [INFERRED][7]:
- CFD omezení pro retail (max páka 1:30) — relevantní pokud bys tradoval CFD
- Options na US akcie přes IBKR: bez omezení ESMA (US underlying)
- Paper trading: žádná regulace (fake money)

### 6. Technická architektura — doporučení

```
┌─────────────────────────────────────────────┐
│          Claude Desktop / Code               │
│  ┌─────────┐  ┌──────────┐  ┌────────────┐ │
│  │ Alpaca  │  │ Alpha    │  │ Financial  │ │
│  │ MCP v2  │  │ Vantage  │  │ Datasets   │ │
│  │ (trade) │  │ MCP      │  │ MCP        │ │
│  └────┬────┘  └────┬─────┘  └─────┬──────┘ │
│       │            │              │         │
│  Trading +    Technická       Fundamenty    │
│  Options      analýza        + earnings     │
│  Market data  SMA/RSI/MACD                  │
└───────┬─────────────────────────────────────┘
        │
        ▼
┌───────────────────┐     ┌──────────────────┐
│  Alpaca (paper)   │     │ Interactive      │
│  Vývoj + test     │     │ Brokers (live)   │
│  US stocks+opts   │     │ EU/ČR, options   │
└───────────────────┘     └──────────────────┘
        │                         │
        ▼                         ▼
┌───────────────────────────────────────────┐
│            Lumibot Framework               │
│  Strategy code (wheel, trailing stop,      │
│  copy trading) — same code for both       │
│  backtest (ThetaData) and live execution  │
└───────────────────────────────────────────┘
        │
        ▼
┌───────────────────────────────────────────┐
│         Smart Money Data Layer             │
│  Lambda Finance API (congressional)       │
│  Quiver Quantitative (alt data)           │
│  Capitol Trades (web scraping fallback)   │
└───────────────────────────────────────────┘
```

**Scheduling:**
- Claude Desktop `/schedule` pro monitoring (jako v tutoriálu)
- Lumibot vlastní scheduler pro execution loop
- Cron/systemd pro long-running strategie

**Risk Management (critical):**
- Position sizing: max 5% portfolia na jednu pozici
- Stop-loss: vždy (trailing stop jako v tutoriálu)
- Wheel strategy: jen na akcie, které chceš vlastnit
- Paper trading MINIMUM 3 měsíce před live

---

## Disagreements & Open Questions

1. **Alpaca EU dostupnost** — WealthKernel akvizice naznačuje brzkou expanzi, ale žádný potvrzený termín pro retail API z ČR. Může to být 2026 H2 nebo později.

2. **MiFID II aplikovatelnost** — Právní experti se shodují, že Article 17 cílí na firmy, ne retail. Ale šedá zóna existuje pro agresivní algo trading s vysokou frekvencí.

3. **Congressional copy trading effectiveness** — Backtest ukazuje +34.8% (McCaul), ale 45denní disclosure zpoždění a survivorship bias v datech. Reálný výkon může být nižší.

4. **Options z EU** — US options přes IBKR fungují, ale komise jsou vyšší než pro US rezidenty. Wheel strategy vyžaduje dostatečný kapitál (100 shares × cena akcie).

5. **Lumibot vs přímý Claude bot** — Tutoriál používá Claude přímo (bez frameworku). Lumibot přidává strukturu ale i komplexitu. Pro začátek může stačit čistý Claude + Alpaca MCP.

---

## Evidence Table

| # | Source | URL | Key Claim | Type | Confidence |
|---|--------|-----|-----------|------|------------|
| 1 | Alpaca Support | https://alpaca.markets/support/is-alpaca-available-outside-the-us | Alpaca jen pro US rezidenty (retail) | primary | high |
| 2 | Alpaca Blog | https://alpaca.markets/blog/alpaca-enters-uk-and-eu-market-through-wealthkernel-acquisition/ | WealthKernel akvizice pro UK/EU expanzi | primary | high |
| 3 | Alpaca MCP GitHub | https://github.com/alpacahq/alpaca-mcp-server | 61 MCP tools, options, paper trading | primary | high |
| 4 | Lambda Finance | https://www.lambdafin.com/articles/capitol-trades-api | Congressional APIs comparison, free tiers | primary | high |
| 5 | Quiver Quantitative | https://www.quiverquant.com/congresstrading/ | Congress trading data + alt data | primary | medium |
| 6 | Lumibot GitHub | https://github.com/Lumiwealth/lumibot | Options backtesting, Alpaca/IBKR native | primary | high |
| 7 | CMS Law / ESMA | https://cms.law/en/che/legal-updates/esma-supervisory-briefing-on-algorithmic-trading-in-the-eu-key-points-and-practical-implications | MiFID II cílí na firmy, ne retail | secondary | high |
| 8 | Alpha Vantage MCP | https://mcp.alphavantage.co/ | 100+ finančních API jako MCP | primary | medium |
| 9 | Financial Datasets MCP | https://github.com/financial-datasets/mcp-server | Fundamentals MCP server | primary | high |
| 10 | EODHD | https://eodhd.com/financial-apis/mcp-server-for-financial-data-by-eodhd | 77 read-only tools | primary | low |
| 11 | LSEG | https://www.lseg.com/en/insights/supercharge-claudes-financial-skills-with-lseg-data | Institutional data MCP | primary | low |
| 12 | Unusual Whales | https://unusualwhales.com/politics | Congressional + options flow data | primary | medium |
| 13 | n8n | https://n8n.io/workflows/4509-daily-us-congress-members-stock-trades-report-via-firecrawl-openai-gmail/ | Congress monitoring workflow template | secondary | low |
| 14 | Multiple | https://autotradelab.com/blog/backtrader-vs-nautilusttrader-vs-vectorbt-vs-zipline-reloaded | Backtesting frameworks comparison | secondary | medium |
| 15 | Finance Magnates | https://www.financemagnates.com/forex/exclusive-czech-regulator-asserts-prop-trading-firms-may-be-subject-to-mifid/ | ČNB: prop firmy mohou spadat pod MiFID | secondary | medium |

## Sources

1. Alpaca Support — https://alpaca.markets/support/is-alpaca-available-outside-the-us
2. Alpaca Blog: WealthKernel Acquisition — https://alpaca.markets/blog/alpaca-enters-uk-and-eu-market-through-wealthkernel-acquisition/
3. Alpaca MCP Server v2 — https://github.com/alpacahq/alpaca-mcp-server
4. Lambda Finance: Capitol Trades APIs — https://www.lambdafin.com/articles/capitol-trades-api
5. Quiver Quantitative — https://www.quiverquant.com/congresstrading/
6. Lumibot — https://github.com/Lumiwealth/lumibot
7. CMS Law: ESMA Supervisory Briefing — https://cms.law/en/che/legal-updates/esma-supervisory-briefing-on-algorithmic-trading-in-the-eu-key-points-and-practical-implications
8. Alpha Vantage MCP — https://mcp.alphavantage.co/
9. Financial Datasets MCP — https://github.com/financial-datasets/mcp-server
10. EODHD MCP — https://eodhd.com/financial-apis/mcp-server-for-financial-data-by-eodhd
11. LSEG MCP — https://www.lseg.com/en/insights/supercharge-claudes-financial-skills-with-lseg-data
12. Unusual Whales — https://unusualwhales.com/politics
13. n8n Congress Workflow — https://n8n.io/workflows/4509-daily-us-congress-members-stock-trades-report-via-firecrawl-openai-gmail/
14. AutoTradeLab: Framework Comparison — https://autotradelab.com/blog/backtrader-vs-nautilusttrader-vs-vectorbt-vs-zipline-reloaded
15. Finance Magnates: Czech Regulator — https://www.financemagnates.com/forex/exclusive-czech-regulator-asserts-prop-trading-firms-may-be-subject-to-mifid/

## Coverage Status

- **[VERIFIED]:** Alpaca MCP v2 features, Lumibot options support, Alpaca US-only status, Lambda Finance API comparison, MiFID II Article 17 scope
- **[INFERRED]:** MiFID II neaplikovatelnost na retail, 45-day STOCK Act delay, IBKR jako nejlepší broker pro ČR
- **[SINGLE-SOURCE]:** Alpaca EU expansion timeline, ČNB stance on algo trading
- **[UNVERIFIED]:** ČR daňové specifika (15%/23%), Tastytrade EU dostupnost, EODHD MCP capabilities
