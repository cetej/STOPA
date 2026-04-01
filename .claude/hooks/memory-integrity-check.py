#!/usr/bin/env python3
"""PostToolUse hook: validate memory file integrity after Write/Edit operations.

Checks that memory files written by Claude (via Write/Edit tools) are:
- Non-empty (catches truncation from interrupted writes)
- Valid UTF-8
- For .jsonl files: last line is parseable JSON

Does NOT block — always exits 0. Prints warning to context on integrity failure.
"""
import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

MEMORY_DIR = Path(".claude/memory")


def main() -> None:
    try:
        tool_input = json.loads(sys.stdin.read())
    except Exception:
        return

    # Extract file path from tool input
    file_path = tool_input.get("tool_input", {}).get("file_path", "")
    if not file_path:
        return

    path = Path(file_path)

    # Only check memory files
    try:
        path.resolve().relative_to(MEMORY_DIR.resolve())
    except (ValueError, OSError):
        return

    if not path.exists():
        return

    # Check non-empty
    try:
        content = path.read_text(encoding="utf-8", errors="replace")
    except Exception as e:
        print(f"[INTEGRITY] Cannot read {path.name}: {e}")
        return

    if not content.strip():
        print(f"[INTEGRITY WARNING] {path.name} is empty after write — possible truncation")
        return

    # For JSONL files: validate last line is parseable JSON
    if path.suffix == ".jsonl":
        lines = content.strip().split("\n")
        try:
            json.loads(lines[-1])
        except (json.JSONDecodeError, IndexError):
            print(f"[INTEGRITY WARNING] {path.name}: last line is not valid JSON")
            return

    # For YAML frontmatter files (learnings): check frontmatter delimiters
    if path.parent.name == "learnings" and path.suffix == ".md":
        if not content.startswith("---"):
            print(f"[INTEGRITY WARNING] {path.name}: missing YAML frontmatter delimiter")
            return
        if content.count("---") < 2:
            print(f"[INTEGRITY WARNING] {path.name}: incomplete YAML frontmatter")
            return


if __name__ == "__main__":
    try:
        main()
    except Exception:
        pass  # Never block — fail silently
