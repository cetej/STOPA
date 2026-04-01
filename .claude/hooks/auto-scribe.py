#!/usr/bin/env python3
"""SessionStart hook: analyze previous session summary via Haiku and extract learnings + patterns.

Lazy evaluation pattern: Stop hook captures session-summary.json, this hook processes it
at next session start. If Haiku call fails, summary is kept for retry.

DeerFlow-inspired improvements (2026-03-28):
- Smart eviction for patterns: frequency × recency instead of FIFO
- Summary field auto-generated for learnings

Output (stdout): Injected into Claude's context as system message.
"""
import json
import os
import re
import subprocess
import sys
from datetime import date, datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
from atomic_utils import atomic_write

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")

MEMORY_DIR = Path(".claude/memory")
SUMMARY_PATH = MEMORY_DIR / "intermediate" / "session-summary.json"
PATTERNS_PATH = MEMORY_DIR / "patterns.md"
LEARNINGS_DIR = MEMORY_DIR / "learnings"

MIN_ACTIVITY_THRESHOLD = 3  # writes + agents >= 3 to be worth analyzing


def load_summary() -> dict | None:
    """Load and validate session summary JSON."""
    if not SUMMARY_PATH.exists():
        return None
    try:
        data = json.loads(SUMMARY_PATH.read_text(encoding="utf-8"))
        activity = data.get("activity", {})
        total = activity.get("writes", 0) + activity.get("agents", 0)
        if total < MIN_ACTIVITY_THRESHOLD:
            # Trivial session — delete and skip
            SUMMARY_PATH.unlink(missing_ok=True)
            return None
        return data
    except (json.JSONDecodeError, KeyError):
        # Corrupt file — delete
        SUMMARY_PATH.unlink(missing_ok=True)
        return None


def load_patterns() -> str:
    """Load current patterns.md content."""
    if PATTERNS_PATH.exists():
        return PATTERNS_PATH.read_text(encoding="utf-8")
    return ""


def build_haiku_prompt(summary: dict, patterns_content: str) -> str:
    """Build the analysis prompt for Haiku."""
    return f"""Analyze this Claude Code session summary and extract learnings and patterns.

SESSION SUMMARY:
{json.dumps(summary, indent=2)}

EXISTING PATTERNS (increment frequency if this session matches):
{patterns_content}

INSTRUCTIONS:
1. Extract notable learnings (bugs found, workflow improvements, architectural decisions).
   Skip trivial observations like "user edited files" — only capture non-obvious insights.
2. Detect recurring patterns by comparing with existing patterns.
3. If this session matches an existing pattern, note it for frequency increment.
4. If a genuinely new behavioral pattern emerges, describe it.

Return ONLY valid JSON (no markdown fencing, no explanation):
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
  ],
  "patterns": [
    {{
      "name": "Pattern Name",
      "category": "recurring_error|workflow_habit|time_pattern|tool_preference",
      "description": "What happens",
      "suggestion": "How to avoid/leverage",
      "is_existing": false
    }}
  ]
}}

If nothing notable, return {{"learnings": [], "patterns": []}}"""


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
            print(f"[Auto-scribe] Haiku call failed (exit {result.returncode})", file=sys.stderr)
            return None

        output = result.stdout.strip()
        # Strip markdown fencing if Haiku wraps it
        output = re.sub(r"^```(?:json)?\s*", "", output)
        output = re.sub(r"\s*```$", "", output)

        return json.loads(output)
    except subprocess.TimeoutExpired:
        print("[Auto-scribe] Haiku call timed out", file=sys.stderr)
        return None
    except json.JSONDecodeError:
        print("[Auto-scribe] Haiku returned invalid JSON", file=sys.stderr)
        return None
    except FileNotFoundError:
        print("[Auto-scribe] claude CLI not found", file=sys.stderr)
        return None


def write_learning(learning: dict) -> bool:
    """Write a learning entry to learnings/ directory."""
    LEARNINGS_DIR.mkdir(parents=True, exist_ok=True)
    today = date.today().isoformat()
    slug = learning.get("title", "unknown")[:50]
    slug = re.sub(r"[^a-z0-9-]", "-", slug.lower()).strip("-")
    filename = f"{today}-auto-{slug}.md"
    filepath = LEARNINGS_DIR / filename

    # Don't overwrite existing files
    if filepath.exists():
        return False

    tags_str = ", ".join(learning.get("tags", []))
    # Auto-generate summary from description + prevention (for memory-whisper matching)
    desc = learning.get('description', 'N/A')
    prevention = learning.get('prevention', '')
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
source: auto-scribe
---

## Description
{desc}

