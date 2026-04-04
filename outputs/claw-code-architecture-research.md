# Claw Code — Architektonická analýza pro STOPA

**Zdroj:** github.com/instructkr/claw-code (→ ultraworkers/claw-code), claw-code.codes
**Datum:** 2026-04-04
**Účel:** Referenční implementace pro STOPA security model, MCP rozšíření, orchestraci

---

## 1. Permission Context Management

### Architektura (3-tier, dual-layer)

**Rust vrstva** (`rust/crates/tools/src/lib.rs`, 4470 řádků):
- `PermissionMode` enum: `ReadOnly` | `WorkspaceWrite` | `DangerFullAccess`
- Každý tool má `required_permission: PermissionMode`
- Default policy: `DangerFullAccess` (maximum restriction) + per-tool downgrade = **fail-closed**

**Python vrstva** (`src/permissions.py`):
```
ToolPermissionContext (frozen dataclass)
├── deny_names: frozenset[str]     — exact tool name matches
├── deny_prefixes: tuple[str, ...]  — prefix-based blocking (e.g., "mcp_")
└── blocks(tool_name) → bool        — case-insensitive check
```

**3 filtrovací dimenze:**
1. `simple_mode` → jen BashTool + FileReadTool + FileEditTool
2. `include_mcp` → filtruje MCP tools by name/source_hint
3. `permission_context` → deny-list based blocking

### 19 Gated Tools s Permission Levels (z Rust `mvp_tool_specs()`)

| # | Tool | Permission | Kategorie |
|---|------|-----------|-----------|
| 1 | `bash` | **DangerFullAccess** | Shell |
| 2 | `read_file` | ReadOnly | File I/O |
| 3 | `write_file` | WorkspaceWrite | File I/O |
| 4 | `edit_file` | WorkspaceWrite | File I/O |
| 5 | `glob_search` | ReadOnly | Search |
| 6 | `grep_search` | ReadOnly | Search |
| 7 | `WebFetch` | ReadOnly | Web |
| 8 | `WebSearch` | ReadOnly | Web |
| 9 | `TodoWrite` | WorkspaceWrite | Task mgmt |
| 10 | `Skill` | ReadOnly | Orchestration |
| 11 | `Agent` | **DangerFullAccess** | Sub-agents |
| 12 | `ToolSearch` | ReadOnly | Discovery |
| 13 | `NotebookEdit` | WorkspaceWrite | File I/O |
| 14 | `Sleep` | ReadOnly | Utility |
| 15 | `SendUserMessage` | ReadOnly | Communication |
| 16 | `Config` | WorkspaceWrite | Settings |
| 17 | `StructuredOutput` | ReadOnly | Output |
| 18 | `REPL` | **DangerFullAccess** | Code exec |
| 19 | `PowerShell` | **DangerFullAccess** | Shell (Win) |

**Rozložení:** 9× ReadOnly, 6× WorkspaceWrite, 4× DangerFullAccess

### Tool Categories Detail (z tools_snapshot.json)

| # | Tool | Permission notes |
|---|------|-----------------|
| 1 | **AgentTool** | Sub-agent spawning — forkSubagent, resumeAgent, runAgent |
| 2 | **BashTool** | Heaviest gating: bashPermissions, bashSecurity, commandSemantics, destructiveCommandWarning, modeValidation, pathValidation, readOnlyValidation, sedValidation, shouldUseSandbox |
| 3 | **PowerShellTool** | Windows analog: powershellPermissions, powershellSecurity, gitSafety, CLM types |
| 4 | **FileEditTool** | Write permission gate |
| 5 | **FileWriteTool** | Write permission gate |
| 6 | **FileReadTool** | Read-only, imageProcessor, limits |
| 7 | **GlobTool** | Read-only |
| 8 | **GrepTool** | Read-only |
| 9 | **MCPTool** | MCP execution, classifyForCollapse |
| 10 | **McpAuthTool** | OAuth PKCE flow |
| 11 | **ListMcpResourcesTool** | MCP resource discovery |
| 12 | **ReadMcpResourceTool** | MCP resource read |
| 13 | **WebFetchTool** | preapproved URL list, network access |
| 14 | **WebSearchTool** | Network access |
| 15 | **NotebookEditTool** | Jupyter write |
| 16 | **EnterPlanModeTool** | Mode transition |
| 17 | **EnterWorktreeTool** | Git worktree creation |
| 18 | **SkillTool** | Skill execution |
| 19 | **RemoteTriggerTool** | Remote session trigger |
| 20 | **CronCreate/Delete/ListTool** | Scheduled task management |
| 21 | **SendMessageTool** | Inter-agent communication |
| 22 | **TodoWriteTool** | Task tracking (low gate) |
| 23 | **TaskCreate/Get/List/Output/Stop/UpdateTool** | Background task management |
| 24 | **TeamCreate/DeleteTool** | Team memory |
| 25 | **LSPTool** | Language server protocol |
| 26 | **TestingPermissionTool** | Test-only permission tool |
| 27 | **ConfigTool** | Settings modification |

