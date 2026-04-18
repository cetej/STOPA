#!/usr/bin/env python3
"""PostToolUse hook: auto-detect learnings eligible for graduation to critical-patterns.md.

Fires on Write/Edit operations to .claude/memory/learnings/ files.
When a learning's `uses` counter crosses the graduation threshold, writes it
to intermediate/graduation-candidates.md for /evolve to review.

Graduation triggers (from memory-files.md):
  - uses >= 10 AND confidence >= 0.8 AND harmful_uses < 2

Pruning triggers:
  - confidence < 0.3

Output: additionalContext JSON when graduation candidate found.
"""
import json
import re
import sys
from datetime import date
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

LEARNINGS_DIR = Path(".claude/memory/learnings")
CANDIDATES_PATH = Path(".claude/memory/intermediate/graduation-candidates.md")
CRITICAL_PATTERNS = Path(".claude/memory/learnings/critical-patterns.md")

# Files to skip
SKIP_FILES = frozenset({
    "critical-patterns.md", "block-manifest.json", "ecosystem-scan.md",
    "concept-graph.json", "corrections.jsonl", "sessions.jsonl",
})


def parse_frontmatter(content: str) -> dict:
    """Parse YAML frontmatter from learning file."""
    if not content.startswith("---"):
        return {}
    end = content.find("---", 3)
    if end == -1:
        return {}
    fm = {}
    for line in content[3:end].strip().split("\n"):
        if ":" in line:
            key, _, val = line.partition(":")
            val = val.strip().strip('"').strip("'")
            # Parse numeric values
            try:
                if "." in val:
                    fm[key.strip()] = float(val)
                else:
                    fm[key.strip()] = int(val)
            except (ValueError, TypeError):
                fm[key.strip()] = val
    return fm


def check_graduation(fm: dict) -> str | None:
    """Check if learning meets graduation or pruning criteria. Returns action or None."""
    uses = fm.get("uses", 0)
    confidence = fm.get("confidence", 0.7)
    harmful = fm.get("harmful_uses", 0)

    # Skip already graduated (maturity: core) learnings
    maturity = fm.get("maturity", "draft")
    if maturity == "core":
        return None

    # Graduation check
    if (uses >= 10 and confidence >= 0.8 and harmful < 2):
        return "graduate"

    # Pruning check
    if confidence < 0.3:
        return "prune"

    return None


def is_already_candidate(filename: str) -> bool:
    """Check if learning is already listed in graduation candidates."""
    if not CANDIDATES_PATH.exists():
        return False
    return filename in CANDIDATES_PATH.read_text(encoding="utf-8", errors="replace")


def is_already_graduated(summary: str) -> bool:
    """Check if learning summary already appears in critical-patterns.md."""
    if not CRITICAL_PATTERNS.exists():
        return False
    content = CRITICAL_PATTERNS.read_text(encoding="utf-8", errors="replace")
    # Check first 80 chars of summary against critical patterns
    return summary[:60] in content if summary else False


def append_candidate(filename: str, fm: dict, action: str):
    """Append graduation/pruning candidate to the candidates file."""
    CANDIDATES_PATH.parent.mkdir(parents=True, exist_ok=True)
    today = date.today().isoformat()

    entry = (
        f"\n### {action.upper()}: {filename}\n"
        f"- **Date detected**: {today}\n"
        f"- **Uses**: {fm.get('uses', 0)} | **Confidence**: {fm.get('confidence', 'N/A')} | "
        f"**Harmful**: {fm.get('harmful_uses', 0)}\n"
        f"- **Summary**: {fm.get('summary', 'N/A')}\n"
        f"- **Component**: {fm.get('component', 'N/A')} | **Severity**: {fm.get('severity', 'N/A')}\n"
    )

    if CANDIDATES_PATH.exists():
        content = CANDIDATES_PATH.read_text(encoding="utf-8", errors="replace")
    else:
        content = "# Graduation Candidates\n\nAuto-detected by graduation-check.py. Review with /evolve.\n"

    content += entry
    CANDIDATES_PATH.write_text(content, encoding="utf-8")


def main():
    # Read hook input from stdin
    try:
        data = json.loads(sys.stdin.read())
    except (json.JSONDecodeError, EOFError):
        return

    tool = data.get("tool_name", "")
    if tool not in ("Write", "Edit"):
        return

    # Extract file path from tool input
    tool_input = data.get("tool_input", {})
    if isinstance(tool_input, str):
        try:
            tool_input = json.loads(tool_input)
        except json.JSONDecodeError:
            return

    file_path = tool_input.get("file_path", "") or tool_input.get("path", "")
    if "learnings/" not in file_path:
        return

    filename = Path(file_path).name
    if filename in SKIP_FILES or filename.startswith("index-"):
        return

    # Read the file and check graduation
    target = Path(file_path)
    if not target.exists():
        return

    try:
        content = target.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return

    fm = parse_frontmatter(content)
    if not fm:
        return

    action = check_graduation(fm)
    if action is None:
        return

    if is_already_candidate(filename):
        return

    summary = str(fm.get("summary", ""))
    if action == "graduate" and is_already_graduated(summary):
        return

    append_candidate(filename, fm, action)

    # Output context to inform Claude
    msg = {
        "additionalContext": (
            f"[graduation-check] Learning '{filename}' is ready for {action}. "
            f"Uses={fm.get('uses', 0)}, confidence={fm.get('confidence', 'N/A')}, "
            f"harmful={fm.get('harmful_uses', 0)}. "
            f"Run /evolve to process graduation candidates."
        )
    }
    print(json.dumps(msg))


if __name__ == "__main__":
    main()
