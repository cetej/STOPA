#!/usr/bin/env python3
"""PostToolUse hook (Skill): Auto-write micro-outcomes after skill completion.

Phase 1 of Intelligence Architecture — Signal Foundation.
Detects skill name and outcome status from tool result, writes minimal
outcome record to .claude/memory/outcomes/ and updates rolling aggregator.

Non-blocking, best-effort: if detection fails, silently exits.
Never overwrites existing outcomes (append-only).
"""
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")

# --- Config ---
OUTCOMES_DIR = Path(".claude/memory/outcomes")
SUMMARY_FILE = Path(".claude/memory/outcomes-summary.json")
MAX_OUTCOMES = 100  # archive threshold

# Outcome detection patterns (conservative: prefer no-write over wrong-write)
SUCCESS_PATTERNS = re.compile(
    r"\b(PASS|passed|success|done|complete[d]?|converge[d]?|verified|"
    r"proven|works|all good|approved|clean|green|hotovo|ok[,.\s]|"
    r"DONE|committed|fixed|improved|optimized|compiled)\b",
    re.IGNORECASE,
)
FAILURE_PATTERNS = re.compile(
    r"\b(FAIL|failed|failure|error|crash|blocked|stuck|"
    r"timeout|budget.?exceeded|circuit.?breaker|STOP|"
    r"nelze|selhalo|nefunguje)\b",
    re.IGNORECASE,
)
PARTIAL_PATTERNS = re.compile(
    r"\b(partial|partially|some.?issues|warnings?|"
    r"plateau|pivot|mixed|incomplete)\b",
    re.IGNORECASE,
)

# Exit reason detection
EXIT_REASONS = {
    "convergence": re.compile(r"converge|target.?reached|100%|all.?pass", re.I),
    "budget_exceeded": re.compile(r"budget|cost.?limit|token.?limit", re.I),
    "crash_loop": re.compile(r"crash|loop|circuit.?breaker|3.?fix|escalat", re.I),
    "stuck": re.compile(r"stuck|stagnant|no.?progress|plateau", re.I),
    "timeout": re.compile(r"timeout|too.?long|time.?limit", re.I),
}

# Skills to skip (meta/read-only, no meaningful outcome)
SKIP_SKILLS = {
    "status", "budget", "compact", "checkpoint",
    "help", "config", "update-config", "keybindings-help",
}


def detect_skill_name(tool_input: str) -> str:
    """Extract skill name from Skill tool input JSON."""
    try:
        data = json.loads(tool_input)
        return data.get("skill", "").strip().lstrip("/")
    except (json.JSONDecodeError, TypeError):
        m = re.search(r'"skill"\s*:\s*"([^"]+)"', tool_input)
        return m.group(1).strip().lstrip("/") if m else ""


def detect_outcome(output: str) -> str:
    """Classify outcome from tool output. Returns success|failure|partial|unknown."""
    # Check last 500 chars (conclusion is usually at the end)
    tail = output[-500:] if len(output) > 500 else output

    fail_matches = len(FAILURE_PATTERNS.findall(tail))
    success_matches = len(SUCCESS_PATTERNS.findall(tail))
    partial_matches = len(PARTIAL_PATTERNS.findall(tail))

    # Failure signals are stronger (conservative: failure > partial > success)
    if fail_matches >= 2:
        return "failure"
    if partial_matches >= 2 and fail_matches >= 1:
        return "partial"
    if success_matches >= 2 and fail_matches == 0:
        return "success"
    if partial_matches >= 1 and success_matches >= 1 and fail_matches == 0:
        return "partial"
    if success_matches >= 1 and fail_matches == 0:
        return "success"

    return "unknown"


def detect_exit_reason(output: str) -> str:
    """Detect exit reason from output text."""
    tail = output[-800:] if len(output) > 800 else output
    for reason, pattern in EXIT_REASONS.items():
        if pattern.search(tail):
            return reason
    return "normal"


def extract_one_line(output: str) -> str:
    """Extract a one-line summary from the output (last meaningful line)."""
    lines = [l.strip() for l in output.strip().splitlines() if l.strip()]
    # Skip very short lines or pure punctuation
    for line in reversed(lines[-10:]):
        if len(line) > 10 and not line.startswith("#") and not line.startswith("---"):
            # Truncate to 100 chars
            return line[:100]
    return "completed"


def write_micro_outcome(skill: str, outcome: str, exit_reason: str, one_line: str) -> Path:
    """Write micro-outcome file. Returns path of written file."""
    OUTCOMES_DIR.mkdir(parents=True, exist_ok=True)

    date = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    # Find unique filename
    base = f"{date}-{skill}-{outcome}"
    path = OUTCOMES_DIR / f"{base}.md"
    n = 1
    while path.exists():
        n += 1
        path = OUTCOMES_DIR / f"{base}-{n}.md"

    content = f"""---
skill: {skill}
date: {date}
outcome: {outcome}
exit_reason: {exit_reason}
one_line: "{one_line}"
---
"""
    path.write_text(content, encoding="utf-8")
    return path


