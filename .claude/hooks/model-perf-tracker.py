#!/usr/bin/env python3
"""PostToolUse hook: Track model performance for Agent tool results.

After an Agent completes, records which model was used, the subtask type,
and whether it succeeded (based on status block in output).

Updates: .claude/memory/optstate/model-routing.json
"""

import json
import os
import re
import sys
from datetime import date
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
PERF_FILE = PROJECT_ROOT / ".claude/memory/optstate/model-routing.json"


def classify_subtask(prompt: str) -> str:
    """Classify subtask type from agent prompt."""
    prompt_lower = prompt[:2000].lower()

    if re.search(r"\brename\b|\bformat\b|\blint\b|\btypo\b", prompt_lower):
        return "mechanical_edit"
    if re.search(r"\btest\b.*\bwrit\b|\bgenerate.test\b", prompt_lower):
        return "test_generation"
    if re.search(r"\bsecurity\b|\bauth\b|\bpayment\b", prompt_lower):
        return "security_critical"
    if re.search(r"\brefactor\b|\bredesign\b|\barchitect\b", prompt_lower):
        return "refactoring"
    if re.search(r"\bresearch\b|\bscout\b|\bexplor\b|\banalyze\b", prompt_lower):
        return "research"

    # Count WRITE files
    write_match = re.search(r"WRITE:\s*\[(.+?)\]", prompt)
    if write_match:
        count = len(write_match.group(1).split(","))
        if count <= 1:
            return "single_file_edit"
        if count <= 3:
            return "multi_file_edit"
        return "large_edit"

    return "single_file_edit"  # default


def extract_success(output: str) -> bool | None:
    """Extract success/failure from agent output status block."""
    if not output:
        return None

    output_tail = output[-2000:]  # check last 2K chars

    # Look for status patterns
    if re.search(r"\bDONE\b", output_tail) and not re.search(r"DONE_WITH_CONCERNS|BLOCKED|NEEDS_CONTEXT", output_tail):
        return True
    if re.search(r"DONE_WITH_CONCERNS", output_tail):
        return True  # partial success still counts
    if re.search(r"\bBLOCKED\b|\bFAILED\b|\bNEEDS_CONTEXT\b", output_tail):
        return False

    return None  # indeterminate


def load_perf() -> dict:
    """Load or initialize performance data."""
    try:
        return json.loads(PERF_FILE.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {
            "last_updated": str(date.today()),
            "total_routings": 0,
            "by_subtask_type": {},
            "escalation_patterns": [],
            "haiku_first_threshold": 3.5,
        }


def save_perf(data: dict) -> None:
    """Save performance data."""
    data["last_updated"] = str(date.today())
    PERF_FILE.parent.mkdir(parents=True, exist_ok=True)
    PERF_FILE.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


def main():
    tool_name = os.environ.get("CLAUDE_TOOL_NAME", "")
    if tool_name != "Agent":
        sys.exit(0)

    try:
        raw = sys.stdin.read().strip()
        hook_input = json.loads(raw) if raw else {}
    except (json.JSONDecodeError, EOFError):
        sys.exit(0)

    tool_input = hook_input.get("tool_input", {})
    tool_output = hook_input.get("tool_output", {})

    prompt = tool_input.get("prompt", "")
    model = tool_input.get("model", "sonnet")  # default assumption
    output_text = str(tool_output.get("stdout", tool_output.get("output", "")))

    if not prompt or len(prompt) < 50:
        sys.exit(0)

    subtask_type = classify_subtask(prompt)
    success = extract_success(output_text)

    if success is None:
        sys.exit(0)  # can't determine — skip

    # Update performance data
    data = load_perf()
    by_type = data.setdefault("by_subtask_type", {})
    type_data = by_type.setdefault(subtask_type, {})
    model_data = type_data.setdefault(model, {"attempts": 0, "success": 0, "avg_critic_score": 0})

    model_data["attempts"] += 1
    if success:
        model_data["success"] += 1

    # Track escalation if failure was followed by model upgrade
    if not success:
        patterns = data.setdefault("escalation_patterns", [])
        patterns.append({
            "date": str(date.today()),
            "subtask_type": subtask_type,
            "model": model,
            "outcome": "failure",
        })
        # Keep only last 20
        data["escalation_patterns"] = patterns[-20:]

    # Auto-tune haiku_first_threshold based on haiku success rates
    haiku_total = 0
    haiku_success = 0
    for type_stats in by_type.values():
        h = type_stats.get("haiku", {})
        haiku_total += h.get("attempts", 0)
        haiku_success += h.get("success", 0)

    if haiku_total >= 10:
        rate = haiku_success / haiku_total
        # If haiku success rate is high (>75%), lower threshold to encourage more haiku
        # If low (<50%), raise threshold to be more conservative
        if rate > 0.75:
            data["haiku_first_threshold"] = max(3.0, data.get("haiku_first_threshold", 3.5) - 0.1)
        elif rate < 0.50:
            data["haiku_first_threshold"] = min(4.0, data.get("haiku_first_threshold", 3.5) + 0.1)

    save_perf(data)


if __name__ == "__main__":
    main()
