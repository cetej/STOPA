#!/usr/bin/env python3
"""PostToolUse hook: track learning retrieval for `uses` counter.

Fires on Read and Grep operations that touch learnings/ files.
Writes increments to a lightweight JSON ledger (no YAML parsing at runtime).
The ledger is merged into YAML frontmatter by learning-lifecycle.py at SessionStart.

LSM-tree inspired: O(1) JSON append at read time, batch merge at session start.
"""
import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
LEDGER_PATH = PROJECT_ROOT / ".claude/memory/intermediate/uses-ledger.json"
LEARNINGS_DIR = "learnings/"

# Files that are indexes, not actual learnings
SKIP_FILES = frozenset({
    "critical-patterns.md", "block-manifest.json", "ecosystem-scan.md",
})


def extract_learning_files(tool_name: str, tool_input: dict) -> list[str]:
    """Extract learning filenames from tool input."""
    files = []

    if tool_name == "Read":
        path = tool_input.get("file_path", "").replace("\\", "/")
        if LEARNINGS_DIR in path:
            fname = Path(path).name
            if fname.endswith(".md") and fname not in SKIP_FILES and not fname.startswith("index-"):
                files.append(fname)

    elif tool_name == "Grep":
        # Grep path or results touching learnings/
        path = tool_input.get("path", "").replace("\\", "/")
        if LEARNINGS_DIR in path:
            # Grep on learnings dir — we can't know which files matched
            # but the pattern was targeting learnings, so we track the grep itself
            # Individual file tracking happens via Read (grep shows filenames, user reads them)
            pass

    return files


def increment_ledger(filenames: list[str]) -> None:
    """Increment use counters in the JSON ledger."""
    if not filenames:
        return

    LEDGER_PATH.parent.mkdir(parents=True, exist_ok=True)

    # Read existing ledger
    ledger = {}
    if LEDGER_PATH.exists():
        try:
            ledger = json.loads(LEDGER_PATH.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            ledger = {}

    # Increment
    for fname in filenames:
        ledger[fname] = ledger.get(fname, 0) + 1

    # Write back atomically
    try:
        # .claude/hooks/ → .claude/ → repo root → scripts/
        sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "scripts"))
        from atomic_utils import atomic_write
        atomic_write(LEDGER_PATH, json.dumps(ledger, ensure_ascii=False, indent=2))
    except ImportError:
        # Fallback: direct write
        LEDGER_PATH.write_text(
            json.dumps(ledger, ensure_ascii=False, indent=2), encoding="utf-8"
        )


def main():
    try:
        hook_input = json.loads(sys.stdin.read())
    except (json.JSONDecodeError, EOFError):
        return

    tool_name = hook_input.get("tool_name", "")
    tool_input = hook_input.get("tool_input", {})

    if tool_name not in ("Read", "Grep"):
        return

    files = extract_learning_files(tool_name, tool_input)
    if files:
        increment_ledger(files)


if __name__ == "__main__":
    try:
        main()
    except Exception:
        pass  # Never block tool execution
