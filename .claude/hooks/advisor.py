#!/usr/bin/env python3
"""
Ambient Advisor — PostToolUse hook (throttled).

Non-blocking skill suggestions based on behavioral patterns.
Fires every 10th tool call, max 1 suggestion per 5 minutes.
NEVER auto-executes — only suggests.

Patterns:
1. Repeated manual grep (5+) without active skill → /scout
2. Multi-file edit (3+) without plan → /orchestrate retrospective
3. Test fail after edit → /systematic-debugging
4. Session without outcomes (3+ skills) → outcomes reminder
5. Context 70%+ without checkpoint → /checkpoint save
"""

import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")

HOOKS_DIR = Path(__file__).parent
STATE_FILE = HOOKS_DIR / "advisor-state.json"
LOG_FILE = HOOKS_DIR / "advisor-log.jsonl"
MEMORY_DIR = HOOKS_DIR.parent / "memory"

THROTTLE_EVERY_N = 10  # fire every Nth tool call
COOLDOWN_SECONDS = 300  # 5 minutes between suggestions


def load_state() -> dict:
    try:
        return json.loads(STATE_FILE.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError):
        return {
            "call_count": 0,
            "last_suggestion_ts": 0,
            "grep_count": 0,
            "edit_file_set": [],
            "skill_count": 0,
            "last_edit_was_py": False,
        }


def save_state(state: dict) -> None:
    STATE_FILE.write_text(json.dumps(state, indent=2, ensure_ascii=False), encoding="utf-8")


def log_suggestion(pattern: str, suggestion: str, accepted: bool = False) -> None:
    entry = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "pattern": pattern,
        "suggestion": suggestion,
        "session": os.environ.get("CLAUDE_SESSION_ID", "unknown"),
    }
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


def check_cooldown(state: dict) -> bool:
    """Return True if cooldown is active (should skip)."""
    last_ts = state.get("last_suggestion_ts", 0)
    return (time.time() - last_ts) < COOLDOWN_SECONDS


def detect_repeated_grep(state: dict) -> str | None:
    """Pattern 1: 5+ Grep/Read calls without active skill."""
    if state.get("grep_count", 0) >= 5:
        # Check if there's an active skill (TodoWrite recent)
        # Simple heuristic: if no skill was used in this session
        if state.get("skill_count", 0) == 0:
            return "Advisor: 5+ manuálních grep/read operací bez aktivního skillu — zvažte /scout pro systematický průzkum"
    return None


def detect_multifile_edit(state: dict) -> str | None:
    """Pattern 2: 3+ files edited without plan (no TodoWrite)."""
    edited = state.get("edit_file_set", [])
    if len(edited) >= 3:
        has_todo = state.get("has_todo", False)
        if not has_todo:
            return f"Advisor: {len(edited)} souborů editováno bez plánu — zvažte /orchestrate retrospective"
    return None


def detect_test_fail_after_edit(state: dict, hook_input: dict) -> str | None:
    """Pattern 3: Bash exit≠0 after Edit."""
    tool_name = hook_input.get("tool_name", "")
    tool_output = hook_input.get("tool_output", {})

    if tool_name == "Bash" and state.get("last_edit_was_py", False):
        # Check exit code
        stdout = str(tool_output.get("stdout", ""))
        exit_code = tool_output.get("exit_code", 0)
        if exit_code != 0 and ("error" in stdout.lower() or "fail" in stdout.lower() or "traceback" in stdout.lower()):
            return "Advisor: test/build selhal po editaci — zvažte /systematic-debugging pro root-cause analýzu"
    return None


def detect_no_outcomes(state: dict) -> str | None:
    """Pattern 4: 3+ skills used, 0 outcomes."""
    if state.get("skill_count", 0) >= 3:
        outcomes_dir = MEMORY_DIR / "outcomes"
        # Count recent outcome files (today)
        today = datetime.now().strftime("%Y-%m-%d")
        recent_outcomes = 0
        if outcomes_dir.exists():
            for f in outcomes_dir.glob(f"{today}*.md"):
                recent_outcomes += 1
        if recent_outcomes == 0:
            return "Advisor: 3+ skills použito bez záznamů výsledků — zvažte zápis outcomes pro tracking"
    return None


def detect_context_pressure(state: dict) -> str | None:
    """Pattern 5: Context 70%+ without checkpoint."""
    stats_file = MEMORY_DIR / "session-stats.json"
    if stats_file.exists():
        try:
            stats = json.loads(stats_file.read_text(encoding="utf-8"))
            pct = stats.get("pct", 0)
            if pct >= 70:
                # Check if checkpoint was saved recently
                cp_file = MEMORY_DIR / "checkpoint.md"
                if cp_file.exists():
                    text = cp_file.read_text(encoding="utf-8", errors="replace")
                    # Simple check: if checkpoint is from today
                    today = datetime.now().strftime("%Y-%m-%d")
                    if today in text:
                        return None  # checkpoint is fresh
                return f"Advisor: context window na {pct}% — zvažte /checkpoint save"
        except Exception:
            pass
    return None


def main():
    try:
        hook_input = json.loads(sys.stdin.read())
    except (json.JSONDecodeError, EOFError):
        return

    tool_name = hook_input.get("tool_name", "")
    tool_input = hook_input.get("tool_input", {})

    state = load_state()

    # Increment call counter
    state["call_count"] = state.get("call_count", 0) + 1

    # Track grep/read calls
    if tool_name in ("Grep", "Read", "Glob"):
        state["grep_count"] = state.get("grep_count", 0) + 1

    # Track file edits
    if tool_name in ("Edit", "Write"):
        file_path = str(tool_input.get("file_path", ""))
        edited = state.get("edit_file_set", [])
        if file_path and file_path not in edited:
            edited.append(file_path)
            state["edit_file_set"] = edited
        state["last_edit_was_py"] = file_path.endswith(".py")

    # Track TodoWrite usage
    if tool_name == "TodoWrite":
        state["has_todo"] = True

    # Track Skill usage
    if tool_name == "Skill":
        state["skill_count"] = state.get("skill_count", 0) + 1

    # Only evaluate patterns every Nth call
    if state["call_count"] % THROTTLE_EVERY_N != 0:
        save_state(state)
        return

    # Check cooldown
    if check_cooldown(state):
        save_state(state)
        return

    # Evaluate patterns in priority order
    suggestion = None
    pattern = ""

    checks = [
        ("test_fail", lambda: detect_test_fail_after_edit(state, hook_input)),
        ("context_pressure", lambda: detect_context_pressure(state)),
        ("repeated_grep", lambda: detect_repeated_grep(state)),
        ("multifile_edit", lambda: detect_multifile_edit(state)),
        ("no_outcomes", lambda: detect_no_outcomes(state)),
    ]

    for pat_name, check_fn in checks:
        result = check_fn()
        if result:
            suggestion = result
            pattern = pat_name
            break

    if suggestion:
        state["last_suggestion_ts"] = time.time()
        log_suggestion(pattern, suggestion)
        save_state(state)
        print(json.dumps({"additionalContext": f"[advisor] {suggestion}"}))
    else:
        save_state(state)


if __name__ == "__main__":
    main()
