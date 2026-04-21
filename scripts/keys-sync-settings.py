"""Merge ~/.claude/keys/secrets.env values into ~/.claude/settings.json env block.

Rationale: Windows desktop Claude Code does not reliably inherit User-scope env vars
(inherited from Explorer parent at launch time). Writing to settings.json env block
guarantees CC loads the keys on every start.

Usage:
    python scripts/keys-sync-settings.py             # apply merge
    python scripts/keys-sync-settings.py --dry-run   # show diff only
    python scripts/keys-sync-settings.py --prune     # remove keys from settings.json
                                                       that are no longer in secrets.env

Safety:
- Preserves all non-secret keys in env block (e.g. CLAUDE_AUTOCOMPACT_PCT_OVERRIDE)
- Preserves all other settings.json sections
- Writes backup to settings.json.bak before modifying
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

HOME = Path.home()
SECRETS = HOME / ".claude" / "keys" / "secrets.env"
SETTINGS = HOME / ".claude" / "settings.json"
BACKUP = HOME / ".claude" / "settings.json.bak"

# Keys that are NOT secrets — never touched by this script
PRESERVED_NON_SECRET_KEYS = {
    "CLAUDE_AUTOCOMPACT_PCT_OVERRIDE",
    "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS",
    "ENABLE_PROMPT_CACHING_1H",
    "CLAUDE_CODE_ENABLE_AWAY_SUMMARY",
    "STOPA_HOOK_PROFILE",
    "STOPA_VERBOSITY",
    "STOPA_VERIFY_HOOKS",
    "STOPA_L2_SENTINEL",
    "STOPA_ADMISSION_GATE",
    "STOPA_TOOL_GATE",
    "STOPA_SENTINEL_MODEL",
}


def parse_secrets_env(path: Path) -> dict[str, str]:
    keys: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            continue
        k, _, v = line.partition("=")
        k, v = k.strip(), v.strip()
        if k and v:  # skip empty values
            keys[k] = v
    return keys


def main() -> int:
    dry_run = "--dry-run" in sys.argv
    prune = "--prune" in sys.argv

    if not SECRETS.exists():
        print(f"ERROR: {SECRETS} not found")
        return 1
    if not SETTINGS.exists():
        print(f"ERROR: {SETTINGS} not found")
        return 1

    secrets = parse_secrets_env(SECRETS)
    settings = json.loads(SETTINGS.read_text(encoding="utf-8"))
    current_env = dict(settings.get("env", {}))

    # Determine what to change
    added: list[str] = []
    updated: list[str] = []
    removed: list[str] = []

    new_env = {}
    # Preserve non-secret keys
    for k, v in current_env.items():
        if k in PRESERVED_NON_SECRET_KEYS:
            new_env[k] = v

    # Merge secrets
    for k, v in secrets.items():
        if k in current_env:
            if current_env[k] != v:
                updated.append(k)
        else:
            added.append(k)
        new_env[k] = v

    # Prune: any secret-looking key in current_env that is NOT in secrets.env and NOT preserved
    if prune:
        for k in current_env:
            if k not in secrets and k not in PRESERVED_NON_SECRET_KEYS:
                removed.append(k)
    else:
        # Without --prune, keep existing secret-looking keys that aren't in secrets.env
        for k, v in current_env.items():
            if k not in new_env:
                new_env[k] = v

    print(f"Summary ({'DRY-RUN' if dry_run else 'APPLIED'}):")
    print(f"  Added:   {len(added)} — {sorted(added)}")
    print(f"  Updated: {len(updated)} — {sorted(updated)}")
    print(f"  Pruned:  {len(removed)} — {sorted(removed)}")
    print(f"  Preserved non-secret: {len([k for k in new_env if k in PRESERVED_NON_SECRET_KEYS])}")
    print(f"  Total env keys after: {len(new_env)}")

    if dry_run:
        return 0

    if not (added or updated or removed):
        print("\nNo changes. settings.json untouched.")
        return 0

    # Backup
    SETTINGS.rename(BACKUP)
    print(f"\nBackup written to: {BACKUP}")

    # Write new settings.json with merged env
    settings["env"] = new_env
    SETTINGS.write_text(json.dumps(settings, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Updated: {SETTINGS}")
    print("\nIMPORTANT: close ALL Claude Code windows (or kill via Task Manager), then relaunch.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