## Prevention
{prevention or 'N/A'}
"""
    atomic_write(filepath, content)
    return True


def compute_eviction_score(frequency: int, last_seen: str) -> float:
    """Compute eviction score: lower = more likely to be evicted.

    DeerFlow-inspired: combines frequency with recency decay.
    Score = frequency × recency_factor, where recency_factor decays over time.
    """
    try:
        last_date = datetime.strptime(last_seen, "%Y-%m-%d")
        days_ago = (datetime.now() - last_date).days
    except (ValueError, TypeError):
        days_ago = 90  # assume old if unparseable

    recency_factor = 1.0 / (1.0 + days_ago / 30.0)  # halves every 30 days
    return frequency * recency_factor


def evict_weakest_pattern(content: str) -> str | None:
    """Remove the pattern with lowest eviction score. Returns updated content or None."""
    pattern_blocks = re.findall(
        r"(### .+?)(?=### |\Z)",
        content,
        re.DOTALL,
    )
    if not pattern_blocks:
        return None

    worst_score = float("inf")
    worst_block = None

    for block in pattern_blocks:
        freq_match = re.search(r"\*\*Frequency\*\*:\s*(\d+)", block)
        date_match = re.search(r"\*\*Last seen\*\*:\s*(\d{4}-\d{2}-\d{2})", block)
        freq = int(freq_match.group(1)) if freq_match else 1
        last_seen = date_match.group(1) if date_match else ""
        score = compute_eviction_score(freq, last_seen)
        if score < worst_score:
            worst_score = score
            worst_block = block

    if worst_block:
        return content.replace(worst_block, "")
    return None


def update_patterns(new_patterns: list, existing_content: str) -> int:
    """Update patterns.md with new/incremented patterns. Returns count of changes."""
    today = date.today().isoformat()
    changes = 0

    # Parse existing patterns
    existing_names = set()
    lines = existing_content.split("\n")
    for line in lines:
        if line.startswith("### "):
            existing_names.add(line[4:].strip().lower())

    updated_content = existing_content

    for pattern in new_patterns:
        name = pattern.get("name", "Unknown")
        name_lower = name.lower()

        if pattern.get("is_existing") or name_lower in existing_names:
            # Increment frequency and update last_seen
            # Find the pattern block and update it
            pattern_re = re.compile(
                rf"(### {re.escape(name)}.*?)(- \*\*Frequency\*\*: )(\d+)(.*?)(- \*\*Last seen\*\*: )\d{{4}}-\d{{2}}-\d{{2}}",
                re.DOTALL | re.IGNORECASE,
            )
            match = pattern_re.search(updated_content)
            if match:
                freq = int(match.group(3)) + 1
                updated_content = (
                    updated_content[: match.start(2)]
                    + f"- **Frequency**: {freq}"
                    + match.group(4)
                    + f"- **Last seen**: {today}"
                    + updated_content[match.end() :]
                )
                changes += 1
        else:
            # Count existing patterns
            existing_count = len(existing_names)
            if existing_count >= 20:
                # Smart eviction: remove the pattern with lowest frequency × recency score
                evicted = evict_weakest_pattern(updated_content)
                if evicted:
                    updated_content = evicted
                    changes += 1
                else:
                    continue

            # Add new pattern
            new_block = f"""
### {name}
- **Category**: {pattern.get('category', 'workflow_habit')}
- **Frequency**: 1
- **Last seen**: {today}
- **Description**: {pattern.get('description', 'N/A')}
- **Suggestion**: {pattern.get('suggestion', 'N/A')}
"""
            # Insert before the end of file
            if "(empty" in updated_content:
                updated_content = updated_content.replace(
                    "(empty — will be populated after first auto-scribe run)", ""
                )
            updated_content = updated_content.rstrip() + "\n" + new_block
            existing_names.add(name_lower)
            changes += 1

    if changes > 0:
        atomic_write(PATTERNS_PATH, updated_content)

    return changes


def main():
    summary = load_summary()
    if summary is None:
        # No summary or trivial session — silent exit
        sys.exit(0)

    patterns_content = load_patterns()
    prompt = build_haiku_prompt(summary, patterns_content)

    result = call_haiku(prompt)
    if result is None:
        # Haiku failed — keep summary for retry at next session
        print(
            "[Auto-scribe] Analysis deferred (Haiku unavailable). Will retry next session.",
            file=sys.stderr,
        )
        sys.exit(0)

    # Process learnings
    learnings = result.get("learnings", [])
    written = sum(1 for l in learnings if write_learning(l))

    # Process patterns
    patterns = result.get("patterns", [])
    pattern_changes = update_patterns(patterns, patterns_content)

    # Clean up summary (processed successfully)
    SUMMARY_PATH.unlink(missing_ok=True)

    # Output to stdout → injected into Claude's context
    if written > 0 or pattern_changes > 0:
        print(f"=== AUTO-SCRIBE ===")
        print(f"Extracted {written} learnings, {pattern_changes} pattern updates from previous session")
        if written > 0:
            print(f"New learnings in: .claude/memory/learnings/")


if __name__ == "__main__":
    main()
