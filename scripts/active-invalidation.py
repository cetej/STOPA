#!/usr/bin/env python3
"""active-invalidation.py — Hippo-inspired commit-driven learning invalidation.

Scans recent git commit messages for migration/deprecation/removal patterns,
matches mentioned tokens against learnings (frontmatter only — tags, component,
filename), and applies a soft sunset by setting `valid_until: today+30`.

Soft sunset (not immediate kill) gives 30 days for manual review or replay
validation. Originals stay on disk for audit trail.

Triggers (token = first regex group):
  - "migrate from X to Y" / "migrace X to Y"
  - "deprecated X" / "deprecate X"
  - "removed X" / "remove X" / "delete X"
  - "renamed X to Y" / "rename X to Y"

Filters to avoid noise:
  - Token must be > 3 chars
  - Token must NOT be in STOPWORDS
  - Match only YAML frontmatter (tags, component, filename) — NOT body text
  - Already-expired learnings are skipped (idempotent)

Usage:
    python scripts/active-invalidation.py --since 7d --dry-run
    python scripts/active-invalidation.py --since-commit HEAD~10
    python scripts/active-invalidation.py --apply

Ref: kitfunso/hippo-memory src/invalidation.ts
"""
import argparse
import json
import re
import subprocess
import sys
from datetime import date, timedelta
from pathlib import Path

STOPA_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(STOPA_ROOT / "scripts"))
from atomic_utils import atomic_write

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")

LEARNINGS_DIR = STOPA_ROOT / ".claude/memory/learnings"
SUNSET_DAYS = 30  # Days from today for valid_until on matched learnings

# Patterns: each compiled regex captures the deprecated/removed token in group 1.
# Group 2 (when present) is the replacement — currently informational only.
PATTERNS = [
    re.compile(r"\bmigrate\s+from\s+([A-Za-z][\w./-]{2,})\s+to\s+([A-Za-z][\w./-]{2,})", re.IGNORECASE),
    re.compile(r"\bmigrace\s+([A-Za-z][\w./-]{2,})\s+(?:na|to)\s+([A-Za-z][\w./-]{2,})", re.IGNORECASE),
    re.compile(r"\brename[ds]?\s+([A-Za-z][\w./-]{2,})\s+to\s+([A-Za-z][\w./-]{2,})", re.IGNORECASE),
    re.compile(r"\bdeprecat(?:e|ed|ing)\s+([A-Za-z][\w./-]{2,})", re.IGNORECASE),
    re.compile(r"\bremove[ds]?\s+([A-Za-z][\w./-]{2,})", re.IGNORECASE),
    re.compile(r"\bdelete[ds]?\s+([A-Za-z][\w./-]{2,})", re.IGNORECASE),
]

# Words that are valid pattern matches but too generic — would invalidate everything
STOPWORDS = frozenset({
    "the", "from", "this", "that", "test", "tests", "code", "file", "files",
    "log", "logs", "error", "errors", "function", "method", "class", "module",
    "package", "library", "tool", "tools", "skill", "skills", "agent", "agents",
    "memory", "rule", "rules", "hook", "hooks", "data", "config", "configs",
    "settings", "command", "commands", "script", "scripts", "all", "old", "new",
    "and", "but", "with", "for", "into", "onto", "out", "import", "imports",
    "branch", "branches", "main", "master", "feature",
    # Generic English nouns commonly appearing in commit subjects
    "noise", "drafts", "draft", "learnings", "learning", "references",
    "reference", "speculative", "stale", "anomaly", "anomalies", "duplicate",
    "duplicates", "patterns", "pattern", "field", "fields", "value", "values",
})


def is_identifier_shape(token: str) -> bool:
    """Token looks like a code identifier (not plain English).

    Requires one of: underscore, dash, dot, or starts with capital letter (CamelCase).
    Plain lowercase words like 'noise' or 'learnings' return False — those should
    only match via filename, not via tags/component.
    """
    if "_" in token or "-" in token or "." in token:
        return True
    if token and token[0].isupper():
        return True
    return False


def get_recent_commits(since: str | None, since_commit: str | None) -> list[dict]:
    """Read git log entries with hash, date, subject, body."""
    fmt = "%H%x1f%aI%x1f%s%x1f%b%x1e"
    cmd = ["git", "log", f"--pretty=format:{fmt}"]
    if since:
        cmd.append(f"--since={since}")
    elif since_commit:
        cmd.append(f"{since_commit}..HEAD")
    else:
        cmd.append("--since=24h")

    try:
        result = subprocess.run(
            cmd, cwd=STOPA_ROOT, capture_output=True, text=True,
            encoding="utf-8", errors="replace", check=True,
        )
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        print(f"[ERR] git log failed: {e}", file=sys.stderr)
        return []

    commits = []
    for entry in result.stdout.split("\x1e"):
        entry = entry.strip()
        if not entry:
            continue
        parts = entry.split("\x1f")
        if len(parts) < 4:
            continue
        sha, iso_date, subject, body = parts[0], parts[1], parts[2], parts[3]
        commits.append({
            "sha": sha[:8],
            "date": iso_date[:10],
            "message": f"{subject}\n{body}".strip(),
        })
    return commits


def extract_tokens(commit_message: str) -> set[str]:
    """Find all invalidation-pattern tokens in a commit message."""
    tokens: set[str] = set()
    for pat in PATTERNS:
        for match in pat.finditer(commit_message):
            tok = match.group(1).strip().rstrip(".,;:")
            if len(tok) > 3 and tok.lower() not in STOPWORDS:
                tokens.add(tok)
    return tokens


def get_frontmatter_head(content: str) -> str:
    """Return YAML frontmatter block (between --- markers) or empty string."""
    if not content.startswith("---"):
        return ""
    end = content.find("---", 3)
    if end == -1:
        return ""
    return content[3:end]


