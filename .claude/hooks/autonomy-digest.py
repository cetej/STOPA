#!/usr/bin/env python3
"""Autonomy digest — reads friction events + permission log, injects reminders
at session start if the assistant has been over-asking, and auto-promotes
repeating Bash patterns to the allow-list.

Runs as a sub-hook inside session-start-orchestrator.py. Output goes to stdout
and is surfaced to the assistant as part of the session banner.
"""
from __future__ import annotations

import json
import re
import sys
import time
from collections import Counter
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parent.parent
FRICTION_LOG = ROOT / "memory" / "autonomy-friction.jsonl"
PERM_LOG = ROOT / "memory" / "permission-log.md"
SETTINGS = ROOT / "settings.json"
LEARN_LOG = ROOT / "memory" / "autonomy-learning.jsonl"

NOW = time.time()
DAY = 86400


def load_friction_events(days: int) -> list[dict]:
    if not FRICTION_LOG.exists():
        return []
    cutoff = NOW - days * DAY
    events: list[dict] = []
    try:
        for line in FRICTION_LOG.read_text(encoding="utf-8", errors="replace").splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                e = json.loads(line)
            except Exception:
                continue
            ts = e.get("ts", "")
            try:
                t = time.mktime(time.strptime(ts, "%Y-%m-%dT%H:%M:%S"))
            except Exception:
                continue
            if t >= cutoff:
                events.append(e)
    except Exception:
        return []
    return events


def load_allow_list() -> set[str]:
    try:
        data = json.loads(SETTINGS.read_text(encoding="utf-8"))
        return set(data.get("permissions", {}).get("allow", []))
    except Exception:
        return set()


def extract_bash_patterns_from_perm_log(days: int) -> Counter:
    """Count Bash-ish tool invocations in permission-log.md to surface patterns
    that occur frequently but aren't yet in the allow-list. (Conservative: we
    only *suggest*, never auto-write on first iteration.)"""
    if not PERM_LOG.exists():
        return Counter()
    cutoff = NOW - days * DAY
    counter: Counter[str] = Counter()
    try:
        for line in PERM_LOG.read_text(encoding="utf-8", errors="replace").splitlines():
            # Format: "- YYYY-MM-DD HH:MM | AUTO | ToolName"
            m = re.match(r"^-\s+(\d{4}-\d{2}-\d{2})\s+(\d{2}:\d{2})\s+\|\s+(\w+)\s+\|\s+(.+)$", line)
            if not m:
                continue
            date_s, time_s, decision, tool = m.groups()
            try:
                t = time.mktime(time.strptime(f"{date_s}T{time_s}", "%Y-%m-%dT%H:%M"))
            except Exception:
                continue
            if t < cutoff:
                continue
            counter[tool.strip()] += 1
    except Exception:
        return Counter()
    return counter


def main() -> int:
    # Read stdin (may contain session_id) but we don't need it.
    try:
        sys.stdin.read()
    except Exception:
        pass

    day_events = load_friction_events(1)
    week_events = load_friction_events(7)
    tool_counts = extract_bash_patterns_from_perm_log(7)
    allow = load_allow_list()

    lines: list[str] = []

    # --- Friction signal ---
    if len(day_events) >= 3:
        lines.append(f"=== AUTONOMY FRICTION (high) ===")
        lines.append(f"Za posledních 24h jsi se {len(day_events)}× zeptal na schválení — uživatel odpověděl krátkým \"ano/ok/pokračuj\".")
        lines.append("Toto je friction signál — uživatel opakovaně řekl: jdi autonomně, nepitvej drobnosti.")
        lines.append("**Tuto session: nesměřuj k potvrzovacím otázkám. U destruktivních akcí ANO. U všeho ostatního NE.**")
    elif len(week_events) >= 8:
        lines.append(f"=== AUTONOMY TREND ({len(week_events)} events / 7d) ===")
        lines.append(f"Autonomy friction trend: {len(week_events)} zbytečných schvalovacích promptů za týden.")
        lines.append("Pamatuj: batch operace > jednotlivé kroky. Behavioral genome § Autonomy.")

    # --- Auto-learning: tools that appear often but aren't explicitly allowed ---
    # Signal for future auto-promotion; conservative — just report for now.
    new_patterns: list[tuple[str, int]] = []
    for tool, count in tool_counts.most_common(20):
        if count < 5:
            continue
        # MCP tools: check wildcard membership
        if tool.startswith("mcp__"):
            prefix_match = any(
                a.startswith("mcp__") and tool.startswith(a.replace("*", ""))
                for a in allow
            )
            if prefix_match:
                continue
        elif tool in allow:
            continue
        new_patterns.append((tool, count))

    if new_patterns:
        lines.append("=== AUTO-LEARN: frequent tools not yet on explicit allow-list ===")
        for tool, count in new_patterns[:5]:
            lines.append(f"  • {tool} — použit {count}× za 7 dní (fallthrough allow funguje, ale explicitní záznam je robustnější)")
        # Log suggestion for /evolve to pick up
        try:
            LEARN_LOG.parent.mkdir(parents=True, exist_ok=True)
            with LEARN_LOG.open("a", encoding="utf-8") as f:
                for tool, count in new_patterns[:5]:
                    f.write(json.dumps({
                        "ts": time.strftime("%Y-%m-%dT%H:%M:%S"),
                        "suggestion": "add_to_allow",
                        "tool": tool,
                        "count_7d": count,
                    }, ensure_ascii=False) + "\n")
        except Exception:
            pass

    if lines:
        print("\n".join(lines))

    return 0


if __name__ == "__main__":
    sys.exit(main())
