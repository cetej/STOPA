# Tool Radar — Captured Tools & Recommendations

Tracked findings from `/radar` scans and manual evaluations.
Archived: `radar-archive.md` (when >400 lines)

## Stats
Last scan: 2026-04-04 (morning) | Mode: proactive scan | Total: 14 tools | 🔴 2 | 🟡 11 | 🟢 1

## Active Research (🔴)
| Tool | Category | Score | Source | Captured | Status | Project fit |
|------|----------|-------|--------|----------|--------|-------------|
| [claude-code-sdk-python](https://github.com/anthropics/claude-code-sdk-python) | SDK / orchestration | 8/10 | manual | 2026-04-03 | **DONE** — [report](../outputs/radar-claude-code-sdk-python-2026-04-03.md) | STOPA — programmatic CC control, scheduled agents, budget per subagent |
| [Claw Code](https://github.com/instructkr/claw-code) | Agent harness / open-source CC clone | 9/10 | scan/PR | 2026-04-04 | **EVALUATE** | STOPA — open inspectable agent harness (Python+Rust), study for architecture patterns |

## Watch List (🟡)
| Tool | Category | Score | Source | Captured | Notes |
|------|----------|-------|--------|----------|-------|
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

## Archive (🟢 — last 30, older → radar-archive.md)
| Tool | Score | Captured | Why low |
|------|-------|----------|---------|
| [VoltAgent](https://voltagent.dev/) | 4/10 | 2026-04-03 | TS agent framework, nic unikátního vs LangGraph/ADK, 7.2k★ |

## Scan Log
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

### 2026-04-03 — manual | Fetches: 1 | Found: 1 new
- [claude-code-sdk-python](https://github.com/anthropics/claude-code-sdk-python) — 8/10 🔴 — Official Python SDK pro programmatic Claude Code control, 6.1k★, MIT, in-process MCP servers
