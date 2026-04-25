#!/usr/bin/env python3
"""STOPA Memory Bridge — MCP server for Anthropic Managed Agents Memory.

Exposes Anthropic's beta `/v1/memory_stores` API to Claude Code as MCP tools.
Allows STOPA skills (/scribe, /handoff, /checkpoint) to dual-write memories
to local `.claude/memory/` AND remote Managed Agent stores.

Why a bridge: Claude Managed Agents Memory mounts at `/mnt/memory/<store>/`
inside Anthropic-hosted Platform-API session containers — Claude Code
sessions cannot mount these directly. This bridge gives CC sessions the
same store via REST API, so memories can be shared between local CC work
and future hosted Managed Agent runs.

Issue: cetej/STOPA#26
Docs: https://platform.claude.com/docs/en/managed-agents/memory
SDK:  anthropic>=0.97.0 (client.beta.memory_stores)

Configuration (env vars):
    ANTHROPIC_API_KEY    Required — your Anthropic API key.
    STOPA_MEMSTORE_ID    Optional — default store_id for path-based ops.
                         Set this so tools without explicit store_id work.

Beta header `managed-agents-2026-04-01` is auto-applied by the SDK on
all memory_stores calls.

Usage as Claude Code MCP server (add to .claude/settings.local.json):
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
"""
from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import Any

from fastmcp import FastMCP

try:
    import anthropic
except ImportError as exc:
    print(
        "ERROR: anthropic SDK not installed. Run: pip install 'anthropic>=0.97.0'",
        file=sys.stderr,
    )
    raise SystemExit(1) from exc

if anthropic.__version__ < "0.97":
    print(
        f"WARNING: anthropic {anthropic.__version__} may not expose memory_stores. "
        "Upgrade with: pip install 'anthropic>=0.97.0'",
        file=sys.stderr,
    )

BETA_HEADER = "managed-agents-2026-04-01"
DEFAULT_STORE_ID = os.environ.get("STOPA_MEMSTORE_ID", "")

mcp = FastMCP("stopa-memory")


def _load_key_from_secrets_file() -> str:
    """Fallback: read ANTHROPIC_API_KEY from ~/.claude/keys/secrets.env.

    Windows User-scope env vars don't always propagate to MCP subprocesses
    started by Claude Code. The secrets.env file is the canonical fallback
    (gitignored, central store across all STOPA projects).
    """
    secrets_path = Path.home() / ".claude" / "keys" / "secrets.env"
    if not secrets_path.exists():
        return ""
    try:
        for line in secrets_path.read_text(encoding="utf-8").splitlines():
            if line.startswith("ANTHROPIC_API_KEY="):
                return line.split("=", 1)[1].strip().strip('"').strip("'")
    except OSError:
        pass
    return ""


def _client() -> anthropic.Anthropic:
    """Lazy-construct Anthropic client.

    Resolution order: env var first, secrets.env file as fallback. Errors
    surface as MCP error responses.
    """
    api_key = os.environ.get("ANTHROPIC_API_KEY", "") or _load_key_from_secrets_file()
    if not api_key:
        raise RuntimeError(
            "ANTHROPIC_API_KEY not found. Checked: $ANTHROPIC_API_KEY, "
            "~/.claude/keys/secrets.env. Set one of these to use the bridge."
        )
    return anthropic.Anthropic(api_key=api_key)


def _resolve_store(store_id: str | None) -> str:
    """Use provided store_id, or fall back to STOPA_MEMSTORE_ID env."""
    sid = store_id or DEFAULT_STORE_ID
    if not sid:
        raise ValueError(
            "No store_id provided and STOPA_MEMSTORE_ID env not set. "
            "Pass store_id explicitly or configure the default in settings."
        )
    return sid