def update_summary(skill: str, outcome: str, exit_reason: str):
    """Update rolling outcomes-summary.json."""
    # Load existing or create new
    if SUMMARY_FILE.exists():
        try:
            data = json.loads(SUMMARY_FILE.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            data = {}
    else:
        data = {}

    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    date_today = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    # Initialize structure
    data.setdefault("last_updated", now)
    data.setdefault("total_runs", 0)
    data.setdefault("by_skill", {})
    data.setdefault("by_exit_reason", {})
    data.setdefault("by_outcome", {"success": 0, "partial": 0, "failure": 0, "unknown": 0})
    data.setdefault("recent_runs", [])  # last 20 runs for trend analysis

    # Update counters
    data["last_updated"] = now
    data["total_runs"] += 1
    data["by_outcome"][outcome] = data["by_outcome"].get(outcome, 0) + 1
    data["by_exit_reason"][exit_reason] = data["by_exit_reason"].get(exit_reason, 0) + 1

    # Per-skill counters
    skill_data = data["by_skill"].setdefault(skill, {"runs": 0, "success": 0, "partial": 0, "failure": 0})
    skill_data["runs"] += 1
    if outcome in ("success", "partial", "failure"):
        skill_data[outcome] += 1

    # Recent runs (FIFO, max 20)
    data["recent_runs"].append({
        "date": date_today,
        "skill": skill,
        "outcome": outcome,
        "exit_reason": exit_reason,
    })
    if len(data["recent_runs"]) > 20:
        data["recent_runs"] = data["recent_runs"][-20:]

    # Compute derived metrics
    total = data["total_runs"]
    successes = data["by_outcome"].get("success", 0)
    data["success_rate"] = round(successes / total, 3) if total > 0 else 0.0

    # 7-day window from recent_runs
    from datetime import timedelta
    cutoff = (datetime.now(timezone.utc) - timedelta(days=7)).strftime("%Y-%m-%d")
    recent_7d = [r for r in data["recent_runs"] if r["date"] >= cutoff]
    data["last_7_days"] = {
        "success": sum(1 for r in recent_7d if r["outcome"] == "success"),
        "partial": sum(1 for r in recent_7d if r["outcome"] == "partial"),
        "failure": sum(1 for r in recent_7d if r["outcome"] == "failure"),
        "total": len(recent_7d),
    }

    # Failure streak
    streak = 0
    for run in reversed(data["recent_runs"]):
        if run["outcome"] == "failure":
            streak += 1
        else:
            break
    data["failure_streak"] = streak

    # Write atomically
    SUMMARY_FILE.parent.mkdir(parents=True, exist_ok=True)
    tmp = SUMMARY_FILE.with_suffix(".tmp")
    tmp.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    tmp.replace(SUMMARY_FILE)


def archive_if_needed():
    """Archive old outcomes if directory exceeds MAX_OUTCOMES files."""
    outcomes = sorted(OUTCOMES_DIR.glob("*.md"))
    if len(outcomes) <= MAX_OUTCOMES:
        return
    archive_dir = OUTCOMES_DIR / "archive"
    archive_dir.mkdir(exist_ok=True)
    # Move oldest half to archive
    to_archive = outcomes[: len(outcomes) - MAX_OUTCOMES // 2]
    for f in to_archive:
        f.rename(archive_dir / f.name)


def _record_failure_inline(skill: str, outcome: str, exit_reason: str, one_line: str, outcome_path: Path):
    """Record failure directly from outcome-writer, bypassing the broken PostToolUse/Write trigger.

    Simplified version of failure-recorder.py logic — creates a minimal failure record
    so the failures/ directory actually gets populated.
    """
    failures_dir = Path(".claude/memory/failures")
    failures_dir.mkdir(parents=True, exist_ok=True)

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

    # Next failure ID
    existing = list(failures_dir.glob("*-F???-*.md"))
    if existing:
        ids = []
        for f in existing:
            match = re.search(r"-F(\d{3})-", f.name)
            if match:
                ids.append(int(match.group(1)))
        fid = f"F{(max(ids) + 1) if ids else 1:03d}"
    else:
        fid = "F001"

    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    slug = re.sub(r"[^a-z0-9]+", "-", one_line.lower())[:40].strip("-")
    filename = f"{today}-{fid}-{slug}.md"

    content = f"""---
id: {fid}
date: {today}
task: "{one_line}"
failure_class: {failure_class}
failure_agent: {skill}
resolved: false
---

## Root Cause

Auto-recorded from outcome: {outcome_path.name}
Exit reason: {exit_reason}

## Reflexion

(To be filled by /learn-from-failure or manual review)
"""
    (failures_dir / filename).write_text(content, encoding="utf-8")


def main():
    tool_name = os.environ.get("CLAUDE_TOOL_NAME", "")
    if tool_name != "Skill":
        return

    tool_input = os.environ.get("CLAUDE_TOOL_INPUT", "")
    tool_output = os.environ.get("CLAUDE_TOOL_OUTPUT", "")

    # Extract skill name
    skill = detect_skill_name(tool_input)
    if not skill or skill in SKIP_SKILLS:
        return

    # Strip namespace prefix (e.g., "stopa-orchestration:scout" → "scout")
    if ":" in skill:
        skill = skill.split(":")[-1]

    # Detect outcome
    outcome = detect_outcome(tool_output)
    if outcome == "unknown":
        # If we can't confidently classify, don't write (conservative)
        return

    exit_reason = detect_exit_reason(tool_output)
    one_line = extract_one_line(tool_output)

    # Write micro-outcome
    try:
        outcome_path = write_micro_outcome(skill, outcome, exit_reason, one_line)
    except OSError:
        return  # non-blocking: silently fail

    # Update aggregator
    try:
        update_summary(skill, outcome, exit_reason)
    except OSError:
        pass  # non-blocking

    # Archive check (occasional)
    try:
        archive_if_needed()
    except OSError:
        pass

    # Direct failure recording — bypasses broken Write-tool trigger
    # (failure-recorder.py waits for Write tool event that never comes
    #  because we use path.write_text(), not the Claude Write tool)
    if outcome in ("failure", "partial"):
        try:
            _record_failure_inline(skill, outcome, exit_reason, one_line, outcome_path)
        except Exception:
            pass  # non-blocking


if __name__ == "__main__":
    main()