### BashTool Security Stack (nejkomplexnější)

```
BashTool
├── bashPermissions.ts    — per-command allow/deny lists
├── bashSecurity.ts       — ~2,500 lines security validation
├── commandSemantics.ts   — semantic classification of commands
├── destructiveCommandWarning.ts — rm, force-push detection
├── modeValidation.ts     — sandbox/trusted mode checks
├── pathValidation.ts     — path traversal prevention
├── readOnlyValidation.ts — enforces read-only in restricted contexts
├── sedValidation.ts      — sed command analysis
└── shouldUseSandbox.ts   — sandboxing decision logic
```

### Auto Mode / TRANSCRIPT_CLASSIFIER (2-stage)

Z Anthropic engineering blogu + leak dat — **dvoustupňový classifier** (běží na Sonnet 4.6):

**Stage 1:** Fast single-token yes/no filtr. Tunovaný k blokování (8.5% false positive rate).
**Stage 2:** Chain-of-thought reasoning pass, triggerovaný jen pokud Stage 1 flaguje. Redukuje FP na 0.4%.

**Reasoning-blind design:** Classifier záměrně STRIPUJE assistant messages a tool outputs. Vidí jen user messages + tool call payloads. → Agent nemůže generovat racionalizace které by ovlivnily classifier. Blokuje prompt injection přes tool outputs.

**Auto-approve tiers:**
| Tier | Auto? | Příklady |
|------|-------|---------|
| Tier 1 | Auto-approved | File reads, search, code navigation |
| Tier 2 | In-project bypass | File writes/edits within project dir (VCS reviewable) |
| Tier 3 | Gated → classifier | Shell, web, MCP, sub-agents, external filesystem |

**Circuit breaker:** 3 consecutive denials NEBO 20 total = session termination.
**Compound commands:** `&&`, `||`, `;`, pipes — evaluated sub-command by sub-command. Pokud jakákoliv komponenta blocked → celý chain denied.

**Deny-and-continue:** Blokované akce vrací důvod místo haltování session. Agent může retry bezpečnějším způsobem.

### Doporučení pro STOPA Security Model

1. **Adoptuj deny-list pattern** — STOPA skills by měly mít `deny_tools:` v YAML frontmatter
2. **Per-skill permission context** — každý skill dostane `ToolPermissionContext` s omezeným tool poolem
3. **3 úrovně:** `read-only` (Grep, Glob, Read), `write` (+ Edit, Write), `full` (+ Bash, Agent)
4. **BashTool gate inspirace:** klasifikace příkazů jako `safe/risky/destructive` pro STOPA hook system
5. **Auto-approve pattern:** místo transcript classifier, STOPA může používat `allowed-tools` v SKILL.md (už existuje) + runtime enforcement

---

## 2. MCP — 6 Transport Implementations

### Přehled transportů

| # | Transport | Use Case | Auth |
|---|-----------|----------|------|
| 1 | **stdio** | Local MCP servers (subprocess) | Implicit (same machine) |
| 2 | **SSE** (Server-Sent Events) | Legacy remote MCP | API key / OAuth |
| 3 | **HTTP** (Streamable HTTP) | New standard remote MCP | OAuth PKCE |
| 4 | **WebSocket** | Real-time bidirectional MCP | Token-based |
| 5 | **SDK** | In-process MCP (embedded) | N/A |
| 6 | **ClaudeAiProxy** | Anthropic-hosted MCP marketplace | OAuth via Anthropic |

### Rust Implementace (5 souborů v `rust/crates/runtime/src/`)

