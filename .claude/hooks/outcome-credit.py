#!/usr/bin/env python3
"""PostToolUse hook: update learning credit counters from outcome records.

Fires on Write operations to .claude/memory/outcomes/ files.
Reads `learnings_applied` from the outcome YAML frontmatter and increments
helpful/harmful/neutral counters on referenced learning files.

Closes the retrieval-use-feedback loop (RCL integration, Phase 1).

Confidence boost on helpful credit follows Hippo logarithmic formula
(arXiv: derived from kitfunso/hippo-memory src/memory.ts:104-155):
  boost(n) = 0.1 * log2(n + 1)
  delta(n -> n+1) = boost(n+1) - boost(n)
This produces diminishing returns: 1st use +0.10, 5th +0.022, 100th +0.0014.
Replaces the prior linear +0.05 per use which saturated confidence at cap=1.0
after ~6 uses, losing rank discrimination between 10x and 100x used learnings.
"""
import json
import math
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
OUTCOMES_DIR = "memory/outcomes/"
LEARNINGS_DIR = PROJECT_ROOT / ".claude/memory/learnings"


def parse_frontmatter(content: str) -> dict:
    """Parse YAML frontmatter from file content."""
    if not content.startswith("---"):
        return {}
    end = content.find("---", 3)
    if end == -1:
        return {}
    fm_text = content[3:end].strip()
    result = {}
    for line in fm_text.splitlines():
        if ":" in line:
            key, _, val = line.partition(":")
            result[key.strip()] = val.strip()
    return result


def parse_learnings_applied(content: str) -> list[dict]:
    """Extract learnings_applied entries from outcome body.

    Format in outcome file:
    ## Learnings Applied
    - file: some-learning.md | credit: helpful | evidence: ...
    - file: other.md | credit: harmful | evidence: ...
    """
    entries = []
    in_section = False
    for line in content.splitlines():
        if line.strip().startswith("## Learnings Applied"):
            in_section = True
            continue
        if in_section and line.startswith("## "):
            break
        if in_section and line.strip().startswith("- file:"):
            parts = {}
            for segment in line.strip().lstrip("- ").split("|"):
                segment = segment.strip()
                if ":" in segment:
                    k, _, v = segment.partition(":")
                    parts[k.strip()] = v.strip()
            if "file" in parts:
                entries.append({
                    "file": parts["file"],
                    "credit": parts.get("credit", "neutral"),
                    "evidence": parts.get("evidence", ""),
                })
    return entries


def update_learning_counter(learning_file: Path, credit: str) -> bool:
    """Update a learning file's counters based on credit signal."""
    if not learning_file.exists():
        return False

    content = learning_file.read_text(encoding="utf-8", errors="replace")
    if not content.startswith("---"):
        return False

    end = content.find("---", 3)
    if end == -1:
        return False

    fm_text = content[3:end]
    body = content[end + 3:]
    modified = False

    def read_field(text: str, field: str) -> int:
        pattern = re.compile(rf"^{field}:\s*(\d+)", re.MULTILINE)
        match = pattern.search(text)
        return int(match.group(1)) if match else 0

    def bump_field(text: str, field: str, delta: int) -> str:
        pattern = re.compile(rf"^({field}:\s*)(\d+)", re.MULTILINE)
        match = pattern.search(text)
        if match:
            old_val = int(match.group(2))
            new_val = max(0, old_val + delta)
            return pattern.sub(rf"\g<1>{new_val}", text, count=1)
        # Field doesn't exist — append it before end of frontmatter
        return text.rstrip() + f"\n{field}: {max(0, delta)}\n"

    def bump_confidence(text: str, delta: float) -> str:
        pattern = re.compile(r"^(confidence:\s*)([\d.]+)", re.MULTILINE)
        match = pattern.search(text)
        if match:
            old_val = float(match.group(2))
            new_val = round(min(1.0, max(0.0, old_val + delta)), 3)
            return pattern.sub(rf"\g<1>{new_val}", text, count=1)
        return text

    def log_boost_delta(uses_before: int) -> float:
        """Hippo log2-based incremental boost: delta(n -> n+1) = 0.1*(log2(n+2) - log2(n+1))."""
        return 0.1 * (math.log2(uses_before + 2) - math.log2(uses_before + 1))

    if credit == "helpful":
        uses_before = read_field(fm_text, "uses")
        fm_text = bump_field(fm_text, "uses", 1)
        fm_text = bump_field(fm_text, "successful_uses", 1)
        fm_text = bump_confidence(fm_text, log_boost_delta(uses_before))
        modified = True
    elif credit == "harmful":
        fm_text = bump_field(fm_text, "uses", 1)
        fm_text = bump_field(fm_text, "harmful_uses", 1)
        fm_text = bump_confidence(fm_text, -0.15)
        modified = True
    elif credit == "neutral":
        fm_text = bump_field(fm_text, "uses", 1)
        modified = True

    if modified:
        new_content = f"---{fm_text}---{body}"
        learning_file.write_text(new_content, encoding="utf-8")

    return modified


def main():
    try:
        hook_input = json.loads(sys.stdin.read())
    except (json.JSONDecodeError, EOFError):
        return

    tool_name = hook_input.get("tool_name", "")
    tool_input = hook_input.get("tool_input", {})

    if tool_name != "Write":
        return

    file_path = tool_input.get("file_path", "").replace("\\", "/")
    if OUTCOMES_DIR not in file_path:
        return

    # Read the just-written outcome file
    outcome_path = Path(file_path)
    if not outcome_path.exists():
        return

    content = outcome_path.read_text(encoding="utf-8", errors="replace")
    entries = parse_learnings_applied(content)

    if not entries:
        return

    updated = []
    for entry in entries:
        learning_path = LEARNINGS_DIR / entry["file"]
        if update_learning_counter(learning_path, entry["credit"]):
            updated.append(f"{entry['file']} ({entry['credit']})")

    if updated:
        print(json.dumps({
            "decision": "allow",
            "reason": f"Credit updated: {', '.join(updated)}"
        }))


if __name__ == "__main__":
    try:
        main()
    except Exception:
        pass  # Never block tool execution
