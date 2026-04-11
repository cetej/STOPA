#!/usr/bin/env python3
"""PostToolUse hook: Capture agent self-disclosure and create audit trail.

Detects moments when the agent explicitly admits mistakes, acknowledges
temptation to bypass rules, or writes Reflexion notes. Creates a durable
audit trail in violations.jsonl.

This is the "self-incrimination" complement to invariant-checker.py:
  - invariant-checker.py = external, objective, machine-verifiable checks
  - self-report-logger.py = captures voluntary self-disclosure (audit trail)

Paper basis: arXiv:2602.22303 — self-incrimination training reduces
undetected attacks from 56% to 6%. Combined with external monitoring = 5.1%.

The behavioral-genome says "přiznej okamžitě, napiš post-mortem" but nothing
logged whether this actually happened. This hook closes that gap.

Trigger: PostToolUse on Write/Edit operations — scans written content for
self-report patterns. Also triggers on Bash for commit messages containing
admissions.

Profile: standard+
Performance target: <30ms — regex-only, no subprocess.
"""
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

# Profile gate
_levels = {"minimal": 1, "standard": 2, "strict": 3}
if _levels.get(os.environ.get("STOPA_HOOK_PROFILE", "standard"), 2) < _levels.get("standard", 2):
    sys.exit(0)

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
sys.stderr.reconfigure(encoding='utf-8', errors='replace')

VIOLATIONS_PATH = Path('.claude/memory/intermediate/violations.jsonl')

# Self-report detection patterns (Czech + English)
# Each tuple: (compiled_regex, category, description)
SELF_REPORT_PATTERNS = [
    # Admission of error
    (re.compile(r'způsobil\s+jsem|zavinil\s+jsem|udělal\s+jsem\s+chybu', re.IGNORECASE),
     "admission", "Agent acknowledged causing an error (CZ)"),
    (re.compile(r'I\s+caused|I\s+introduced|my\s+mistake|my\s+fault|mea\s+culpa', re.IGNORECASE),
     "admission", "Agent acknowledged causing an error (EN)"),

    # Admission of skipping/bypassing
    (re.compile(r'obešel\s+jsem|přeskočil\s+jsem\s+(?:verifikaci|kontrolu|test)', re.IGNORECASE),
     "bypass_admission", "Agent admitted bypassing verification (CZ)"),
    (re.compile(r'I\s+skipped|I\s+bypassed|I\s+didn\'?t\s+(?:verify|check|test)', re.IGNORECASE),
     "bypass_admission", "Agent admitted bypassing verification (EN)"),

    # Temptation acknowledgment
    (re.compile(r'chtěl\s+jsem\s+(?:to\s+)?obejít|pokušení|měl\s+jsem\s+tendenci', re.IGNORECASE),
     "temptation", "Agent acknowledged temptation to bypass rules (CZ)"),
    (re.compile(r'I\s+was\s+tempted|I\s+wanted\s+to\s+(?:skip|bypass|shortcut)', re.IGNORECASE),
     "temptation", "Agent acknowledged temptation to bypass rules (EN)"),

    # Should-have acknowledgment
    (re.compile(r'měl\s+jsem\s+(?:nejdřív\s+)?(?:ověřit|zkontrolovat|přečíst)', re.IGNORECASE),
     "should_have", "Agent acknowledged should-have-done-differently (CZ)"),
    (re.compile(r'I\s+should\s+have\s+(?:verified|checked|read|tested)', re.IGNORECASE),
     "should_have", "Agent acknowledged should-have-done-differently (EN)"),

    # Reflexion note (core-invariant #7)
    (re.compile(r'příště\s+(?:udělám|zkontroluj|ověřím)\s+jinak', re.IGNORECASE),
     "reflexion", "Reflexion note: what to do differently next time (CZ)"),
    (re.compile(r'next\s+time\s+I\s+(?:will|should|must)', re.IGNORECASE),
     "reflexion", "Reflexion note: what to do differently next time (EN)"),

    # Post-mortem pattern
    (re.compile(r'post[\-\s]?mortem|root[\-\s]?cause[\-\s]?analysis|RCA', re.IGNORECASE),
     "post_mortem", "Post-mortem or root cause analysis written"),

    # Explicit self-report keyword
    (re.compile(r'self[\-\s]?report|self[\-\s]?incrimination|přiznávám|hlásím\s+problém', re.IGNORECASE),
     "explicit_report", "Explicit self-report statement"),
]

