"""Shared secret loader for standalone STOPA scripts.

Resolution order:
  1. OS environment variable (works for CC sessions, Task Scheduler if set globally)
  2. ~/.claude/keys/secrets.env file (canonical STOPA store, gitignored)

Why both: Windows env var propagation is unreliable (User-scope vars don't
always reach MCP subprocesses or Task Scheduler children). The secrets.env
file is the deterministic fallback.

Used by: brain-ingest.py, brain-watch.py, and any future standalone script
that needs API keys outside the CC runtime.
"""
from __future__ import annotations

import os
from pathlib import Path

SECRETS_FILE = Path.home() / ".claude" / "keys" / "secrets.env"


def get_secret(key: str, default: str | None = None) -> str | None:
    """Resolve a secret by name. env var → secrets.env → default."""
    val = os.environ.get(key)
    if val:
        return val
    val = _read_from_file(key)
    if val:
        return val
    return default


def _read_from_file(key: str) -> str | None:
    if not SECRETS_FILE.exists():
        return None
    try:
        for raw_line in SECRETS_FILE.read_text(encoding="utf-8").splitlines():
            line = raw_line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" not in line:
                continue
            k, v = line.split("=", 1)
            if k.strip() == key:
                return v.strip().strip('"').strip("'")
    except OSError:
        return None
    return None


def require_secret(key: str) -> str:
    """Like get_secret but raises if missing — for fail-fast scripts."""
    val = get_secret(key)
    if not val:
        raise RuntimeError(
            f"{key} not found. Checked: $ENV[{key}], {SECRETS_FILE}. "
            "Set the env var or add the line to secrets.env."
        )
    return val
