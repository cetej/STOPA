#!/usr/bin/env python3
"""memstore — direct CLI for Anthropic Managed Memory store.

Bypass for when CC's MCP integration isn't loading the bridge tools into
the tool list. This script lets you read/write/list memories directly
from the terminal — no MCP, no CC restart needed.

Usage:
    python scripts/memstore.py list                       # list all memories
    python scripts/memstore.py list /decisions/           # filter by path prefix
    python scripts/memstore.py read /decisions/2026.md    # read content
    python scripts/memstore.py write /test/foo.md "hello" # create or update
    python scripts/memstore.py write /path/file.md @file.txt  # write content from file
    python scripts/memstore.py delete /test/foo.md        # delete by path
    python scripts/memstore.py versions /path/file.md     # list versions
    python scripts/memstore.py info                       # store metadata
    python scripts/memstore.py stores                     # list all stores in org

Env vars (any one works — first match wins):
    STOPA_MEMSTORE_ID           explicit store id
    .claude/settings.local.json env.STOPA_MEMSTORE_ID  (auto-loaded)

API key resolution (first match wins):
    ANTHROPIC_API_KEY env var
    ~/.claude/keys/secrets.env  (line: ANTHROPIC_API_KEY=...)

Exit codes:
    0  success
    1  config / auth error
    2  API error (network, 4xx, 5xx)
    3  not found (read/delete on missing path)
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "stopa-memory-mcp"))

BETA = "managed-agents-2026-04-01"


def _load_store_id() -> str:
    """Resolve store_id: env first, then settings.local.json fallback."""
    sid = os.environ.get("STOPA_MEMSTORE_ID", "")
    if sid:
        return sid
    settings = PROJECT_ROOT / ".claude" / "settings.local.json"
    if settings.exists():
        try:
            data = json.loads(settings.read_text(encoding="utf-8"))
            return data.get("env", {}).get("STOPA_MEMSTORE_ID", "")
        except (OSError, json.JSONDecodeError):
            pass
    return ""


def _client():
    """Anthropic client with secrets.env fallback (cross-shell on Windows)."""
    import anthropic  # type: ignore

    api_key = os.environ.get("ANTHROPIC_API_KEY", "")
    if not api_key:
        secrets = Path.home() / ".claude" / "keys" / "secrets.env"
        if secrets.exists():
            for line in secrets.read_text(encoding="utf-8").splitlines():
                if line.startswith("ANTHROPIC_API_KEY="):
                    api_key = line.split("=", 1)[1].strip().strip('"').strip("'")
                    break
    if not api_key:
        print("ERROR: ANTHROPIC_API_KEY not found in env or ~/.claude/keys/secrets.env", file=sys.stderr)
        sys.exit(1)
    return anthropic.Anthropic(api_key=api_key)


def _find_id(client, store_id: str, path: str) -> str | None:
    page = client.beta.memory_stores.memories.list(
        memory_store_id=store_id, path_prefix=path, limit=20, betas=[BETA]
    )
    for m in page.data:
        if m.path == path:
            return m.id
    return None


def cmd_stores(_args, client, _store_id) -> int:
    page = client.beta.memory_stores.list(limit=50, betas=[BETA])
    if not page.data:
        print("(no stores)")
        return 0
    print(f"{'STORE ID':<40} {'NAME':<40} CREATED")
    for s in page.data:
        print(f"{s.id:<40} {s.name:<40} {s.created_at}")
    return 0


def cmd_info(_args, client, store_id) -> int:
    s = client.beta.memory_stores.retrieve(memory_store_id=store_id, betas=[BETA])
    print(f"id:          {s.id}")
    print(f"name:        {s.name}")
    print(f"description: {getattr(s, 'description', None)}")
    print(f"created_at:  {s.created_at}")
    return 0


def cmd_list(args, client, store_id) -> int:
    kwargs = {"memory_store_id": store_id, "limit": args.limit, "order": args.order, "betas": [BETA]}
    if args.prefix:
        kwargs["path_prefix"] = args.prefix
    page = client.beta.memory_stores.memories.list(**kwargs)
    if not page.data:
        print(f"(no memories{' under ' + args.prefix if args.prefix else ''})")
        return 0
    print(f"{'PATH':<60} {'BYTES':>8} CREATED")
    for m in page.data:
        size = getattr(m, "size_bytes", "—")
        print(f"{m.path:<60} {str(size):>8} {getattr(m, 'created_at', '')}")
    print(f"\n{len(page.data)} memories in {store_id}")
    return 0


def cmd_read(args, client, store_id) -> int:
    mid = _find_id(client, store_id, args.path)
    if not mid:
        print(f"NOT FOUND: {args.path}", file=sys.stderr)
        return 3
    m = client.beta.memory_stores.memories.retrieve(memory_id=mid, memory_store_id=store_id, betas=[BETA])
    print(getattr(m, "content", ""))
    return 0


def cmd_write(args, client, store_id) -> int:
    content = args.content
    if content.startswith("@"):
        content = Path(content[1:]).read_text(encoding="utf-8")

    mid = _find_id(client, store_id, args.path)
    if mid:
        m = client.beta.memory_stores.memories.update(
            memory_id=mid, memory_store_id=store_id, content=content, betas=[BETA]
        )
        op = "updated"
    else:
        m = client.beta.memory_stores.memories.create(
            memory_store_id=store_id, content=content, path=args.path, betas=[BETA]
        )
        op = "created"
    print(f"{op}: {m.path}  (memory_id={m.id}, {len(content)} bytes)")
    return 0


def cmd_delete(args, client, store_id) -> int:
    mid = _find_id(client, store_id, args.path)
    if not mid:
        print(f"NOT FOUND: {args.path}", file=sys.stderr)
        return 3
    client.beta.memory_stores.memories.delete(memory_id=mid, memory_store_id=store_id, betas=[BETA])
    print(f"deleted: {args.path}")
    return 0


def cmd_versions(args, client, store_id) -> int:
    mid = _find_id(client, store_id, args.path)
    if not mid:
        print(f"NOT FOUND: {args.path}", file=sys.stderr)
        return 3
    page = client.beta.memory_stores.memory_versions.list(
        memory_id=mid, memory_store_id=store_id, limit=20, betas=[BETA]
    )
    print(f"{'VERSION ID':<40} {'BYTES':>8} CREATED")
    for v in page.data:
        size = getattr(v, "size_bytes", "—")
        print(f"{v.id:<40} {str(size):>8} {getattr(v, 'created_at', '')}")
    print(f"\n{len(page.data)} versions of {args.path}")
    return 0


def main() -> int:
    p = argparse.ArgumentParser(description="Direct CLI for Anthropic Managed Memory store")
    sub = p.add_subparsers(dest="cmd", required=True)

    sub.add_parser("stores", help="list all stores in org")
    sub.add_parser("info", help="show current store metadata")

    p_list = sub.add_parser("list", help="list memories")
    p_list.add_argument("prefix", nargs="?", default="", help="path prefix filter")
    p_list.add_argument("--limit", type=int, default=50)
    p_list.add_argument("--order", choices=["asc", "desc"], default="desc")

    p_read = sub.add_parser("read", help="read memory by path")
    p_read.add_argument("path")

    p_write = sub.add_parser("write", help="write memory (create or update)")
    p_write.add_argument("path")
    p_write.add_argument("content", help='literal text or @filename to read content from file')

    p_del = sub.add_parser("delete", help="delete memory by path")
    p_del.add_argument("path")

    p_ver = sub.add_parser("versions", help="list version history of a memory")
    p_ver.add_argument("path")

    args = p.parse_args()

    client = _client()

    # `stores` works without store_id; everything else needs it
    if args.cmd == "stores":
        return cmd_stores(args, client, None)

    store_id = _load_store_id()
    if not store_id:
        print("ERROR: STOPA_MEMSTORE_ID not set (env or settings.local.json)", file=sys.stderr)
        return 1

    handlers = {
        "info": cmd_info,
        "list": cmd_list,
        "read": cmd_read,
        "write": cmd_write,
        "delete": cmd_delete,
        "versions": cmd_versions,
    }
    return handlers[args.cmd](args, client, store_id)


if __name__ == "__main__":
    sys.exit(main())
