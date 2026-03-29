#!/usr/bin/env python3
"""TaskCompleted hook: auto-capture learnings from completed orchestrated tasks.

Architecture (lazy evaluation):
- Reads state.md (current task summary) + last 60 lines of activity-log.md
- Calls Haiku to evaluate if the task produced a learning worth capturing
- confidence >= 0.8 → write to learnings/ directly
- confidence <  0.8 → print suggestion to stdout (injected into Claude's context)

If Haiku call fails: silent exit (no crash, no noise).
"""
import json
import re
import subprocess
import sys
from datetime import date
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")

MEMORY_DIR = Path(".claude/memory")
STATE_PATH = MEMORY_DIR / "state.md"
ACTIVITY_LOG = MEMORY_DIR / "activity-log.md"
LEARNINGS_DIR = MEMORY_DIR / "learnings"
CONFIDENCE_THRESHOLD = 0.8


def read_state() -> str:
    """Read current task state."""
    if not STATE_PATH.exists():
        return ""
    return STATE_PATH.read_text(encoding="utf-8", errors="replace")


def read_recent_activity(n_lines: int = 60) -> str:
    """Read last N lines of activity log."""
    if not ACTIVITY_LOG.exists():
        return ""
    lines = ACTIVITY_LOG.read_text(encoding="utf-8", errors="replace").splitlines()
    return "\n".join(lines[-n_lines:])


def build_prompt(state: str, activity: str) -> str:
    return f"""Analyze this completed STOPA orchestration task and decide if a reusable learning should be captured.

TASK STATE:
{state[:2000]}

RECENT ACTIVITY (last 60 lines):
{activity[:1500]}

INSTRUCTIONS:
Evaluate whether this task produced a non-obvious insight worth capturing for future sessions.
A learning is worth capturing if:
- A bug or unexpected behavior was discovered and fixed
- An architectural decision was made that future sessions should respect
- A workflow pattern emerged that was significantly more effective than alternatives
- An anti-pattern was identified (something that doesn't work and why)

A learning is NOT worth capturing if:
- The task was routine (standard feature implementation with no surprises)
- No obstacles or unexpected decisions occurred
- The insight is obvious or already well-known

Return ONLY valid JSON (no markdown fencing):
{{
  "confidence": 0.0,
  "capture": false,
  "learning": {{
    "title": "short-kebab-case-slug",
    "type": "bug_fix|architecture|anti_pattern|best_practice|workflow",
    "severity": "critical|high|medium|low",
    "component": "skill|hook|memory|orchestration|pipeline|general",
    "tags": ["tag1", "tag2"],
    "description": "What happened and what to do. 2 sentences max.",
    "prevention": "How to avoid or leverage this in the future."
  }},
  "suggestion": "One-line suggestion if confidence < 0.8 (empty string otherwise)"
}}

If nothing notable, return confidence 0.0 and capture false."""


def call_haiku(prompt: str) -> dict | None:
    """Call Haiku via claude CLI and parse JSON response."""
    try:
        result = subprocess.run(
            ["claude", "--model", "haiku", "--print", "-p", prompt],
            capture_output=True,
            text=True,
            timeout=12,
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


def write_learning(learning: dict) -> str | None:
    """Write learning to learnings/ with YAML frontmatter. Returns filename or None."""
    LEARNINGS_DIR.mkdir(parents=True, exist_ok=True)
    today = date.today().isoformat()
    slug = learning.get("title", "unknown")[:50]
    slug = re.sub(r"[^a-z0-9-]", "-", slug.lower()).strip("-")
    filename = f"{today}-auto-{slug}.md"
    filepath = LEARNINGS_DIR / filename

    if filepath.exists():
        return None  # Don't overwrite

    tags_str = ", ".join(learning.get("tags", []))
    desc = learning.get("description", "N/A")
    prevention = learning.get("prevention", "")
    summary = (desc + (f" Fix: {prevention[:60]}" if prevention and len(desc) < 100 else ""))
    summary = summary[:200].replace('"', "'").replace("\n", " ").strip()

    content = f"""---
date: {today}
type: {learning.get("type", "workflow")}
severity: {learning.get("severity", "medium")}
component: {learning.get("component", "general")}
tags: [{tags_str}]
summary: "{summary}"
uses: 0
harmful_uses: 0
source: auto-compound
---

## Problém
{desc}

## Řešení / Prevence
{prevention or "N/A"}
"""
    filepath.write_text(content, encoding="utf-8")
    return filename


def main():
    state = read_state()
    if not state.strip():
        sys.exit(0)

    activity = read_recent_activity()
    prompt = build_prompt(state, activity)

    result = call_haiku(prompt)
    if result is None:
        sys.exit(0)  # Haiku unavailable — silent exit

    confidence = float(result.get("confidence", 0.0))
    should_capture = result.get("capture", False)

    if should_capture and confidence >= CONFIDENCE_THRESHOLD:
        learning = result.get("learning", {})
        if learning and learning.get("title"):
            filename = write_learning(learning)
            if filename:
                print(f"[Auto-compound] Learning captured: {filename} (confidence: {confidence:.0%})")
    elif result.get("suggestion"):
        # Low confidence — print suggestion to context without writing
        print(f"[Auto-compound] Possible learning (confidence: {confidence:.0%}): {result['suggestion']}")
        print("  → Run /scribe if you want to capture this manually.")


if __name__ == "__main__":
    main()