| Soubor | Zodpovědnost |
|--------|-------------|
| `mcp.rs` | Name normalization, FNV-1a config hashing, signature generation |
| `mcp_client.rs` | Transport enum, bootstrap, auth abstraction |
| `mcp_stdio.rs` | McpServerManager — JSON-RPC protocol, spawn/kill |
| `mcp_lifecycle_hardened.rs` | 11-phase lifecycle state machine |
| `mcp_tool_bridge.rs` | McpToolRegistry — thread-safe client registry |

### 11-Phase Lifecycle State Machine

```
ConfigLoad → ServerRegistration → SpawnConnect → InitializeHandshake
  → ToolDiscovery → [ResourceDiscovery] → Ready ↔ Invocation
  → Shutdown → Cleanup
```

- Jakákoliv fáze může přejít do `ErrorSurfacing` → `Ready` (recovery) nebo `Shutdown`
- ResourceDiscovery je volitelné (může jít přímo do Ready)
- **Degraded mode:** `McpDegradedReport` sleduje working/failed servery, available/missing tools — systém pokračuje s částečnou dostupností

### Name Normalization & Config Hashing

- **Tool naming:** `mcp__{normalized_server_name}__{normalized_tool_name}`
- Normalizace: non-`[a-zA-Z0-9_-]` → `_`, collapse pro `claude.ai` prefixed names
- **Config hashing:** FNV-1a → stable 16-char hex hash, scope-independent (User vs Local = same hash)
- Použití: deduplication + change detection

### Transport-Specific Auth

| Transport | OAuth | Headers | headersHelper | Special |
|-----------|-------|---------|---------------|---------|
| Stdio | — | — | — | `command`, `args`, `env`, `toolCallTimeoutMs` |
| SSE | ✓ PKCE | ✓ | ✓ | Legacy remote |
| HTTP | ✓ PKCE | ✓ | ✓ | Modern remote (streamable) |
| WebSocket | — | ✓ | ✓ | Full-duplex, no OAuth |
| SDK | — | — | — | Just `name` (in-process) |
| ManagedProxy | Managed | — | — | `url`, `id`, CCR proxy unwrapping |

**headersHelper pattern:** External script dynamicky generuje auth headers — užitečné pro rotating tokens.
**CCR Proxy:** ManagedProxy URLs jdou přes `api.anthropic.com/v2/session_ingress/shttp/mcp/`, `unwrap_ccr_proxy_url()` extrahuje real URL z query params.

### Error Handling & Retry

```
McpServerManagerError:
  Io           — OS-level
  Transport    — communication failure (retryable)
  JsonRpc      — server error response
  InvalidResponse — malformed response
  Timeout      — exceeded deadline (retryable)
  UnknownTool/UnknownServer — routing failure
```

- **Retry:** Transport + Timeout errors → 1 automatic retry po server reset
- **Timeouts:** initialize=10s, tools/list=30s, tools/call=60s (configurable per-server)
- **JSON-RPC framing:** `Content-Length: N\r\n\r\n{json}` (ne newline-delimited)

### Aktuální stav: jen Stdio je plně implementovaný v runtime

SSE, HTTP, WebSocket, SDK, ManagedProxy — config parsing funguje, ale runtime execution je tracked jako "unsupported". Tohle je hlavní gap v Rust portu.

### Doporučení pro mcp-builder skill

1. **Transport selection decision tree:**
   - Local CLI tool → **Stdio** (spawn subprocess, env vars pro secrets)
   - Remote API → **HTTP** (streamable, OAuth PKCE)
   - Real-time/bidirectional → **WebSocket** (headers auth)
   - In-process library → **SDK**
   - Anthropic marketplace → **ManagedProxy**
2. **OAuth PKCE template** — `clientId`, `callbackPort`, `authServerMetadataUrl` ready-to-use
3. **headersHelper script template** — pro rotating tokens
4. **Paginated discovery** — MCP servery MUSÍ podporovat cursor-based pagination v `tools/list`
5. **JSON-RPC framing** — `Content-Length` header, ne newline-delimited
6. **Graceful degradation** — servery by měly vracet partial results místo total failure
7. **Config hash pattern** — FNV-1a pro change detection při rekonfiguraci
8. **`structuredContent` v tool results** — MCP spec extension, vrací `content` (text blocks) + `structuredContent` (arbitrary JSON)
9. **Timeout documentation** — servery dělající heavy work musí dokumentovat expected timeouts
10. **Tool name normalization** — server musí počítat s prefixed names `mcp__{server}__{tool}`

---

