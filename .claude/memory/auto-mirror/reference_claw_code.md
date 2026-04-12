---
name: reference_claw_code
description: Claw Code architecture patterns — permission deny-lists, 6 MCP transports, multi-agent orchestration with QueryEngine
type: reference
---

Claw Code = clean-room open-source rewrite CC architektury (github.com/instructkr/claw-code → ultraworkers/claw-code).
Repo: 73% Rust (crates: api, runtime, tools, commands, plugins, server, lsp), 27% Python (porting scaffold).

## Permission System (dual-layer)
- Rust: `PermissionMode` enum — ReadOnly (9) | WorkspaceWrite (6) | DangerFullAccess (4 tools: bash, Agent, REPL, PowerShell)
- Default policy: DangerFullAccess (fail-closed) + per-tool downgrade to declared level
- Python: `ToolPermissionContext` frozen dataclass s `deny_names` + `deny_prefixes`, case-insensitive
- Auto Mode: 2-stage classifier (Sonnet 4.6) — Stage 1 fast filter (8.5% FP) → Stage 2 CoT (0.4% FP)
- **Reasoning-blind**: classifier stripuje assistant messages, vidí jen user msgs + tool payloads → anti-injection
- Circuit breaker: 3 consecutive denials OR 20 total = session termination
- COORDINATOR_MODE: koordinátor má JEN Agent + SendMessage + TaskStop (žádný filesystem access)

## 6 MCP Transports (Rust: 5 files in runtime/src/)
stdio | SSE | HTTP (streamable) | WebSocket | SDK (in-process) | ManagedProxy (claudeai marketplace)
- 11-phase lifecycle state machine: ConfigLoad→ServerReg→Spawn→Init→ToolDiscovery→[ResourceDiscovery]→Ready↔Invocation→Shutdown
- Config hashing: FNV-1a (not SHA-256), 16-char hex, scope-independent
- OAuth PKCE: SSE + HTTP only. WebSocket: headers/headersHelper only, no OAuth
- JSON-RPC framing: Content-Length header, NOT newline-delimited
- Degraded mode: continues with partial server availability
- **Only stdio fully implemented in runtime** — SSE/HTTP/WS/SDK/ManagedProxy = config parsed, execution "unsupported"

## Orchestration
- `PortRuntime` → `QueryEnginePort` → `TurnResult` pipeline
- Budget: `max_turns` + `max_budget_tokens` + `compact_after_turns`
- 5 built-in agents: general, explore, plan, verification, guide
- `forkSubagent` + `spawnMultiAgent` pro parallel execution
- COORDINATOR_MODE: JSON placeholder, not yet ported (higher-level than AgentTool)

## Actionable pro STOPA
Plný research output: `outputs/claw-code-architecture-research.md`
