#!/usr/bin/env python3
"""PostToolUse hook: Machine-verifiable core invariant checker.

Runs after Write/Edit operations to objectively verify STOPA core invariants.
Unlike self-report (which relies on agent's willingness), this hook checks
factual conditions that cannot be rationalized away.

Inspired by: arXiv:2602.22303 — self-incrimination training shows that
combining self-report with external monitoring is most robust (5.1% vs 6%).
This hook is the "external monitoring" complement to self-report-logger.py.

Invariants checked:
  INV1: Skills must be developed in STOPA, never in target projects
  INV2: commands/ and skills/ must stay in sync (desync detection)
  INV3: Skill description must start with "Use when..."
  INV4: No API keys/secrets in JSON config files
  INV5: No destructive queue/server ops without explicit consent markers

Severity levels:
  BLOCK  — violation that should prevent the edit (INV4 overlap with security-scan)
  WARN   — violation that should be flagged but not blocked
  INFO   — informational, logged only

Output:
  - JSON decision (approve + optional message) to stdout
  - Violations appended to .claude/memory/intermediate/violations.jsonl

Profile: standard+
Performance target: <50ms — pure path/regex checks, no subprocess.
"""
import json
import os
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

# Profile gate
_levels = {"minimal": 1, "standard": 2, "strict": 3}
if _levels.get(os.environ.get("STOPA_HOOK_PROFILE", "standard"), 2) < _levels.get("standard", 2):
    sys.exit(0)

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
sys.stderr.reconfigure(encoding='utf-8', errors='replace')

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
VIOLATIONS_PATH = PROJECT_ROOT / '.claude/memory/intermediate/violations.jsonl'

# Target projects where skills should NOT be created directly
TARGET_PROJECTS = {'NG-ROBOT', 'test1', 'ADOBE-AUTOMAT'}

# Patterns for secret detection (subset of security-scan.py — INV4 specific to JSON)
SECRET_PATTERNS = [
    re.compile(
        r'''(?:api[_-]?key|api[_-]?secret|auth[_-]?token|access[_-]?token'''
        r'''|secret[_-]?key|private[_-]?key|password|passwd)'''
        r'''\s*[=:]\s*["'][A-Za-z0-9+/=_\-]{16,}["']''',
        re.IGNORECASE
    ),
    re.compile(r'''["']sk-[A-Za-z0-9]{20,}["']'''),
    re.compile(r'''["']ghp_[A-Za-z0-9]{36,}["']'''),
    re.compile(r'''["']gho_[A-Za-z0-9]{36,}["']'''),
    re.compile(r'''["']xox[bprs]-[A-Za-z0-9\-]{10,}["']'''),
]


def normalize_path(filepath: str) -> str:
    """Normalize path separators for cross-platform comparison."""
    return filepath.replace("\\", "/")


def check_inv1_skill_location(filepath: str) -> dict | None:
    """INV1: Skills must be developed in STOPA, never in target projects."""
    norm = normalize_path(filepath)

    for project in TARGET_PROJECTS:
        # Check if file is a skill in a target project
        if f"/{project}/" in norm or norm.startswith(f"{project}/"):
            if "SKILL.md" in norm or ".claude/commands/" in norm or ".claude/skills/" in norm:
                return {
                    "invariant": "INV1",
                    "severity": "WARN",
                    "message": f"Skill file written to target project '{project}' — skills must be developed in STOPA first",
                    "filepath": filepath,
                }
    return None


def check_inv2_sync(filepath: str) -> dict | None:
    """INV2: commands/ and skills/ must stay in sync.

    Performs actual content diff between commands/<name>.md and skills/<name>/SKILL.md.
    Only logs violation when files actually differ — skill-sync.sh runs in parallel
    and usually resolves the desync within milliseconds, so preventive reminders
    create heavy log noise (251/308 violations were false-positives, 2026-04-27 audit).
    """
    norm = normalize_path(filepath)

    cmd_match = re.search(r'\.claude/commands/([^/]+)\.md$', norm)
    skill_match = re.search(r'\.claude/skills/([^/]+)/SKILL\.md$', norm)

    if cmd_match:
        skill_name = cmd_match.group(1)
        counterpart = PROJECT_ROOT / f'.claude/skills/{skill_name}/SKILL.md'
        edited = PROJECT_ROOT / f'.claude/commands/{skill_name}.md'
        msg_pair = (f"commands/{skill_name}.md", f"skills/{skill_name}/SKILL.md")
    elif skill_match:
        skill_name = skill_match.group(1)
        counterpart = PROJECT_ROOT / f'.claude/commands/{skill_name}.md'
        edited = PROJECT_ROOT / f'.claude/skills/{skill_name}/SKILL.md'
        msg_pair = (f"skills/{skill_name}/SKILL.md", f"commands/{skill_name}.md")
    else:
        return None

    if not counterpart.exists():
        return None

    try:
        edited_content = edited.read_text(encoding='utf-8', errors='replace') if edited.exists() else ""
        counterpart_content = counterpart.read_text(encoding='utf-8', errors='replace')
    except OSError:
        return None

    if edited_content == counterpart_content:
        return None

    return {
        "invariant": "INV2",
        "severity": "WARN",
        "message": f"DESYNC: {msg_pair[0]} differs from {msg_pair[1]} — run skill-sync.sh or sync manually",
        "filepath": filepath,
    }


