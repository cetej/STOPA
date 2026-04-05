#!/usr/bin/env python3
"""SessionStart hook: automated learning lifecycle management.

Hippocampus-inspired (Phase 1c): learnings that prove useful get promoted,
harmful ones get retired, stale ones get flagged.

Rules:
- Promotion: uses >= 10 AND confidence >= 0.8 AND harmful_uses < 2
  → auto-add to critical-patterns.md (max 10, weakest displaced)
- Retirement: harmful_uses >= 3 AND harmful_uses >= uses
  → move to learnings-archive/ with [RETIRED] tag
- Stale flag: 60+ days unused AND confidence < 0.5
  → add [STALE] to tags for lower retrieval priority
- Confidence decay: delegated to learnings_retrieval.py (already exists)

Runs at SessionStart, ~100ms typical. Outputs summary as additionalContext.
"""
import json
import re
import sys
import time
from datetime import datetime
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

LEARNINGS_DIR = Path(".claude/memory/learnings")
CRITICAL_PATTERNS = LEARNINGS_DIR / "critical-patterns.md"
ARCHIVE_DIR = Path(".claude/memory/learnings-archive")
USES_LEDGER = Path(".claude/memory/intermediate/uses-ledger.json")
MAX_CRITICAL = 10

SKIP_FILES = frozenset({
    "critical-patterns.md", "index-general.md",
    "block-manifest.json", "ecosystem-scan.md",
})


def parse_frontmatter(content: str) -> dict:
    """Extract YAML frontmatter as flat dict."""
    if not content.startswith("---"):
        return {}
    end = content.find("---", 3)
    if end == -1:
        return {}
    result = {}
    for line in content[3:end].strip().split("\n"):
        if ":" in line:
            key, _, val = line.partition(":")
            result[key.strip()] = val.strip()
    return result


def merge_uses_ledger() -> int:
    """Merge uses-ledger.json counters into learning YAML frontmatter.

    Returns number of learnings updated.
    """
    if not USES_LEDGER.exists():
        return 0
    try:
        ledger = json.loads(USES_LEDGER.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return 0

    if not ledger:
        return 0

    updated = 0
    for filename, increment in ledger.items():
        if increment <= 0:
            continue
        fpath = LEARNINGS_DIR / filename
        if not fpath.exists():
            continue
        try:
            content = fpath.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue

        # Update uses: field in YAML frontmatter
        uses_match = re.search(r"^uses:\s*(\d+)", content, re.MULTILINE)
        if uses_match:
            old_uses = int(uses_match.group(1))
            new_uses = old_uses + increment
            content = content.replace(
                uses_match.group(), f"uses: {new_uses}", 1
            )
        else:
            # No uses: field — insert after harmful_uses or confidence or tags
            insert_after = re.search(
                r"^(harmful_uses|confidence|tags):.*$", content, re.MULTILINE
            )
            if insert_after:
                pos = insert_after.end()
                content = content[:pos] + f"\nuses: {increment}" + content[pos:]
            else:
                continue  # Can't find insertion point

        # Boost confidence by 0.05 per use (max 1.0)
        conf_match = re.search(r"^confidence:\s*([\d.]+)", content, re.MULTILINE)
        if conf_match:
            old_conf = float(conf_match.group(1))
            new_conf = min(1.0, old_conf + increment * 0.05)
            content = content.replace(
                conf_match.group(), f"confidence: {new_conf:.2f}", 1
            )

        try:
            fpath.write_text(content, encoding="utf-8")
            updated += 1
        except OSError:
            continue

    # Clear ledger after successful merge
    try:
        USES_LEDGER.write_text("{}", encoding="utf-8")
    except OSError:
        pass

    return updated


def scan_learnings() -> list[dict]:
    """Scan all learning files and return metadata + path."""
    if not LEARNINGS_DIR.exists():
        return []
    results = []
    for f in LEARNINGS_DIR.glob("*.md"):
        if f.name in SKIP_FILES:
            continue
        try:
            content = f.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        meta = parse_frontmatter(content)
        if not meta:
            continue
        results.append({
            "path": f,
            "name": f.name,
            "content": content,
            "uses": int(meta.get("uses", "0")),
            "harmful_uses": int(meta.get("harmful_uses", "0")),
            "confidence": float(meta.get("confidence", "0.7")),
            "date": meta.get("date", ""),
            "summary": meta.get("summary", f.stem),
            "tags": meta.get("tags", ""),
            "severity": meta.get("severity", "medium"),
        })
    return results


def find_promotion_candidates(learnings: list[dict]) -> list[dict]:
    """Learnings eligible for critical-patterns: uses >= 10, confidence >= 0.8, harmful < 2."""
    return [
        l for l in learnings
        if l["uses"] >= 10 and l["confidence"] >= 0.8 and l["harmful_uses"] < 2
    ]


def find_retirement_candidates(learnings: list[dict]) -> list[dict]:
    """Learnings that should be retired: harmful >= 3 AND harmful >= uses."""
    return [
        l for l in learnings
        if l["harmful_uses"] >= 3 and l["harmful_uses"] >= l["uses"]
    ]


def find_stale_candidates(learnings: list[dict]) -> list[dict]:
    """Learnings unused for 60+ days with low confidence."""
    now = datetime.now()
    stale = []
    for l in learnings:
        if not l["date"]:
            continue
        try:
            d = datetime.strptime(l["date"], "%Y-%m-%d")
            days = (now - d).days
        except ValueError:
            continue
        if days >= 60 and l["uses"] == 0 and l["confidence"] < 0.5:
            if "[STALE]" not in l.get("tags", ""):
                stale.append(l)
    return stale


def promote_to_critical(candidates: list[dict]) -> list[str]:
    """Add promotion candidates to critical-patterns.md."""
    if not candidates or not CRITICAL_PATTERNS.exists():
        return []

    try:
        cp_content = CRITICAL_PATTERNS.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return []

    # Count existing entries (lines starting with - or *)
    existing_entries = [
        line for line in cp_content.split("\n")
        if line.strip().startswith(("- ", "* "))
    ]

    promoted = []
    for c in candidates:
        # Check if already in critical-patterns
        if c["name"] in cp_content:
            continue

        # If at capacity, skip (don't auto-displace yet — let /evolve handle)
        if len(existing_entries) + len(promoted) >= MAX_CRITICAL:
            break

        entry = f"- **{c['summary'][:100]}** (promoted from `{c['name']}`, uses={c['uses']}, conf={c['confidence']})"
        promoted.append(entry)

    if promoted:
        # Append to critical-patterns
        new_content = cp_content.rstrip() + "\n" + "\n".join(promoted) + "\n"
        try:
            CRITICAL_PATTERNS.write_text(new_content, encoding="utf-8")
        except OSError:
            return []

    return [c["name"] for c in candidates[:len(promoted)]]


def retire_learnings(candidates: list[dict]) -> list[str]:
    """Move harmful learnings to archive."""
    ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)
    retired = []
    for c in candidates:
        src = c["path"]
        dst = ARCHIVE_DIR / c["name"]
        try:
            # Add [RETIRED] marker
            content = c["content"]
            if "tags:" in content:
                content = content.replace("tags:", "tags: [RETIRED],", 1) if "[" in content.split("tags:")[1].split("\n")[0] else content
            dst.write_text(content, encoding="utf-8")
            src.unlink()
            retired.append(c["name"])
        except OSError:
            continue
    return retired


