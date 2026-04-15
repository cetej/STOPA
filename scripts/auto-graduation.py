#!/usr/bin/env python3
"""auto-graduation.py: Automatically promote eligible learnings to critical-patterns.md.

Reads autodream-report.json for graduation candidates, then:
- Checks current capacity of critical-patterns.md (max 10)
- Promotes candidates if capacity available
- Skips (and logs) if at capacity
- Marks promoted learnings with graduated_to field

Run after autodream.py:
    python scripts/auto-graduation.py [--dry-run]

Exit codes:
    0 — success (including "nothing to do")
    1 — error (file not found, parse failure)
"""
import json
import re
import sys
from datetime import date
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))
from atomic_utils import atomic_write

REPORT_PATH = REPO_ROOT / ".claude/memory/intermediate/autodream-report.json"
CRITICAL_PATTERNS = REPO_ROOT / ".claude/memory/learnings/critical-patterns.md"
LEARNINGS_DIR = REPO_ROOT / ".claude/memory/learnings"

MAX_CAPACITY = 10
ENTRY_HEADER_RE = re.compile(r"^## (\d+)\.", re.MULTILINE)


def count_entries(content: str) -> int:
    """Count ## N. sections in critical-patterns.md."""
    return len(ENTRY_HEADER_RE.findall(content))


def next_slot(content: str) -> int:
    """Return next available slot number."""
    matches = ENTRY_HEADER_RE.findall(content)
    if not matches:
        return 1
    return max(int(m) for m in matches) + 1


def read_learning(filepath: Path) -> tuple[dict, str]:
    """Return (frontmatter fields, body text)."""
    content = filepath.read_text(encoding="utf-8", errors="replace")
    match = re.match(r"^---\n(.*?)\n---\n(.*)", content, re.DOTALL)
    if not match:
        return {}, content
    raw_yaml, body = match.group(1), match.group(2)
    fields: dict = {}
    for line in raw_yaml.splitlines():
        if ":" in line:
            k, _, v = line.partition(":")
            fields[k.strip()] = v.strip()
    return fields, body.strip()


def set_graduated_to(filepath: Path, slot: int) -> None:
    """Add or update graduated_to field in learning frontmatter."""
    content = filepath.read_text(encoding="utf-8", errors="replace")
    match = re.match(r"^(---\n)(.*?)(\n---\n)(.*)", content, re.DOTALL)
    if not match:
        return
    prefix, raw_yaml, sep, body = match.groups()
    # Remove existing graduated_to if present
    raw_yaml = re.sub(r"^graduated_to:.*\n?", "", raw_yaml, flags=re.MULTILINE)
    # Add new graduated_to
    raw_yaml = raw_yaml.rstrip() + f"\ngraduated_to: critical-patterns-{slot}\n"
    new_content = prefix + raw_yaml + sep + body
    atomic_write(filepath, new_content)


def build_entry(slot: int, fields: dict, body: str, source_filename: str) -> str:
    """Build a critical-patterns.md entry block."""
    today = date.today().isoformat()
    summary = fields.get("summary", "").strip('"').strip("'")
    # Use verify_check if available, else manual
    verify_check = fields.get("verify_check", "manual")
    if verify_check.startswith('"') or verify_check.startswith("'"):
        verify_check = verify_check.strip('"').strip("'")

    # Build heading from summary (first sentence, truncated)
    heading_raw = summary.split(".")[0].strip()
    if len(heading_raw) > 70:
        heading_raw = heading_raw[:67] + "..."

    entry = f"\n## {slot}. {heading_raw}\n"
    entry += f"{summary}\n"
    if verify_check and verify_check != "manual":
        entry += f"verify: {verify_check}\n"
    else:
        entry += "verify: manual\n"
    entry += f"last_confirmed: {today}\n"
    entry += f"source_learning: {source_filename}\n"
    return entry


def main(dry_run: bool = False) -> int:
    if not REPORT_PATH.exists():
        print("[auto-graduation] No autodream report found — run autodream.py first.")
        return 0

    try:
        report = json.loads(REPORT_PATH.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as e:
        print(f"[auto-graduation] ERROR reading report: {e}", file=sys.stderr)
        return 1

    candidates = report.get("graduation_candidates", [])
    if not candidates:
        print("[auto-graduation] No graduation candidates in report.")
        return 0

    if not CRITICAL_PATTERNS.exists():
        print(f"[auto-graduation] ERROR: {CRITICAL_PATTERNS} not found.", file=sys.stderr)
        return 1

    cp_content = CRITICAL_PATTERNS.read_text(encoding="utf-8", errors="replace")
    current_count = count_entries(cp_content)
    available = MAX_CAPACITY - current_count

    print(f"[auto-graduation] {len(candidates)} candidate(s), capacity {current_count}/{MAX_CAPACITY}")

    if available <= 0:
        print(
            f"[auto-graduation] critical-patterns.md at capacity ({current_count}/10). "
            "Run /evolve to demote a stale entry before graduating new learnings."
        )
        return 0

    promoted = 0
    skipped = []

    for candidate in candidates:
        if promoted >= available:
            skipped.append(candidate["file"])
            continue

        filepath = LEARNINGS_DIR / candidate["file"]
        if not filepath.exists():
            print(f"  [WARN] {candidate['file']} not found, skipping.")
            skipped.append(candidate["file"])
            continue

        fields, body = read_learning(filepath)

        # Double-check: skip if already graduated
        if fields.get("maturity") == "core" or fields.get("graduated_to"):
            print(f"  [SKIP] {candidate['file']} already graduated ({fields.get('graduated_to', 'maturity:core')})")
            skipped.append(candidate["file"])
            continue

        slot = next_slot(cp_content)
        entry = build_entry(slot, fields, body, candidate["file"])

        if dry_run:
            print(f"  [DRY-RUN] Would promote {candidate['file']} → slot {slot}")
            print(f"  Entry preview:\n{entry}")
        else:
            # Append entry to critical-patterns.md
            cp_content = cp_content.rstrip() + "\n" + entry
            atomic_write(CRITICAL_PATTERNS, cp_content)

            # Mark learning as graduated
            set_graduated_to(filepath, slot)

            print(f"  [PROMOTED] {candidate['file']} → critical-patterns #{slot}")
            promoted += 1

    if skipped:
        print(f"  [SKIPPED] {len(skipped)} candidate(s) — capacity or already graduated: {', '.join(skipped)}")

    if not dry_run and promoted > 0:
        print(f"[auto-graduation] Done. {promoted} learning(s) promoted to critical-patterns.md.")

    return 0


if __name__ == "__main__":
    dry_run = "--dry-run" in sys.argv
    sys.exit(main(dry_run=dry_run))
