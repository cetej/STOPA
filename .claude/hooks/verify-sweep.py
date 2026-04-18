#!/usr/bin/env python3
"""SessionStart hook: verify all rules that have verify_check: in YAML frontmatter.

Runs Grep/Glob/exists checks to enforce that codebase follows stated patterns.
- Reads learnings/*.md (YAML verify_check: field)
- Scans skills/*/SKILL.md for stale file references (paths that no longer exist)
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

# .claude/hooks/ → .claude/ → repo root → scripts/
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "scripts"))
from atomic_utils import atomic_write

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

    # 1b. Model gate staleness warnings (inspired by CC @[MODEL_LAUNCH] tagging)
    import os as _os
    current_model = _os.environ.get("ANTHROPIC_MODEL", "")
    if not current_model:
        try:
            _settings = json.loads(Path(".claude/settings.json").read_text(encoding="utf-8"))
            current_model = _settings.get("model", "")
        except Exception:
            pass

    model_gate_warnings = []
    if LEARNINGS_DIR.exists() and current_model:
        for lf in sorted(LEARNINGS_DIR.glob("*.md")):
            if lf.name == "critical-patterns.md":
                continue
            try:
                content = lf.read_text(encoding="utf-8", errors="replace")
                meta = parse_yaml_frontmatter(content)
                gate = meta.get("model_gate", "")
                if gate and gate not in current_model:
                    model_gate_warnings.append(
                        f"  ⚠ [{lf.name}] model_gate: {gate} (current: {current_model})"
                    )
            except Exception:
                pass

    # 2. Scan skill bodies for stale file references
    skills_dir = Path(".claude/skills")
    # Files that skills CREATE at runtime — not expected to exist beforehand
    RUNTIME_CREATED = {
        "implementation-plan.md", "scratchpad.md", "codebase-map.md",
        "env-snapshot.md", "session-stats.json", "trigger-log.jsonl",
        "skill-usage.jsonl", "skill-versions.md", "critic-accuracy.jsonl",
        "discovered-patterns.md", "panic-episodes.jsonl",
        "system-evolve.json", "LEARNINGS.md", ".compile",
    }
    # Directories that skills create on first run
    RUNTIME_CREATED_DIRS = {"briefings"}
    # Path fragments that are templates/examples, not actual file references
    TEMPLATE_FRAGMENTS = {"YYYY-MM-DD", "example", "<", ">", "{", "}", "*", "http", "e.g"}
    if skills_dir.exists():
        ref_patterns = [
            re.compile(r'\$\{CLAUDE_SKILL_DIR\}/(\S+?)(?=[`"\s\)\]]|$)'),
            re.compile(r'Read\s+[`"]?(\.\S+?\.\w+)'),
            re.compile(r'`(\.claude/\S+?\.\w+)`'),
        ]
        seen_refs: set[str] = set()  # dedup
        for skill_dir in sorted(skills_dir.iterdir()):
            if not skill_dir.is_dir():
                continue
            skill_file = skill_dir / "SKILL.md"
            if not skill_file.exists():
                continue
            try:
                skill_text = skill_file.read_text(encoding="utf-8", errors="replace")
            except Exception:
                continue

            for pat in ref_patterns:
                for m in pat.finditer(skill_text):
                    ref_path_str = m.group(1)
                    if "${CLAUDE_SKILL_DIR}" in m.group(0):
                        resolved = skill_dir / ref_path_str
                    else:
                        resolved = Path(ref_path_str)

                    # Skip templates, URLs, variables
                    if any(frag in ref_path_str for frag in TEMPLATE_FRAGMENTS):
                        continue
                    if ref_path_str.startswith("//"):
                        continue
                    # Skip runtime-created files (skills create these on first run)
                    if Path(ref_path_str).name in RUNTIME_CREATED:
                        continue
                    # Skip files inside runtime-created directories
                    if any(part in RUNTIME_CREATED_DIRS for part in Path(ref_path_str).parts):
                        continue
                    # Dedup per skill
                    dedup_key = f"{skill_dir.name}:{ref_path_str}"
                    if dedup_key in seen_refs:
                        continue
                    seen_refs.add(dedup_key)

                    if not resolved.exists():
                        checked += 1
                        failed += 1
                        violations.append({
                            "timestamp": ts,
                            "source": f"skills/{skill_dir.name}/SKILL.md",
                            "label": f"stale reference: {ref_path_str}",
                            "check": f"FileExists({resolved})",
                            "result": f"file not found",
                        })

    # 3. Check critical-patterns.md inline verify: annotations
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

    # 4. Check SKILL.md frontmatter conventions (rules/skill-files.md)
    # Gated by STOPA_VERIFY_SKILL_FRONTMATTER=1 — emits ~63 violations on full audit
    import os as _os
    if _os.environ.get("STOPA_VERIFY_SKILL_FRONTMATTER") == "1":
        skills_dir = Path(".claude/skills")
        if skills_dir.exists():
            for skill_dir in sorted(skills_dir.iterdir()):
                if not skill_dir.is_dir():
                    continue
                skill_file = skill_dir / "SKILL.md"
                if not skill_file.exists():
                    continue
                try:
                    content = skill_file.read_text(encoding="utf-8", errors="replace")
                    meta = parse_yaml_frontmatter(content)

                    # Rule: description must start with "Use when..." (rules/skill-files.md)
                    desc = meta.get("description", "")
                    if desc and not desc.strip().lower().startswith("use when"):
                        checked += 1
                        failed += 1
                        violations.append({
                            "timestamp": ts,
                            "source": f"skills/{skill_dir.name}/SKILL.md",
                            "label": "description should start with 'Use when...'",
                            "check": "description starts with 'Use when'",
                            "result": f"starts with: {desc[:60]!r}",
                        })

                    # Rule: max-depth required (core-invariant #8)
                    if "max-depth" not in meta:
                        checked += 1
                        failed += 1
                        violations.append({
                            "timestamp": ts,
                            "source": f"skills/{skill_dir.name}/SKILL.md",
                            "label": "missing max-depth (core-invariant #8)",
                            "check": "max-depth field present",
                            "result": "field missing",
                        })
                except Exception:
                    pass

    # 5. Log violations
    if violations:
        VIOLATIONS_LOG.parent.mkdir(parents=True, exist_ok=True)
        with VIOLATIONS_LOG.open("a", encoding="utf-8") as f:
            for v in violations:
                f.write(json.dumps(v, ensure_ascii=False) + "\n")

        # Prune violations.jsonl to last 200 entries (atomic rewrite)
        try:
            lines = VIOLATIONS_LOG.read_text(encoding="utf-8").strip().split("\n")
            if len(lines) > 200:
                atomic_write(VIOLATIONS_LOG, "\n".join(lines[-200:]) + "\n")
        except Exception:
            pass

    # 5. Output to Claude context
    if violations:
        print(f"\n=== RULE VIOLATIONS ({failed}/{checked} checks failed) ===")
        for v in violations:
            print(f"  ✗ [{v['source']}] {v['label']}")
            print(f"    check: {v['check'][:80]}")
            print(f"    found: {v['result']}")
        print("=== Address violations before starting work ===\n")
    elif checked > 0:
        print(f"[verify-sweep] {checked} rule checks passed ✓")

    # 5b. Model gate warnings (informational, not violations)
    if model_gate_warnings:
        print(f"\n[model-gate] {len(model_gate_warnings)} learning(s) may be stale for current model:")
        for w in model_gate_warnings:
            print(w)
        print("  → Run /evolve to review model-specific learnings\n")

    sys.exit(0)


if __name__ == "__main__":
    main()
