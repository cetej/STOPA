#!/usr/bin/env python3
"""Background async extractor: processes mid-session snapshots into learnings.

Called by mid-session-capture.py as a fire-and-forget subprocess.
Uses Haiku to extract learnings from recent activity, same format as auto-scribe.py.
Runs outside the hook timeout — takes as long as needed.
"""
import json
import os
import re
import subprocess
import sys
from datetime import date
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")

MEMORY_DIR = Path(".claude/memory")
PENDING_PATH = MEMORY_DIR / "intermediate" / "pending-capture.json"
LEARNINGS_DIR = MEMORY_DIR / "learnings"


def load_pending() -> dict | None:
    """Load and consume pending capture snapshot."""
    if not PENDING_PATH.exists():
        return None
    try:
        data = json.loads(PENDING_PATH.read_text(encoding="utf-8"))
        return data
    except (json.JSONDecodeError, OSError):
        PENDING_PATH.unlink(missing_ok=True)
        return None


def build_prompt(snapshot: dict) -> str:
    """Build extraction prompt for Haiku."""
    activity = "\n".join(snapshot.get("recent_activity", []))
    return f"""Analyze this mid-session activity log and extract any notable learnings.

ACTIVITY (last 30 operations):
{activity}

CURRENT STATE: {snapshot.get('state_snapshot', 'unknown')}

INSTRUCTIONS:
- Extract ONLY genuinely notable insights (bugs found, workflow patterns, architectural decisions).
- Skip trivial operations like "user read file" or "user ran git status".
- Be very selective — only 0-2 learnings per extraction. Quality over quantity.
- If nothing notable, return empty learnings array.

Return ONLY valid JSON (no markdown fencing):
{{
  "learnings": [
    {{
      "title": "short-kebab-case-slug",
      "type": "bug_fix|architecture|anti_pattern|best_practice|workflow",
      "severity": "critical|high|medium|low",
      "component": "skill|hook|memory|orchestration|pipeline|general",
      "tags": ["tag1", "tag2"],
      "description": "What happened and why it matters",
      "prevention": "How to avoid or leverage this"
    }}
  ]
}}"""


def call_haiku(prompt: str) -> dict | None:
    """Call Haiku and parse JSON response."""
    try:
        result = subprocess.run(
            ["claude", "--model", "haiku", "--print", "-p", prompt],
            capture_output=True,
            text=True,
            timeout=15,
            encoding="utf-8",
            errors="replace",
        )
        if result.returncode != 0:
            return None
        output = result.stdout.strip()
        output = re.sub(r"^```(?:json)?\s*", "", output)
        output = re.sub(r"\s*```$", "", output)
        return json.loads(output)
    except (subprocess.TimeoutExpired, json.JSONDecodeError, FileNotFoundError):
        return None


def write_learning(learning: dict) -> bool:
    """Write a learning entry to learnings/ directory."""
    LEARNINGS_DIR.mkdir(parents=True, exist_ok=True)
    today = date.today().isoformat()
    slug = learning.get("title", "unknown")[:50]
    slug = re.sub(r"[^a-z0-9-]", "-", slug.lower()).strip("-")
    filename = f"{today}-mid-{slug}.md"
    filepath = LEARNINGS_DIR / filename

    if filepath.exists():
        return False

    tags_str = ", ".join(learning.get("tags", []))
    desc = learning.get("description", "N/A")
    prevention = learning.get("prevention", "")
    summary = desc[:120]
    if prevention and len(summary) < 100:
        summary += f" Fix: {prevention[:60]}"
    summary = summary.replace('"', "'").replace("\n", " ").strip()

    content = f"""---
date: {today}
type: {learning.get('type', 'workflow')}
severity: {learning.get('severity', 'medium')}
component: {learning.get('component', 'general')}
tags: [{tags_str}]
summary: "{summary}"
source: mid-session-capture
---

## Description
{desc}

## Prevention
{prevention or 'N/A'}
"""
    filepath.write_text(content, encoding="utf-8")
    return True


def main():
    snapshot = load_pending()
    if snapshot is None:
        return

    prompt = build_prompt(snapshot)
    result = call_haiku(prompt)

    if result is None:
        # Keep pending for retry (auto-scribe at next SessionStart will pick it up)
        return

    learnings = result.get("learnings", [])
    written = sum(1 for l in learnings if write_learning(l))

    # Clean up pending snapshot (processed successfully)
    PENDING_PATH.unlink(missing_ok=True)

    if written > 0:
        print(f"[Mid-session capture] Extracted {written} learnings", file=sys.stderr)


if __name__ == "__main__":
    main()
