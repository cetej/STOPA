#!/usr/bin/env python3
"""Summarize recent STOPA sessions for auto-evolve pipeline.

Reads session traces from .traces/sessions/*.jsonl, groups tool calls by skill,
and produces per-skill evidence summaries in .claude/memory/summaries/.

Part of the SkillClaw-inspired auto-evolve pipeline:
  summarize-sessions.py → evolve-skills.py → /evolve --candidates

Usage:
    python scripts/summarize-sessions.py [--days N] [--min-sessions N]
"""
import json
import sys
import time
from collections import defaultdict
from datetime import datetime, timedelta
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

TRACES_DIR = Path(".traces/sessions")
OUTCOMES_DIR = Path(".claude/memory/outcomes")
SUMMARIES_DIR = Path(".claude/memory/summaries")
SKILL_USAGE_FILE = Path(".claude/memory/skill-usage.jsonl")


def parse_args():
    """Parse CLI arguments."""
    days = 7
    min_sessions = 2
    for i, arg in enumerate(sys.argv[1:], 1):
        if arg == "--days" and i < len(sys.argv) - 1:
            days = int(sys.argv[i + 1])
        elif arg == "--min-sessions" and i < len(sys.argv) - 1:
            min_sessions = int(sys.argv[i + 1])
    return days, min_sessions


