# Polymarket Trading Bots & LLM-Powered Prediction Market Tools

Research date: 2026-03-24

---

## 1. GitHub Repos -- Legit, Buildable Projects

### Tier A: Official / High-Quality

| Repo | Stars | Lang | What it does |
|------|-------|------|-------------|
| [Polymarket/agents](https://github.com/Polymarket/agents) | ~2.6k | Python | **Official** Polymarket AI agent framework. LLM decision-making, live market data, news signals, real trade execution. MIT license. |
| [discountry/polymarket-trading-bot](https://github.com/discountry/polymarket-trading-bot) | - | Python | Gasless trades, WebSocket real-time data, monitors 15-min Up/Down markets for probability drops. Beginner-friendly. |
| [warproxxx/poly-maker](https://github.com/warproxxx/poly-maker) | - | Python | Automated market making on Polymarket CLOB. Configurable via Google Sheets. Both-sides liquidity. |
| [ent0n29/polybot](https://github.com/ent0n29/polybot) | - | Python | Reverse-engineering Polymarket strategies. Trading infrastructure toolkit. |

### Tier B: Claude/LLM-Integrated Bots

| Repo | What it does |
|------|-------------|
| [artvandelay/polymarket-agents](https://github.com/artvandelay/polymarket-agents) | MCP server (10 tools) + autonomous trading bot. **Claude Sonnet** decision-making, pluggable strategies, SQLite persistence. |
| [caiovicentino/polymarket-mcp-server](https://github.com/caiovicentino/polymarket-mcp-server) | **45 MCP tools** for Claude. Real-time monitoring, enterprise safety features. Full trading capability. |
| [dylanpersonguy/Fully-Autonomous-Polymarket-AI-Trading-Bot](https://github.com/dylanpersonguy/Fully-Autonomous-Polymarket-AI-Trading-Bot) | Multi-model ensemble (GPT-4o, Claude, Gemini). 15+ risk checks, whale tracking, fractional Kelly sizing, 9-tab dashboard. |
| [llSourcell/Poly-Trader](https://github.com/llSourcell/Poly-Trader) | Siraj Raval's autonomous Polymarket agent (educational). |
| [alsk1992/CloddsBot](https://github.com/alsk1992/CloddsBot) | AI trading agent across 1000+ markets -- Polymarket, Kalshi, Binance, Hyperliquid, Solana DEXs, 5 EVM chains. Built on Claude. Self-hosted. |

### Tier C: Curated Lists

| Repo | What it does |
|------|-------------|
| [harish-garg/Awesome-Polymarket-Tools](https://github.com/harish-garg/Awesome-Polymarket-Tools) | Curated list of 170+ Polymarket tools, bots, and resources. |

> **WARNING:** GitHub is flooded with SEO-spam repos (keyword-stuffed descriptions repeating "polymarket trading bot" 15x). Most repos from orgs like `dev-protocol`, `Zeta-Trade`, `infraform`, `legit-script-group` are low-quality or outright scams. Stick to repos with actual README content, commit history, and code quality.

---

## 2. The Viral Bot Story ($1K to $14K)

### What actually happened (March 10, 2026)

A viral X post compared two AI agents, each starting with **$1,000** on Polymarket for 48 hours:

- **Claude-powered agent:** Grew to **$14,216** (1,322% return)
- **OpenClaw agent:** Fully liquidated (lost everything)

The post hit **1.2M views** but disclosed no strategy details or risk parameters.

### Key sources:
- [BingX: Claude turns $1,000 into $14,216 on Polymarket in 48 hours](https://bingx.com/en/news/post/claude-turns-into-on-polymarket-in-hours-as-openclaw-agent-is-wiped-out)
- [Phemex: AI Agent Claude Gains 1,322% on Polymarket in 48 Hours](https://phemex.com/news/article/ai-trading-agent-claude-achieves-1322-return-on-polymarket-65634)
- [CryptoNews: Claude and OpenClaw face off](https://cryptonews.net/news/other/32536607/)
- [TMA Street: AI Trading Bot Turns $1,000 Into $14,216](https://tmastreet.com/ai-trading-bot-turns-1000-into-14216-on-polymarket-in-48-hours/)
- [BeInCrypto: Traders Use Claude AI Bots to Win Millions](https://beincrypto.com/claude-ai-polymarket-trading-bots-millions/)
- [Medium: Claude AI Trading Bots Are Making Hundreds of Thousands](https://medium.com/@weare1010/claude-ai-trading-bots-are-making-hundreds-of-thousands-on-polymarket-2840efb9f2cd)

### Earlier documented case (Dec 2025 - Jan 2026)

Wallet `0x8dxd` started with **$313**, accumulated **$438,000** by January 6, 2026. 98% win rate across 6,615 predictions on BTC/ETH/SOL 15-minute up/down contracts. Strategy: pure **latency arbitrage** -- monitoring Binance/Coinbase real-time feeds and buying the near-certain winning side before Polymarket repriced.

### OHMO.AI claim ($1,400 to $238K in 11 days)

Widely shared but originates from "content loops" -- recycled posts and screenshots. No primary source verified. CFTC has warned about fraudsters exploiting AI hype to promote automated trading systems.

Source: [Cybeauty: The Truth Behind the Viral Polymarket AI](https://cybeauty.ai/from-1k-to-200k-in-11-days-the-truth-behind-the-viral-polymarket-ai-trading-story/)

### The real edge

The profitable bots are NOT doing "AI prediction" -- they exploit **latency arbitrage**:
- Polymarket's short-term crypto contracts reprice slower than spot prices on Binance/Coinbase
- Bots monitor real-time exchange feeds via WebSocket
- When actual probability is ~85% but Polymarket still shows ~50/50, bot buys the mispriced side
- This is speed-based, not intelligence-based

---

## 3. MCP Servers for Trading

### Polymarket-specific MCP Servers

| Server | Tools | Focus | npm/install |
|--------|-------|-------|-------------|
| [caiovicentino/polymarket-mcp-server](https://github.com/caiovicentino/polymarket-mcp-server) | 45 | Full trading + monitoring + safety | GitHub |
| [berlinbra/polymarket-mcp](https://github.com/berlinbra/polymarket-mcp) | 4 | Read-only (market info, prices, history) | GitHub |
| [ozgureyilmaz/polymarket-mcp](https://github.com/ozgureyilmaz/polymarket-mcp) | ~10 | Real-time data, search | GitHub |
| [IQAIcom/mcp-polymarket](https://github.com/IQAIcom/mcp-polymarket) | ~22 | Interaction with Polymarket | `@iqai/mcp-polymarket` (npm) |
| [aryankeluskar/polymarket-mcp](https://github.com/aryankeluskar/polymarket-mcp) | - | 2900 downloads first weekend | npm |
| [pab1it0/polymarket-mcp](https://github.com/pab1it0/polymarket-mcp) | - | Gamma Markets API | GitHub |
| [artvandelay/polymarket-agents](https://github.com/artvandelay/polymarket-agents) | 10 | Odds, orderbook, spread, history + trading bot | GitHub |
| [JamesANZ/prediction-market-mcp](https://github.com/JamesANZ/prediction-market-mcp) | - | Multi-platform: Polymarket + PredictIt + Kalshi | GitHub |
| [agent-next/polymarket-paper-trader](https://github.com/agent-next/polymarket-paper-trader) | - | Paper trading simulator for AI agents | `npx clawhub install` |

### Multi-platform / Exchange MCP Servers

| Server | Covers |
|--------|--------|
| [JamesANZ/prediction-market-mcp](https://github.com/JamesANZ/prediction-market-mcp) | Polymarket + PredictIt + Kalshi |
| [alsk1992/CloddsBot](https://github.com/alsk1992/CloddsBot) | Polymarket, Kalshi, Binance, Hyperliquid, Solana DEXs, 5 EVM chains |

### Claude Code Skills (not MCP servers but relevant)

- [Polymarket Development Suite](https://mcpmarket.com/tools/skills/polymarket-development-suite) -- Claude Code skill on MCPMarket
- [Polymarket Trading Data Integration](https://mcpmarket.com/tools/skills/polymarket-trading-data-integration) -- Blockchain integration skill

---

## 4. Polymarket API -- Current State

### Architecture: 3 APIs + WebSocket

| API | Purpose | Auth required | Base URL |
|-----|---------|---------------|----------|
| **Gamma API** | Market metadata, categories, resolution info | No (read-only) | `gamma-api.polymarket.com` |
| **CLOB API** | Order book, trading, positions | Yes (for writes) | `clob.polymarket.com` |
| **REST/Data API** | Historical data, prices, volumes | Partial | `polymarket.com/api` |
| **WebSocket** | Real-time price updates, orderbook changes, trades | No (for public streams) | Various endpoints |

### Authentication

- **Read-only endpoints:** Generally no auth required
- **Trading:** Requires API key derived from wallet signature + private key signing
- **Create API key:** Through Polymarket interface or derive from wallet
- **Chain:** Polygon (MATIC) -- trades settled on-chain via CTF (Conditional Token Framework)

### Rate Limits (Cloudflare-enforced)

| Endpoint type | Limit | Behavior |
|--------------|-------|----------|
| Public REST | ~60 req/min | Throttled (not rejected) |
| Authenticated REST | 10-100 req/sec (varies) | Per IP + per API key |
| WebSocket | Virtually unlimited | Connection limits per API key |
| Sliding window | Yes | Resets continuously |

**Key insight:** WebSocket connections do NOT count against REST rate limits. For real-time data, always prefer WebSocket.

### API availability

- As of 2026: API is **no longer geoblocked in the US** (previously was)
- Full docs: [docs.polymarket.com](https://docs.polymarket.com)
- Python SDK: `py-clob-client` (official)

Sources:
- [Polymarket Rate Limits docs](https://docs.polymarket.com/api-reference/rate-limits)
- [QuantVPS: Polymarket API Now Available in the U.S.](https://www.quantvps.com/blog/polymarket-us-api-available)
- [AgentBets: Polymarket API Tutorial](https://agentbets.ai/guides/polymarket-api-guide/)

---

## 5. Key Tools & Data Sources Used by Successful Bots

### Data Sources

| Category | Tools / APIs | Used for |
|----------|-------------|----------|
| **Exchange feeds** | Binance WebSocket, Coinbase WebSocket, Bybit | Latency arbitrage (crypto markets) |
| **News** | NewsAPI, GDELT, Google News RSS, AP/Reuters feeds | Event-driven trading |
| **Social/Sentiment** | Twitter/X API, Reddit API, Telegram scraping | Sentiment signals |
| **Polling** | FiveThirtyEight, RealClearPolitics, 270toWin | Political market pricing |
| **LLM APIs** | Claude API, OpenAI API, Gemini API | Decision-making, news analysis |
| **Polymarket native** | Gamma API, CLOB API, WebSocket streams | Market data, orderbook, execution |

### Bot Architecture Patterns (from successful implementations)

1. **Latency Arbitrage** (most profitable, documented):
   - WebSocket feed from Binance/Coinbase
   - Compare real-time price momentum vs Polymarket 15-min contract odds
   - Buy mispriced side when delta exceeds threshold
   - Requires: low-latency hosting (QuantVPS, Hetzner), sub-second execution

2. **News-Driven Event Trading**:
   - Monitor news APIs + social media for breaking events
   - LLM (Claude) analyzes relevance to open Polymarket markets
   - Calculate new probability estimate
   - Trade if market price diverges significantly from estimate
   - Bayesian updating on continuous signals

3. **Multi-Model Ensemble**:
   - Multiple LLMs (Claude, GPT-4o, Gemini) independently estimate probabilities
   - Aggregate via weighted average or voting
   - Trade when consensus diverges from market price
   - Example: dylanpersonguy's bot uses this approach

4. **Copy Trading / Whale Tracking**:
   - Monitor on-chain transactions of known profitable wallets
   - Mirror their positions with configurable delay/sizing
   - Filter by win rate, volume, recency

5. **Market Making**:
   - Provide liquidity on both YES/NO sides
   - Earn spread while managing inventory risk
   - Requires: capital, sophisticated risk controls
   - Example: warproxxx/poly-maker

### Key Technical Stack

```
Runtime:        Python 3.11+ or TypeScript/Node.js
Polymarket SDK: py-clob-client (official Python)
LLM:            Claude API (Anthropic) -- most common for decision layer
Database:       SQLite (simple) or PostgreSQL (production)
Hosting:        QuantVPS, Hetzner, or local machine
Monitoring:     Custom dashboard or terminal UI
Risk mgmt:      Kelly criterion sizing, max position limits, circuit breakers
```

### Two-Layer Architecture (from Dev Genius article)

Blog post: [Just Built A Two-Layer AI System That Trades Polymarket and Kalshi While I Sleep](https://blog.devgenius.io/just-built-a-two-layer-ai-system-that-trades-polymarket-and-kalshi-while-i-sleep-heres-the-aa59ead275f6)

- **Layer 1 (Research Agent):** Scans news, evaluates markets, generates probability estimates
- **Layer 2 (Execution Agent):** Takes Layer 1 signals, manages risk, executes trades
- Separation prevents the research agent from having trade execution access (safety)

---

## 6. Actionable Next Steps

### Quickest path to a working bot:

1. **Start with `Polymarket/agents`** -- official, MIT licensed, well-documented
2. **Add MCP layer** using `caiovicentino/polymarket-mcp-server` (45 tools) or `berlinbra/polymarket-mcp` (simpler, 4 tools)
3. **For latency arb:** Add Binance/Coinbase WebSocket feeds, focus on 15-min crypto Up/Down markets
4. **For news-driven:** Add NewsAPI + Claude analysis layer, target political/event markets with slower resolution

### Minimum viable stack:

```
1. Polymarket API account + wallet (Polygon)
2. py-clob-client (official SDK)
3. Claude API for decision-making
4. WebSocket for real-time data
5. SQLite for state/history
6. Simple risk rules (max position, stop loss)
```
