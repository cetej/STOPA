# MCP Transport Patterns Reference

Source: Claw Code architecture analysis (2026-04-04), CC source leak, official MCP spec.

## Transport Selection Decision Tree

```
What kind of MCP server are you building?
│
├─ Local CLI tool / subprocess
│  └─ **Stdio** — spawn process, communicate via stdin/stdout
│     - Auth: env vars for secrets
│     - Config: { "command": "python", "args": ["-m", "myserver"], "env": {} }
│     - Timeout: toolCallTimeoutMs (default 60s, configurable per-server)
│
├─ Remote API / cloud service
│  ├─ Need bidirectional real-time?
│  │  └─ **WebSocket** — full-duplex, headers auth
│  │     - Config: { "type": "ws", "url": "wss://...", "headers": {} }
│  │     - No OAuth support — use header tokens or headersHelper script
│  │
│  └─ Standard request/response?
│     └─ **HTTP (streamable)** — modern MCP standard
│        - Config: { "type": "http", "url": "https://...", "oauth": { "clientId": "...", "callbackPort": 3000 } }
│        - Full OAuth PKCE support
│        - headersHelper for rotating tokens
│
├─ In-process library (embedded)
│  └─ **SDK** — no URL, no subprocess
│     - Config: { "type": "sdk", "name": "my-embedded-server" }
│     - No auth needed (same process)
│
└─ Anthropic marketplace
   └─ **ManagedProxy** (ClaudeAiProxy)
      - Config: { "type": "claudeai-proxy", "url": "...", "id": "..." }
      - Auth managed by Anthropic
      - URLs proxied through api.anthropic.com/v2/session_ingress/shttp/mcp/
```

## Implementation Patterns

### JSON-RPC Framing (for stdio servers)
Use `Content-Length: N\r\n\r\n{json}` framing, NOT newline-delimited JSON.

### Paginated Tool Discovery
MCP clients send `tools/list` with cursor-based pagination. Your server MUST handle:
```json
// Request
{"method": "tools/list", "params": {"cursor": "abc123"}}
// Response
{"tools": [...], "nextCursor": "def456"}  // null cursor = last page
```

### Config Hashing (FNV-1a)
Clients hash server configs for dedup and change detection. If your config changes, clients detect it and reconnect.

### Tool Name Normalization
Clients prefix tool names: `mcp__{server_name}__{tool_name}`. Non-alphanumeric chars → `_`.
Your server should NOT assume its tool names arrive unmodified.

### Graceful Degradation
If your server has multiple tools and one fails, return partial results for the others. Clients support `McpDegradedReport` — they continue with available tools.

### headersHelper Pattern (for remote servers)
Clients support an external script that dynamically generates auth headers:
```json
{
  "type": "http",
  "url": "https://api.example.com/mcp",
  "headersHelper": "/path/to/token-rotator.sh"
}
```
Script returns JSON: `{"Authorization": "Bearer <rotated-token>"}`

### OAuth PKCE Template (for SSE/HTTP servers)
```json
{
  "type": "http",
  "url": "https://api.example.com/mcp",
  "oauth": {
    "clientId": "my-mcp-client",
    "callbackPort": 3000,
    "authServerMetadataUrl": "https://auth.example.com/.well-known/oauth-authorization-server"
  }
}
```

### structuredContent Extension
Tool results can include both human-readable `content` and machine-parseable `structuredContent`:
```json
{
  "content": [{"type": "text", "text": "Found 3 results"}],
  "structuredContent": {"results": [...], "count": 3}
}
```

## Timeouts (recommended defaults)
| Operation | Default | Notes |
|-----------|---------|-------|
| initialize | 10s | Connection handshake |
| tools/list | 30s | Tool discovery |
| tools/call | 60s | Configurable per-server via toolCallTimeoutMs |

## Error Handling
| Error Type | Retryable? | Action |
|-----------|-----------|--------|
| Transport | Yes (1x) | Reset server, retry |
| Timeout | Yes (1x) | Reset server, retry |
| JsonRpc | No | Log error, propagate |
| InvalidResponse | No | Reset server, propagate |
| UnknownTool | No | Routing failure — check tool names |
