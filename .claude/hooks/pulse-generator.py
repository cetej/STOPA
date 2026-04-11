#!/usr/bin/env python3
"""SessionStart hook: Generate unified system pulse across all registered projects.

Phase 3 of Intelligence Architecture — Unified World Model.
Reads memory files from all projects in projects.json, produces a single
pulse.json snapshot at ~/.claude/memory/pulse.json.

Non-blocking: gracefully handles missing projects/files.
Read-only on project dirs: never mutates source files.
"""
import json
import os
import re
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")

# --- Config ---
PROJECTS_FILE = Path.home() / ".claude" / "memory" / "projects.json"
PULSE_FILE = Path.home() / ".claude" / "memory" / "pulse.json"
CACHE_MAX_AGE_MINUTES = 30  # Don't regenerate if pulse is <30min old


def load_projects() -> list[dict]:
    """Load project registry."""
    if not PROJECTS_FILE.exists():
        return []
    try:
        data = json.loads(PROJECTS_FILE.read_text(encoding="utf-8"))
        return data.get("projects", [])
    except (json.JSONDecodeError, OSError):
        return []


def parse_frontmatter(content: str) -> dict:
    """Parse simple YAML-like frontmatter from markdown file."""
    if not content.startswith("---"):
        return {}
    end = content.find("---", 3)
    if end == -1:
        return {}
    result = {}
    for line in content[3:end].strip().splitlines():
        if ":" in line:
            key, _, val = line.partition(":")
            result[key.strip()] = val.strip().strip('"').strip("'")
    return result


def read_safe(path: Path, limit: int = 50) -> str:
    """Read file safely, return empty string on failure. Limit to N lines."""
    try:
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
        return "\n".join(lines[:limit])
    except OSError:
        return ""


def extract_checkpoint_info(memory_dir: Path) -> dict:
    """Extract checkpoint summary from a project."""
    cp_file = memory_dir / "checkpoint.md"
    if not cp_file.exists():
        return {"exists": False}

    content = read_safe(cp_file, 30)
    fm = parse_frontmatter(content)

    # Parse from frontmatter or body
    info = {"exists": True}

    # Date
    saved_match = re.search(r"\*\*Saved\*\*:\s*(\d{4}-\d{2}-\d{2})", content)
    if saved_match:
        info["saved"] = saved_match.group(1)
    elif "saved" in fm:
        info["saved"] = fm["saved"][:10]

    # Task
    task_match = re.search(r"\*\*Task\*\*:\s*(.+)", content)
    if task_match:
        task = task_match.group(1).strip()
        info["task"] = task if task.lower() != "none" else None

    # Progress
    progress_match = re.search(r"(\d+)/(\d+)\s*subtasks?\s*(done|complete)", content, re.I)
    if progress_match:
        info["progress"] = f"{progress_match.group(1)}/{progress_match.group(2)}"

    return info


def extract_state_info(memory_dir: Path) -> dict:
    """Extract active task from state.md."""
    state_file = memory_dir / "state.md"
    if not state_file.exists():
        return {"active_task": None}

    content = read_safe(state_file, 20)
    fm = parse_frontmatter(content)

    task = fm.get("task", fm.get("current_task", ""))
    if task and task.lower() not in ("none", "null", ""):
        return {"active_task": task}
    return {"active_task": None}


def extract_budget_info(memory_dir: Path) -> dict:
    """Extract budget tier and spend from budget.md."""
    budget_file = memory_dir / "budget.md"
    if not budget_file.exists():
        return {}

    content = read_safe(budget_file, 30)
    fm = parse_frontmatter(content)

    info = {}
    if "tier" in fm:
        info["tier"] = fm["tier"]

    # Count agent spawns
    agent_count = content.count("Agent spawned") + content.count("agent spawned")
    if agent_count:
        info["agents_spawned"] = agent_count

    return info


def extract_outcomes_info(memory_dir: Path) -> dict:
    """Extract outcomes summary if available."""
    summary_file = memory_dir / "outcomes-summary.json"
    if not summary_file.exists():
        return {}

    try:
        data = json.loads(summary_file.read_text(encoding="utf-8"))
        return {
            "total_runs": data.get("total_runs", 0),
            "success_rate": data.get("success_rate", 0),
            "last_7_days": data.get("last_7_days", {}),
            "failure_streak": data.get("failure_streak", 0),
        }
    except (json.JSONDecodeError, OSError):
        return {}


def count_learnings(memory_dir: Path) -> int:
    """Count learning files."""
    learnings_dir = memory_dir / "learnings"
    if not learnings_dir.is_dir():
        return 0
    return len(list(learnings_dir.glob("*.md")))


