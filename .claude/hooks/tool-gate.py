#!/usr/bin/env python3
"""PreToolUse hook: Runtime enforcement of skill permission declarations.

Reads the active skill context and permission registry to enforce
allowed-tools/deny-tools/constrained-tools declarations at runtime.

Inspired by Google MCP Toolbox for Databases pattern:
agents access resources only through predefined, approved operations.

Modes (STOPA_TOOL_GATE env var):
  warn    — log violations to stderr, never block (default)
  enforce — block coordinator tier + explicit deny-tools, warn others
  off     — disabled entirely

stdin: tool_input JSON from Claude Code
env: CLAUDE_TOOL_NAME — name of the tool being called
"""
import fnmatch
import json
import os
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")

REGISTRY_PATH = Path(".claude/memory/intermediate/skill-permissions.json")
ACTIVE_SKILL_PATH = Path(".claude/memory/intermediate/active-skill.json")

# Gate mode: warn (default), enforce, off
GATE_MODE = os.environ.get("STOPA_TOOL_GATE", "warn").lower()


def load_json(path: Path) -> dict | None:
    """Load JSON file, return None on any error."""
    try:
        return json.loads(path.read_text(encoding="utf-8", errors="replace"))
    except (OSError, json.JSONDecodeError):
        return None


def check_constrained(tool_name: str, tool_input: dict, patterns: list[str]) -> str | None:
    """Check if tool invocation matches constrained patterns.

    Returns None if allowed, or a reason string if blocked.
    """
    if tool_name == "Bash":
        command = tool_input.get("command", "")
        for pattern in patterns:
            if fnmatch.fnmatch(command, pattern):
                return None  # Matches an allowed pattern
            # Also check if command starts with the pattern prefix
            # e.g., pattern "python *" should match "python script.py"
            prefix = pattern.rstrip("*").rstrip()
            if prefix and command.startswith(prefix):
                return None
        allowed_str = ", ".join(f'"{p}"' for p in patterns[:5])
        return f"Bash command doesn't match allowed patterns: {allowed_str}"

    # For non-Bash constrained tools, we don't have a generic matcher yet
    # Future: match Write/Edit file paths, Agent prompts, etc.
    return None


def main():
    # Fast exit if disabled
    if GATE_MODE == "off":
        sys.exit(0)

    tool_name = os.environ.get("CLAUDE_TOOL_NAME", "")
    if not tool_name:
        sys.exit(0)

    # Load active skill context
    active = load_json(ACTIVE_SKILL_PATH)
    if not active or "skill" not in active:
        sys.exit(0)  # No active skill — no enforcement

    skill_name = active["skill"]

    # Load permission registry
    registry = load_json(REGISTRY_PATH)
    if not registry or skill_name not in registry:
        sys.exit(0)  # Skill not in registry — no enforcement

    perms = registry[skill_name]
    allowed = perms.get("allowed", [])
    denied = perms.get("denied", [])
    tier = perms.get("tier", "")
    constrained = perms.get("constrained", {})

    # --- Check deny-tools ---
    if tool_name in denied:
        reason = (
            f"Tool Gate: [{skill_name}] deny-tools declares {tool_name} as forbidden"
        )
        if GATE_MODE == "enforce" or tier == "coordinator":
            print(json.dumps({"decision": "block", "reason": f"\u26d4 {reason}"}))
        else:
            print(f"\u26a0\ufe0f {reason} (warn mode — not blocking)", file=sys.stderr)
        sys.exit(0)

    # --- Check allowed-tools (whitelist) ---
    if allowed and tool_name not in allowed:
        reason = (
            f"Tool Gate: [{skill_name}] allowed-tools does not include {tool_name}"
        )
        if GATE_MODE == "enforce" or tier == "coordinator":
            print(json.dumps({"decision": "block", "reason": f"\u26d4 {reason}"}))
        else:
            print(f"\u26a0\ufe0f {reason} (warn mode — not blocking)", file=sys.stderr)
        sys.exit(0)

    # --- Check constrained-tools (pattern matching) ---
    if tool_name in constrained:
        # Read tool input from stdin for pattern matching
        try:
            raw = sys.stdin.read().strip()
            tool_input = json.loads(raw) if raw else {}
        except (json.JSONDecodeError, EOFError):
            tool_input = {}

        patterns = constrained[tool_name]
        if isinstance(patterns, str):
            patterns = [patterns]

        violation = check_constrained(tool_name, tool_input, patterns)
        if violation:
            reason = f"Tool Gate: [{skill_name}] constrained-tools — {violation}"
            if GATE_MODE == "enforce" or tier == "coordinator":
                print(json.dumps({"decision": "block", "reason": f"\u26d4 {reason}"}))
            else:
                print(f"\u26a0\ufe0f {reason} (warn mode)", file=sys.stderr)

    sys.exit(0)


if __name__ == "__main__":
    main()
