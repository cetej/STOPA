#!/usr/bin/env python3
"""UserPromptSubmit hook: debounced mid-session memory capture.

DeerFlow-inspired: instead of waiting until session end (Stop hook) to capture
learnings, this hook periodically extracts insights during the session.

Mechanism:
- On each user prompt, checks if enough activity has accumulated (>= 5 significant ops)
  AND enough time has passed since last capture (>= 120s debounce).
- If both conditions met, writes a mid-session snapshot to intermediate/pending-capture.json
  and triggers async Haiku extraction in background.
- The extraction writes learnings to learnings/ just like auto-scribe.py does at SessionStart.
- Must complete in <1s — only writes a marker file, no LLM calls inline.

Thread replacement: if a pending capture exists and hasn't been processed yet,
it gets replaced (not appended) — only the latest snapshot matters.
"""
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path

import sys, os
_levels = {'minimal': 1, 'standard': 2, 'strict': 3}
if _levels.get(os.environ.get('STOPA_HOOK_PROFILE', 'standard'), 2) < _levels.get('standard', 2):
    sys.exit(0)

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

MEMORY_DIR = Path(".claude/memory")
ACTIVITY_LOG = MEMORY_DIR / "activity-log.md"
PENDING_PATH = MEMORY_DIR / "intermediate" / "pending-capture.json"
LAST_CAPTURE_PATH = MEMORY_DIR / "intermediate" / "last-capture-ts"

DEBOUNCE_SECONDS = 120  # minimum time between captures
MIN_OPS_SINCE_CAPTURE = 5  # minimum significant ops to trigger capture
CAPTURE_SCRIPT = Path(".claude/hooks/mid-session-extract.py")


def count_recent_ops() -> int:
    """Count significant operations in activity log since last capture."""
    if not ACTIVITY_LOG.exists():
        return 0

    last_capture_ts = 0
    if LAST_CAPTURE_PATH.exists():
        try:
            last_capture_ts = float(LAST_CAPTURE_PATH.read_text().strip())
        except (ValueError, OSError):
            pass

    try:
        lines = ACTIVITY_LOG.read_text(encoding="utf-8", errors="replace").split("\n")
    except OSError:
        return 0

    # Count lines with significant operations (Write, Edit, Agent, Skill)
    significant = 0
    for line in lines:
        if any(op in line for op in ("Write", "Edit", "MultiEdit", "Agent", "Skill")):
            # Extract timestamp and check if after last capture
            ts_match = re.search(r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2})", line)
            if ts_match and last_capture_ts > 0:
                try:
                    line_ts = time.mktime(time.strptime(ts_match.group(1), "%Y-%m-%d %H:%M"))
                    if line_ts <= last_capture_ts:
                        continue
                except (ValueError, OverflowError):
                    pass
            significant += 1

    return significant


def should_capture() -> bool:
    """Check debounce timer and activity threshold."""
    # Check debounce
    if LAST_CAPTURE_PATH.exists():
        try:
            last_ts = float(LAST_CAPTURE_PATH.read_text().strip())
            if time.time() - last_ts < DEBOUNCE_SECONDS:
                return False
        except (ValueError, OSError):
            pass

    # Check activity threshold
    return count_recent_ops() >= MIN_OPS_SINCE_CAPTURE


def write_snapshot():
    """Write mid-session snapshot and trigger async extraction."""
    PENDING_PATH.parent.mkdir(parents=True, exist_ok=True)

    # Build minimal snapshot from activity log
    try:
        log_text = ACTIVITY_LOG.read_text(encoding="utf-8", errors="replace")
        # Take last 30 lines of activity log as context
        recent_lines = log_text.strip().split("\n")[-30:]
    except OSError:
        recent_lines = []

    # State snapshot
    state_path = MEMORY_DIR / "state.md"
    state_snippet = ""
    if state_path.exists():
        try:
            state_text = state_path.read_text(encoding="utf-8", errors="replace")
            # Extract active task line
            for line in state_text.split("\n"):
                if "Goal" in line or "Active Task" in line:
                    state_snippet = line.strip()
                    break
        except OSError:
            pass

    snapshot = {
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "type": "mid-session",
        "recent_activity": recent_lines,
        "state_snapshot": state_snippet,
    }

    # Atomic write (thread replacement — overwrites any pending capture)
    tmp_path = PENDING_PATH.with_suffix(".tmp")
    tmp_path.write_text(json.dumps(snapshot, ensure_ascii=False, indent=2), encoding="utf-8")
    tmp_path.rename(PENDING_PATH)

    # Update last capture timestamp
    LAST_CAPTURE_PATH.write_text(str(time.time()), encoding="utf-8")

    # Trigger async extraction (fire and forget)
    if CAPTURE_SCRIPT.exists():
        try:
            subprocess.Popen(
                [sys.executable, str(CAPTURE_SCRIPT)],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
            )
        except OSError:
            pass


def main():
    # Silent hook — never outputs to stdout (no context injection)
    try:
        if should_capture():
            write_snapshot()
    except Exception:
        pass  # Never fail the user prompt


if __name__ == "__main__":
    main()