def count_stale_learnings(memory_dir: Path, stale_days: int = 90) -> int:
    """Count learnings older than stale_days."""
    learnings_dir = memory_dir / "learnings"
    if not learnings_dir.is_dir():
        return 0

    cutoff = (datetime.now(timezone.utc) - timedelta(days=stale_days)).strftime("%Y-%m-%d")
    stale = 0
    for f in learnings_dir.glob("*.md"):
        # Filename starts with date: YYYY-MM-DD-...
        date_match = re.match(r"(\d{4}-\d{2}-\d{2})", f.name)
        if date_match and date_match.group(1) < cutoff:
            stale += 1
    return stale


def count_open_failures(memory_dir: Path) -> int:
    """Count unresolved failure records."""
    failures_dir = memory_dir / "failures"
    if not failures_dir.is_dir():
        return 0

    count = 0
    for f in failures_dir.glob("*.md"):
        content = read_safe(f, 15)
        if "resolved: false" in content or "resolved: False" in content:
            count += 1
    return count


def determine_health(project_data: dict) -> str:
    """Determine project health: green/yellow/red."""
    # Red conditions
    if project_data.get("failure_streak", 0) >= 3:
        return "red"
    if project_data.get("open_failures", 0) >= 3:
        return "red"

    # Yellow conditions
    if project_data.get("stale_learnings", 0) >= 5:
        return "yellow"
    if project_data.get("open_failures", 0) >= 1:
        return "yellow"
    outcomes_7d = project_data.get("outcomes_7d", {})
    if outcomes_7d.get("failure", 0) >= 2:
        return "yellow"

    # Check checkpoint staleness
    cp = project_data.get("checkpoint", {})
    if cp.get("saved"):
        try:
            saved = datetime.strptime(cp["saved"], "%Y-%m-%d").replace(tzinfo=timezone.utc)
            age = (datetime.now(timezone.utc) - saved).days
            if age > 14:
                return "yellow"
        except ValueError:
            pass

    return "green"


def count_capability_gaps(memory_dir: Path) -> int:
    """Count open capability gaps."""
    gaps_file = memory_dir / "capability-gaps.md"
    if not gaps_file.exists():
        return 0
    try:
        text = gaps_file.read_text(encoding="utf-8", errors="replace")
        count = 0
        for line in text.split("\n"):
            if line.startswith("|") and "open" in line.lower():
                count += 1
        return count
    except Exception:
        return 0


def build_project_pulse(project: dict) -> dict:
    """Build pulse data for a single project."""
    path = Path(project.get("path", ""))
    memory_dir = path / ".claude" / "memory"

    result = {
        "name": project.get("name", "unknown"),
        "type": project.get("type", ""),
        "path_exists": path.is_dir(),
    }

    if not memory_dir.is_dir():
        result["health"] = "unknown"
        result["has_memory"] = False
        return result

    result["has_memory"] = True

    # Gather data
    state = extract_state_info(memory_dir)
    result["active_task"] = state.get("active_task")

    cp = extract_checkpoint_info(memory_dir)
    result["checkpoint"] = cp

    budget = extract_budget_info(memory_dir)
    result.update(budget)

    outcomes = extract_outcomes_info(memory_dir)
    if outcomes:
        result["outcomes_total"] = outcomes.get("total_runs", 0)
        result["outcomes_7d"] = outcomes.get("last_7_days", {})
        result["failure_streak"] = outcomes.get("failure_streak", 0)
        result["success_rate"] = outcomes.get("success_rate", 0)

    result["learnings_count"] = count_learnings(memory_dir)
    result["stale_learnings"] = count_stale_learnings(memory_dir)
    result["open_failures"] = count_open_failures(memory_dir)
    result["capability_gaps"] = count_capability_gaps(memory_dir)

    # Determine health
    result["health"] = determine_health(result)

    return result