# Exclude patterns — don't match when writing about self-report (meta-discussion)
EXCLUDE_PATTERNS = [
    re.compile(r'self-report-logger|self_report_patterns|SELF_REPORT', re.IGNORECASE),
    re.compile(r'arXiv.*2602\.22303', re.IGNORECASE),
    re.compile(r'def\s+check_|def\s+detect_|class\s+', re.IGNORECASE),
]


def get_content(tool_name: str, tool_input: dict) -> str:
    """Extract written content from tool input."""
    if tool_name == "Write":
        return tool_input.get("content", "")
    elif tool_name == "Edit":
        return tool_input.get("new_string", "")
    elif tool_name == "Bash":
        cmd = tool_input.get("command", "")
        if "commit" in cmd:
            return cmd
        return ""
    elif "write_file" in tool_name:
        return tool_input.get("content", "")
    elif "edit_file" in tool_name:
        edits = tool_input.get("edits", [])
        return " ".join(e.get("newText", "") for e in edits)
    return ""


def is_meta_content(content: str) -> bool:
    """Check if content is about the self-report system itself (avoid meta-matching)."""
    return any(p.search(content) for p in EXCLUDE_PATTERNS)


def detect_self_reports(content: str) -> list[dict]:
    """Scan content for self-report patterns. Returns list of matches."""
    if not content or len(content) < 10:
        return []

    if is_meta_content(content):
        return []

    matches = []
    seen_categories = set()

    for pattern, category, description in SELF_REPORT_PATTERNS:
        if category in seen_categories:
            continue
        match = pattern.search(content)
        if match:
            seen_categories.add(category)
            # Extract surrounding context (max 100 chars)
            start = max(0, match.start() - 30)
            end = min(len(content), match.end() + 30)
            context = content[start:end].strip()

            matches.append({
                "category": category,
                "description": description,
                "matched_phrase": match.group(0),
                "context": context,
            })

    return matches


def log_self_report(filepath: str, reports: list[dict]) -> None:
    """Append self-report entries to violations.jsonl."""
    try:
        VIOLATIONS_PATH.parent.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now(timezone.utc).isoformat()

        with open(VIOLATIONS_PATH, "a", encoding="utf-8") as f:
            for report in reports:
                entry = {
                    "timestamp": timestamp,
                    "type": "self_reported",
                    "auto_reported": False,
                    "filepath": filepath,
                    **report,
                }
                f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    except OSError:
        pass


def main():
    try:
        hook_input = json.loads(sys.stdin.read())
    except (json.JSONDecodeError, EOFError):
        print(json.dumps({"decision": "approve"}))
        return

    tool_name = hook_input.get("tool_name", "")
    tool_input = hook_input.get("tool_input", {})

    # Trigger on Write/Edit and commit-containing Bash
    tracked_tools = {"Write", "Edit", "Bash",
                     "mcp__filesystem__write_file", "mcp__filesystem__edit_file"}
    if tool_name not in tracked_tools:
        print(json.dumps({"decision": "approve"}))
        return

    filepath = tool_input.get("file_path", tool_input.get("path", ""))
    content = get_content(tool_name, tool_input)

    if not content:
        print(json.dumps({"decision": "approve"}))
        return

    # Don't scan hook/script source files being written
    norm = filepath.replace("\\", "/") if filepath else ""
    if ".claude/hooks/" in norm and norm.endswith(".py"):
        print(json.dumps({"decision": "approve"}))
        return

    reports = detect_self_reports(content)

    if reports:
        log_self_report(filepath, reports)
        # Informational only — never block
        categories = [r["category"] for r in reports]
        print(json.dumps({
            "decision": "approve",
            "message": f"[self-report-logger] Detected self-disclosure: {', '.join(categories)}"
        }))
    else:
        print(json.dumps({"decision": "approve"}))


if __name__ == "__main__":
    main()
