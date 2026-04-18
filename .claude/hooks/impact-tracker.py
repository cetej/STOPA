#!/usr/bin/env python3
"""PostToolUse hook: track impact of applied learnings via critic scores.

Pragmatic alternative to A/B testing: instead of running critic twice
(with/without learning), track rolling average of critic scores for tasks
where specific learnings were applied.

Flow:
1. uses-tracker.py records which learnings were read (uses-ledger.json)
2. This hook fires after Skill(critic) completes
3. Extracts critic score from output (PASS/FAIL + severity counts)
4. Updates impact_score for all learnings used in this session

Impact score update rule (rolling average, last 5 applications):
  - PASS → +0.1 (max 1.0)
  - FAIL → -0.15 (min 0.0)
  - No change → 0 (neutral)

Writes to: .claude/memory/intermediate/impact-ledger.json
Merged into learning YAML by learning-lifecycle.py at SessionStart.
"""
import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
USES_LEDGER = PROJECT_ROOT / ".claude/memory/intermediate/uses-ledger.json"
IMPACT_LEDGER = PROJECT_ROOT / ".claude/memory/intermediate/impact-ledger.json"


def extract_critic_result(output: str) -> str | None:
    """Extract PASS/FAIL from critic skill output."""
    output_lower = output.lower()
    if any(w in output_lower for w in ["pass", "approved", "clean", "no issues", "all good"]):
        return "PASS"
    if any(w in output_lower for w in ["fail", "issues found", "problems", "needs work"]):
        return "FAIL"
    return None


def get_session_learnings() -> list[str]:
    """Get learnings that were read during this session."""
    if not USES_LEDGER.exists():
        return []
    try:
        ledger = json.loads(USES_LEDGER.read_text(encoding="utf-8"))
        # Return filenames with uses incremented this session
        return [k for k, v in ledger.items() if isinstance(v, dict) and v.get("session_delta", 0) > 0]
    except (json.JSONDecodeError, OSError):
        return []


def update_impact(learnings: list[str], result: str):
    """Update impact scores for applied learnings."""
    if not learnings:
        return

    # Load existing impact ledger
    impact = {}
    if IMPACT_LEDGER.exists():
        try:
            impact = json.loads(IMPACT_LEDGER.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            impact = {}

    delta = 0.1 if result == "PASS" else -0.15

    for filename in learnings:
        entry = impact.get(filename, {"score": 0.0, "history": []})
        history = entry.get("history", [])
        history.append(result)
        # Keep last 5
        history = history[-5:]
        # Compute rolling score
        score = entry.get("score", 0.0) + delta
        score = max(0.0, min(1.0, score))
        impact[filename] = {"score": round(score, 2), "history": history}

    try:
        IMPACT_LEDGER.parent.mkdir(parents=True, exist_ok=True)
        IMPACT_LEDGER.write_text(json.dumps(impact, indent=2), encoding="utf-8")
    except OSError:
        pass


def main():
    try:
        data = json.loads(sys.stdin.read())
    except (json.JSONDecodeError, EOFError):
        return

    tool = data.get("tool_name", "")
    if tool != "Skill":
        return

    # Check if it was the critic skill
    tool_input = data.get("tool_input", {})
    if isinstance(tool_input, str):
        try:
            tool_input = json.loads(tool_input)
        except json.JSONDecodeError:
            return

    skill_name = tool_input.get("skill", "")
    if skill_name not in ("critic", "/critic"):
        return

    # Extract result
    output = data.get("tool_output", "")[:3000]
    result = extract_critic_result(output)
    if result is None:
        return

    # Get learnings used this session
    learnings = get_session_learnings()
    if not learnings:
        return

    update_impact(learnings, result)


if __name__ == "__main__":
    main()
