"""SessionStart hook: detect CLAUDE.md drift vs project profiles.

Runs `regen-claude-md.py --check` silently. If drift is detected (exit 1),
prints a one-line warning to the session header. Idempotent — never modifies files.

Why: project profiles in ~/.claude/memory/projects/ change without the
auto-managed CLAUDE.md table being regenerated. This hook surfaces the gap
so the user can run `python scripts/regen-claude-md.py --write` when convenient.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

if sys.stdout.encoding.lower() != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

REPO = Path(__file__).resolve().parents[2]
SCRIPT = REPO / "scripts" / "regen-claude-md.py"


def main() -> int:
    if not SCRIPT.exists():
        return 0  # script not present — silently skip

    try:
        result = subprocess.run(
            [sys.executable, str(SCRIPT), "--check"],
            cwd=str(REPO),
            capture_output=True,
            text=True,
            timeout=10,
        )
    except (subprocess.TimeoutExpired, OSError):
        return 0  # never block session start on hook errors

    if result.returncode == 1:
        print(
            "[regen-drift] CLAUDE.md is out of date with project profiles. "
            "Run: python scripts/regen-claude-md.py --write"
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
