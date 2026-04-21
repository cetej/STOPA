"""Idempotently inject NO TELEGRAM policy header into scheduled task SKILL.md files.

Usage: python scripts/inject-no-telegram-policy.py [--dry-run]
"""

import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

POLICY_MARKER = "<!-- NO-TELEGRAM-POLICY v1 -->"
POLICY_BLOCK = f"""{POLICY_MARKER}
**Notification policy (2026-04-21):** NO Telegram — user disabled. Ignore any "send Telegram", "Telegram reply", `mcp__plugin_telegram_telegram__*`, or `telegram-notify.sh` instructions below. Instead:
- **Routine OK output** → append single line to `C:\\Users\\stock\\Documents\\000_NGM\\STOPA\\.claude\\memory\\daily-reports.md` in format `YYYY-MM-DD HH:MM | task-name | status summary`.
- **Genuine problems** (failures, vulnerabilities, new criticals, quota issues) → append structured entry to `C:\\Users\\stock\\Documents\\000_NGM\\STOPA\\.claude\\memory\\alerts.md` per its template.
- **Nothing to report** → silent exit.

"""

TASKS_DIR = Path.home() / ".claude" / "scheduled-tasks"
DRY_RUN = "--dry-run" in sys.argv


def inject(path: Path) -> str:
    text = path.read_text(encoding="utf-8", errors="replace")
    if POLICY_MARKER in text:
        return "already_present"

    lines = text.splitlines(keepends=True)
    if not lines or not lines[0].startswith("---"):
        return "no_frontmatter"

    closer_idx = None
    for i, line in enumerate(lines[1:], start=1):
        if line.startswith("---"):
            closer_idx = i
            break

    if closer_idx is None:
        return "no_frontmatter_close"

    insert_at = closer_idx + 1
    blank_prefix = "\n" if insert_at < len(lines) and lines[insert_at].strip() else ""
    new_lines = lines[:insert_at] + [blank_prefix + POLICY_BLOCK] + lines[insert_at:]
    new_text = "".join(new_lines)

    if not DRY_RUN:
        path.write_text(new_text, encoding="utf-8")
    return "injected"


def main() -> None:
    if not TASKS_DIR.exists():
        print(f"ERROR: {TASKS_DIR} not found")
        sys.exit(1)

    stats: dict[str, int] = {}
    skill_files = sorted(TASKS_DIR.glob("*/SKILL.md"))
    for skill in skill_files:
        result = inject(skill)
        stats[result] = stats.get(result, 0) + 1
        print(f"  {result:<20} {skill.parent.name}")

    print()
    print(f"Summary ({'DRY-RUN' if DRY_RUN else 'APPLIED'}):")
    for k, v in sorted(stats.items()):
        print(f"  {v:>3} {k}")


if __name__ == "__main__":
    main()
