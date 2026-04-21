#!/usr/bin/env python3
"""Memory health monitor — background monitor for stopa-orchestration plugin.

Each stdout line is delivered to Claude as a notification (CC v2.1.105+ monitors).
Emits a single line when memory files exceed maintenance thresholds. Dedupe via
hash so the same finding is not reported repeatedly.

Thresholds (from .claude/rules/memory-files.md + core-invariants.md):
- memory/*.md > 500 lines        (archive threshold)
- memory/failures/ > 40 files    (warn at 40, ceiling 50)
- memory/outcomes/ > 80 files    (warn at 80, ceiling 100)

Exits silently if .claude/memory/ not found. Long-running loop stops at session end.

Usage:
  monitor-memory-health.py          # persistent loop (monitor mode)
  monitor-memory-health.py --once   # single check, exit (test mode)
"""
from __future__ import annotations

import argparse
import hashlib
import sys
import time
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

MAX_LINES = 500
MAX_FAILURES = 40
MAX_OUTCOMES = 80
CHECK_INTERVAL_S = 30 * 60  # 30 min


def find_memory_dir() -> Path | None:
    cwd = Path.cwd()
    for candidate in (cwd / ".claude" / "memory", cwd / "memory"):
        if candidate.is_dir():
            return candidate
    return None


def count_lines(path: Path) -> int:
    try:
        with path.open("r", encoding="utf-8", errors="replace") as fh:
            return sum(1 for _ in fh)
    except OSError:
        return 0


def check_memory(mem_dir: Path) -> list[str]:
    issues: list[str] = []

    for md_file in sorted(mem_dir.glob("*.md")):
        lines = count_lines(md_file)
        if lines > MAX_LINES:
            issues.append(f"{md_file.name}: {lines} lines")

    failures_dir = mem_dir / "failures"
    if failures_dir.is_dir():
        count = sum(1 for _ in failures_dir.glob("*.md"))
        if count > MAX_FAILURES:
            issues.append(f"failures/: {count} files")

    outcomes_dir = mem_dir / "outcomes"
    if outcomes_dir.is_dir():
        count = sum(1 for _ in outcomes_dir.glob("*.md"))
        if count > MAX_OUTCOMES:
            issues.append(f"outcomes/: {count} files")

    return issues


def emit(issues: list[str]) -> None:
    head = "; ".join(issues[:3])
    tail = f" (+{len(issues) - 3} more)" if len(issues) > 3 else ""
    print(
        f"[memory-health] STOPA memory exceeds thresholds: {head}{tail} — run /sweep",
        flush=True,
    )


def hash_issues(issues: list[str]) -> str:
    return hashlib.md5("|".join(sorted(issues)).encode("utf-8")).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--once", action="store_true", help="Run single check and exit (test mode)"
    )
    args = parser.parse_args()

    mem_dir = find_memory_dir()
    if mem_dir is None:
        return 0  # silent exit — no memory in this project

    if args.once:
        issues = check_memory(mem_dir)
        if issues:
            emit(issues)
        else:
            print("[memory-health] OK — no thresholds exceeded", flush=True)
        return 0

    last_hash: str | None = None
    while True:
        issues = check_memory(mem_dir)
        if issues:
            current_hash = hash_issues(issues)
            if current_hash != last_hash:
                emit(issues)
                last_hash = current_hash
        try:
            time.sleep(CHECK_INTERVAL_S)
        except KeyboardInterrupt:
            return 0


if __name__ == "__main__":
    sys.exit(main())