def learning_mentions_token(content: str, filename: str, token: str) -> bool:
    """Match token in filename (always allowed) or frontmatter tags/component
    (only if token has identifier shape — avoids plain-English false positives).
    """
    tok_lower = token.lower()
    if tok_lower in filename.lower():
        return True

    # Restrict tags/component match to identifier-shaped tokens
    if not is_identifier_shape(token):
        return False

    fm = get_frontmatter_head(content)
    if not fm:
        return False

    # tags: [a, b, c]  OR  tags: a, b, c
    tags_m = re.search(r"^tags:\s*\[?(.*?)\]?\s*$", fm, re.MULTILINE)
    if tags_m and tok_lower in tags_m.group(1).lower():
        return True

    # component: name
    comp_m = re.search(r"^component:\s*[\"']?(\w[\w-]*)", fm, re.MULTILINE)
    if comp_m and tok_lower == comp_m.group(1).lower():
        return True

    return False


def get_valid_until(content: str) -> str | None:
    """Read existing valid_until value from frontmatter, or None if absent."""
    fm = get_frontmatter_head(content)
    m = re.search(r"^valid_until:\s*[\"']?(\d{4}-\d{2}-\d{2})", fm, re.MULTILINE)
    return m.group(1) if m else None


def set_valid_until(content: str, target_date: date) -> str:
    """Set or update valid_until field in frontmatter, preserving everything else."""
    if not content.startswith("---"):
        return content
    end = content.find("---", 3)
    if end == -1:
        return content

    fm = content[3:end]
    body = content[end:]
    target_str = target_date.isoformat()

    pat = re.compile(r"^valid_until:.*$", re.MULTILINE)
    if pat.search(fm):
        new_fm = pat.sub(f"valid_until: {target_str}", fm, count=1)
    else:
        # Append before closing --- (fm has leading/trailing newlines)
        new_fm = fm.rstrip() + f"\nvalid_until: {target_str}\n"

    return f"---{new_fm}{body}"


def main():
    parser = argparse.ArgumentParser(
        description="Commit-driven learning invalidation (Hippo-inspired)",
    )
    parser.add_argument("--since", default="7d", help="Git --since value (default: 7d)")
    parser.add_argument("--since-commit", help="Range from <commit>..HEAD (overrides --since)")
    parser.add_argument("--dry-run", action="store_true", default=True,
                        help="Show what would change without writing (default)")
    parser.add_argument("--apply", action="store_true",
                        help="Actually write changes (overrides --dry-run)")
    parser.add_argument("--json", action="store_true", help="Emit JSON report")
    parser.add_argument("--learnings-dir", default=str(LEARNINGS_DIR),
                        help="Override learnings directory")
    args = parser.parse_args()

    learnings_dir = Path(args.learnings_dir)
    if not learnings_dir.exists():
        print(f"[ERR] Learnings dir does not exist: {learnings_dir}", file=sys.stderr)
        sys.exit(1)

    write_mode = args.apply
    today = date.today()
    sunset_date = today + timedelta(days=SUNSET_DAYS)

    commits = get_recent_commits(args.since, args.since_commit)
    if not commits:
        if args.json:
            print(json.dumps({"commits": 0, "tokens": [], "matches": []}))
        else:
            print("No commits in range — nothing to scan.")
        return

    # Aggregate tokens across all commits
    all_tokens: dict[str, list[str]] = {}  # token → list of commit shas
    for c in commits:
        for tok in extract_tokens(c["message"]):
            all_tokens.setdefault(tok, []).append(c["sha"])

    if not all_tokens:
        if args.json:
            print(json.dumps({"commits": len(commits), "tokens": [], "matches": []}))
        else:
            print(f"Scanned {len(commits)} commit(s); no invalidation patterns found.")
        return

    # Match tokens against learnings
    matches: list[dict] = []
    for fp in sorted(learnings_dir.glob("*.md")):
        if fp.name in {"critical-patterns.md"} or fp.name.startswith("index-"):
            continue
        try:
            content = fp.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue

        existing_valid_until = get_valid_until(content)
        # Skip already-expired (idempotent)
        if existing_valid_until:
            try:
                if date.fromisoformat(existing_valid_until) < today:
                    continue
            except ValueError:
                pass

        for token, shas in all_tokens.items():
            if learning_mentions_token(content, fp.name, token):
                matches.append({
                    "file": fp.name,
                    "token": token,
                    "commit_shas": shas,
                    "existing_valid_until": existing_valid_until,
                    "new_valid_until": sunset_date.isoformat(),
                })
                if write_mode:
                    new_content = set_valid_until(content, sunset_date)
                    if new_content != content:
                        atomic_write(fp, new_content)
                break  # one match per file is enough

    if args.json:
        print(json.dumps({
            "commits": len(commits),
            "tokens": sorted(all_tokens.keys()),
            "matches": matches,
            "applied": write_mode,
        }, ensure_ascii=False, indent=2))
    else:
        mode = "APPLY" if write_mode else "DRY-RUN"
        print(f"[{mode}] Scanned {len(commits)} commit(s).")
        print(f"Detected tokens: {', '.join(sorted(all_tokens.keys())) or '(none)'}")
        if matches:
            print(f"\nMatched {len(matches)} learning(s) → valid_until={sunset_date.isoformat()}:")
            for m in matches:
                prev = f" (was {m['existing_valid_until']})" if m['existing_valid_until'] else ""
                print(f"  - {m['file']:60s} ← {m['token']}{prev}")
        else:
            print("No learnings matched detected tokens.")
        if not write_mode:
            print("\n(dry-run; rerun with --apply to write changes)")


if __name__ == "__main__":
    main()
