# stopa-memory-mcp

MCP bridge that exposes Anthropic's [Managed Agents Memory](https://platform.claude.com/docs/en/managed-agents/memory) (public beta, April 2026) to Claude Code sessions.

## Why this exists

Anthropic's Managed Agents Memory stores mount at `/mnt/memory/<store>/` inside Platform-API session containers. Claude Code sessions cannot mount these directly — they aren't Managed Agent sessions. This bridge solves that with REST: the same memory store, reachable from CC over MCP.

This means STOPA skills (`/scribe`, `/handoff`, `/checkpoint`) can dual-write to local `.claude/memory/` AND a remote Managed Agent store, giving us versioned audit trail + future interop with hosted agents — without abandoning the local-first model.

Tracking issue: [cetej/STOPA#26](https://github.com/cetej/STOPA/issues/26)
Feasibility report: `outputs/managed-agents-memory-cc-fit-2026-04-25.md`

## Install

```bash
pip install 'anthropic>=0.97.0' fastmcp mcp
```

## Configure

Set environment variables (typically in `.claude/settings.local.json`, never checked in):

| Var | Required | Purpose |
|-----|----------|---------|
| `ANTHROPIC_API_KEY` | yes | API key with Managed Agents beta access |
| `STOPA_MEMSTORE_ID` | optional | Default store ID for tools without explicit `store_id` |

Add to `.claude/settings.local.json`:

```json
{
  "mcpServers": {
    "stopa-memory": {
      "command": "python",
      "args": ["C:/Users/stock/Documents/000_NGM/STOPA/stopa-memory-mcp/server.py"],
      "env": {
        "ANTHROPIC_API_KEY": "sk-ant-...",
        "STOPA_MEMSTORE_ID": "memstore_..."
      }
    }
  }
}
```

Restart Claude Code. The bridge tools appear with prefix `mcp__stopa-memory__memstore_*`.

## First-time setup

1. Create a store (one-time, from CC after install):
   ```
   memstore_create_store(name="stopa-shared-memory")
   ```
2. Copy the returned `id` (looks like `memstore_01abc...`).
3. Add it as `STOPA_MEMSTORE_ID` in settings.local.json.
4. Restart CC. All path-based tools now default to that store.

## Tools

Store operations:

| Tool | Description |
|------|-------------|
| `memstore_list_stores` | List all stores in org |
| `memstore_create_store(name, description?)` | Create new store |
| `memstore_get_store(store_id?)` | Get store details |
| `memstore_archive_store(store_id)` | Soft-delete store |

Memory operations (path-based, like a filesystem):

| Tool | Description |
|------|-------------|
| `memstore_list_memories(path_prefix?, store_id?, limit, order)` | List memories, optionally filtered by path prefix |
| `memstore_read_memory(path, store_id?)` | Read memory content by exact path |
| `memstore_write_memory(path, content, store_id?)` | Create or update memory at path |
| `memstore_delete_memory(path, store_id?)` | Delete memory (versions kept 30 days) |
| `memstore_list_versions(path, store_id?, limit)` | List version history |

All path-based tools accept an optional `store_id`. If omitted, the bridge uses `STOPA_MEMSTORE_ID` from env.

## Beta limits (April 2026)

- 1,000 stores per org
- 2,000 memories per store
- 100 MB per store, 100 kB per memory
- 30-day version retention

## Future integration in STOPA skills

Planned dual-write pattern (not yet implemented in skills — bridge only for now):

```python
# /scribe — capture decision
local_path = ".claude/memory/decisions.md"
Edit(file_path=local_path, ...)            # always
memstore_write_memory(path=local_path, content=..., store_id=...)  # if bridge configured
```

This lives in skill SKILL.md as opt-in step gated on bridge availability detection.

## Risks

**Pricing not yet announced.** Beta is currently free; Anthropic may bill per-MB or per-version at GA. Watch [WaveSpeedAI pricing tracker](https://wavespeed.ai/blog/posts/claude-managed-agents-pricing-2026/).

**Native CC integration may land.** Anthropic could ship first-class CC ↔ memstore in next CC release, making this bridge redundant. Watch [CC changelog](https://docs.claude.com/en/docs/claude-code/changelog) — if integration arrives, deprecate this bridge.
