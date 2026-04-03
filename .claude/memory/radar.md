# Tool Radar — Captured Tools & Recommendations

Tracked findings from `/radar` scans and manual evaluations.
Archived: `radar-archive.md` (when >400 lines)

## Stats
Last scan: 2026-04-03 (auto) | Mode: proactive scan | Total: 6 tools | 🔴 1 | 🟡 4 | 🟢 1

## Active Research (🔴)
| Tool | Category | Score | Source | Captured | Status | Project fit |
|------|----------|-------|--------|----------|--------|-------------|
| [claude-code-sdk-python](https://github.com/anthropics/claude-code-sdk-python) | SDK / orchestration | 8/10 | manual | 2026-04-03 | deepresearch pending | STOPA — programmatic CC control |

## Watch List (🟡)
| Tool | Category | Score | Source | Captured | Notes |
|------|----------|-------|--------|----------|-------|
| [FastMCP](https://github.com/jlowin/fastmcp) | MCP framework | 7/10 | scan/GitHub | 2026-04-03 | v3.2.0, 24.2k★, 1M dl/day. Pro STOPA MCP server building |
| [LiteParse](https://github.com/run-llama/liteparse) | PDF parsing | 6/10 | scan/MarkTechPost | 2026-04-03 | TypeScript, local-first, spatial PDF→LLM. Pro NG-ROBOT |
| [Junie CLI](https://blog.jetbrains.com/junie/) | Coding agent | 5/10 | scan/JetBrains | 2026-04-03 | Beta, LLM-agnostic, MCP support. Competitor analysis pro CC |
| [Google ADK TS](https://github.com/google/adk-js) | Agent framework | 5/10 | scan/Google | 2026-04-03 | Multi-agent, type-safe, MCP toolbox. Google ecosystem |

## Archive (🟢 — last 30, older → radar-archive.md)
| Tool | Score | Captured | Why low |
|------|-------|----------|---------|
| [VoltAgent](https://voltagent.dev/) | 4/10 | 2026-04-03 | TS agent framework, nic unikátního vs LangGraph/ADK, 7.2k★ |

## Scan Log
### 2026-04-03 18:00 — proactive scan | Searches: 10 | Fetches: 5 | Found: 5 new
- [FastMCP](https://github.com/jlowin/fastmcp) — 7/10 🟡 — Python MCP server framework, 24.2k★, v3.2.0, 1M dl/day
- [LiteParse](https://github.com/run-llama/liteparse) — 6/10 🟡 — TypeScript local PDF parser s spatial awareness, LlamaIndex
- [Junie CLI](https://blog.jetbrains.com/junie/) — 5/10 🟡 — JetBrains LLM-agnostic coding agent CLI, beta
- [Google ADK TS](https://github.com/google/adk-js) — 5/10 🟡 — Google TypeScript multi-agent framework, MCP support
- [VoltAgent](https://voltagent.dev/) — 4/10 🟢 — TS agent framework, 7.2k★, nic unikátního
- Skipped: OpenClaw (news.md#9), Karpathy autoresearch (/autoresearch), Cotality MCP (Gate 1 fail)

### 2026-04-03 — manual | Fetches: 1 | Found: 1 new
- [claude-code-sdk-python](https://github.com/anthropics/claude-code-sdk-python) — 8/10 🔴 — Official Python SDK pro programmatic Claude Code control, 6.1k★, MIT, in-process MCP servers
