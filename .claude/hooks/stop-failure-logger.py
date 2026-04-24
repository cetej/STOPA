#!/usr/bin/env python3
"""StopFailure hook: persist failure record from API-ended turns.

Fires on the `StopFailure` hook event (CC v2.1.x). Complements the existing
`stop-failure.sh` notifier — this script writes the persistent trajectory
record so later sessions (or `/learn-from-failure`) can replay the incident.

Follows the failure format in `.claude/rules/memory-files.md § Failures`.
Classification rules:
- rate limit / 503 / timeout / timed out / 429 -> `timeout`
- OOM / ENOENT / EACCES / no such file / disk full -> `resource`
- everything else -> `logic`

Hook never blocks recovery: any unexpected error exits 0 silently.
"""
import json
import re
import sys
from datetime import date
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
FAILURES_DIR = PROJECT_ROOT / ".claude/memory/failures"
STATE_FILE = PROJECT_ROOT / ".claude/memory/state.md"
BUDGET_FILE = PROJECT_ROOT / ".claude/memory/budget.md"
MAX_FAILURES = 50

TIMEOUT_MARKERS = (
    "rate limit",
    "rate-limit",
    "429",
    "503",
    "504",
    "529",
    "overloaded",
    "timeout",
    "timed out",
    "server_error",
    "invalid_request",
    "api_error",
    "overloaded_error",
)

# Generic API error signals with no actionable context — not worth a failure record
SKIP_IF_BARE = ("server_error", "invalid_request", "api_error", "overloaded_error", "unknown_error")
RESOURCE_MARKERS = (
    "out of memory",
    " oom",
    "enomem",
    "enoent",
    "eacces",
    "no such file",
    "permission denied",
    "disk full",
    "disk space",
    "no space left",
)


def classify_error(message: str) -> str:
    m = message.lower()
    if any(kw in m for kw in TIMEOUT_MARKERS):
        return "timeout"
    if any(kw in m for kw in RESOURCE_MARKERS):
        return "resource"
    return "logic"


def next_failure_id() -> str:
    existing = list(FAILURES_DIR.glob("*-F???-*.md"))
    ids = []
    for p in existing:
        match = re.search(r"-F(\d{3})-", p.name)
        if match:
            ids.append(int(match.group(1)))
    return f"F{(max(ids) + 1) if ids else 1:03d}"


def archive_old_failures() -> None:
    failures = sorted(FAILURES_DIR.glob("*-F???-*.md"), key=lambda f: f.name)
    if len(failures) <= MAX_FAILURES:
        return
    archive_dir = FAILURES_DIR / "archive"
    archive_dir.mkdir(exist_ok=True)
    for old in failures[: len(failures) - MAX_FAILURES]:
        old.rename(archive_dir / old.name)


def read_active_task() -> str:
    if not STATE_FILE.exists():
        return "unknown"
    try:
        for line in STATE_FILE.read_text(encoding="utf-8", errors="replace").splitlines():
            if line.startswith("**Goal**:"):
                return line.replace("**Goal**:", "").strip().strip('"')
    except OSError:
        return "unknown"
    return "unknown"


def read_active_tier() -> str:
    if not BUDGET_FILE.exists():
        return "light"
    try:
        text = BUDGET_FILE.read_text(encoding="utf-8", errors="replace").lower()
    except OSError:
        return "light"
    for tier in ("farm", "deep", "standard", "light"):
        if tier in text:
            return tier
    return "light"


def extract_error_message(payload: object) -> str:
    """Pull a human-readable error blurb out of whatever payload shape arrives."""
    if isinstance(payload, dict):
        for key in ("error", "message", "reason", "stop_reason", "api_error"):
            val = payload.get(key)
            if isinstance(val, str) and val.strip():
                return val.strip()
            if isinstance(val, dict):
                nested = val.get("message") or val.get("reason")
                if isinstance(nested, str) and nested.strip():
                    return nested.strip()
        # Fall back to a truncated dump so classification still has signal
        return json.dumps(payload, ensure_ascii=False)[:500]
    if isinstance(payload, str):
        return payload.strip() or "unknown_error"
    return "unknown_error"


def slugify(text: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return slug[:40] if slug else "api-failure"


def build_record(
    fid: str,
    today: str,
    task: str,
    tier: str,
    failure_class: str,
    error_msg: str,
) -> str:
    safe_err = error_msg[:240].replace("`", "'")
    return f"""---
id: {fid}
date: {today}
task: "{task}"
task_class: pipeline
complexity: medium
tier: {tier}
failure_class: {failure_class}
failure_agent: session
resolved: false
resolution_learning: ""
source: stop_failure_hook
---

## Trajectory

1. Session working on "{task}" at tier:{tier}
2. `StopFailure` event fired — API error ended the turn before normal Stop hook
3. `stop-failure-logger.py` captured payload and classified as `{failure_class}`

## Root Cause

Pending analysis. Raw error signal: `{safe_err}`

## Reflexion

Classification: `{failure_class}`. Next session should:
- `timeout` → back off (5-10 min), then retry; do not immediately re-run
- `resource` → STOP, do not retry automatically; check disk/memory first
- `logic` → read `.claude/memory/checkpoint.md` and resume cleanly

Run `/learn-from-failure session` if this recurs.
"""


def main() -> None:
    try:
        raw = sys.stdin.read()
        payload = json.loads(raw) if raw.strip() else {}
    except (json.JSONDecodeError, ValueError):
        payload = {}

    error_msg = extract_error_message(payload)
    failure_class = classify_error(error_msg)
    task = read_active_task()
    tier = read_active_tier()
    today = date.today().isoformat()

    # Skip noise: bare API-error signals with no active task context — nothing to learn from
    if task == "unknown" and error_msg.strip().lower() in SKIP_IF_BARE:
        print(json.dumps({"decision": "allow", "reason": f"StopFailure skipped (bare {error_msg}, no task context)"}))
        return

    FAILURES_DIR.mkdir(parents=True, exist_ok=True)

    fid = next_failure_id()
    slug = slugify(f"api-failure-{failure_class}")
    filename = FAILURES_DIR / f"{today}-{fid}-{slug}.md"

    record = build_record(fid, today, task, tier, failure_class, error_msg)
    filename.write_text(record, encoding="utf-8")

    archive_old_failures()

    print(
        json.dumps(
            {
                "decision": "allow",
                "reason": f"StopFailure {fid} recorded: {failure_class} (task: {task})",
            }
        )
    )


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        # Hook must never block recovery. Log to stderr, exit 0.
        print(f"stop-failure-logger error: {e}", file=sys.stderr)
        sys.exit(0)
