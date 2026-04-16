#!/usr/bin/env python3
"""PostToolUse hook: enqueue compact suggestion when activity count is high.

Triggers after 30+ tool operations in current session.
Replaces suggest-compact.sh — uses sidecar queue instead of stdout.
Profile: standard+
"""
import os
import sys
from pathlib import Path

# Profile check
_levels = {"minimal": 1, "standard": 2, "strict": 3}
if _levels.get(os.environ.get("STOPA_HOOK_PROFILE", "standard"), 2) < _levels.get("standard", 2):
    sys.exit(0)

sys.path.insert(0, str(Path(__file__).resolve().parent))
from sidecar_queue import enqueue

LOG = Path(".claude/memory/activity-log.md")
MARKER = Path(f"/tmp/stopa-compact-suggested-{os.getppid()}")


def main() -> None:
    # Only suggest once per session
    if MARKER.exists():
        return

    if not LOG.exists():
        return

    # Count total entries
    try:
        content = LOG.read_text(encoding="utf-8", errors="replace")
        total = sum(1 for line in content.split("\n") if line.startswith("- "))
    except OSError:
        return

    if total >= 30:
        MARKER.touch(exist_ok=True)
        enqueue({
            "type": "compact_suggestion",
            "priority": "medium",
            "message": f"Session has {total} tracked operations. Consider /compact to reduce context size.",
            "action": "/compact",
            "source": "suggest-compact",
        })


if __name__ == "__main__":
    try:
        main()
    except Exception:
        pass  # Never block — fail silently
