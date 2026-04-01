#!/usr/bin/env python3
"""PostToolUse hook (Write|Edit): enqueue checkpoint suggestion when task is 70%+ complete.

Advisory only — debounced to max 1 suggestion per 30 minutes.
Replaces auto-checkpoint-suggest.sh — uses sidecar queue instead of stdout.
Profile: standard+
"""
import os
import re
import sys
import time
from pathlib import Path

# Profile check
_levels = {"minimal": 1, "standard": 2, "strict": 3}
if _levels.get(os.environ.get("STOPA_HOOK_PROFILE", "standard"), 2) < _levels.get("standard", 2):
    sys.exit(0)

sys.path.insert(0, str(Path(__file__).resolve().parent))
from sidecar_queue import enqueue

STATE_FILE = Path(".claude/memory/state.md")
CHECKPOINT_FILE = Path(".claude/memory/checkpoint.md")
MARKER = Path("/tmp/stopa-checkpoint-suggested")


def main() -> None:
    if not STATE_FILE.exists():
        return

    # Debounce: skip if suggested in last 30 minutes
    if MARKER.exists():
        try:
            marker_age = time.time() - MARKER.stat().st_mtime
            if marker_age < 1800:
                return
        except OSError:
            pass

    # Parse state.md for subtask completion
    try:
        content = STATE_FILE.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return

    total = len(re.findall(r"^\s*[-*]\s*\[.\]|^\s*[-*].*\|.*\|", content, re.MULTILINE))
    done = len(re.findall(
        r"^\s*[-*]\s*\[x\]|^\s*[-*].*completed|^\s*[-*].*DONE",
        content, re.MULTILINE | re.IGNORECASE
    ))

    # Need at least 3 tasks and 70%+ completion
    if total < 3:
        return
    ratio = done * 100 // total
    if ratio < 70:
        return

    # Check if checkpoint already saved recently (last 30 min)
    if CHECKPOINT_FILE.exists():
        try:
            cp_age = time.time() - CHECKPOINT_FILE.stat().st_mtime
            if cp_age < 1800:
                return
        except OSError:
            pass

    # Mark suggestion time
    MARKER.touch(exist_ok=True)

    enqueue({
        "type": "checkpoint_suggestion",
        "priority": "high",
        "message": f"Task is {ratio}% complete ({done}/{total} subtasks). Consider /checkpoint save.",
        "action": "/checkpoint save",
        "source": "auto-checkpoint-suggest",
    })


if __name__ == "__main__":
    try:
        main()
    except Exception:
        pass  # Never block — fail silently
