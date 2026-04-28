#!/usr/bin/env python3
"""
Trigger Intelligence Engine — PostToolUse hook.

Evaluates ECA (Event-Condition-Action) rules from trigger-rules.yaml
when writes happen to outcomes/ or learnings/ directories.

Also evaluates composition-rules.yaml for proactive skill sequence injection
when outcome events match composition triggers.

Max trigger depth = 1 (no cascading triggers).
Max 3 triggers per session.
Cooldown per-rule + per-context via trigger-state.json.
Log fires to trigger-log.jsonl.
Log composition fires to composition-log.jsonl.
"""

import json
import os
import re
import sys
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path

# Encoding fix for Windows
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")

HOOKS_DIR = Path(__file__).parent
PROJECT_ROOT = HOOKS_DIR.parent.parent
MEMORY_DIR = HOOKS_DIR.parent / "memory"
STATE_FILE = HOOKS_DIR / "trigger-state.json"
RULES_FILE = HOOKS_DIR / "trigger-rules.yaml"
LOG_FILE = HOOKS_DIR / "trigger-log.jsonl"
COMPOSITION_RULES_FILE = HOOKS_DIR / "composition-rules.yaml"
COMPOSITION_LOG_FILE = HOOKS_DIR / "composition-log.jsonl"

# Skills that must never appear in a composition sequence
DESTRUCTIVE_SKILLS = frozenset({
    "fix-issue", "autofix", "koder", "git", "commit", "push",
    "rm", "delete", "drop", "clear", "reset",
})

MAX_TRIGGERS_PER_SESSION = 3
SESSION_KEY = os.environ.get("CLAUDE_SESSION_ID", "unknown")


def load_state() -> dict:
    try:
        return json.loads(STATE_FILE.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def save_state(state: dict) -> None:
    STATE_FILE.write_text(json.dumps(state, indent=2, ensure_ascii=False), encoding="utf-8")


def log_fire(rule_id: str, message: str, context: str = "") -> None:
    entry = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "rule": rule_id,
        "message": message,
        "context": context,
        "session": SESSION_KEY,
    }
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


def load_rules() -> list:
    """Load rules from YAML (simple parser — no PyYAML dependency).

    Uses indentation tracking to determine which section (condition/action)
    each key belongs to.
    """
    if not RULES_FILE.exists():
        return []

    text = RULES_FILE.read_text(encoding="utf-8")
    rules = []
    current_rule = None
    current_section = None  # "condition" or "action" or None

    # Fields that are always condition-level
    CONDITION_KEYS = {
        "threshold", "min_runs", "min_uses", "max_harmful",
        "same_pattern_threshold", "max_age_days", "window_days",
        "threshold_below", "min_confidence", "outcome", "file",
        "group_by", "source_file",
    }
    # Fields that are always action-level
    ACTION_KEYS = {"message", "target"}
    # Float fields
    FLOAT_KEYS = {"threshold_below", "min_confidence"}
    # Int fields
    INT_KEYS = {
        "threshold", "min_runs", "min_uses", "max_harmful",
        "same_pattern_threshold", "max_age_days", "window_days",
        "cooldown_minutes",
    }

    for line in text.split("\n"):
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue

        # Detect indentation level
        indent = len(line) - len(line.lstrip())

        if stripped.startswith("- id:"):
            if current_rule:
                rules.append(current_rule)
            current_rule = {"id": stripped.split(":", 1)[1].strip()}
            current_section = None
            continue

        if not current_rule:
            continue

        # Track which section we're in based on key names
        if stripped.startswith("condition:"):
            current_section = "condition"
            continue
        elif stripped.startswith("action:"):
            current_section = "action"
            continue

        if ":" not in stripped:
            continue

        key, _, val = stripped.partition(":")
        key = key.strip()
        val = val.strip().strip('"').strip("'")
        # Strip inline YAML comments
        if "  #" in val:
            val = val[:val.index("  #")].strip()

        if not val:
            continue

        # Route key to the right place
        if key == "enabled":
            current_rule[key] = val.lower() == "true"
        elif key == "cooldown_minutes":
            current_rule[key] = int(val)
        elif key == "description":
            current_rule[key] = val
        elif key == "matcher":
            current_rule[key] = val
        elif key == "event":
            current_rule[key] = val
        elif key == "type":
            if current_section == "action":
                current_rule.setdefault("action", {})[key] = val
            elif current_section == "condition":
                current_rule.setdefault("condition", {})[key] = val
            else:
                # Heuristic: first type goes to condition, second to action
                cond = current_rule.get("condition", {})
                if "type" not in cond:
                    current_rule.setdefault("condition", {})[key] = val
                else:
                    current_rule.setdefault("action", {})[key] = val
        elif key in CONDITION_KEYS:
            if key in FLOAT_KEYS:
                current_rule.setdefault("condition", {})[key] = float(val)
            elif key in INT_KEYS:
                current_rule.setdefault("condition", {})[key] = int(val)
            elif key == "group_by":
                val_clean = val.strip("[]")
                current_rule.setdefault("condition", {})[key] = [
                    x.strip() for x in val_clean.split(",")
                ]
            else:
                current_rule.setdefault("condition", {})[key] = val
        elif key in ACTION_KEYS:
            current_rule.setdefault("action", {})[key] = val

    if current_rule:
        rules.append(current_rule)

    return [r for r in rules if r.get("enabled", True)]