def extract_session_data(trace_file: Path) -> dict:
    """Extract structured data from a session JSONL trace."""
    skills_referenced: set[str] = set()
    tool_calls: list[dict] = []
    errors: list[dict] = []
    total_calls = 0
    error_count = 0

    try:
        with open(trace_file, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    record = json.loads(line)
                except json.JSONDecodeError:
                    continue

                total_calls += 1
                tool = record.get("tool", "")
                exit_code = record.get("exit", 0)

                # Track skills
                if "skill" in record:
                    skills_referenced.add(record["skill"])

                # Track errors (interesting signal for evolution)
                if exit_code != 0:
                    error_count += 1
                    errors.append({
                        "tool": tool,
                        "exit": exit_code,
                        "path": record.get("path", ""),
                        "cmd": record.get("cmd", "")[:100],
                        "ts": record.get("ts", ""),
                    })

                # Track tool usage pattern (compact)
                tool_calls.append({
                    "tool": tool,
                    "exit": exit_code,
                    "skill": record.get("skill"),
                })
    except OSError:
        return {}

    if not skills_referenced:
        return {}  # Sessions without skills are not useful for skill evolution

    return {
        "file": str(trace_file),
        "session_id": trace_file.stem,
        "skills_referenced": sorted(skills_referenced),
        "total_calls": total_calls,
        "error_count": error_count,
        "error_rate": round(error_count / max(total_calls, 1), 3),
        "errors": errors[:10],  # Cap at 10 errors
        "tool_sequence": _compress_tool_sequence(tool_calls),
    }


def _compress_tool_sequence(tool_calls: list[dict]) -> list[str]:
    """Compress tool call sequence into a compact pattern.

    Instead of listing every call, group consecutive same-tool calls:
    [Read, Read, Read, Edit, Read, Bash] → ["Read×3", "Edit", "Read", "Bash"]
    """
    if not tool_calls:
        return []

    compressed: list[str] = []
    current_tool = tool_calls[0]["tool"]
    count = 1

    for tc in tool_calls[1:]:
        if tc["tool"] == current_tool:
            count += 1
        else:
            compressed.append(f"{current_tool}×{count}" if count > 1 else current_tool)
            current_tool = tc["tool"]
            count = 1
    compressed.append(f"{current_tool}×{count}" if count > 1 else current_tool)

    return compressed


def find_outcome(session_id: str) -> str | None:
    """Find an outcome file matching this session (by date prefix)."""
    if not OUTCOMES_DIR.exists():
        return None

    date_prefix = session_id[:10]  # "2026-04-07"
    for f in OUTCOMES_DIR.glob(f"{date_prefix}*.md"):
        if f.name == ".gitkeep":
            continue
        try:
            return f.read_text(encoding="utf-8", errors="replace")[:500]
        except OSError:
            pass
    return None


def group_by_skill(sessions: list[dict]) -> dict[str, dict]:
    """Group session evidence by skill (SkillClaw aggregation step)."""
    skill_groups: dict[str, list] = defaultdict(list)

    for session in sessions:
        for skill in session["skills_referenced"]:
            skill_groups[skill].append(session)

    result = {}
    for skill, skill_sessions in sorted(skill_groups.items()):
        # Deduplicate sessions (same session can appear for multiple skills)
        seen = set()
        unique_sessions = []
        for s in skill_sessions:
            if s["session_id"] not in seen:
                seen.add(s["session_id"])
                unique_sessions.append(s)

        # Aggregate error patterns across sessions
        all_errors = []
        for s in unique_sessions:
            all_errors.extend(s.get("errors", []))

        result[skill] = {
            "session_count": len(unique_sessions),
            "total_calls_across_sessions": sum(s["total_calls"] for s in unique_sessions),
            "avg_error_rate": round(
                sum(s["error_rate"] for s in unique_sessions) / max(len(unique_sessions), 1), 3
            ),
            "sessions": [
                {
                    "session_id": s["session_id"],
                    "total_calls": s["total_calls"],
                    "error_rate": s["error_rate"],
                    "tool_sequence": s["tool_sequence"][:20],  # Cap sequence length
                    "errors": s["errors"][:3],  # Cap errors per session
                }
                for s in unique_sessions
            ],
            "aggregated_errors": all_errors[:15],  # Cap total errors
        }

    return result


def main():
    days, min_sessions = parse_args()
    cutoff = datetime.now() - timedelta(days=days)

    if not TRACES_DIR.exists():
        print("No traces directory found. Run some sessions first.")
        sys.exit(1)

    # Collect sessions from trace files
    sessions = []
    for trace_file in sorted(TRACES_DIR.glob("*.jsonl")):
        try:
            file_date = datetime.strptime(trace_file.stem[:10], "%Y-%m-%d")
            if file_date < cutoff:
                continue
        except ValueError:
            continue

        session_data = extract_session_data(trace_file)
        if session_data:
            # Try to find matching outcome
            outcome = find_outcome(session_data["session_id"])
            if outcome:
                session_data["outcome_snippet"] = outcome
            sessions.append(session_data)

    if not sessions:
        print(f"No sessions with skill references found in last {days} days.")
        sys.exit(0)

    # Group by skill (SkillClaw aggregation step)
    skill_groups = group_by_skill(sessions)

    # Filter skills with too few sessions
    filtered = {
        skill: data for skill, data in skill_groups.items()
        if data["session_count"] >= min_sessions
    }

    # Write summary
    SUMMARIES_DIR.mkdir(parents=True, exist_ok=True)
    summary = {
        "generated": datetime.now().isoformat(),
        "config": {"days_back": days, "min_sessions": min_sessions},
        "total_sessions_analyzed": len(sessions),
        "skills_with_evidence": len(filtered),
        "skill_groups": filtered,
    }

    output_file = SUMMARIES_DIR / f"summary-{time.strftime('%Y-%m-%d')}.json"
    output_file.write_text(json.dumps(summary, indent=2, ensure_ascii=False))

    # Report
    print(f"Sessions analyzed: {len(sessions)} (last {days} days)")
    print(f"Skills with evidence (>={min_sessions} sessions):")
    for skill, data in sorted(filtered.items(), key=lambda x: -x[1]["session_count"]):
        err_flag = " ⚠" if data["avg_error_rate"] > 0.05 else ""
        print(f"  {skill}: {data['session_count']} sessions, "
              f"avg error rate {data['avg_error_rate']:.1%}{err_flag}")
    print(f"\nSummary → {output_file}")


if __name__ == "__main__":
    main()
