#!/usr/bin/env python3
"""STOPA memory health — background plugin monitor.

Runs once at session start via the plugin `monitors` manifest key (CC v2.1.105+).
Scans the STOPA memory directory for actionable health issues and emits one
notification line per issue. Exits silently when memory is healthy or when no
STOPA memory directory exists (monitor becomes a no-op in non-STOPA projects).

Each stdout line is delivered to Claude as a notification, so issue lines are
kept short and action-oriented. At most MAX_NOTIFICATIONS issues are emitted;
additional issues are collapsed into a single summary line.

MemoryBackend abstraction (ADR 0016/0017):
- Reads target path from env var `STOPA_MEMORY_DIR` when set.
- Falls back to `.claude/memory` relative to the session working directory.
- Does not read or write backend-specific files; relies on the filesystem view
  that every backend exposes (files + well-known subdirectories).
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

MEMORY_DIR = Path(os.environ.get("STOPA_MEMORY_DIR", ".claude/memory"))

LINE_LIMIT = 500
FAILURES_THRESHOLD = 40
LEARNINGS_THRESHOLD = 200
MAX_NOTIFICATIONS = 5


def _line_count(path: Path) -> int:
    try:
        with path.open("r", encoding="utf-8", errors="replace") as fh:
            return sum(1 for _ in fh)
    except OSError:
        return 0


def _count_md(dir_path: Path) -> int:
    try:
        return sum(1 for entry in dir_path.iterdir() if entry.is_file() and entry.suffix == ".md")
    except OSError:
        return 0


def main() -> int:
    if not MEMORY_DIR.is_dir():
        return 0

    issues: list[str] = []

    for md in sorted(MEMORY_DIR.glob("*.md")):
        if "-archive" in md.stem:
            continue
        lines = _line_count(md)
        if lines > LINE_LIMIT:
            issues.append(
                f"[stopa:memory] {md.name} has {lines} lines (>{LINE_LIMIT}) "
                f"— archive old entries to {md.stem}-archive.md"
            )

    failures_dir = MEMORY_DIR / "failures"
    if failures_dir.is_dir():
        count = _count_md(failures_dir)
        if count > FAILURES_THRESHOLD:
            issues.append(
                f"[stopa:memory] failures/ has {count} files (>{FAILURES_THRESHOLD}) "
                "— run /sweep to archive records older than 60 days"
            )

    learnings_dir = MEMORY_DIR / "learnings"
    if learnings_dir.is_dir():
        count = _count_md(learnings_dir)
        if count > LEARNINGS_THRESHOLD:
            issues.append(
                f"[stopa:memory] learnings/ has {count} files (>{LEARNINGS_THRESHOLD}) "
                "— run /evolve to prune low-confidence entries"
            )

    for issue in issues[:MAX_NOTIFICATIONS]:
        print(issue, flush=True)

    extra = len(issues) - MAX_NOTIFICATIONS
    if extra > 0:
        print(
            f"[stopa:memory] +{extra} more issue(s) suppressed — run /sweep for full audit",
            flush=True,
        )

    return 0


if __name__ == "__main__":
    sys.exit(main())
