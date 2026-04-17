#!/usr/bin/env python3
"""
Auto-Checkpoint Hook — NLAH File-Backed State (P3)

Notification hook: suggests checkpoint when state.md has changed
and no checkpoint has been saved in the last 30 minutes.

Light-touch: only prints advisory message, doesn't write anything.

Inspired by: arXiv:2603.25723 (NLAH) — state must always be current
"""

import json
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path


def main():
    hook_input = json.loads(sys.stdin.read())

    memory_dir = Path(os.environ.get("CLAUDE_PROJECT_DIR", ".")) / ".claude" / "memory"
    state_file = memory_dir / "state.md"
    checkpoint_file = memory_dir / "checkpoint.md"

    if not state_file.exists():
        print(json.dumps({"decision": "approve"}))
        return

    # Check if state has active task (not idle)
    try:
        content = state_file.read_text(encoding="utf-8")
        if "status: idle" in content or "status: null" in content:
            print(json.dumps({"decision": "approve"}))
            return
    except OSError:
        print(json.dumps({"decision": "approve"}))
        return

    # Check checkpoint freshness
    if checkpoint_file.exists():
        checkpoint_mtime = datetime.fromtimestamp(checkpoint_file.stat().st_mtime)
        if datetime.now() - checkpoint_mtime < timedelta(minutes=30):
            print(json.dumps({"decision": "approve"}))
            return

    # Check if state was modified more recently than checkpoint
    state_mtime = datetime.fromtimestamp(state_file.stat().st_mtime)
    if checkpoint_file.exists():
        checkpoint_mtime = datetime.fromtimestamp(checkpoint_file.stat().st_mtime)
        if state_mtime <= checkpoint_mtime:
            print(json.dumps({"decision": "approve"}))
            return

    # State is active, modified, and checkpoint is stale
    mins_since = int((datetime.now() - (checkpoint_mtime if checkpoint_file.exists()
                       else state_mtime)).total_seconds() / 60)

    print(json.dumps({
        "decision": "approve",
        "message": f"[auto-checkpoint] Active task detected, last checkpoint {mins_since}min ago. Consider running /checkpoint save."
    }))


if __name__ == "__main__":
    main()
