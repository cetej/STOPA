#!/usr/bin/env python3
"""SessionStart hook: verify all rules that have verify_check: in YAML frontmatter.

Runs Grep/Glob/exists checks to enforce that codebase follows stated patterns.
- Reads learnings/*.md (YAML verify_check: field)
- Reads critical-patterns.md (inline "verify: ..." annotations)
- Outputs violations to context + appends to violations.jsonl
- Silently passes if all checks green

Verify format examples:
  YAML:    verify_check: "Grep('pattern', path='.claude/skills/') → 5+ matches"
  Inline:  verify: Glob('.claude/skills/harness/SKILL.md') → 1+ matches
"""
import json
import re
import sys
from datetime import datetime
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")

LEARNINGS_DIR = Path(".claude/memory/learnings")
VIOLATIONS_LOG = Path(".claude/memory/violations.jsonl")
CRITICAL_PATTERNS = Path(".claude/memory/learnings/critical-patterns.md")


# ---------------------------------------------------------------------------
# Parsers
# ---------------------------------------------------------------------------

def parse_yaml_frontmatter(content: str) -> dict:
    """Extract YAML frontmatter as flat string dict."""
    if not content.startswith("---"):
        return {}
    end = content.find("---", 3)
    if end == -1:
        return {}
    yaml_block = content[3:end].strip()
    result = {}
    for line in yaml_block.split("\n"):
        if ":" in line:
            key, _, val = line.partition(":")
            key = key.strip()
            val = val.strip().strip('"').strip("'")
            if key:
                result[key] = val
    return result


def extract_inline_verify_checks(content: str) -> list[tuple[str, str]]:
    """Extract inline 'verify: ...' lines from critical-patterns.md.

    Returns list of (context_label, verify_string) tuples.
    Context_label = heading text before the verify line.
    """
    checks = []
    current_heading = "unknown"
    for line in content.split("\n"):
        heading_match = re.match(r'^##+ (.+)', line)
        if heading_match:
            current_heading = heading_match.group(1).strip()
        verify_match = re.match(r'\s*verify:\s*(.+)', line, re.IGNORECASE)
        if verify_match:
            checks.append((current_heading, verify_match.group(1).strip()))
    return checks


# ---------------------------------------------------------------------------
# Check execution
# ---------------------------------------------------------------------------

def run_grep(pattern: str, path_str: str, glob_pat: str | None) -> int:
    """Count grep matches across files. Returns total match count."""
    base = Path(path_str) if path_str else Path(".")
    if not base.exists():
        return 0

    if glob_pat:
        files = list(base.rglob(glob_pat))
    elif base.is_file():
        files = [base]
    else:
        files = [f for f in base.rglob("*.md") if f.is_file()] + \
                [f for f in base.rglob("*.py") if f.is_file()] + \
                [f for f in base.rglob("*.sh") if f.is_file()] + \
                [f for f in base.rglob("*.json") if f.is_file()]

    count = 0
    try:
        compiled = re.compile(pattern, re.MULTILINE | re.IGNORECASE)
    except re.error:
        return 0

    for f in files:
        if not f.is_file():
            continue
        try:
            text = f.read_text(encoding="utf-8", errors="replace")
            count += len(compiled.findall(text))
        except Exception:
            pass
    return count


def run_glob(pattern: str) -> int:
    """Count glob matches from project root."""
    return len(list(Path(".").glob(pattern)))


def parse_expected(expected_str: str) -> tuple[str, int]:
    """Parse '0 matches', '5+ matches', '1 match' → (op, n)."""
    s = expected_str.lower().replace("matches", "").replace("match", "").strip()
    if not s:
        return (">=", 1)
    plus_match = re.match(r"(\d+)\+", s)
    if plus_match:
        return (">=", int(plus_match.group(1)))
    if re.match(r"^\d+$", s):
        return ("==", int(s))
    return (">=", 1)


def check_count(count: int, expected_str: str) -> bool:
    op, n = parse_expected(expected_str)
    if op == "==":
        return count == n
    if op == ">=":
        return count >= n
    return True