## 3. Multi-Agent Orchestration Layer

### Architektura

Claw Code orchetruje přes několik vrstev:

```
PortRuntime (main orchestrator)
├── route_prompt()         — token-based routing to commands/tools
├── bootstrap_session()    — full session initialization
├── run_turn_loop()        — multi-turn execution with budget
│
QueryEnginePort (execution engine)
├── submit_message()       — single turn with permission checks
├── stream_submit_message() — streaming variant
├── compact_messages_if_needed() — context management
├── persist_session()      — session persistence
│
AgentTool subsystem
├── forkSubagent.ts        — parallel agent spawning
├── resumeAgent.ts         — agent resume from saved state
├── runAgent.ts            — agent execution
├── agentMemory.ts         — per-agent memory isolation
├── agentMemorySnapshot.ts — memory snapshots for handoff
├── spawnMultiAgent.ts     — multi-agent coordination
│
Built-in Agent Types
├── generalPurposeAgent    — broad capability
├── exploreAgent           — codebase exploration
├── planAgent              — architecture planning
├── verificationAgent      — adversarial verification
└── clawCodeGuideAgent     — self-help agent
```

### QueryEngine Patterns

**Budget control:**
```python
QueryEngineConfig:
  max_turns: 8
  max_budget_tokens: 2000
  compact_after_turns: 12
  structured_output: bool
  structured_retry_limit: 2
```

**Turn lifecycle:**
```
submit_message()
  → check max_turns limit
  → format output (plain/structured)
  → project token usage
  → check budget limit → stop_reason: 'max_budget_reached'
  → append to transcript
  → compact if needed
  → return TurnResult(stop_reason, usage, denials)
```

**Streaming events:**
```
message_start → command_match → tool_match → permission_denial → message_delta → message_stop
```

### COORDINATOR_MODE (z leak + oficiální docs)

**Kritický insight:** Koordinátor NEMÁ přístup k filesystem tools!

```
COORDINATOR_MODE_ALLOWED_TOOLS = [Agent, SendMessage, TaskStop]
```

- Koordinátor je čistě management/synthesis layer — nemůže číst/psát soubory
- Nutí delegaci místo "udělám sám" antipattern
- System prompt: "Do not rubber-stamp weak work"
- 4 fáze: Research → Synthesis → Implementation → Verification

### Agent Teams (experimentální, Opus 4.6 only)

```
Team Lead + N Teammates (3-5 doporučeno)
├── Shared task list (file-based, locking)
├── Message mailbox (direct + broadcast)
├── Plan approval gate (teammate v plan mode → lead schválí/zamítne)
└── Hooks: TeammateIdle, TaskCreated, TaskCompleted (exit code 2 = reject)
```

**3 režimy spawnu:**
| Režim | Princip | Use case |
|-------|---------|----------|
| **Fork** | Byte-identická kopie parent kontextu, využívá prompt cache | Paralelní práce |
| **Teammate** | Separátní pane (tmux/iTerm), file-based mailbox | Nezávislé workstreamy |
| **Worktree** | Vlastní git worktree, izolovaný branch per agent | Exploratorní/riskantní práce |

### Subagents (5 built-in)

| Agent | Model | Tool access | Purpose |
|-------|-------|-------------|---------|
| Explore | Haiku | Read-only | Codebase exploration |
| Plan | inherited | Read-only | Architecture planning |
| General | inherited | All | Broad capability |
| Verification | inherited | All | Adversarial verification |
| Guide | inherited | Read-only | Self-help |

### Porovnání s STOPA /orchestrate

| Aspekt | Claw Code | STOPA /orchestrate |
|--------|-----------|-------------------|
| **Task decomposition** | Token-based routing (`_score()`) | Intelligent planning (PLAN phase) |
| **Budget** | Token count (`max_budget_tokens`) | Tier-based (light/standard/deep/farm) |
| **Circuit breaker** | `max_turns` limit | 3× same agent loop → STOP |
| **Permission** | ToolPermissionContext deny-list | `allowed-tools` in SKILL.md |
| **Agent types** | 5 built-in (general, explore, plan, verify, guide) | Custom skills as agents |
| **Memory** | agentMemory + agentMemorySnapshot | Shared memory files (.claude/memory/) |
| **Verification** | Built-in verificationAgent | /critic skill |
| **Persistence** | Session store (JSON) | Checkpoint files (markdown) |
| **Streaming** | Native event stream | N/A (tool results) |
| **Coordinator** | COORDINATOR_MODE (not yet implemented) | /orchestrate skill |

