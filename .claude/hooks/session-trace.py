#!/usr/bin/env python3
"""PostToolUse hook: lightweight session trace capture for Semantic Observability.

Always-on (no marker needed). Captures tool call sequences from every session
to enable behavior discovery via /discover.

Unlike trace-capture.py (rich traces for optimization runs), this is minimal:
- tool name, exit code, file path/command, timestamp
- No output snippets (saves ~90% storage)
- Skip read-only tools (Read, Glob, Grep) unless they fail
- Auto-purge sessions older than 14 days

Writes to: .traces/sessions/YYYY-MM-DD-HHmm.jsonl
Session ID derived from CLAUDE_SESSION_ID env var or timestamp-based fallback.
"""
import json
import os
import sys
import time
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
TRACES_DIR = PROJECT_ROOT / ".traces/sessions"
MAX_AGE_DAYS = 14
READ_ONLY_TOOLS = frozenset({"Read", "Glob", "Grep", "TodoRead"})
# Skip tools that fire too frequently and add noise
NOISE_TOOLS = frozenset({"TodoWrite"})
SESSION_FILE_CACHE = PROJECT_ROOT / ".claude/memory/intermediate/session-trace-path"


def get_session_path() -> Path:
    """Get or create the session trace file path for this session."""
    # Try cached path first (avoids filesystem scan on every call)
    if SESSION_FILE_CACHE.exists():
        try:
            cached = SESSION_FILE_CACHE.read_text(encoding="utf-8").strip()
            cached_path = Path(cached)
            if cached_path.exists():
                return cached_path
        except OSError:
            pass

    # Derive session ID from env or create timestamp-based
    session_id = os.environ.get("CLAUDE_SESSION_ID", "")
    if session_id:
        # Use first 8 chars of session ID for filename
        session_slug = session_id[:8]
    else:
        # Fallback: use date-hour-minute
        session_slug = time.strftime("%H%M")

    date_str = time.strftime("%Y-%m-%d")
    filename = f"{date_str}-{session_slug}.jsonl"
    session_path = TRACES_DIR / filename

    # Cache the path
    try:
        SESSION_FILE_CACHE.parent.mkdir(parents=True, exist_ok=True)
        SESSION_FILE_CACHE.write_text(str(session_path), encoding="utf-8")
    except OSError:
        pass

    return session_path


def purge_old_traces():
    """Remove session traces older than MAX_AGE_DAYS. Runs at most once per session."""
    purge_marker = PROJECT_ROOT / ".claude/memory/intermediate/session-trace-purged"
    today = time.strftime("%Y-%m-%d")

    # Only purge once per day
    if purge_marker.exists():
        try:
            last_purge = purge_marker.read_text(encoding="utf-8").strip()
            if last_purge == today:
                return
        except OSError:
            pass

    if not TRACES_DIR.exists():
        return

    cutoff = time.time() - (MAX_AGE_DAYS * 86400)
    for f in TRACES_DIR.glob("*.jsonl"):
        try:
            if f.stat().st_mtime < cutoff:
                f.unlink()
        except OSError:
            pass

    try:
        purge_marker.parent.mkdir(parents=True, exist_ok=True)
        purge_marker.write_text(today, encoding="utf-8")
    except OSError:
        pass


def main():
    # Parse stdin JSON from Claude Code
    try:
        stdin_data = sys.stdin.read()
    except Exception:
        return

    if not stdin_data:
        return

    try:
        event = json.loads(stdin_data)
    except json.JSONDecodeError:
        return

    tool_name = event.get("tool_name", "")
    exit_code = event.get("tool_exit_code", 0)
    tool_input = event.get("tool_input", "")

    if not tool_name:
        return

    # Skip noise tools
    if tool_name in NOISE_TOOLS:
        return

    # Skip read-only tools unless they failed (failure = interesting signal)
    if tool_name in READ_ONLY_TOOLS and exit_code == 0:
        return

    # Extract minimal structured fields
    input_path = None
    input_cmd = None
    skill_name = None

    if isinstance(tool_input, dict):
        input_path = tool_input.get("file_path") or tool_input.get("path")
        input_cmd = tool_input.get("command")
        skill_name = tool_input.get("skill")
        # Truncate command to 200 chars (enough for pattern detection)
        if input_cmd and len(input_cmd) > 200:
            input_cmd = input_cmd[:200]
    elif isinstance(tool_input, str) and tool_name == "Bash":
        input_cmd = tool_input[:200]

    # Build lightweight record
    record = {
        "ts": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "tool": tool_name,
        "exit": exit_code,
    }
    if input_path:
        record["path"] = str(input_path)
    if input_cmd:
        record["cmd"] = input_cmd
    if skill_name:
        record["skill"] = skill_name

    # Write to session trace file
    session_path = get_session_path()
    try:
        session_path.parent.mkdir(parents=True, exist_ok=True)
        with open(session_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")
    except OSError:
        pass

    # Purge old traces (cheap, once per day)
    purge_old_traces()


if __name__ == "__main__":
    try:
        main()
    except Exception:
        pass  # Never fail the tool use
