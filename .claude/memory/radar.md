# Tool Radar — Captured Tools & Recommendations

Tracked findings from `/radar` scans and manual evaluations.
Archived: `radar-archive.md` (when >400 lines)

## Stats
Last scan: 2026-04-06 (scheduled, proactive scan #6) | Mode: auto | Total: 29 tools | 🔴 4 | 🟡 23 | 🟢 2

## Active Research (🔴)
| Tool | Category | Score | Source | Captured | Status | Project fit |
|------|----------|-------|--------|----------|--------|-------------|
| [claude-code-sdk-python](https://github.com/anthropics/claude-code-sdk-python) | SDK / orchestration | 8/10 | manual | 2026-04-03 | **DONE** — [report](../outputs/radar-claude-code-sdk-python-2026-04-03.md) | STOPA — programmatic CC control, scheduled agents, budget per subagent |
| [Claw Code](https://github.com/instructkr/claw-code) | Agent harness / open-source CC clone | 9/10 | scan/PR | 2026-04-04 | **EVALUATE** | STOPA — open inspectable agent harness (Python+Rust), study for architecture patterns |
| [mcp-scan](https://github.com/invariantlabs-ai/mcp-scan) | MCP security scanner | 8/10 | scan | 2026-04-05 | **EVALUATE** | STOPA — scan all MCP servers before adding; rug pull + tool poisoning attack vector |
| [TradingAgents](https://github.com/TauricResearch/TradingAgents) | Financial multi-agent framework | 8/10 | scan | 2026-04-06 | **EVALUATE** | POLYBOT + ORAKULUM — multi-agent LLM trading (Analyst/Trader/Risk roles, LangGraph, Apache-2.0, 47k★) |

## Watch List (🟡)
| Tool | Category | Score | Source | Captured | Notes |
|------|----------|-------|--------|----------|-------|
| [T² Scaling Laws](https://arxiv.org/abs/2604.01411) | Research / scaling | 7/10 | manual/user | 2026-04-06 | Train-to-Test scaling: overtraining menší model + pass@k inference > Chinchilla-optimal velký model. Implikace pro STOPA model tier selection (haiku overtrained + sampling > sonnet one-shot). Roberts et al., UW-Madison. |
| [RLSD (Self-Distilled RLVR)](https://arxiv.org/abs/2604.03128) | Research / training | 5/10 | manual/user | 2026-04-06 | Hybrid RLVR + self-distillation: teacher moduluje update magnitude, env reward určuje směr. Řeší info leakage kolaps čisté distillation. Qwen3-VL-8B, +2.3% nad GRPO. WIP paper. Pro nás: mentální model, ne přímé použití. |
| [FastMCP](https://github.com/jlowin/fastmcp) | MCP framework | 7/10 | scan/GitHub | 2026-04-03 | v3.2.0, 24.2k★, 1M dl/day. Pro STOPA MCP server building |
| [Sonatype Guide MCP](https://github.com/sonatype/dependency-management-mcp-server) | MCP / dependency safety | 7/10 | scan | 2026-04-04 | Free MCP server pro Claude Code. Prevents hallucinated packages (27% LLM error rate). `claude mcp add sonatype-mcp` |
| [Jolt AI](https://www.usejolt.ai/) | Coding assistant / large codebase | 5/10 | scan/PH | 2026-04-04 | AI codegen pro 100K-8M line codebases. VS Code + JetBrains. Commercial SaaS. |
| [LiteParse](https://github.com/run-llama/liteparse) | PDF parsing | 6/10 | scan/MarkTechPost | 2026-04-03 | TypeScript, local-first, spatial PDF→LLM. Pro NG-ROBOT |
| [Junie CLI](https://blog.jetbrains.com/junie/) | Coding agent | 5/10 | scan/JetBrains | 2026-04-03 | Beta, LLM-agnostic, MCP support. Competitor analysis pro CC |
| [Google ADK TS](https://github.com/google/adk-js) | Agent framework | 5/10 | scan/Google | 2026-04-03 | Multi-agent, type-safe, MCP toolbox. Google ecosystem |
| [Strands Agents](https://github.com/strands-agents) | Agent SDK | 6/10 | scan/AWS | 2026-04-03 | AWS open-source, Python+TS, MCP native, multi-agent (Graph/Swarm/Workflow) |
| [Google Colab MCP](https://github.com/googlecolab/colab-mcp) | MCP server | 6/10 | scan/Google | 2026-04-03 | Agent-to-Colab notebook control, Python, uvx install |
| [Gemini CLI](https://github.com/google-gemini/gemini-cli) | Coding agent | 6/10 | scan/Google | 2026-04-03 | Apache 2.0, ReAct loop, MCP+extensions, Jules integration. CC competitor |
| [Mastra](https://github.com/mastra-ai/mastra) | Agent framework | 5/10 | scan/HN | 2026-04-03 | TS-first, 22.6k★, Apache 2.0, RAG+memory+eval built-in |
| [MCPCore](https://mcpcore.io/) | MCP hosting | 5/10 | scan/PH | 2026-04-03 | Managed MCP server infra (auth, secrets, logs, AES-256) |
| [auto-harness](https://github.com/neosigmaai/auto-harness) | Self-improving agent loop | 6/10 | manual/Twitter | 2026-04-05 | Failure mining → clustering → eval gen → regression gate. OpenAI SDK, adaptable. Key insight: regression gate compounds gains. |
| [Maritime](https://maritime.sh/) | Agent hosting / cloud infra | 5/10 | scan/PH | 2026-04-05 | Stateful agent hosting, sleep/wake (no cold starts), $1-10/mo, private beta. Commercial. Pro deployment ZACHVEV/MONITOR agents v budoucnu. |
| [openai-agents-js](https://github.com/openai/openai-agents-js) | Agent framework / TypeScript | 5/10 | scan | 2026-04-05 | Produkční Swarm nástupce, 2.6k★, MIT. Differentiator: voice/realtime (WebRTC/SIP). STOPA Python → awareness only; lepší než Mastra pro voice use cases. |
| [OpenFang](https://github.com/RightNow-AI/openfang) | Agent OS / Rust | 6/10 | manual | 2026-04-05 | 137K LOC, 14 crates, 1767+ testy, 40MB idle, 180ms cold start. WASM sandbox, Merkle audit chain. Pre-1.0 (v0.3.30). Bundled "Hands": OSINT Collector (→MONITOR), Predictor (→POLYBOT), Researcher. REST API 140+ endpoints → použitelné z Pythonu. Stack mismatch (Rust vs Python), ale architektura zajímavá jako reference. |
| [Memvid](https://github.com/memvid/memvid) | Agent memory / single-file | 6/10 | manual/GH trending | 2026-04-05 | Rust core, Python/Node SDK, Apache 2.0. Single `.mv2` file = embeddings + HNSW + Tantivy FTS + temporal index + WAL. v2.0.139+, active (2-4wk releases). Claims +35% LoCoMo, 0.025ms P50. AES-256-GCM encryption. Zero-infra vs Mem0/Zep. Pro NG-ROBOT/MONITOR scaling, ne pro STOPA (markdown grep-first stačí). |
| [oh-my-pi](https://github.com/can1357/oh-my-pi) | Terminal coding agent | 7/10 | scan | 2026-04-06 | TypeScript+Rust+Bun, 2.7k★, fork pi-mono. **Hash-anchored edits** = 10× méně whitespace chyb. LSP pro 40+ jazyků. Parallel subagenti. MCP support. `bun install -g @oh-my-pi/pi-coding-agent`. CC competitor s unikátní architekturou. |
| [open-swe](https://github.com/langchain-ai/open-swe) | Async coding agent | 7/10 | scan | 2026-04-06 | Python, MIT, LangGraph, 9.2k★. Async multi-task — Slack/Linear/GitHub triggery, každý task v izolovaném sandboxu, auto-PR. Subagenti. 15 cílených tools. Enterprise pattern study pro NG-ROBOT/STOPA orchestration. |
| [microsoft/agent-framework](https://github.com/microsoft/agent-framework) | Agent orchestration framework | 5/10 | scan | 2026-04-06 | Python+.NET, MIT, 8.9k★. Graph-based, DevUI, OpenTelemetry, RL labs. Nahrazuje Semantic Kernel + AutoGen. Generický (podobný LangGraph/Mastra), ale Microsoft authority. |
| [simonw/scan-for-secrets](https://github.com/simonw/scan-for-secrets) | Security / secrets scanner | 6/10 | scan | 2026-04-06 | Python, simonw, v0.2. Skenuje soubory na secrets před sdílením. Stream výsledků, multi-dir, Python API. Komplementuje mcp-scan pro pre-share security checks. `pip install scan-for-secrets`. |
| [MAI-Transcribe-1](https://learn.microsoft.com/en-us/azure/ai-services/speech-service/mai-transcribe) | Speech-to-text / Azure API | 7/10 | scan | 2026-04-06 | Microsoft Foundry, closed weights, Azure preview. #1 FLEURS WER (3.9% avg, 25 langs incl. Czech). Python SDK `azure-ai-transcription`, $0.36/hod. Whisper alternative pro NG-ROBOT media expansion. Žádné SLA v preview. |

## Archive (🟢 — last 30, older → radar-archive.md)
| Tool | Score | Captured | Why low |
|------|-------|----------|---------|
| [VoltAgent](https://voltagent.dev/) | 4/10 | 2026-04-03 | TS agent framework, nic unikátního vs LangGraph/ADK, 7.2k★ |
| [Perplexity Computer](https://www.perplexity.ai/hub/blog/introducing-perplexity-computer) | AI super-agent / commercial | 4/10 | scan | 2026-04-06 | $200/mo, closed, cloud-only. Orchestruje 19 modelů autonomně. MCP odmítli (context window + auth tření). Perplexity API Platform existuje. Local agent pouze macOS. Gate 2 fail pro většinu STOPA use-cases. |

## Scan Log
### 2026-04-06 — scheduled scan #6 | Searches: 11 | Fetches: 3 | Found: 3 new
- [TradingAgents](https://github.com/TauricResearch/TradingAgents) — 8/10 🔴 — Python+LangGraph multi-agent financial trading. Roles: Fundamentals/Sentiment/News/Technical Analysts, Researcher duo, Trader, Risk Mgmt, Portfolio Mgr. 47k★, Apache-2.0, v0.2.2, cross-platform (Docker). Přímý fit pro POLYBOT (paper trading) + ORAKULUM (multi-agent debate pattern). `pip install .`
- [MAI-Transcribe-1](https://learn.microsoft.com/en-us/azure/ai-services/speech-service/mai-transcribe) — 7/10 🟡 — Microsoft SOTA speech-to-text, #1 FLEURS WER 3.9% (25 jazyků vč. češtiny). Closed weights, Azure preview, $0.36/hod, 2.5× rychlejší než Azure Fast Transcription. Python SDK `azure-ai-transcription`. Relevantní pro NG-ROBOT media expansion jako Whisper alternative.
- [Perplexity Computer](https://www.perplexity.ai/hub/blog/introducing-perplexity-computer) — 4/10 🟢 — Komerční AI super-agent ($200/mo), orchestruje 19 modelů. MCP odmítli pro produkci (context overhead). Gate 2 fail. API Platform zajímavá ale commercial.
- Skipped (already tracked): TradingAgents ecosystem references to LangGraph, FastMCP, Gemma 4 (model →/watch), OpenAI Responses API (→/watch), AutoResearch Karpathy (→/autoresearch), AISuite (established 2024), Dify (established 2023), Cursor Composer 2 (commercial product)

### 2026-04-05 — manual | Memvid (memvid/memvid) — 6/10 🟡
- #1 GitHub trending. Rust single-file memory layer for AI agents. `.mv2` = HNSW vectors + Tantivy FTS + temporal + WAL + encryption. Python SDK available. Zero-infra alternative to Mem0/Zep/LangMem. Unique in portability. STOPA nepotřebuje (markdown grep stačí), ale NG-ROBOT archiv a MONITOR OSINT corpus = budoucí fit.

### 2026-04-05 — manual | OpenFang (RightNow-AI/openfang) — 6/10 🟡
- Rust Agent OS, 14 crates, WASM sandbox, bundled OSINT/Predictor/Researcher hands. Pre-1.0. REST API → Python-compatible přes HTTP. MONITOR+POLYBOT fit.

### 2026-04-04 morning — proactive scan #3 | Searches: 10 | Fetches: 0 | Found: 3 new
- [Claw Code](https://github.com/instructkr/claw-code) — 9/10 🔴 — Open-source Claude Code clean-room rewrite (Python+Rust), 72k+ stars in days. Agent harness architecture study value.
- [Sonatype Guide MCP](https://github.com/sonatype/dependency-management-mcp-server) — 7/10 🟡 — Free MCP server for Claude Code. Real-time dependency safety, prevents hallucinated packages.
- [Jolt AI](https://www.usejolt.ai/) — 5/10 🟡 — AI codegen for 100K-8M line codebases, VS Code + JetBrains, commercial
- Skipped (already tracked): FastMCP, LiteParse, Junie CLI, Google ADK TS, Strands, Colab MCP, Gemini CLI, Mastra, MCPCore, VoltAgent
- Skipped (not tools/news): GitHub Copilot training data policy, ChatGPT 5.4, Dify (established 2023)
- Skipped (already in news.md): OpenClaw

### 2026-04-03 evening — proactive scan #2 | Searches: 10 | Fetches: 5 | Found: 5 new
- [Strands Agents](https://github.com/strands-agents) — 6/10 🟡 — AWS open-source agent SDK, Python+TS, MCP native, Graph/Swarm/Workflow patterns
- [Google Colab MCP](https://github.com/googlecolab/colab-mcp) — 6/10 🟡 — MCP server pro agent→Colab notebook control, Google official
- [Gemini CLI](https://github.com/google-gemini/gemini-cli) — 6/10 🟡 — Google open-source terminal agent, ReAct, MCP, Jules. CC competitor
- [Mastra](https://github.com/mastra-ai/mastra) — 5/10 🟡 — TS agent framework, 22.6k★, RAG+memory+eval+MCP
- [MCPCore](https://mcpcore.io/) — 5/10 🟡 — Managed MCP server hosting (auth, secrets, AES-256, observability)
- Skipped (already tracked): FastMCP, LiteParse, Junie CLI, Google ADK TS, VoltAgent
- Skipped (not tools): OpenAI Responses API updates (→ /watch), Delta (Jan 2026, niche)

### 2026-04-03 18:00 — proactive scan | Searches: 10 | Fetches: 5 | Found: 5 new
- [FastMCP](https://github.com/jlowin/fastmcp) — 7/10 🟡 — Python MCP server framework, 24.2k★, v3.2.0, 1M dl/day
- [LiteParse](https://github.com/run-llama/liteparse) — 6/10 🟡 — TypeScript local PDF parser s spatial awareness, LlamaIndex
- [Junie CLI](https://blog.jetbrains.com/junie/) — 5/10 🟡 — JetBrains LLM-agnostic coding agent CLI, beta
- [Google ADK TS](https://github.com/google/adk-js) — 5/10 🟡 — Google TypeScript multi-agent framework, MCP support
- [VoltAgent](https://voltagent.dev/) — 4/10 🟢 — TS agent framework, 7.2k★, nic unikátního
- Skipped: OpenClaw (news.md#9), Karpathy autoresearch (/autoresearch), Cotality MCP (Gate 1 fail)

### 2026-04-05 — scheduled scan #4 | Searches: 10 | Fetches: 3 | Found: 3 new
- [mcp-scan](https://github.com/invariantlabs-ai/mcp-scan) — 8/10 🔴 — Invariant Labs MCP security scanner. Detects tool poisoning, rug pulls, cross-origin escalation. Run before adding any MCP server. April 1 2026: tool poisoning attack documented (hidden directives in tool docstrings). Critical for STOPA security.
- [Maritime](https://maritime.sh/) — 5/10 🟡 — Stateful agent hosting platform. Sleep/wake (no cold starts), $1-10/mo. Private beta. Future relevance for deploying ZACHVEV/MONITOR/POLYBOT agents.
- [openai-agents-js](https://github.com/openai/openai-agents-js) — 5/10 🟡 — Production Swarm for TypeScript, MIT, 2.6k★. Voice/realtime differentiator. STOPA is Python → awareness only.
- Skipped (already tracked): FastMCP 2.0 (upgrade noted — enterprise auth added), Jolt AI, LiteParse, Junie CLI, Google ADK JS, Strands, Colab MCP, Gemini CLI, Mastra, MCPCore, VoltAgent, auto-harness

### 2026-04-06 — scheduled scan #5 | Searches: 11 | Fetches: 5 | Found: 4 new
- [oh-my-pi](https://github.com/can1357/oh-my-pi) — 7/10 🟡 — Terminal AI coding agent (TypeScript+Rust+Bun). Hash-anchored edits (10× whitespace fix), LSP 40+ langs, parallel subagents, MCP. 2.7k★ fork of pi-mono. CC competitor with novel edit anchoring architecture.
- [open-swe](https://github.com/langchain-ai/open-swe) — 7/10 🟡 — LangChain async coding agent on LangGraph. 9.2k★, MIT, Python. Trigger via Slack/Linear/GitHub, isolated cloud sandboxes per task, auto-PR, subagents. Enterprise orchestration patterns relevant to NG-ROBOT.
- [simonw/scan-for-secrets](https://github.com/simonw/scan-for-secrets) — 6/10 🟡 — Simon Willison secrets scanner v0.2. Scans files before sharing, Python API, streaming results. Complements mcp-scan for pre-commit/pre-share security.
- [microsoft/agent-framework](https://github.com/microsoft/agent-framework) — 5/10 🟡 — Microsoft Python+.NET agent framework, 8.9k★, MIT. Graph orchestration, DevUI, RL labs. Supercedes Semantic Kernel + AutoGen.
- Ecosystem note: OpenAI Responses API (March 2026) now uses **SKILL.md format** compatible with Anthropic Claude — STOPA skills theoretically portable to OpenAI. No action needed now, but important for future multi-provider distribution.
- Skipped: research-llm-apis (simonw reference repo, not actionable tool), scan results overlapping with existing entries (Gemini CLI, Strands, FastMCP, Google ADK TS, LiteParse, Mastra)

### 2026-04-05 — manual | Fetches: 1 | Found: 1 new
- [auto-harness](https://github.com/neosigmaai/auto-harness) — 6/10 🟡 — NeoSigma self-improving loop: failure mining → root-cause clustering → eval gen → regression gate. Tau3 0.56→0.78. Concepts adoptable do STOPA /autoharness + /eval.

### 2026-04-03 — manual | Fetches: 1 | Found: 1 new
- [claude-code-sdk-python](https://github.com/anthropics/claude-code-sdk-python) — 8/10 🔴 — Official Python SDK pro programmatic Claude Code control, 6.1k★, MIT, in-process MCP servers
