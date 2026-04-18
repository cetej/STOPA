#!/usr/bin/env python3
"""PostToolUse hook: auto-record failure entries from outcome files.

Fires on Write operations to .claude/memory/outcomes/ files.
When outcome == 'failure' or 'partial', creates a failure record in failures/.
Counts same-class failures and suggests /learn-from-failure at 2+.

RCL integration, Phase 2.
"""
import json
import re
import sys
from datetime import date
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
OUTCOMES_DIR = "memory/outcomes/"
FAILURES_DIR = PROJECT_ROOT / ".claude/memory/failures"
MAX_FAILURES = 50

# --- ASI-Evolve Structured Diagnostics (arXiv:2603.29640) ---

# Fine-grained pattern types within each failure_class
PATTERN_KEYWORDS = [
    ("logic_wrong_assumption", [r"assumed", r"expected.*but got", r"wrong model", r"incorrect assumption"]),
    ("logic_scope_creep", [r"too many files", r"scope expanded", r"cross-cutting", r"more files than"]),
    ("resource_oom", [r"oom", r"memory", r"context window", r"token limit"]),
    ("timeout_long_task", [r"too long", r"many iterations", r"time limit"]),
    ("timeout_stuck_loop", [r"stuck", r"crash_loop", r"same error", r"repeating"]),
    ("integration_dependency", [r"missing dep", r"import error", r"hook blocked", r"not found"]),
]

APPROACH_CHANGES = {
    "logic_wrong_assumption": "Verify assumptions with a scout pass before writing code.",
    "logic_scope_creep": "Constrain scope with glob-first file enumeration before starting.",
    "resource_budget_exceeded": "Break task into smaller subtasks; use light tier for initial pass.",
    "resource_oom": "Use haiku for exploration phases; avoid loading all files at once.",
    "timeout_long_task": "Add intermediate checkpoints; split into 2-3 sequential subtasks.",
    "timeout_stuck_loop": "Check circuit breakers; use /systematic-debugging before retry.",
    "integration_dependency": "Run env snapshot before agent dispatch; pre-check requires: field.",
    "unknown": "Run /learn-from-failure for manual analysis.",
}


def classify_pattern_type(content: str, exit_reason: str, failure_class: str) -> str:
    """Classify fine-grained pattern type from outcome body text."""
    if exit_reason == "budget_exceeded":
        return "resource_budget_exceeded"
    body_lower = content.lower()
    for pattern_type, keywords in PATTERN_KEYWORDS:
        if any(re.search(kw, body_lower) for kw in keywords):
            return pattern_type
    return f"{failure_class}_unspecified" if failure_class != "logic" else "unknown"


def extract_root_cause_hypothesis(content: str) -> str:
    """Extract the most informative sentence about root cause from outcome body."""
    cause_re = re.compile(
        r"\b(fail|error|because|cause|wrong|issue|problem|blocked|broke|crash)\b", re.I
    )
    for line in content.splitlines():
        line = line.strip()
        if 20 < len(line) < 200 and cause_re.search(line):
            if not line.startswith("#") and not line.startswith("---"):
                return line.lstrip("- *").strip()
    return "No hypothesis extractable — review outcome file manually."


def recommend_approach_change(pattern_type: str, same_count: int) -> str:
    """Return recommended approach change for this failure pattern."""
    rec = APPROACH_CHANGES.get(pattern_type, APPROACH_CHANGES["unknown"])
    if same_count >= 3:
        rec = f"RECURRING ({same_count}x): {rec}"
    return rec


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
            result[key.strip()] = val.strip().strip('"').strip("'")
    return result


def next_failure_id() -> str:
    """Get next failure ID (F001, F002, ...)."""
    existing = list(FAILURES_DIR.glob("*-F???-*.md"))
    if not existing:
        return "F001"
    ids = []
    for f in existing:
        match = re.search(r"-F(\d{3})-", f.name)
        if match:
            ids.append(int(match.group(1)))
    return f"F{(max(ids) + 1) if ids else 1:03d}"