def check_cooldown(state: dict, rule_id: str, cooldown_minutes: int, context: str = "") -> bool:
    """Return True if cooldown is active (should skip)."""
    key = f"{rule_id}:{context}" if context else rule_id
    cooldowns = state.get("cooldowns", {})
    last_fire = cooldowns.get(key)

    if not last_fire:
        return False

    try:
        last_dt = datetime.fromisoformat(last_fire)
        if last_dt.tzinfo is None:
            last_dt = last_dt.replace(tzinfo=timezone.utc)
        now = datetime.now(timezone.utc)
        return (now - last_dt) < timedelta(minutes=cooldown_minutes)
    except (ValueError, TypeError):
        return False


def set_cooldown(state: dict, rule_id: str, context: str = "") -> None:
    key = f"{rule_id}:{context}" if context else rule_id
    state.setdefault("cooldowns", {})[key] = datetime.now(timezone.utc).isoformat()


def get_session_fire_count(state: dict) -> int:
    return state.get("session_fires", {}).get(SESSION_KEY, 0)


def increment_session_fires(state: dict) -> None:
    state.setdefault("session_fires", {})[SESSION_KEY] = (
        state.get("session_fires", {}).get(SESSION_KEY, 0) + 1
    )


def load_outcomes_summary() -> dict:
    summary_file = MEMORY_DIR / "outcomes-summary.json"
    try:
        return json.loads(summary_file.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def evaluate_failure_pattern(condition: dict) -> tuple[bool, str]:
    """Check for 2+ failures with same failure_class + failure_agent in window."""
    window_days = condition.get("window_days", 7)
    threshold = condition.get("threshold", 2)
    cutoff = datetime.now(timezone.utc) - timedelta(days=window_days)

    failures_dir = MEMORY_DIR / "failures"
    if not failures_dir.exists():
        return False, ""

    # Group failures by (failure_class, failure_agent)
    groups: dict[tuple, int] = {}
    for f in failures_dir.glob("*.md"):
        if f.name == ".gitkeep":
            continue
        try:
            text = f.read_text(encoding="utf-8", errors="replace")
            # Parse YAML frontmatter
            fc = fa = date_str = ""
            for line in text.split("\n"):
                line = line.strip()
                if line.startswith("failure_class:"):
                    fc = line.split(":", 1)[1].strip()
                elif line.startswith("failure_agent:"):
                    fa = line.split(":", 1)[1].strip()
                elif line.startswith("date:"):
                    date_str = line.split(":", 1)[1].strip()

            if not date_str or not fc:
                continue

            file_date = datetime.strptime(date_str, "%Y-%m-%d").replace(tzinfo=timezone.utc)
            if file_date >= cutoff:
                key = (fc, fa)
                groups[key] = groups.get(key, 0) + 1
        except Exception:
            continue

    for (fc, fa), count in groups.items():
        if count >= threshold:
            return True, f"{fc}/{fa}"

    return False, ""


def evaluate_success_rate(condition: dict) -> tuple[bool, str]:
    """Check if 7d success rate dropped below threshold."""
    summary = load_outcomes_summary()
    last_7d = summary.get("last_7_days", {})
    total = last_7d.get("total", 0)
    min_runs = condition.get("min_runs", 5)

    if total < min_runs:
        return False, ""

    success = last_7d.get("success", 0)
    rate = (success / total * 100) if total > 0 else 100
    threshold = condition.get("threshold_below", 0.6) * 100

    if rate < threshold:
        return True, f"{rate:.0f}"
    return False, ""


def evaluate_file_age(condition: dict) -> tuple[bool, str]:
    """Check if a file is older than max_age_days."""
    filepath = Path(condition.get("file", ""))
    if not filepath.is_absolute():
        filepath = PROJECT_ROOT / filepath
    max_age = condition.get("max_age_days", 3)

    if not filepath.exists():
        return True, "file missing"

    try:
        data = json.loads(filepath.read_text(encoding="utf-8"))
        last_updated = data.get("last_updated", "")
        if not last_updated:
            return True, "no timestamp"

        update_dt = datetime.fromisoformat(last_updated.replace("Z", "+00:00"))
        age = datetime.now(timezone.utc) - update_dt
        if age > timedelta(days=max_age):
            return True, f"{age.days}d old"
    except Exception:
        return True, "parse error"

    return False, ""


def evaluate_graduation_check(condition: dict) -> tuple[bool, str]:
    """Check if any learning meets graduation criteria."""
    min_uses = condition.get("min_uses", 10)
    min_confidence = condition.get("min_confidence", 0.8)
    max_harmful = condition.get("max_harmful", 2)

    learnings_dir = MEMORY_DIR / "learnings"
    if not learnings_dir.exists():
        return False, ""

    for f in learnings_dir.glob("*.md"):
        try:
            text = f.read_text(encoding="utf-8", errors="replace")
            uses = confidence = harmful = 0
            for line in text.split("\n"):
                line = line.strip()
                if line.startswith("uses:"):
                    uses = int(line.split(":", 1)[1].strip())
                elif line.startswith("confidence:"):
                    confidence = float(line.split(":", 1)[1].strip())
                elif line.startswith("harmful_uses:"):
                    harmful = int(line.split(":", 1)[1].strip())

            if uses >= min_uses and confidence >= min_confidence and harmful < max_harmful:
                return True, f.name
        except Exception:
            continue

    return False, ""


def evaluate_streak(condition: dict) -> tuple[bool, str]:
    """Check for N consecutive successes."""
    threshold = condition.get("threshold", 5)
    target_outcome = condition.get("outcome", "success")

    summary = load_outcomes_summary()
    recent = summary.get("recent_runs", [])

    if len(recent) < threshold:
        return False, ""

    # Check last N runs
    streak = 0
    for run in reversed(recent):
        if run.get("outcome") == target_outcome:
            streak += 1
        else:
            break

    if streak >= threshold:
        return True, str(streak)
    return False, ""


def evaluate_gap_count(condition: dict) -> tuple[bool, str]:
    """Check if any capability gap is repeated N times."""
    source = condition.get("source_file", ".claude/memory/capability-gaps.md")
    threshold = condition.get("same_pattern_threshold", 3)

    filepath = PROJECT_ROOT / source
    if not filepath.exists():
        return False, ""

    try:
        text = filepath.read_text(encoding="utf-8", errors="replace")
        # Parse table rows: | Date | Query/Need | Times | ...
        for line in text.split("\n"):
            if line.startswith("|") and not line.startswith("| Date") and not line.startswith("|--"):
                parts = [p.strip() for p in line.split("|")]
                if len(parts) >= 4:
                    try:
                        times = int(parts[3])
                        if times >= threshold:
                            return True, parts[2]  # query/need
                    except (ValueError, IndexError):
                        continue
    except Exception:
        pass

    return False, ""


EVALUATORS = {
    "failure_pattern": evaluate_failure_pattern,
    "success_rate": evaluate_success_rate,
    "file_age": evaluate_file_age,
    "graduation_check": evaluate_graduation_check,
    "streak": evaluate_streak,
    "gap_count": evaluate_gap_count,
}


def evaluate_rule(rule: dict) -> tuple[bool, str]:
    """Evaluate a single rule's condition. Returns (fired, context_string)."""
    condition = rule.get("condition", {})
    cond_type = condition.get("type", "")

    evaluator = EVALUATORS.get(cond_type)
    if not evaluator:
        return False, ""

    return evaluator(condition)


def format_message(template: str, context: str) -> str:
    """Simple template substitution."""
    result = template
    # Replace common placeholders
    result = result.replace("{failure_class}/{failure_agent}", context)
    result = result.replace("{rate}", context)
    result = result.replace("{filename}", context)
    result = result.replace("{pattern}", context)
    return result


def matches_tool_input(rule: dict, tool_input: str) -> bool:
    """Check if the written file matches the rule's matcher pattern."""
    matcher = rule.get("matcher", "")
    if not matcher:
        return True
    for pattern in matcher.split("|"):
        pattern = pattern.strip()
        if pattern and pattern in tool_input:
            return True
    return False


# ---------------------------------------------------------------------------
# Composition Engine (Session D / Phase 4b)
# ---------------------------------------------------------------------------

def load_composition_rules() -> list:
    """Parse composition-rules.yaml into a list of composition dicts."""
    if not COMPOSITION_RULES_FILE.exists():
        return []

    text = COMPOSITION_RULES_FILE.read_text(encoding="utf-8")
    compositions: list[dict] = []
    current: dict | None = None
    in_compositions = False
    section = None  # "trigger" | "sequence" | None

    for raw_line in text.split("\n"):
        stripped = raw_line.strip()
        if not stripped or stripped.startswith("#"):
            continue

        indent = len(raw_line) - len(raw_line.lstrip())

        if stripped == "compositions:":
            in_compositions = True
            continue

        if not in_compositions:
            continue

        if stripped.startswith("- name:"):
            if current:
                compositions.append(current)
            name = stripped.split(":", 1)[1].strip().strip('"').strip("'")
            current = {"name": name, "sequence": [], "trigger": {}, "cooldown_minutes": 60}
            section = None
            continue

        if current is None:
            continue

        if stripped == "trigger:":
            section = "trigger"
            continue
        if stripped == "sequence:":
            section = "sequence"
            continue

        # Top-level fields reset section
        if ":" in stripped and not stripped.startswith("-"):
            key, _, val = stripped.partition(":")
            key = key.strip()
            if key not in ("skill", "outcome", "failure_class"):
                section = None  # leaving trigger sub-block

        if section == "trigger":
            if ":" in stripped:
                k, _, v = stripped.partition(":")
                current["trigger"][k.strip()] = v.strip().strip('"').strip("'")
        elif section == "sequence":
            if stripped.startswith("- "):
                current["sequence"].append(stripped[2:].strip().strip('"').strip("'"))
        else:
            if ":" in stripped:
                k, _, v = stripped.partition(":")
                k, v = k.strip(), v.strip().strip('"').strip("'")
                if k == "budget_cap":
                    try:
                        current["budget_cap"] = float(v)
                    except ValueError:
                        pass
                elif k == "cooldown":
                    v_clean = v.split()[0]  # strip inline comments
                    if v_clean.endswith("h"):
                        try:
                            current["cooldown_minutes"] = int(float(v_clean[:-1]) * 60)
                        except ValueError:
                            current["cooldown_minutes"] = 0
                    else:
                        try:
                            current["cooldown_minutes"] = int(v_clean)
                        except ValueError:
                            current["cooldown_minutes"] = 60
                elif k == "enabled":
                    current["enabled"] = v.lower() == "true"
                elif k == "description":
                    current["description"] = v

    if current:
        compositions.append(current)

    return [c for c in compositions if c.get("enabled", True)]


FLOWS_DIR = HOOKS_DIR.parent / "skills" / "mcp-flow" / "flows"
SAFE_FLOW_CLASSES = frozenset({"read-only", "mutating-local"})


def get_flow_safety_class(flow_name: str) -> str:
    """Read safety_class from a flow YAML. Fail-safe to 'mutating-external' on missing/unreadable."""
    flow_path = FLOWS_DIR / f"{flow_name}.yaml"
    if not flow_path.exists():
        return "mutating-external"
    try:
        text = flow_path.read_text(encoding="utf-8", errors="replace")
        for line in text.split("\n"):
            stripped = line.strip()
            if stripped.startswith("safety_class:"):
                val = stripped.split(":", 1)[1].strip().strip('"').strip("'")
                # strip inline comment
                if "  #" in val:
                    val = val[:val.index("  #")].strip()
                return val.lower()
    except Exception:
        pass
    return "mutating-external"


def validate_composition_safety(sequence: list) -> bool:
    """Return True if no step in the sequence contains a destructive skill.

    Special case for /mcp-flow: extract the flow name and check its safety_class.
    Only 'read-only' and 'mutating-local' flows may fire proactively.
    """
    for step in sequence:
        step_lower = step.lower().strip()
        # Standard destructive-skill substring check
        for ds in DESTRUCTIVE_SKILLS:
            if ds in step_lower:
                return False
        # Per-flow safety check for /mcp-flow steps
        if step_lower.startswith("/mcp-flow"):
            tokens = step_lower.split()
            if len(tokens) < 2:
                # /mcp-flow without a flow name = invalid → reject
                return False
            flow_name = tokens[1]
            if get_flow_safety_class(flow_name) not in SAFE_FLOW_CLASSES:
                return False
    return True


def parse_outcome_from_write(tool_input_dict: dict) -> tuple[str, str, str]:
    """Extract (skill, outcome, failure_class) from a just-written outcome file content."""
    file_path = tool_input_dict.get("file_path", "")
    content = tool_input_dict.get("content", "")
    if not content or "outcomes/" not in file_path:
        return "", "", ""

    skill = outcome = failure_class = ""
    in_fm = False
    for line in content.split("\n"):
        s = line.strip()
        if s == "---":
            if not in_fm:
                in_fm = True
            else:
                break
        elif in_fm:
            if s.startswith("skill:"):
                skill = s.split(":", 1)[1].strip().strip('"')
            elif s.startswith("outcome:"):
                outcome = s.split(":", 1)[1].strip().strip('"')
            elif s.startswith("failure_class:"):
                failure_class = s.split(":", 1)[1].strip().strip('"')
    return skill, outcome, failure_class


def check_budget_cap(cap: float) -> bool:
    """Return True if budget allows this composition (cap in USD)."""
    if cap <= 0:
        return True
    budget_file = MEMORY_DIR / "budget.md"
    if not budget_file.exists():
        return True
    try:
        text = budget_file.read_text(encoding="utf-8", errors="replace")
        for line in text.split("\n"):
            line_l = line.lower().strip()
            if "balance" in line_l or "remaining" in line_l:
                m = re.search(r"\$?(\d+\.?\d*)", line)
                if m:
                    return float(m.group(1)) >= cap
    except Exception:
        pass
    return True  # default: allow


def log_composition(name: str, trigger_skill: str, trigger_outcome: str, sequence: list) -> None:
    entry = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "composition": name,
        "trigger_skill": trigger_skill,
        "trigger_outcome": trigger_outcome,
        "sequence": sequence,
        "session": SESSION_KEY,
    }
    with open(COMPOSITION_LOG_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


def evaluate_compositions(tool_input_dict: dict, state: dict) -> list[str]:
    """Evaluate composition rules against the just-written outcome. Returns injected messages."""
    skill, outcome, failure_class = parse_outcome_from_write(tool_input_dict)
    if not skill or not outcome:
        return []

    compositions = load_composition_rules()
    messages = []

    for comp in compositions:
        trigger = comp.get("trigger", {})
        t_skill = trigger.get("skill", "*")
        t_outcome = trigger.get("outcome", "")
        t_fc = trigger.get("failure_class", "")

        # Match skill (wildcard or exact)
        if t_skill != "*" and t_skill != skill:
            continue
        # Match outcome
        if t_outcome and t_outcome != outcome:
            continue
        # Match failure_class if specified
        if t_fc and t_fc != failure_class:
            continue

        name = comp["name"]
        sequence = comp.get("sequence", [])
        if not sequence:
            continue

        # Safety check — never fire destructive compositions
        if not validate_composition_safety(sequence):
            continue

        # Budget cap
        if not check_budget_cap(comp.get("budget_cap", 0.0)):
            continue

        # Cooldown (keyed by composition name)
        cooldown_min = comp.get("cooldown_minutes", 60)
        if cooldown_min > 0 and check_cooldown(state, f"comp:{name}", cooldown_min):
            continue

        # Fire
        steps = " → ".join(sequence)
        msg = f"[composition:{name}] Navrhovaná sekvence: {steps}"
        messages.append(msg)

        # Update cooldown
        if cooldown_min > 0:
            set_cooldown(state, f"comp:{name}")
        log_composition(name, skill, outcome, sequence)

    return messages


def main():
    # Read hook input from stdin
    try:
        hook_input = json.loads(sys.stdin.read())
    except (json.JSONDecodeError, EOFError):
        return

    tool_name = hook_input.get("tool_name", "")
    tool_input = json.dumps(hook_input.get("tool_input", {}))

    # Only fire on Write/Edit to outcomes/ or learnings/
    if tool_name not in ("Write", "Edit", "mcp__filesystem__write_file", "mcp__filesystem__edit_file"):
        return

    if not any(p in tool_input for p in ("outcomes/", "learnings/", "failures/", "capability-gaps")):
        return

    # Prevent recursive triggering
    if os.environ.get("TRIGGER_DEPTH", "0") != "0":
        return

    state = load_state()

    # Check session fire cap
    if get_session_fire_count(state) >= MAX_TRIGGERS_PER_SESSION:
        return

    rules = load_rules()
    fires = []

    for rule in rules:
        rule_id = rule.get("id", "unknown")

        # Check matcher against tool input
        if not matches_tool_input(rule, tool_input):
            continue

        # Evaluate condition first (need context for cooldown key)
        fired, context = evaluate_rule(rule)
        if not fired:
            continue

        # Check cooldown (uses context as part of key)
        cooldown_min = rule.get("cooldown_minutes", 60)
        if check_cooldown(state, rule_id, cooldown_min, context):
            continue

        # Check session cap again (may have changed during loop)
        if get_session_fire_count(state) >= MAX_TRIGGERS_PER_SESSION:
            break

        # Fire!
        action = rule.get("action", {})
        action_type = action.get("type", "notify")
        message_template = action.get("message", f"Trigger fired: {rule_id}")
        message = format_message(message_template, context)

        if action_type == "notify":
            fires.append(message)
        elif action_type == "inject_skill":
            fires.append(message)
        elif action_type == "append_file":
            target = action.get("target", "")
            if target:
                target_path = PROJECT_ROOT / target
                try:
                    with open(target_path, "a", encoding="utf-8") as f:
                        f.write(f"\n| {datetime.now().strftime('%Y-%m-%d')} | {context} | 1 | open | — |\n")
                except Exception:
                    pass

        # Update state
        set_cooldown(state, rule_id, context)
        increment_session_fires(state)
        log_fire(rule_id, message, context)

    # Evaluate compositions (outcome-based proactive sequences)
    if "outcomes/" in tool_input:
        tool_input_dict = hook_input.get("tool_input", {})
        comp_messages = evaluate_compositions(tool_input_dict, state)
        fires.extend(comp_messages)

    save_state(state)

    # Output for Claude Code
    if fires:
        # Trigger messages get [trigger] prefix; composition messages keep their own prefix
        output_parts = []
        for m in fires:
            if m.startswith("[composition:"):
                output_parts.append(m)
            else:
                output_parts.append(f"[trigger] {m}")
        output = {"additionalContext": "\n".join(output_parts)}
        print(json.dumps(output))


if __name__ == "__main__":
    main()