def evaluate_verify(verify_str: str) -> tuple[bool, str]:
    """Parse and run a verify check string.

    Returns (passed: bool, description: str)
    """
    if not verify_str or verify_str.strip().lower() == "manual":
        return True, "manual (skipped)"

    # Extract expected value from → clause
    arrow_match = re.search(r"→\s*(.+)$", verify_str)
    if not arrow_match:
        return True, "no expected value → skipped"
    expected_str = arrow_match.group(1).strip()

    # --- Grep check ---
    # Grep('pattern', path='...') or Grep('pattern', path='...', glob='...')
    grep_match = re.match(
        r"""Grep\(['"](.*?)['"]\s*(?:,\s*path=['"](.*?)['"])?(?:,\s*glob=['"](.*?)['"])?\)""",
        verify_str, re.IGNORECASE
    )
    if grep_match:
        pattern = grep_match.group(1)
        path = grep_match.group(2) or "."
        glob_pat = grep_match.group(3)
        count = run_grep(pattern, path, glob_pat)
        passed = check_count(count, expected_str)
        op, n = parse_expected(expected_str)
        direction = "≥" if op == ">=" else "="
        return passed, f"Grep → found {count} (expected {direction}{n})"

    # --- Glob check ---
    glob_match = re.match(r"""Glob\(['"](.*?)['"]\)""", verify_str, re.IGNORECASE)
    if glob_match:
        pattern = glob_match.group(1)
        count = run_glob(pattern)
        passed = check_count(count, expected_str)
        op, n = parse_expected(expected_str)
        return passed, f"Glob → found {count} (expected {'≥' if op=='>=' else '='}{n})"

    return True, f"unknown format → skipped"


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    checked = 0
    failed = 0
    violations = []
    ts = datetime.now().isoformat()

    # 1. Check learning YAML files (verify_check: field)
    if LEARNINGS_DIR.exists():
        for lf in sorted(LEARNINGS_DIR.glob("*.md")):
            if lf.name == "critical-patterns.md":
                continue  # handled separately below
            try:
                content = lf.read_text(encoding="utf-8", errors="replace")
                meta = parse_yaml_frontmatter(content)
                verify_str = meta.get("verify_check", "")
                if not verify_str:
                    continue
                checked += 1
                passed, desc = evaluate_verify(verify_str)
                if not passed:
                    failed += 1
                    summary = meta.get("summary", "")[:80]
                    violations.append({
                        "timestamp": ts,
                        "source": lf.name,
                        "label": summary or lf.stem,
                        "check": verify_str,
                        "result": desc,
                    })
            except Exception:
                pass

    # 2. Check critical-patterns.md inline verify: annotations
    if CRITICAL_PATTERNS.exists():
        try:
            content = CRITICAL_PATTERNS.read_text(encoding="utf-8", errors="replace")
            for label, verify_str in extract_inline_verify_checks(content):
                checked += 1
                passed, desc = evaluate_verify(verify_str)
                if not passed:
                    failed += 1
                    violations.append({
                        "timestamp": ts,
                        "source": "critical-patterns.md",
                        "label": label,
                        "check": verify_str,
                        "result": desc,
                    })
        except Exception:
            pass

    # 3. Log violations
    if violations:
        VIOLATIONS_LOG.parent.mkdir(parents=True, exist_ok=True)
        with VIOLATIONS_LOG.open("a", encoding="utf-8") as f:
            for v in violations:
                f.write(json.dumps(v, ensure_ascii=False) + "\n")

        # Prune violations.jsonl to last 200 entries
        try:
            lines = VIOLATIONS_LOG.read_text(encoding="utf-8").strip().split("\n")
            if len(lines) > 200:
                VIOLATIONS_LOG.write_text("\n".join(lines[-200:]) + "\n", encoding="utf-8")
        except Exception:
            pass

    # 4. Output to Claude context
    if violations:
        print(f"\n=== RULE VIOLATIONS ({failed}/{checked} checks failed) ===")
        for v in violations:
            print(f"  ✗ [{v['source']}] {v['label']}")
            print(f"    check: {v['check'][:80]}")
            print(f"    found: {v['result']}")
        print("=== Address violations before starting work ===\n")
    elif checked > 0:
        print(f"[verify-sweep] {checked} rule checks passed ✓")

    sys.exit(0)


if __name__ == "__main__":
    main()
