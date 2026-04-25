#!/usr/bin/env python3
"""Live integration test for stopa-memory-mcp.

Validates the bridge against real Anthropic API. Run this once after
configuring ANTHROPIC_API_KEY to confirm SDK call paths work end-to-end.

Cycle: list_stores -> create test store -> write memory -> read it back
       -> list versions -> delete memory -> archive store -> verify.

Usage:
    export ANTHROPIC_API_KEY=sk-ant-...
    python live_test.py

Costs: minimal (1 store create, 1 memory write, ~5 reads/lists, archive).
       Beta is currently free; this would be a few cents at expected GA pricing.

Exit codes:
    0  all stages passed — bridge is live-ready
    1  network/API error — check API key + beta access
    2  unexpected response shape — SDK may have drifted
"""
from __future__ import annotations

import os
import sys
import time
import traceback
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

if not os.environ.get("ANTHROPIC_API_KEY"):
    print("ERROR: ANTHROPIC_API_KEY not set in environment.")
    print("  PowerShell: $env:ANTHROPIC_API_KEY = 'sk-ant-...'")
    print("  bash:       export ANTHROPIC_API_KEY=sk-ant-...")
    sys.exit(1)

import server  # noqa: E402

OK = "[OK]"
FAIL = "[FAIL]"
INFO = "[..]"


def log(prefix: str, msg: str) -> None:
    print(f"  {prefix} {msg}")


def main() -> int:
    test_store_name = f"stopa-bridge-livetest-{datetime.utcnow():%Y%m%d-%H%M%S}"
    test_path = f"/livetest/{int(time.time())}.md"
    test_content = f"# Live test\n\nTimestamp: {datetime.utcnow().isoformat()}Z\n"

    print(f"\n{'═' * 60}")
    print(f"  stopa-memory-mcp LIVE TEST")
    print(f"  Store name: {test_store_name}")
    print(f"  Memory path: {test_path}")
    print(f"{'═' * 60}\n")

    store_id = ""

    try:
        # Stage 1: list existing stores
        log(INFO, "1/7 list_stores")
        result = server.memstore_list_stores(limit=5)
        log(OK, f"     found {len(result['stores'])} existing store(s)")

        # Stage 2: create test store
        log(INFO, "2/7 create_store")
        result = server.memstore_create_store(
            name=test_store_name,
            description="Bridge live-test artifact, safe to delete",
        )
        store_id = result["id"]
        log(OK, f"     created {store_id}")

        # Stage 3: get store details
        log(INFO, "3/7 get_store")
        result = server.memstore_get_store(store_id=store_id)
        if result["id"] != store_id:
            log(FAIL, f"     store_id mismatch: {result['id']} != {store_id}")
            return 2
        log(OK, f"     name={result['name']!r}")

        # Stage 4: write memory
        log(INFO, "4/7 write_memory")
        result = server.memstore_write_memory(
            path=test_path, content=test_content, store_id=store_id
        )
        if result["operation"] != "created":
            log(FAIL, f"     expected operation=created, got {result['operation']}")
            return 2
        log(OK, f"     {result['operation']} memory_id={result['memory_id']}")

        # Stage 5: read it back
        log(INFO, "5/7 read_memory")
        result = server.memstore_read_memory(path=test_path, store_id=store_id)
        if not result["found"]:
            log(FAIL, "     memory not found after write")
            return 2
        if result["content"] != test_content:
            log(FAIL, "     content roundtrip mismatch")
            return 2
        log(OK, f"     content roundtrip OK ({len(result['content'])} bytes)")

        # Stage 6: list versions
        log(INFO, "6/7 list_versions")
        result = server.memstore_list_versions(path=test_path, store_id=store_id)
        log(OK, f"     {len(result['versions'])} version(s) recorded")

        # Stage 7: delete and archive
        log(INFO, "7/7 delete_memory + archive_store")
        result = server.memstore_delete_memory(path=test_path, store_id=store_id)
        if not result["deleted"]:
            log(FAIL, f"     delete failed: {result.get('reason')}")
            return 2
        server.memstore_archive_store(store_id=store_id)
        log(OK, "     test memory deleted, store archived")

    except Exception as exc:
        print()
        log(FAIL, f"stage failed: {type(exc).__name__}: {exc}")
        print()
        traceback.print_exc()
        if store_id:
            print(f"\n  CLEANUP: archive store manually if needed: {store_id}")
        return 1

    print()
    print(f"  All 7 stages passed — bridge is live-ready.")
    print(f"  Bridge: stopa-memory-mcp/server.py")
    print(f"  Add to .claude/settings.local.json under mcpServers.stopa-memory")
    print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