def build_alerts(projects_data: list[dict]) -> list[dict]:
    """Generate system-wide alerts from project data."""
    alerts = []

    for p in projects_data:
        name = p.get("name", "?")

        if not p.get("path_exists"):
            alerts.append({"level": "error", "project": name, "message": f"Project path not found"})
            continue

        if not p.get("has_memory"):
            continue  # Projects without memory are fine (no orchestration)

        if p.get("health") == "red":
            alerts.append({"level": "error", "project": name, "message": f"Health RED — check failures"})

        if p.get("open_failures", 0) >= 1:
            alerts.append({
                "level": "warn",
                "project": name,
                "message": f"{p['open_failures']} unresolved failure(s)",
            })

        stale = p.get("stale_learnings", 0)
        if stale >= 5:
            alerts.append({
                "level": "info",
                "project": name,
                "message": f"{stale} stale learnings (>90 days)",
            })

        cp = p.get("checkpoint", {})
        if cp.get("saved"):
            try:
                age = (datetime.now(timezone.utc) - datetime.strptime(cp["saved"], "%Y-%m-%d").replace(tzinfo=timezone.utc)).days
                if age > 14:
                    alerts.append({
                        "level": "info",
                        "project": name,
                        "message": f"Checkpoint is {age} days old",
                    })
            except ValueError:
                pass

    return alerts


def compute_system_health(projects_data: list[dict]) -> dict:
    """Compute system-wide health metrics."""
    active_projects = [p for p in projects_data if p.get("has_memory")]

    if not active_projects:
        return {"overall": "unknown", "active_projects": 0}

    healths = [p.get("health", "unknown") for p in active_projects]

    # Overall: worst health across projects
    if "red" in healths:
        overall = "red"
    elif "yellow" in healths:
        overall = "yellow"
    else:
        overall = "green"

    # Signal coverage: fraction of projects with outcomes data
    with_outcomes = sum(1 for p in active_projects if p.get("outcomes_total", 0) > 0)
    coverage = round(with_outcomes / len(active_projects), 2) if active_projects else 0

    # Total learnings across projects
    total_learnings = sum(p.get("learnings_count", 0) for p in active_projects)

    return {
        "overall": overall,
        "active_projects": len(active_projects),
        "signal_coverage": coverage,
        "total_learnings": total_learnings,
    }


def format_pulse_message(pulse: dict) -> str:
    """Format a compact pulse message for SessionStart display."""
    sys_health = pulse.get("system_health", {})
    overall = sys_health.get("overall", "?")
    active = sys_health.get("active_projects", 0)
    coverage = sys_health.get("signal_coverage", 0)

    lines = [f"=== System Pulse: {overall.upper()} ({active} projects, {coverage:.0%} signal coverage) ==="]

    # Per-project summary
    for p in pulse.get("projects", []):
        if not p.get("has_memory"):
            continue
        name = p["name"]
        health = p.get("health", "?")
        task = p.get("active_task") or "idle"
        if len(task) > 40:
            task = task[:37] + "..."
        lines.append(f"  {name}: {health} — {task}")

    # Top alerts
    alerts = pulse.get("alerts", [])
    errors = [a for a in alerts if a["level"] == "error"]
    warns = [a for a in alerts if a["level"] == "warn"]

    if errors:
        for a in errors[:2]:
            lines.append(f"  ! {a['project']}: {a['message']}")
    if warns:
        for a in warns[:2]:
            lines.append(f"  ~ {a['project']}: {a['message']}")

    return "\n".join(lines)


def main():
    # Check cache: don't regenerate if fresh
    if PULSE_FILE.exists():
        try:
            existing = json.loads(PULSE_FILE.read_text(encoding="utf-8"))
            generated = existing.get("generated", "")
            if generated:
                gen_time = datetime.fromisoformat(generated.replace("Z", "+00:00"))
                age_min = (datetime.now(timezone.utc) - gen_time).total_seconds() / 60
                if age_min < CACHE_MAX_AGE_MINUTES:
                    # Cache is fresh — just output the message
                    print(format_pulse_message(existing))
                    return
        except (json.JSONDecodeError, ValueError, OSError):
            pass  # Regenerate

    # Load projects
    projects = load_projects()
    if not projects:
        print("=== System Pulse: no projects registered ===")
        return

    # Build pulse for each project
    projects_data = []
    for proj in projects:
        if proj.get("status") != "active":
            continue
        projects_data.append(build_project_pulse(proj))

    # Build alerts
    alerts = build_alerts(projects_data)

    # System health
    sys_health = compute_system_health(projects_data)

    # Assemble pulse
    pulse = {
        "generated": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "projects": projects_data,
        "alerts": alerts,
        "system_health": sys_health,
    }

    # Write pulse (global location)
    PULSE_FILE.parent.mkdir(parents=True, exist_ok=True)
    tmp = PULSE_FILE.with_suffix(".tmp")
    tmp.write_text(json.dumps(pulse, indent=2, ensure_ascii=False), encoding="utf-8")
    tmp.replace(PULSE_FILE)

    # Output summary for SessionStart display
    print(format_pulse_message(pulse))


if __name__ == "__main__":
    main()
