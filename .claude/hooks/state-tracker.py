#!/usr/bin/env python3
"""PostToolUse hook (Write|Edit): auto-populate state.md with session activity.

Solves the critical gap: state.md is always empty after sessions because nothing
writes to it automatically. This hook tracks:
- Files being edited (path, timestamp, count)
- Session start time
- Branch context

state.md format:
---
session_start: YYYY-MM-DDTHH:MM:SS
branch: main
last_update: YYYY-MM-DDTHH:MM:SS
---

## Active Task

<populated by orchestrate/manual, preserved by this hook>

## Session Files

| File | Edits | Last touched |
|------|-------|-------------|
| path/to/file.py | 3 | 14:23 |

The hook APPENDS to the files table, never overwrites Active Task section.
"""
import json
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

STOPA_ROOT = Path(__file__).resolve().parent.parent.parent
STATE_FILE = STOPA_ROOT / ".claude" / "memory" / "state.md"


def get_branch() -> str:
    try:
        r = subprocess.run(
            ["git", "branch", "--show-current"],
            capture_output=True, text=True, timeout=3,
            cwd=str(STOPA_ROOT),
        )
        return r.stdout.strip() or "unknown"
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return "unknown"


def extract_file_path() -> str | None:
    """Extract the file path from CLAUDE_TOOL_INPUT env var."""
    tool_input = sys.stdin.read() if not sys.stdin.isatty() else ""
    if not tool_input:
        # Try env var
        import os
        tool_input = os.environ.get("CLAUDE_TOOL_INPUT", "")

    if not tool_input:
        return None

    # Parse JSON tool input to get file_path
    try:
        data = json.loads(tool_input)
        return data.get("file_path") or data.get("path") or None
    except (json.JSONDecodeError, TypeError):
        pass

    # Fallback: regex for file_path in string
    m = re.search(r'"file_path"\s*:\s*"([^"]+)"', tool_input)
    return m.group(1) if m else None


def normalize_path(raw_path: str) -> str:
    """Normalize to relative path from STOPA_ROOT."""
    try:
        p = Path(raw_path)
        try:
            rel = p.relative_to(STOPA_ROOT)
            return str(rel).replace("\\", "/")
        except ValueError:
            # Not under STOPA_ROOT — use as-is but shorten
            return str(p.name)
    except Exception:
        return raw_path


def parse_state() -> tuple[str, str, dict[str, dict]]:
    """Parse existing state.md → (active_task_section, frontmatter, files_dict).

    files_dict: {relative_path: {"edits": int, "last": "HH:MM"}}
    """
    active_task = "_No active task._"
    frontmatter = ""
    files: dict[str, dict] = {}

    if not STATE_FILE.exists():
        return active_task, frontmatter, files

    try:
        text = STATE_FILE.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return active_task, frontmatter, files

    # Extract frontmatter
    fm_match = re.match(r"^---\n(.*?\n)---\n", text, re.DOTALL)
    if fm_match:
        frontmatter = fm_match.group(1)

    # Extract Active Task section (everything between ## Active Task and ## Session Files)
    at_match = re.search(r"## Active Task\n+(.*?)(?=\n## |\Z)", text, re.DOTALL)
    if at_match:
        task_text = at_match.group(1).strip()
        if task_text and "no active task" not in task_text.lower():
            active_task = task_text

    # Parse Session Files table
    table_match = re.search(r"## Session Files.*?\n\|.*?\|.*?\|.*?\|\n\|[-| ]+\|\n(.*?)(?=\n## |\Z)", text, re.DOTALL)
    if table_match:
        for line in table_match.group(1).strip().splitlines():
            cols = [c.strip() for c in line.split("|")]
            if len(cols) >= 4:  # | path | edits | time |
                fpath = cols[1].strip()
                try:
                    edits = int(cols[2].strip())
                except (ValueError, IndexError):
                    edits = 1
                last_time = cols[3].strip() if len(cols) > 3 else ""
                if fpath and fpath != "File":
                    files[fpath] = {"edits": edits, "last": last_time}

    return active_task, frontmatter, files


def write_state(active_task: str, branch: str, files: dict[str, dict]):
    """Write updated state.md."""
    now = datetime.now()

    # Build frontmatter
    fm_lines = [
        "---",
        f"branch: {branch}",
        f"last_update: {now.strftime('%Y-%m-%dT%H:%M:%S')}",
        "---",
        "",
    ]

    # Active Task section
    lines = fm_lines + [
        "# Shared Memory — Task State",
        "",
        "## Active Task",
        "",
        active_task,
        "",
    ]

    # Session Files table
    if files:
        lines.append("## Session Files")
        lines.append("")
        lines.append("| File | Edits | Last touched |")
        lines.append("|------|-------|-------------|")

        # Sort by last touched (descending) then by edits
        sorted_files = sorted(
            files.items(),
            key=lambda x: (x[1].get("last", ""), x[1].get("edits", 0)),
            reverse=True,
        )

        # Keep max 30 files
        for fpath, info in sorted_files[:30]:
            edits = info.get("edits", 1)
            last = info.get("last", "")
            lines.append(f"| {fpath} | {edits} | {last} |")

        lines.append("")

    try:
        STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
        STATE_FILE.write_text("\n".join(lines), encoding="utf-8")
    except OSError as e:
        print(f"[state-tracker] write error: {e}", file=sys.stderr)


def main():
    file_path = extract_file_path()
    if not file_path:
        sys.exit(0)

    rel_path = normalize_path(file_path)

    # Skip memory files themselves (avoid circular tracking)
    if ".claude/memory/" in rel_path and rel_path.endswith("state.md"):
        sys.exit(0)

    branch = get_branch()
    active_task, _fm, files = parse_state()

    now_time = datetime.now().strftime("%H:%M")

    if rel_path in files:
        files[rel_path]["edits"] = files[rel_path].get("edits", 0) + 1
        files[rel_path]["last"] = now_time
    else:
        files[rel_path] = {"edits": 1, "last": now_time}

    write_state(active_task, branch, files)
    sys.exit(0)


if __name__ == "__main__":
    main()
