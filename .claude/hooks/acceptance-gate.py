#!/usr/bin/env python3
"""
Acceptance Gate Hook — NLAH Self-Evolution Discipline (P2)

PostToolUse hook: after Write/Edit on tracked artifact types,
runs lightweight validation. Advisory only (doesn't block).

Artifact types and their validations:
- SKILL.md    → YAML frontmatter check + description starts with "Use when"
- *.py hooks  → Python syntax check (ast.parse)
- *.yaml recipes → YAML parse check
- settings.json → JSON parse check

Inspired by: arXiv:2603.25723 (NLAH) — self-evolution = acceptance-gated attempts
"""

import ast
import json
import os
import sys
from pathlib import Path


def validate_skill(filepath: str) -> str | None:
    """Validate SKILL.md: has frontmatter, description starts with 'Use when'."""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        if not content.startswith("---"):
            return "SKILL.md missing YAML frontmatter (must start with ---)"

        # Check description field
        import re
        desc_match = re.search(r'^description:\s*["\']?(.+)', content, re.MULTILINE)
        if desc_match:
            desc = desc_match.group(1).strip().strip("\"'")
            if not desc.startswith("Use when") and not desc.startswith("Use this"):
                return f"description field must start with 'Use when...' (got: '{desc[:50]}...')"

        return None
    except Exception as e:
        return f"Validation error: {e}"


def validate_python(filepath: str) -> str | None:
    """Validate Python file: syntax check via ast.parse."""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            source = f.read()
        ast.parse(source, filename=filepath)
        return None
    except SyntaxError as e:
        return f"Python syntax error at line {e.lineno}: {e.msg}"


def validate_yaml(filepath: str) -> str | None:
    """Validate YAML file: parse check."""
    try:
        import yaml  # noqa: F401 — may not be available
        with open(filepath, "r", encoding="utf-8") as f:
            yaml.safe_load(f)
        return None
    except ImportError:
        return None  # Can't validate without PyYAML, skip
    except Exception as e:
        return f"YAML parse error: {e}"


def validate_json(filepath: str) -> str | None:
    """Validate JSON file: parse check."""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            json.load(f)
        return None
    except json.JSONDecodeError as e:
        return f"JSON parse error at line {e.lineno}: {e.msg}"


def main():
    hook_input = json.loads(sys.stdin.read())

    tool_name = hook_input.get("tool_name", "")
    tool_input = hook_input.get("tool_input", {})

    # Only trigger on Write/Edit
    if tool_name not in ("Write", "Edit"):
        print(json.dumps({"decision": "approve"}))
        return

    filepath = tool_input.get("file_path", "")
    if not filepath:
        print(json.dumps({"decision": "approve"}))
        return

    p = Path(filepath)
    error = None

    # Determine artifact type and validate
    if p.name == "SKILL.md" or (p.suffix == ".md" and ".claude/commands/" in filepath.replace("\\", "/")):
        error = validate_skill(filepath)
    elif p.suffix == ".py" and ".claude/hooks/" in filepath.replace("\\", "/"):
        error = validate_python(filepath)
    elif p.suffix in (".yaml", ".yml") and ".claude/recipes/" in filepath.replace("\\", "/"):
        error = validate_yaml(filepath)
    elif p.name == "settings.json":
        error = validate_json(filepath)

    if error:
        # Advisory: report but don't block
        print(json.dumps({
            "decision": "approve",
            "message": f"[acceptance-gate] {error}"
        }))
    else:
        print(json.dumps({"decision": "approve"}))


if __name__ == "__main__":
    main()