def flag_stale(candidates: list[dict]) -> list[str]:
    """Add [STALE] tag to learnings unused for 60+ days."""
    flagged = []
    for c in candidates:
        try:
            content = c["content"]
            # Add STALE to tags
            if "tags:" in content:
                tags_line = re.search(r"^tags:.*$", content, re.MULTILINE)
                if tags_line:
                    old_line = tags_line.group()
                    if "[" in old_line:
                        new_line = old_line.replace("[", "[STALE, ", 1)
                    else:
                        new_line = old_line + ", STALE"
                    content = content.replace(old_line, new_line, 1)
            c["path"].write_text(content, encoding="utf-8")
            flagged.append(c["name"])
        except OSError:
            continue
    return flagged


def main():
    try:
        json.load(sys.stdin)  # consume stdin
    except (json.JSONDecodeError, EOFError):
        pass

    # 0. Merge uses ledger (accumulated during previous session)
    merged = merge_uses_ledger()

    learnings = scan_learnings()
    if not learnings:
        if merged:
            print(json.dumps({"additionalContext": f"[Learning lifecycle] Merged {merged} use counters from ledger"}))
        return

    actions = []
    if merged:
        actions.append(f"Merged {merged} use counters from ledger")

    # 1. Promotions
    promo_candidates = find_promotion_candidates(learnings)
    if promo_candidates:
        promoted = promote_to_critical(promo_candidates)
        if promoted:
            actions.append(f"Promoted {len(promoted)} learnings to critical-patterns: {', '.join(promoted)}")

    # 2. Retirements
    retire_candidates = find_retirement_candidates(learnings)
    if retire_candidates:
        retired = retire_learnings(retire_candidates)
        if retired:
            actions.append(f"Retired {len(retired)} harmful learnings: {', '.join(retired)}")

    # 3. Stale flagging
    stale_candidates = find_stale_candidates(learnings)
    if stale_candidates:
        flagged = flag_stale(stale_candidates)
        if flagged:
            actions.append(f"Flagged {len(flagged)} stale learnings: {', '.join(flagged)}")

    # Output summary
    if actions:
        summary = "[Learning lifecycle] " + " | ".join(actions)
        print(json.dumps({"additionalContext": summary}))


if __name__ == "__main__":
    try:
        main()
    except Exception:
        pass  # Never block session start
