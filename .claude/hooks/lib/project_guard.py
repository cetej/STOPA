"""Shared project boundary guard for STOPA Python hooks.

Usage at top of hook:
    from lib.project_guard import should_skip
    if should_skip():
        sys.exit(0)

Or with already-parsed input:
    from lib.project_guard import is_outside_project
    if is_outside_project(file_path):
        sys.exit(0)

Behavior:
    - Reads tool input from stdin, extracts file_path/path
    - If file is outside STOPA project root → returns True (skip)
    - If file is within STOPA or no path detected → returns False (run hook)
"""
import json
import os
import sys
from pathlib import Path

# STOPA root = grandparent of hooks/lib/
STOPA_ROOT = Path(__file__).resolve().parent.parent.parent.parent
# Normalize
STOPA_ROOT_STR = str(STOPA_ROOT).replace("\\", "/").rstrip("/")


def is_outside_project(file_path: str | None) -> bool:
    """Check if a file path is outside the STOPA project."""
    if not file_path:
        return False  # No path → assume in-project, let hook run

    # Normalize
    normalized = file_path.replace("\\", "/")

    # Absolute path check
    if os.path.isabs(normalized):
        return not normalized.startswith(STOPA_ROOT_STR + "/")

    # Relative path — resolve against STOPA root
    try:
        resolved = str((STOPA_ROOT / normalized).resolve()).replace("\\", "/")
        return not resolved.startswith(STOPA_ROOT_STR + "/")
    except (OSError, ValueError):
        return False


def extract_file_path(tool_input: dict) -> str | None:
    """Extract file path from tool input dict."""
    return tool_input.get("file_path") or tool_input.get("path")


def should_skip() -> bool:
    """Read stdin, check if target file is outside STOPA.

    Call this at the very top of a hook — it consumes stdin.
    Returns True if hook should exit(0) immediately.
    """
    try:
        raw = sys.stdin.read()
        data = json.loads(raw) if raw.strip() else {}
    except (json.JSONDecodeError, ValueError):
        return False

    file_path = extract_file_path(data)
    return is_outside_project(file_path)
