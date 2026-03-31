#!/usr/bin/env python3
"""UserPromptSubmit hook: suggest relevant skills based on user prompt keywords/patterns."""
import json
import os
import re
import sys
from pathlib import Path

sys.stdin.reconfigure(encoding="utf-8", errors="replace")
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# Profile gate: standard+
_levels = {'minimal': 1, 'standard': 2, 'strict': 3}
if _levels.get(os.environ.get('STOPA_HOOK_PROFILE', 'standard'), 2) < _levels['standard']:
    sys.exit(0)

def load_rules():
    rules_path = Path(__file__).parent / "skill-rules.json"
    if not rules_path.exists():
        return {}
    with open(rules_path, encoding="utf-8") as f:
        return json.load(f)

def detect_cross_project(prompt_lower):
    """Detect signals that the task might span STOPA and a target project."""
    # Known project names
    project_names = ["ng-robot", "ngrobot", "test1", "adobe-automat", "záchvěv", "zachvev",
                     "monitor", "grafik", "kartograf", "polybot", "orakulum", "dane"]
    # Orchestration-change signals (user won't use these terms, but the intent surfaces)
    orch_signals = ["lepší workflow", "automaticky", "pokaždé když", "vždy když", "hook",
                    "skill", "orchestrace", "orchestraci", "při každém", "across all",
                    "ve všech projektech", "everywhere", "všude", "obecně", "general",
                    "from now on", "od teď", "vždycky"]

    has_project = any(p in prompt_lower for p in project_names)
    has_orch = any(s in prompt_lower for s in orch_signals)

    # Cross-project: mentions another project while in current, or wants systemic change
    return has_project or has_orch


def suggest(prompt, rules):
    prompt_lower = prompt.lower()
    matches = []
    for skill, rule in rules.items():
        if any(kw in prompt_lower for kw in rule.get("keywords", [])):
            matches.append((skill, rule["tier"]))
        elif any(re.search(p, prompt_lower) for p in rule.get("patterns", []) if p):
            matches.append((skill, rule["tier"]))

    # Auto-suggest /triage when cross-project signals detected
    if detect_cross_project(prompt_lower) and not any(s == "triage" for s, _ in matches):
        matches.append(("triage", "critical"))

    return matches

def main():
    try:
        hook_input = json.load(sys.stdin)
    except (json.JSONDecodeError, EOFError):
        return

    # Extract prompt text from hook input
    message = hook_input.get("message", {})
    if isinstance(message, dict):
        content = message.get("content", "")
        if isinstance(content, list):
            content = " ".join(
                c.get("text", "") for c in content if isinstance(c, dict)
            )
    elif isinstance(message, str):
        content = message
    else:
        content = str(message)

    if not content or len(content) < 5:
        return

    rules = load_rules()
    matches = suggest(content, rules)

    if not matches:
        return

    # Sort: critical first, then high, medium
    tier_order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
    matches.sort(key=lambda x: tier_order.get(x[1], 99))

    # Max 3 suggestions
    top = matches[:3]
    lines = []
    for skill, tier in top:
        prefix = {"critical": ">>", "high": ">", "medium": "-"}.get(tier, "-")
        lines.append(f"{prefix} /{skill}")

    suggestion = "Skills: " + ", ".join(f"/{s}" for s, _ in top)
    print(json.dumps({"additionalContext": suggestion}))

if __name__ == "__main__":
    main()