def _find_memory_id(store_id: str, path: str) -> str | None:
    """Return memory_id for exact path match within a store, or None."""
    client = _client()
    page = client.beta.memory_stores.memories.list(
        memory_store_id=store_id,
        path_prefix=path,
        limit=20,
        betas=[BETA_HEADER],
    )
    for mem in page.data:
        if mem.path == path:
            return mem.id
    return None


# ─────────────────────────────────────────────────────────────────────────────
# Store-level operations
# ─────────────────────────────────────────────────────────────────────────────

@mcp.tool()
def memstore_list_stores(include_archived: bool = False, limit: int = 50) -> dict:
    """List all memory stores in the org.

    Args:
        include_archived: include archived stores (default False)
        limit: max stores to return (default 50)

    Returns dict with `stores` list (each: id, name, description, created_at).
    """
    client = _client()
    page = client.beta.memory_stores.list(
        include_archived=include_archived,
        limit=limit,
        betas=[BETA_HEADER],
    )
    return {
        "stores": [
            {
                "id": s.id,
                "name": s.name,
                "description": getattr(s, "description", None),
                "created_at": str(s.created_at),
            }
            for s in page.data
        ],
        "default_store_id": DEFAULT_STORE_ID or None,
    }


@mcp.tool()
def memstore_create_store(name: str, description: str = "") -> dict:
    """Create a new memory store.

    Args:
        name: human-readable store name (e.g. "stopa-shared-memory")
        description: optional description

    Returns the new store's id and metadata.
    """
    client = _client()
    kwargs: dict[str, Any] = {"name": name, "betas": [BETA_HEADER]}
    if description:
        kwargs["description"] = description
    store = client.beta.memory_stores.create(**kwargs)
    return {
        "id": store.id,
        "name": store.name,
        "description": getattr(store, "description", None),
        "created_at": str(store.created_at),
    }


@mcp.tool()
def memstore_get_store(store_id: str | None = None) -> dict:
    """Get details of a memory store (uses STOPA_MEMSTORE_ID if not provided)."""
    sid = _resolve_store(store_id)
    client = _client()
    store = client.beta.memory_stores.retrieve(memory_store_id=sid, betas=[BETA_HEADER])
    return {
        "id": store.id,
        "name": store.name,
        "description": getattr(store, "description", None),
        "created_at": str(store.created_at),
        "metadata": getattr(store, "metadata", {}),
    }


@mcp.tool()
def memstore_archive_store(store_id: str) -> dict:
    """Archive a store (soft delete — memories preserved, store hidden by default)."""
    client = _client()
    archived = client.beta.memory_stores.archive(
        memory_store_id=store_id, betas=[BETA_HEADER]
    )
    return {"id": archived.id, "archived_at": str(getattr(archived, "archived_at", ""))}


# ─────────────────────────────────────────────────────────────────────────────
# Memory-level operations (path-based for STOPA filesystem ergonomics)
# ─────────────────────────────────────────────────────────────────────────────

@mcp.tool()
def memstore_list_memories(
    path_prefix: str = "",
    store_id: str | None = None,
    limit: int = 50,
    order: str = "desc",
) -> dict:
    """List memories in a store, optionally filtered by path prefix.

    Args:
        path_prefix: only return memories whose path starts with this (default: all)
        store_id: target store (uses STOPA_MEMSTORE_ID if omitted)
        limit: max memories to return
        order: 'asc' or 'desc' by created_at

    Returns dict with `memories` list (each: id, path, created_at, size_bytes).
    """
    sid = _resolve_store(store_id)
    client = _client()
    kwargs: dict[str, Any] = {
        "memory_store_id": sid,
        "limit": limit,
        "order": order,
        "betas": [BETA_HEADER],
    }
    if path_prefix:
        kwargs["path_prefix"] = path_prefix
    page = client.beta.memory_stores.memories.list(**kwargs)
    return {
        "store_id": sid,
        "memories": [
            {
                "id": m.id,
                "path": m.path,
                "created_at": str(getattr(m, "created_at", "")),
                "size_bytes": getattr(m, "size_bytes", None),
            }
            for m in page.data
        ],
    }


