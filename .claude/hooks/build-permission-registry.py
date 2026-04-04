#!/usr/bin/env python3
"""SessionStart hook: Build permission registry from SKILL.md frontmatter.

Parses all SKILL.md files and generates a JSON registry mapping
skill names to their allowed/denied/constrained tool permissions.
Used by tool-gate.py for runtime enforcement.

Output: .claude/memory/intermediate/skill-permissions.json
"""
import json
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")

SKILLS_DIR = Path(".claude/skills")
COMMANDS_DIR = Path(".claude/commands")
OUTPUT = Path(".claude/memory/intermediate/skill-permissions.json")


def parse_yaml_list(value: str) -> list[str]:
    """Parse YAML list from frontmatter value.

    Handles formats:
      - Inline: Read, Write, Edit
      - JSON array: ["Read", "Write"]
      - YAML array: [Read, Write]
    """
    value = value.strip()
    if not value:
        return []

    # JSON/YAML array format: ["Read", "Write"] or [Read, Write]
    if value.startswith("["):
        value = value.strip("[]")
        items = [v.strip().strip('"').strip("'") for v in value.split(",")]
        return [i for i in items if i]

    # Comma-separated inline: Read, Write, Edit
    if "," in value:
        return [v.strip() for v in value.split(",") if v.strip()]

    # Single value
    return [value] if value else []


def parse_frontmatter(content: str) -> dict:
    """Extract YAML frontmatter fields from SKILL.md content."""
    if not content.startswith("---"):
        return {}

    end = content.find("---", 3)
    if end == -1:
        return {}

    fm_text = content[3:end].strip()
    result = {}
    current_key = None
    list_items = []

    for line in fm_text.split("\n"):
        # YAML list item (continuation of previous key)
        if line.strip().startswith("- ") and current_key:
            item = line.strip()[2:].strip().strip('"').strip("'")
            list_items.append(item)
            continue

        # If we were collecting list items, save them
        if current_key and list_items:
            result[current_key] = list_items
            list_items = []
            current_key = None

        # Key-value pair
        match = re.match(r"^(\w[\w-]*)\s*:\s*(.*)", line)
        if match:
            key = match.group(1)
            value = match.group(2).strip()

            if key in ("allowed-tools", "deny-tools", "constrained-tools",
                        "permission-tier", "name"):
                if value:
                    # Inline value
                    result[key] = value
                    current_key = None
                else:
                    # Value on next lines (YAML list)
                    current_key = key
                    list_items = []

    # Save remaining list items
    if current_key and list_items:
        result[current_key] = list_items

    return result


def parse_constrained_tools(value) -> dict[str, list[str]]:
    """Parse constrained-tools field.

    Format in YAML:
      constrained-tools:
        Bash: ["python *", "git *"]
    Or:
      constrained-tools: {Bash: ["python *", "git *"]}
    """
    if isinstance(value, dict):
        return value
    if isinstance(value, str):
        # Try JSON parse
        value = value.strip()
        if value.startswith("{"):
            try:
                return json.loads(value)
            except json.JSONDecodeError:
                pass
    return {}


def build_registry() -> dict:
    """Scan all skills and build permission registry."""
    registry = {}

    # Scan skills/ directory (canonical source)
    if SKILLS_DIR.exists():
        for skill_dir in sorted(SKILLS_DIR.iterdir()):
            skill_file = skill_dir / "SKILL.md"
            if not skill_file.exists():
                continue

            try:
                content = skill_file.read_text(encoding="utf-8", errors="replace")
            except OSError:
                continue

            fm = parse_frontmatter(content)
            name = fm.get("name", skill_dir.name)
            if not name:
                continue

            # Parse allowed-tools
            allowed_raw = fm.get("allowed-tools", [])
            if isinstance(allowed_raw, str):
                allowed = parse_yaml_list(allowed_raw)
            elif isinstance(allowed_raw, list):
                allowed = [str(i).strip() for i in allowed_raw if str(i).strip()]
            else:
                allowed = []

            # Parse deny-tools
            denied_raw = fm.get("deny-tools", [])
            if isinstance(denied_raw, str):
                denied = parse_yaml_list(denied_raw)
            elif isinstance(denied_raw, list):
                denied = [str(i).strip() for i in denied_raw if str(i).strip()]
            else:
                denied = []

            # Parse permission-tier
            tier = fm.get("permission-tier", "")
            if isinstance(tier, list):
                tier = tier[0] if tier else ""

            # Parse constrained-tools
            constrained = parse_constrained_tools(fm.get("constrained-tools", {}))

            registry[name] = {
                "allowed": allowed,
                "denied": denied,
                "tier": tier,
                "constrained": constrained,
            }

    return registry


def main():
    registry = build_registry()

    # Ensure output directory exists
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    # Write registry
    OUTPUT.write_text(
        json.dumps(registry, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    # Summary to stderr (visible in hook output)
    skills_with_perms = sum(
        1 for v in registry.values()
        if v["allowed"] or v["denied"] or v["tier"]
    )
    print(
        f"Permission registry: {len(registry)} skills, "
        f"{skills_with_perms} with declared permissions",
        file=sys.stderr,
    )


if __name__ == "__main__":
    main()
