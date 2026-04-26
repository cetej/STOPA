---
date: 2026-04-25
type: bug_fix
severity: high
component: hook
tags: [mcp, settings, claude-code, config]
summary: "Claude Code MCP servers must be registered in ~/.claude/mcp.json (user-global) or .mcp.json (project-local), NOT in settings.local.json mcpServers block. The settings.local.json mcpServers field is silently ignored — symptoms: tools never appear in deferred tool list after restart."
source: critic_finding
uses: 6
successful_uses: 0
harmful_uses: 0
confidence: 1.00
maturity: validated
verify_check: "Grep('mcpServers', path='~/.claude.json') → 1+ matches"
skill_scope: []
related: [2026-03-27-secrets-in-config-files.md, 2026-03-27-playwright-mcp-download-hijack.md, 2026-04-14-mcp-server-token-overhead.md]
---

## Problém

While integrating `stopa-memory-mcp` bridge after PR #29, registered the MCP server in `.claude/settings.local.json` under `mcpServers` key. After restart, tools `mcp__stopa-memory__memstore_*` never appeared in the deferred tool list — `ToolSearch` returned "No matching deferred tools found".

The server module loaded fine standalone (9 tools registered with FastMCP, 6/6 mock tests passing), but Claude Code's MCP discovery never picked it up.

## Root Cause

Claude Code reads MCP server registrations from `~/.claude.json` (user-global, top-level `mcpServers` key + per-project `projects[<path>].mcpServers`). The legacy `~/.claude/mcp.json` file exists but is NOT loaded by current CC (verified 2026-04-25 via `claude mcp list` — file had 8 servers, list returned 4 correct ones from `.claude.json` only).

Wrong locations CC silently ignores:
- `~/.claude/mcp.json` — orphan file, not loaded
- `.claude/settings.local.json` `mcpServers` block — never read
- `.claude/settings.json` `mcpServers` block — never read

There is no warning, no error, just empty MCP discovery. Symptoms: tools never appear in deferred tool list, `claude mcp list` doesn't show the server.

## Řešení

**Use the CLI command — DO NOT edit JSON manually:**

```bash
claude mcp add-json <name> '{"command":"python","args":["/abs/path/server.py"],"env":{"VAR":"value"}}'
```

This writes to `~/.claude.json` in the correct format. Verify with `claude mcp list` immediately:
```bash
claude mcp list
# Should show: <name>: <command> <args> - ✓ Connected
```

If `✓ Connected` shown → registration succeeded. Restart CC for tools to appear in deferred tool list. Verify via `ToolSearch({query: "<name>", max_results: 10})`.

Manual JSON edit alternative (if CLI unavailable): edit `~/.claude.json`, add to top-level `mcpServers` object. Same format as CLI writes.

NEVER put API keys in this JSON — server should fall back to `~/.claude/keys/secrets.env` (see `reference_anthropic_key.md`).

## Prevence

- Before publishing a new MCP server's setup docs: confirm the example points to `~/.claude/mcp.json`, not `settings.local.json`.
- Add lint check to `verify-sweep.py` §Y: if `settings.local.json` contains `mcpServers` key, flag warning ("MCP config in wrong location").
- Skill `update-config` should reject `mcpServers` modifications in settings.json files and route to `~/.claude/mcp.json` automatically.

## References

- Discovered during issue #26 bridge integration (2026-04-25 session)
- `claude --help` output: `--mcp-config <configs...>` flag points to JSON files, not settings
- `claude mcp` subcommand exists for managing servers via CLI (alternative to manual JSON edit)