def check_inv3_description(filepath: str, content: str) -> dict | None:
    """INV3: Skill description must start with 'Use when...'."""
    norm = normalize_path(filepath)

    if "SKILL.md" not in norm and ".claude/commands/" not in norm:
        return None

    # Look for description field in YAML frontmatter
    desc_match = re.search(r'^description:\s*["\']?(.+)', content, re.MULTILINE)
    if desc_match:
        desc = desc_match.group(1).strip().strip("\"'")
        if desc and not desc.startswith("Use when") and not desc.startswith("Use this"):
            return {
                "invariant": "INV3",
                "severity": "WARN",
                "message": f"Skill description doesn't start with 'Use when...' — got: '{desc[:60]}...'",
                "filepath": filepath,
            }
    return None


def check_inv4_secrets_in_json(filepath: str, content: str) -> dict | None:
    """INV4: No API keys/secrets in JSON config files."""
    norm = normalize_path(filepath)

    if not norm.endswith('.json'):
        return None

    for pattern in SECRET_PATTERNS:
        match = pattern.search(content)
        if match:
            # Redact the actual secret in the message
            matched_text = match.group(0)
            redacted = matched_text[:20] + "..." if len(matched_text) > 20 else matched_text
            return {
                "invariant": "INV4",
                "severity": "BLOCK",
                "message": f"Secret/API key detected in JSON config: {redacted} — use env vars instead",
                "filepath": filepath,
            }
    return None


def check_inv5_destructive_ops(filepath: str, content: str) -> dict | None:
    """INV5: No destructive queue/server operations in scripts without consent.

    Checks for patterns that clear queues, restart servers, or delete data
    in Python/shell scripts.
    """
    norm = normalize_path(filepath)

    if not (norm.endswith('.py') or norm.endswith('.sh')):
        return None

    destructive_patterns = [
        (re.compile(r'\.clear\(\)|queue.*=\s*\[\]|\.truncate\(', re.IGNORECASE),
         "Queue/data clear operation"),
        (re.compile(r'subprocess.*restart|os\.system.*restart|systemctl\s+restart', re.IGNORECASE),
         "Server restart operation"),
        (re.compile(r'shutil\.rmtree|rm\s+-rf\s+/', re.IGNORECASE),
         "Recursive deletion"),
    ]

    for pattern, desc in destructive_patterns:
        if pattern.search(content):
            return {
                "invariant": "INV5",
                "severity": "INFO",
                "message": f"Potentially destructive operation: {desc} — ensure user consent",
                "filepath": filepath,
            }
    return None


def log_violation(violation: dict) -> None:
    """Append violation to JSONL log."""
    try:
        VIOLATIONS_PATH.parent.mkdir(parents=True, exist_ok=True)
        entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "type": "invariant_violation",
            "auto_reported": True,
            **violation,
        }
        with open(VIOLATIONS_PATH, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    except OSError:
        pass  # Best-effort logging


def get_file_content(tool_name: str, tool_input: dict, filepath: str) -> str:
    """Extract the content being written/edited."""
    if tool_name == "Write":
        return tool_input.get("content", "")
    elif tool_name == "Edit":
        return tool_input.get("new_string", "")
    # For filesystem MCP tools
    elif "write_file" in tool_name:
        return tool_input.get("content", "")
    elif "edit_file" in tool_name:
        # edit_file uses edits array
        edits = tool_input.get("edits", [])
        return " ".join(e.get("newText", "") for e in edits)
    return ""


def main():
    try:
        hook_input = json.loads(sys.stdin.read())
    except (json.JSONDecodeError, EOFError):
        print(json.dumps({"decision": "approve"}))
        return

    tool_name = hook_input.get("tool_name", "")
    tool_input = hook_input.get("tool_input", {})

    # Only trigger on Write/Edit operations
    write_tools = {"Write", "Edit", "mcp__filesystem__write_file", "mcp__filesystem__edit_file"}
    if tool_name not in write_tools:
        print(json.dumps({"decision": "approve"}))
        return

    filepath = tool_input.get("file_path", tool_input.get("path", ""))
    if not filepath:
        print(json.dumps({"decision": "approve"}))
        return

    # Project boundary guard — skip files outside STOPA
    from lib.project_guard import is_outside_project
    if is_outside_project(filepath):
        print(json.dumps({"decision": "approve"}))
        return

    content = get_file_content(tool_name, tool_input, filepath)

    # Run all invariant checks
    violations = []

    checks = [
        check_inv1_skill_location(filepath),
        check_inv2_sync(filepath),
        check_inv3_description(filepath, content),
        check_inv4_secrets_in_json(filepath, content),
        check_inv5_destructive_ops(filepath, content),
    ]

    for result in checks:
        if result is not None:
            violations.append(result)
            log_violation(result)

    if not violations:
        print(json.dumps({"decision": "approve"}))
        return

    # Check if any BLOCK-severity violation
    has_block = any(v["severity"] == "BLOCK" for v in violations)

    # Build message
    messages = []
    for v in violations:
        prefix = f"[{v['severity']}]" if v["severity"] != "INFO" else "[info]"
        messages.append(f"[invariant-checker] {prefix} {v['invariant']}: {v['message']}")

    combined_message = "\n".join(messages)

    if has_block:
        # Block the operation — INV4 (secrets) is the only BLOCK case
        print(json.dumps({
            "decision": "block",
            "reason": combined_message,
        }))
    else:
        # Approve but warn
        print(json.dumps({
            "decision": "approve",
            "message": combined_message,
        }))


if __name__ == "__main__":
    main()
