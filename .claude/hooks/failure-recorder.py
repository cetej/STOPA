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

OUTCOMES_DIR = "memory/outcomes/"
FAILURES_DIR = Path(".claude/memory/failures")
MAX_FAILURES = 50


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

    failure_content = f"""---
id: {fid}
date: {today}
task: "{task}"
failure_class: {failure_class}
failure_agent: {skill}
resolved: false
resolution_learning: ""
source_outcome: "{outcome_path.name}"
---

## Trajectory

{trajectory.strip() if trajectory.strip() else f"See outcome file: {outcome_path.name}"}

## Root Cause

To be analyzed — auto-generated from outcome record.

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