### Porovnání s STOPA /orchestrate (rozšířené)

| Aspekt | CC native | STOPA |
|--------|-----------|-------|
| **Coordinator tool access** | OMEZENÝ (Agent, SendMessage, TaskStop only) | PLNÝ (orchestrátor má přístup ke všemu) |
| **Budget tiers** | Žádné — lineární škálování, max 16 iterations | 4 tiers: light/standard/deep/farm |
| **Circuit breakers** | Implicitní (turn/iteration caps) | Explicitní: 3× agent loop, 2× critic FAIL, depth > 2 |
| **Error classification** | Žádná — teammate prostě zastaví | 3 kategorie: infrastructure/transient/logic |
| **Communication** | Star topology (COORDINATOR) nebo mesh (Teams) | Shared memory files |
| **Plan approval** | Nativní gate (plan mode → approve/reject) | Manuální — orchestrátor se ptá na high-level plan |
| **Quality hooks** | TaskCompleted hook, exit code 2 = reject | /critic skill, verify-before-done rule |
| **Context isolation** | Nativní — každý subagent vlastní context window | Ruční — sub-agenti sdílí kontext hlavní session |

**CC je silnější v:** tool restriction pro koordinátora, plan approval gate, nativní context isolation
**STOPA je silnější v:** error classification, budget tiers, circuit breaker logika, memory persistence

### Doporučení pro STOPA orchestrace

1. **TOOL RESTRICTION PRO ORCHESTRÁTOR** (highest priority) — /orchestrate by neměl mít přístup k Bash/Edit/Write. Nutí delegaci místo "udělám sám". Implementace: `allowed-tools: [Agent, Read, Grep, Glob]` v SKILL.md
2. **Plan approval gate** — sub-agent v plan mode musí dostat schválení od orchestrátora před implementací. Redukuje waste.
3. **TaskCompleted hook pattern** — hook ověřuje kvalitu výstupu agenta. Exit code 2 = reject + feedback. Elegantní náhrada za critic-loop.
4. **Structured turn results** — sub-agenti vrací JSON `{result, confidence, findings}` místo raw markdown
5. **Streaming events** — pro KAIROS: `subtask_start`, `budget_warning`, `circuit_break`
6. **Budget jako token count** — doplnit /budget o token-level tracking (ccusage integration)

---

## Shrnutí — Top 6 Actionable Items pro STOPA

### Priorita 1: Orchestrátor Tool Restriction (**game-changer**)
- /orchestrate NESMÍ mít Bash/Edit/Write — jen Agent, Read, Grep, Glob
- Vzor z COORDINATOR_MODE: koordinátor deleguje, nepracuje sám
- Implementace: `allowed-tools: [Agent, Read, Grep, Glob, TodoWrite]` v SKILL.md
- **Proč:** Odstraní antipattern kde orchestrátor dělá práci místo delegace

### Priorita 2: Security Model Enhancement
- Přidat `deny_tools:` field do SKILL.md YAML frontmatter
- Runtime enforcement: skill dostane jen tools z `allowed-tools`, zbytek je denied
- BashTool klasifikace: `safe/risky/destructive` pro hook-based gating

### Priorita 3: Plan Approval Gate
- Sub-agent spuštěný v plan mode → pošle plán orchestrátoru → approve/reject
- Redukuje waste z špatně naplánované práce
- Vzor: CC Agent Teams TaskCreated hook s exit code 2

### Priorita 4: MCP Builder Rozšíření
- Templates pro všech 6 transportů (stdio, SSE, HTTP, WebSocket, SDK, ClaudeAiProxy)
- OAuth PKCE ready-to-use template pro remote MCP
- Transport selection decision tree
- Config hash validation pattern

### Priorita 5: Structured Agent Output
- Sub-agenti vrací JSON: `{result, confidence, findings, suggestions}`
- Lepší parsing, aggregace, decision-making v orchestrátoru
- Nahrazuje "interpretuj raw markdown" guessing

### Priorita 6: Event-Based Agent Communication
- Připrava na KAIROS: event stream pattern pro agent lifecycle
- Events: `agent_start`, `subtask_complete`, `budget_warning`, `circuit_break`
- TaskCompleted hook pattern: exit code 2 = reject + feedback
