"""SessionStart hook — warn if required API keys are missing from environment.

Appends to alerts.md (severity: medium) if a required key is missing.
Does NOT block session start. Does NOT validate key values (use keys-health.py for that).

Required keys (update list as infrastructure evolves):
    ANTHROPIC_API_KEY — blocks L2 permission sentinel, sub-agent spawns
    FAL_KEY           — blocks /nano, /klip
    BRAVE_API_KEY     — blocks /watch, /radar, /deepresearch
    GITHUB_TOKEN      — blocks /fix-issue, /autofix, GitHub MCP

Exit 0 always (soft warn).
"""

from __future__ import annotations

import os
import sys
from datetime import datetime
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

REQUIRED_KEYS = [
    ("ANTHROPIC_API_KEY", "L2 permission sentinel, sub-agents"),
    ("FAL_KEY", "/nano, /klip"),
    ("BRAVE_API_KEY", "/watch, /radar, /deepresearch"),
    ("GITHUB_TOKEN", "/fix-issue, /autofix, GitHub MCP"),
]

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
ALERTS_FILE = PROJECT_ROOT / ".claude" / "memory" / "alerts.md"
STATE_FILE = PROJECT_ROOT / ".claude" / "memory" / "intermediate" / "keys-presence-state.json"


def load_last_state() -> set[str]:
    if not STATE_FILE.exists():
        return set()
    try:
        import json
        data = json.loads(STATE_FILE.read_text(encoding="utf-8"))
        return set(data.get("missing", []))
    except Exception:
        return set()


def save_state(missing: set[str]) -> None:
    import json
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(
        json.dumps({"ts": datetime.now().isoformat(), "missing": sorted(missing)}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def append_alert(missing: list[tuple[str, str]]) -> None:
    ALERTS_FILE.parent.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime("%Y-%m-%d %H:%M")
    keys_list = ", ".join(k for k, _ in missing)
    with ALERTS_FILE.open("a", encoding="utf-8") as f:
        f.write(f"\n## {ts} — [keys-presence] Missing API keys: {keys_list}\n")
        f.write(f"- **Severity:** medium\n")
        f.write(f"- **Source:** SessionStart keys-presence-check.py\n")
        f.write(f"- **Detail:** The following required keys are not in environment:\n")
        for key, purpose in missing:
            f.write(f"  - `{key}` — blocks {purpose}\n")
        f.write(f"- **Action suggested:** fill values in `~/.claude/keys/secrets.env`, run `pwsh scripts/keys-sync.ps1`, restart CC.\n")
        f.write(f"- **Status:** open\n")


def main() -> None:
    missing = [(k, p) for k, p in REQUIRED_KEYS if not os.environ.get(k, "").strip()]
    missing_set = {k for k, _ in missing}
    last_missing = load_last_state()

    # Only alert on change — avoid spamming alerts.md on every session start
    if missing_set and missing_set != last_missing:
        append_alert(missing)

    save_state(missing_set)


if __name__ == "__main__":
    try:
        main()
    except Exception:
        # Soft-fail — never block session
        pass
