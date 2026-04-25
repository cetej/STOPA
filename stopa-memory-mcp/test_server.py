#!/usr/bin/env python3
"""Mock-based smoke tests for stopa-memory-mcp server.

Verifies SDK call paths and helper logic without making real API calls.
Run: python test_server.py
"""
from __future__ import annotations

import os
import sys
from unittest.mock import MagicMock, patch

os.environ["ANTHROPIC_API_KEY"] = "sk-ant-dummy-test-key"
sys.path.insert(0, os.path.dirname(__file__))

import server  # noqa: E402

BETA = "managed-agents-2026-04-01"


def _mock_client_with_empty_pages() -> MagicMock:
    """Build a mock Anthropic client with stub pagination responses."""
    client = MagicMock()
    page = MagicMock()
    page.data = []
    client.beta.memory_stores.list.return_value = page
    client.beta.memory_stores.memories.list.return_value = page
    return client


def test_list_stores_sends_beta_header() -> None:
    """memstore_list_stores must include the managed-agents beta header."""
    client = _mock_client_with_empty_pages()
    with patch.object(server, "_client", return_value=client):
        server.memstore_list_stores(include_archived=False, limit=10)
    call = client.beta.memory_stores.list.call_args.kwargs
    assert BETA in call["betas"], f"beta header missing: {call['betas']}"
    assert call["limit"] == 10


def test_list_memories_requires_store_id() -> None:
    """Without STOPA_MEMSTORE_ID and explicit arg, must raise ValueError."""
    client = _mock_client_with_empty_pages()
    server.DEFAULT_STORE_ID = ""
    with patch.object(server, "_client", return_value=client):
        try:
            server.memstore_list_memories(path_prefix="/x/")
        except ValueError:
            return
        raise AssertionError("expected ValueError when no store_id")


def test_list_memories_with_default_store() -> None:
    """When STOPA_MEMSTORE_ID is set, calls flow through with prefix filter."""
    client = _mock_client_with_empty_pages()
    server.DEFAULT_STORE_ID = "memstore_test123"
    with patch.object(server, "_client", return_value=client):
        server.memstore_list_memories(path_prefix="/decisions/")
    call = client.beta.memory_stores.memories.list.call_args.kwargs
    assert call["memory_store_id"] == "memstore_test123"
    assert call["path_prefix"] == "/decisions/"


def test_write_memory_creates_when_not_exists() -> None:
    """Write to a new path issues memories.create."""
    client = _mock_client_with_empty_pages()
    new = MagicMock(id="mem_new", path="/new.md", version_id="v1")
    client.beta.memory_stores.memories.create.return_value = new
    server.DEFAULT_STORE_ID = "memstore_test123"
    with patch.object(server, "_client", return_value=client):
        result = server.memstore_write_memory(path="/new.md", content="hello")
    assert result["operation"] == "created"
    assert result["memory_id"] == "mem_new"


def test_write_memory_updates_when_exists() -> None:
    """Write to an existing path issues memories.update."""
    client = _mock_client_with_empty_pages()
    existing = MagicMock()
    existing.id = "mem_existing"
    existing.path = "/existing.md"
    client.beta.memory_stores.memories.list.return_value.data = [existing]
    updated = MagicMock(id="mem_existing", path="/existing.md", version_id="v2")
    client.beta.memory_stores.memories.update.return_value = updated
    server.DEFAULT_STORE_ID = "memstore_test123"
    with patch.object(server, "_client", return_value=client):
        result = server.memstore_write_memory(path="/existing.md", content="new")
    assert result["operation"] == "updated"


def test_delete_memory_not_found() -> None:
    """Delete on a missing path returns deleted=False without raising."""
    client = _mock_client_with_empty_pages()
    server.DEFAULT_STORE_ID = "memstore_test123"
    with patch.object(server, "_client", return_value=client):
        result = server.memstore_delete_memory(path="/missing.md")
    assert result["deleted"] is False
    assert result["reason"] == "path not found"


def main() -> None:
    tests = [
        test_list_stores_sends_beta_header,
        test_list_memories_requires_store_id,
        test_list_memories_with_default_store,
        test_write_memory_creates_when_not_exists,
        test_write_memory_updates_when_exists,
        test_delete_memory_not_found,
    ]
    failed = 0
    for t in tests:
        try:
            t()
            print(f"  [PASS] {t.__name__}")
        except AssertionError as exc:
            failed += 1
            print(f"  [FAIL] {t.__name__}: {exc}")
        except Exception as exc:
            failed += 1
            print(f"  [ERROR] {t.__name__}: {type(exc).__name__}: {exc}")

    print()
    print(f"{len(tests) - failed}/{len(tests)} passed")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
