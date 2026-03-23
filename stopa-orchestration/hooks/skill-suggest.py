#!/usr/bin/env python3
"""UserPromptSubmit hook: suggest relevant skills based on user prompt keywords/patterns."""
import json
import re
import sys
from pathlib import Path

def load_rules():
    rules_path = Path(__file__).parent / "skill-rules.json"
    if not rules_path.exists():
        return {}
    with open(rules_path, encoding="utf-8") as f:
        return json.load(f)

def suggest(prompt, rules):
    prompt_lower = prompt.lower()
    matches = []
    for skill, rule in rules.items():
        if any(kw in prompt_lower for kw in rule.get("keywords", [])):
            matches.append((skill, rule["tier"]))
        elif any(re.search(p, prompt_lower) for p in rule.get("patterns", []) if p):
            matches.append((skill, rule["tier"]))
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
