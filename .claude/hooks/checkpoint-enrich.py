#!/usr/bin/env python3
"""Stop hook: enrich checkpoint.md with actual session context from state.md.

Runs at session end (Stop event). Reads state.md (populated by state-tracker.py)
and enriches the checkpoint resume prompt with:
- List of files actually edited in the session
- Active task description (if any)
- Git branch and last commit
- Top 3 most-edited files as "focus areas"

This replaces the generic "Task: none" with actionable context for the next session.
"""
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

STOPA_ROOT = Path(__file__).resolve().parent.parent.parent
CHECKPOINT = STOPA_ROOT / ".claude" / "memory" / "checkpoint.md"
STATE = STOPA_ROOT / ".claude" / "memory" / "state.md"


def run_cmd(cmd: list[str], timeout: int = 5) -> str:
    try:
        r = subprocess.run(
            cmd, capture_output=True, text=True, timeout=timeout,
            cwd=str(STOPA_ROOT), encoding="utf-8", errors="replace",
        )
        return r.stdout.strip()
    except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
        return ""


def get_session_files() -> list[tuple[str, int]]:
    """Parse state.md Session Files table → [(path, edits), ...] sorted by edits desc."""
    if not STATE.exists():
        return []
    try:
        text = STATE.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return []

    files = []
    table_match = re.search(
        r"## Session Files.*?\n\|.*?\|.*?\|.*?\|\n\|[-| ]+\|\n(.*?)(?=\n## |\Z)",
        text, re.DOTALL,
    )
    if not table_match:
        return []

    for line in table_match.group(1).strip().splitlines():
        cols = [c.strip() for c in line.split("|")]
        if len(cols) >= 3:
            fpath = cols[1].strip()
            try:
                edits = int(cols[2].strip())
            except (ValueError, IndexError):
                edits = 1
            if fpath and fpath != "File":
                files.append((fpath, edits))

    return sorted(files, key=lambda x: -x[1])


def get_active_task() -> str:
    """Extract active task from state.md."""
    if not STATE.exists():
        return "none"
    try:
        text = STATE.read_text(encoding="utf-8", errors="replace")[:1000]
        m = re.search(r"## Active Task\s*\n+(.+)", text)
        if m and "no active task" not in m.group(1).lower():
            return m.group(1).strip()
    except OSError:
        pass
    return "none"


def build_resume_prompt() -> str:
    """Build a rich resume prompt from state.md + git context."""
    task = get_active_task()
    branch = run_cmd(["git", "branch", "--show-current"]) or "unknown"
    last_commit = run_cmd(["git", "log", "--oneline", "-1", "--no-decorate"]) or "unknown"
    files = get_session_files()

    lines = []
    lines.append(f"> **Task**: {task}")
    lines.append(f">")
    lines.append(f"> **Context**: Last commit `{last_commit}`. Branch: {branch}.")

    if files:
        top = files[:5]
        file_summary = ", ".join(f"`{f}` ({n}x)" for f, n in top)
        lines.append(f"> Most-edited files: {file_summary}.")

        total_edits = sum(n for _, n in files)
        lines.append(f"> Session: {len(files)} files touched, {total_edits} total edits.")

    if task != "none":
        lines.append(f">")
        lines.append(f"> **Resume**: Pokračuj v úkolu \"{task}\". Zkontroluj state.md pro detaily.")
    else:
        lines.append(f">")
        lines.append(f"> **Resume**: Zkontroluj state.md — session files ukazují na čem se pracovalo.")

    return "\n".join(lines)


def enrich_checkpoint():
    """Replace the resume prompt section in checkpoint.md with enriched version."""
    if not CHECKPOINT.exists():
        return

    try:
        text = CHECKPOINT.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return

    new_prompt = build_resume_prompt()

    # Replace existing resume prompt block
    # Pattern: ## Resume Prompt\n\n> **Task**: ... (everything until next ## or end)
    pattern = r"(## Resume Prompt\s*\n+)(>.*?)(?=\n---|\n## |\Z)"
    match = re.search(pattern, text, re.DOTALL)

    if match:
        updated = text[:match.start(2)] + new_prompt + text[match.end(2):]
    else:
        # No resume prompt found — append one
        updated = text.rstrip() + "\n\n## Resume Prompt\n\n" + new_prompt + "\n"

    try:
        CHECKPOINT.write_text(updated, encoding="utf-8")
    except OSError as e:
        print(f"[checkpoint-enrich] write error: {e}", file=sys.stderr)


def main():
    # Only enrich if state.md has actual data
    files = get_session_files()
    if not files:
        sys.exit(0)

    enrich_checkpoint()
    sys.exit(0)


if __name__ == "__main__":
    main()