@mcp.tool()
def memstore_read_memory(path: str, store_id: str | None = None) -> dict:
    """Read memory content by exact path.

    Args:
        path: memory path (e.g. "/decisions/2026-04-25.md")
        store_id: target store (uses STOPA_MEMSTORE_ID if omitted)

    Returns {found: bool, path, content, memory_id, version_id} or {found: False}.
    """
    sid = _resolve_store(store_id)
    memory_id = _find_memory_id(sid, path)
    if not memory_id:
        return {"found": False, "path": path, "store_id": sid}

    client = _client()
    mem = client.beta.memory_stores.memories.retrieve(
        memory_id=memory_id, memory_store_id=sid, betas=[BETA_HEADER]
    )
    return {
        "found": True,
        "memory_id": mem.id,
        "path": mem.path,
        "content": getattr(mem, "content", None),
        "version_id": getattr(mem, "version_id", None),
        "store_id": sid,
    }


@mcp.tool()
def memstore_write_memory(path: str, content: str, store_id: str | None = None) -> dict:
    """Write memory at path (create new or update existing).

    Args:
        path: memory path (e.g. "/decisions/2026-04-25.md")
        content: memory content (max 100 kB per memory in beta)
        store_id: target store (uses STOPA_MEMSTORE_ID if omitted)

    Returns {operation: 'created'|'updated', memory_id, path, version_id}.
    """
    sid = _resolve_store(store_id)
    client = _client()
    memory_id = _find_memory_id(sid, path)

    if memory_id:
        mem = client.beta.memory_stores.memories.update(
            memory_id=memory_id,
            memory_store_id=sid,
            content=content,
            betas=[BETA_HEADER],
        )
        op = "updated"
    else:
        mem = client.beta.memory_stores.memories.create(
            memory_store_id=sid,
            content=content,
            path=path,
            betas=[BETA_HEADER],
        )
        op = "created"

    return {
        "operation": op,
        "memory_id": mem.id,
        "path": mem.path,
        "version_id": getattr(mem, "version_id", None),
        "store_id": sid,
    }


@mcp.tool()
def memstore_delete_memory(path: str, store_id: str | None = None) -> dict:
    """Delete memory at path. Path versions are preserved per Anthropic's 30-day retention.

    Args:
        path: memory path to delete
        store_id: target store (uses STOPA_MEMSTORE_ID if omitted)
    """
    sid = _resolve_store(store_id)
    memory_id = _find_memory_id(sid, path)
    if not memory_id:
        return {"deleted": False, "reason": "path not found", "path": path}

    client = _client()
    client.beta.memory_stores.memories.delete(
        memory_id=memory_id, memory_store_id=sid, betas=[BETA_HEADER]
    )
    return {"deleted": True, "path": path, "memory_id": memory_id, "store_id": sid}


@mcp.tool()
def memstore_list_versions(path: str, store_id: str | None = None, limit: int = 20) -> dict:
    """List version history of a memory at path. Versions retained 30 days in beta.

    Args:
        path: memory path
        store_id: target store
        limit: max versions to return
    """
    sid = _resolve_store(store_id)
    memory_id = _find_memory_id(sid, path)
    if not memory_id:
        return {"path": path, "versions": [], "found": False}

    client = _client()
    page = client.beta.memory_stores.memory_versions.list(
        memory_id=memory_id,
        memory_store_id=sid,
        limit=limit,
        betas=[BETA_HEADER],
    )
    return {
        "path": path,
        "memory_id": memory_id,
        "found": True,
        "versions": [
            {
                "version_id": v.id,
                "created_at": str(getattr(v, "created_at", "")),
                "size_bytes": getattr(v, "size_bytes", None),
            }
            for v in page.data
        ],
    }


# ─────────────────────────────────────────────────────────────────────────────
# Entry point
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    mcp.run()
