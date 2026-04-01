#!/usr/bin/env python3
"""Sidecar queue utility for deferred hook suggestions.

Instead of printing suggestions directly into Claude's context mid-task,
hooks enqueue items here. The orchestrator drains the queue between waves.

Queue file: .claude/memory/intermediate/sidecar-queue.json

Usage:
    from sidecar_queue import enqueue, drain, drain_stale

    enqueue({"type": "compact_suggestion", "priority": "medium", ...})
    items = drain()  # returns and clears all items
    stale = drain_stale(max_age_seconds=7200)  # drain items older than 2h
"""
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
from atomic_utils import atomic_write

QUEUE_PATH = Path(".claude/memory/intermediate/sidecar-queue.json")


def _read_queue() -> list[dict]:
    """Read current queue items."""
    if not QUEUE_PATH.exists():
        return []
    try:
        content = QUEUE_PATH.read_text(encoding="utf-8")
        data = json.loads(content)
        return data if isinstance(data, list) else []
    except (json.JSONDecodeError, OSError):
        return []


def enqueue(item: dict) -> None:
    """Add an item to the sidecar queue.

    Item schema:
        timestamp: ISO8601 (auto-added if missing)
        priority: "high" | "medium" | "low"
        type: "compact_suggestion" | "checkpoint_suggestion" | "learning_suggestion" | "custom"
        message: human-readable description
        action: optional CLI command (e.g., "/compact")
        source: hook name that enqueued this
    """
    if "timestamp" not in item:
        from datetime import datetime
        item["timestamp"] = datetime.now().isoformat()

    items = _read_queue()
    items.append(item)
    atomic_write(QUEUE_PATH, json.dumps(items, ensure_ascii=False, indent=2))


def drain() -> list[dict]:
    """Return all queued items and clear the queue."""
    items = _read_queue()
    if items:
        atomic_write(QUEUE_PATH, "[]")
    return items


def drain_stale(max_age_seconds: int = 7200) -> list[dict]:
    """Drain items older than max_age_seconds, keep recent ones.

    Returns the stale items that were removed.
    """
    items = _read_queue()
    if not items:
        return []

    now = time.time()
    stale = []
    fresh = []

    for item in items:
        ts = item.get("timestamp", "")
        try:
            from datetime import datetime
            item_time = datetime.fromisoformat(ts).timestamp()
            if now - item_time > max_age_seconds:
                stale.append(item)
            else:
                fresh.append(item)
        except (ValueError, TypeError):
            stale.append(item)  # Can't parse timestamp → treat as stale

    if stale:
        atomic_write(QUEUE_PATH, json.dumps(fresh, ensure_ascii=False, indent=2))

    return stale


def summary(items: list[dict]) -> str:
    """Format queued items as a concise summary for context injection."""
    if not items:
        return ""
    lines = ["[Sidecar Queue — deferred suggestions]"]
    for item in sorted(items, key=lambda x: {"high": 0, "medium": 1, "low": 2}.get(x.get("priority", "low"), 3)):
        action = f" → {item['action']}" if item.get("action") else ""
        lines.append(f"- [{item.get('priority', '?')}] {item.get('message', '?')}{action}")
    return "\n".join(lines)


if __name__ == "__main__":
    # Self-test
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    import tempfile
    import os

    # Use temp path for testing
    original = QUEUE_PATH
    test_dir = Path(tempfile.mkdtemp())
    QUEUE_PATH = test_dir / "test-queue.json"

    # Workaround: patch module-level variable via globals
    globals()["QUEUE_PATH"] = QUEUE_PATH

    try:
        # Test enqueue
        enqueue({"type": "compact_suggestion", "priority": "medium", "message": "30+ ops", "source": "test"})
        enqueue({"type": "checkpoint_suggestion", "priority": "high", "message": "70% done", "source": "test"})

        items = _read_queue()
        assert len(items) == 2, f"Expected 2 items, got {len(items)}"

        # Test drain
        drained = drain()
        assert len(drained) == 2, f"Expected 2 drained, got {len(drained)}"
        assert len(_read_queue()) == 0, "Queue should be empty after drain"

        # Test summary
        s = summary(drained)
        assert "70% done" in s, "Summary should contain message"

        print("All sidecar-queue tests passed")
    finally:
        # Cleanup
        try:
            QUEUE_PATH.unlink(missing_ok=True)
            test_dir.rmdir()
        except Exception:
            pass
