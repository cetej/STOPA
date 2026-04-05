#!/usr/bin/env python3
"""
Critic Accuracy Tracker — NLAH Verifier Divergence Detection (P2)

PostToolUse hook: after git commit, checks if a /critic verdict preceded it
and logs the implicit user signal (commit after PASS = aligned, commit after FAIL = overridden).

Writes to .claude/memory/critic-accuracy.jsonl

Inspired by: arXiv:2603.25723 (NLAH) — verifier divergence detection
"""

import json
import os
import sys
import re
from datetime import datetime
from pathlib import Path


def main():
    hook_input = json.loads(sys.stdin.read())

    tool_name = hook_input.get("tool_name", "")
    tool_input = hook_input.get("tool_input", {})

    # Only trigger on Bash tool with git commit commands
    if tool_name != "Bash":
        print(json.dumps({"decision": "approve"}))
        return

    command = tool_input.get("command", "")
    if "git commit" not in command:
        print(json.dumps({"decision": "approve"}))
        return

    # Check if critic state file exists (written by critic skill)
    memory_dir = Path(os.environ.get("CLAUDE_PROJECT_DIR", ".")) / ".claude" / "memory"
    critic_state = memory_dir / "critic-last-verdict.json"
    accuracy_log = memory_dir / "critic-accuracy.jsonl"

    if not critic_state.exists():
        print(json.dumps({"decision": "approve"}))
        return

    try:
        with open(critic_state, "r", encoding="utf-8") as f:
            verdict_data = json.load(f)

        # User committed after critic verdict = implicit feedback
        entry = {
            "date": datetime.now().strftime("%Y-%m-%d"),
            "task": verdict_data.get("task", "unknown"),
            "verdict": verdict_data.get("verdict", "unknown"),
            "score": verdict_data.get("score", 0),
            "user_outcome": "accepted" if verdict_data.get("verdict") == "PASS" else "overridden",
            "aligned": verdict_data.get("verdict") == "PASS",
            "dimensions": verdict_data.get("dimensions", {}),
        }

        # Append to JSONL
        with open(accuracy_log, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")

        # Clear the state file (consumed)
        critic_state.unlink()

    except (json.JSONDecodeError, KeyError, OSError):
        pass  # Don't block commits on tracking errors

    print(json.dumps({"decision": "approve"}))


if __name__ == "__main__":
    main()
