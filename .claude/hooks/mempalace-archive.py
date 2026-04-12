#!/usr/bin/env python3
"""Stop hook: archive session summary to MemPalace.

Reads the session-summary.json (produced by session-summary.sh) and
checkpoint.md, then stores a condensed session record as a MemPalace drawer.

Wing: project name (from cwd or git remote)
Room: "sessions" (all session records in one room)
Content: structured session summary with task, files, learnings, errors

Runs AFTER session-summary.sh (order matters in settings.json).
Skips subagent Stop events and trivial sessions (< 2 significant ops).

Dependencies: mempalace (pip install mempalace)
"""
import json
import sys
import os
from pathlib import Path
from datetime import datetime

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

PALACE_DIR = Path.home() / ".mempalace" / "palace"
MEMORY_DIR = Path(".claude/memory")
SUMMARY_FILE = MEMORY_DIR / "intermediate" / "session-summary.json"
CHECKPOINT_FILE = MEMORY_DIR / "checkpoint.md"


def get_project_name() -> str:
    """Derive project name from git remote or cwd."""
    try:
        import subprocess

        result = subprocess.run(
            ["git", "remote", "get-url", "origin"],
            capture_output=True,
            text=True,
            timeout=5,
        )
        if result.returncode == 0:
            url = result.stdout.strip()
            # Extract repo name from URL
            name = url.rstrip("/").split("/")[-1]
            if name.endswith(".git"):
                name = name[:-4]
            return name.lower()
    except Exception:
        pass
    return Path.cwd().name.lower()


def read_checkpoint_summary() -> str:
    """Extract resume-relevant section from checkpoint.md."""
    if not CHECKPOINT_FILE.exists():
        return ""
    try:
        text = CHECKPOINT_FILE.read_text(encoding="utf-8", errors="replace")
        # Take everything above the detail log boundary
        boundary = "## Session Detail Log"
        idx = text.find(boundary)
        if idx > 0:
            text = text[:idx]
        # Trim to max 2000 chars
        if len(text) > 2000:
            text = text[:2000] + "\n...(truncated)"
        return text
    except Exception:
        return ""


def build_drawer_content(summary: dict, checkpoint: str) -> str:
    """Build structured content for the MemPalace drawer."""
    ts = summary.get("timestamp", datetime.now().isoformat())
    activity = summary.get("activity", {})
    task = summary.get("task", "none")
    skills = summary.get("skills", [])
    errors = summary.get("errors", [])
    files = summary.get("files_touched", [])
    corrections = summary.get("corrections_today", 0)
    frustrations = summary.get("frustrations_today", 0)

    lines = [
        f"# Session {ts[:10]}",
        f"**Task**: {task}",
        f"**Activity**: {activity.get('writes', 0)} writes, "
        f"{activity.get('agents', 0)} agents, "
        f"{activity.get('skills', 0)} skill calls, "
        f"{activity.get('errors', 0)} errors",
    ]

    if skills:
        lines.append(f"**Skills used**: {', '.join(skills)}")

    if corrections > 0 or frustrations > 0:
        lines.append(
            f"**Corrections**: {corrections}, **Frustrations**: {frustrations}"
        )

    if files:
        lines.append("\n## Files Touched")
        for f in files[:20]:  # cap at 20
            lines.append(f"- {f}")

    if errors:
        lines.append("\n## Errors")
        for e in errors[:5]:
            lines.append(f"- {e}")

    if checkpoint:
        lines.append("\n## Checkpoint Summary")
        lines.append(checkpoint)

    return "\n".join(lines)


def main():
    # Skip subagent events
    try:
        hook_input = sys.stdin.read()
        if hook_input and '"agent_type"' in hook_input:
            return
    except Exception:
        pass

    # Check if session-summary.json exists (produced by session-summary.sh)
    if not SUMMARY_FILE.exists():
        return

    try:
        summary = json.loads(SUMMARY_FILE.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return

    # Skip trivial sessions
    activity = summary.get("activity", {})
    total = (
        activity.get("writes", 0)
        + activity.get("agents", 0)
        + activity.get("skills", 0)
    )
    if total < 2:
        return

    # Check mempalace is available
    try:
        from mempalace.palace import get_collection
    except ImportError:
        print("mempalace-archive: mempalace not installed, skipping")
        return

    # Ensure palace directory exists
    PALACE_DIR.mkdir(parents=True, exist_ok=True)

    # Build content
    checkpoint = read_checkpoint_summary()
    content = build_drawer_content(summary, checkpoint)

    # Store in MemPalace
    project = get_project_name()
    ts = summary.get("timestamp", datetime.now().isoformat())
    date_str = ts[:10]

    try:
        collection = get_collection(str(PALACE_DIR))
        # Add as a drawer with metadata
        doc_id = f"session-{project}-{date_str}-{ts[11:19].replace(':', '')}"
        collection.add(
            documents=[content],
            metadatas=[
                {
                    "wing": project,
                    "room": "sessions",
                    "hall": "events",
                    "source_file": f"session-{date_str}",
                    "date": date_str,
                    "added_by": "stopa-archive-hook",
                }
            ],
            ids=[doc_id],
        )
        print(f"mempalace-archive: archived session to {project}/sessions ({len(content)} chars)")
    except Exception as e:
        # Non-fatal — session archive is best-effort
        print(f"mempalace-archive: failed to archive: {e}")


if __name__ == "__main__":
    main()