def count_same_class(failure_class: str, failure_agent: str) -> int:
    """Count existing failures with same class + agent."""
    count = 0
    for f in FAILURES_DIR.glob("*.md"):
        if f.name == ".gitkeep":
            continue
        try:
            content = f.read_text(encoding="utf-8", errors="replace")
            fm = parse_frontmatter(content)
            if fm.get("failure_class") == failure_class and fm.get("failure_agent") == failure_agent:
                count += 1
        except OSError:
            continue
    return count


def archive_old_failures():
    """Archive oldest failures when over MAX_FAILURES."""
    failures = sorted(FAILURES_DIR.glob("*-F???-*.md"), key=lambda f: f.name)
    if len(failures) <= MAX_FAILURES:
        return
    archive_dir = FAILURES_DIR / "archive"
    archive_dir.mkdir(exist_ok=True)
    to_archive = failures[:len(failures) - MAX_FAILURES]
    for f in to_archive:
        f.rename(archive_dir / f.name)


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

    outcome_path = Path(file_path)
    if not outcome_path.exists():
        return

    content = outcome_path.read_text(encoding="utf-8", errors="replace")
    fm = parse_frontmatter(content)

    outcome = fm.get("outcome", "")
    if outcome not in ("failure", "partial"):
        return

    # Extract fields
    skill = fm.get("skill", "unknown")
    task = fm.get("task", "unknown")
    exit_reason = fm.get("exit_reason", "unknown")

    # Map exit_reason to failure_class
    class_map = {
        "crash_loop": "logic",
        "budget_exceeded": "resource",
        "stuck": "logic",
        "plateau": "logic",
        "timeout": "timeout",
        "infra_error": "resource",
    }
    failure_class = class_map.get(exit_reason, "logic")

    # ASI-Evolve structured diagnostics
    pattern_type = classify_pattern_type(content, exit_reason, failure_class)
    root_cause = extract_root_cause_hypothesis(content)

    # Create failure record
    FAILURES_DIR.mkdir(parents=True, exist_ok=True)
    fid = next_failure_id()
    today = date.today().isoformat()
    slug = re.sub(r"[^a-z0-9]+", "-", task.lower())[:40].strip("-")
    filename = f"{today}-{fid}-{slug}.md"

    # Extract trajectory from outcome body (section ## Trajectory Summary)
    trajectory = ""
    in_traj = False
    for line in content.splitlines():
        if "## Trajectory Summary" in line or "## What Failed" in line:
            in_traj = True
            continue
        if in_traj and line.startswith("## "):
            break
        if in_traj:
            trajectory += line + "\n"

    # Count before writing so we include current record
    same_count = count_same_class(failure_class, skill) + 1
    approach = recommend_approach_change(pattern_type, same_count)

    failure_content = f"""---
id: {fid}
date: {today}
task: "{task}"
failure_class: {failure_class}
pattern_type: {pattern_type}
failure_agent: {skill}
resolved: false
resolution_learning: ""
source_outcome: "{outcome_path.name}"
---

## Trajectory

{trajectory.strip() if trajectory.strip() else f"See outcome file: {outcome_path.name}"}

## Root Cause

{root_cause}

## Diagnostic

- **pattern_type**: {pattern_type}
- **recommended_change**: {approach}

## Reflexion

Pending analysis. Run `/learn-from-failure` for systematic review.
"""

    failure_path = FAILURES_DIR / filename
    failure_path.write_text(failure_content, encoding="utf-8")

    # Archive old if needed
    archive_old_failures()

    # Count same-class failures for trigger
    same_count = count_same_class(failure_class, skill)

    messages = [f"Failure {fid} recorded: {failure_class} in {skill}"]
    if same_count >= 2:
        messages.append(
            f"⚠️ {same_count}× {failure_class} failure in {skill} "
            f"— consider `/learn-from-failure {skill}` for systematic analysis"
        )

    print(json.dumps({
        "decision": "allow",
        "reason": " | ".join(messages)
    }))


if __name__ == "__main__":
    try:
        main()
    except Exception:
        pass  # Never block tool execution
