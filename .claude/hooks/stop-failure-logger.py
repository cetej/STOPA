#!/usr/bin/env python3
"""StopFailure hook: persist structured failure record on API errors ending turns.

Fires on CC v2.1.x StopFailure event. Classifies the error (timeout/resource/logic)
and writes a YAML failure record to .claude/memory/failures/ for later retrieval
by /learn-from-failure and orchestrator pattern matching.

Complements stop-failure.sh (which handles user-visible recovery guidance + slack).
"""
import json
import re
import sys
from datetime import date
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")
sys.stdin.reconfigure(encoding="utf-8", errors="replace")

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
FAILURES_DIR = PROJECT_ROOT / ".claude/memory/failures"
STATE_FILE = PROJECT_ROOT / ".claude/memory/state.md"
MAX_FAILURES = 50

TIMEOUT_PATTERNS = [
    re.compile(p, re.IGNORECASE)
    for p in [
        r"rate.?limit|429|too many requests|RateLimitError",
        r"503|Service Unavailable|temporarily unavailable",
        r"502|Bad Gateway",
        r"529|overloaded|OverloadedError",
        r"timeout|timed?\s*out|ETIMEDOUT",
    ]
]

RESOURCE_PATTERNS = [
    re.compile(p, re.IGNORECASE)
    for p in [
        r"ENOENT|FileNotFoundError|No such file or directory",
        r"EACCES|PermissionError|Permission denied|Access is denied",
        r"ENOSPC|No space left on device|disk full",
        r"MemoryError|OutOfMemoryError|\bOOM\b|out of memory",
        r"ENOMEM|Cannot allocate memory",
        r"context window|token limit|context length exceeded",
    ]
]


def classify_failure(error_msg: str) -> str:
    """Map error text to HERA failure_class: timeout | resource | logic."""
    if not error_msg:
        return "logic"
    for pattern in TIMEOUT_PATTERNS:
        if pattern.search(error_msg):
            return "timeout"
    for pattern in RESOURCE_PATTERNS:
        if pattern.search(error_msg):
            return "resource"
    return "logic"


def extract_error_text(payload: dict) -> str:
    """Pull an error string from the hook payload — schema is not fully stable."""
    candidates = [
        payload.get("error"),
        payload.get("error_message"),
        payload.get("reason"),
        payload.get("message"),
    ]
    for c in candidates:
        if isinstance(c, str) and c.strip():
            return c
    error_obj = payload.get("error")
    if isinstance(error_obj, dict):
        for key in ("message", "type", "code"):
            val = error_obj.get(key)
            if isinstance(val, str) and val.strip():
                return val
    return json.dumps(payload, ensure_ascii=False)[:500]


def current_task() -> str:
    """Read active task from state.md if available."""
    if not STATE_FILE.exists():
        return "api-failure"
    try:
        content = STATE_FILE.read_text(encoding="utf-8", errors="replace")
        match = re.search(r"^\*\*Goal\*\*:\s*(.+)$", content, re.MULTILINE)
        if match:
            return match.group(1).strip()[:120]
    except OSError:
        pass
    return "api-failure"


def next_failure_id() -> str:
    existing = list(FAILURES_DIR.glob("*-F???-*.md"))
    ids = []
    for f in existing:
        match = re.search(r"-F(\d{3})-", f.name)
        if match:
            ids.append(int(match.group(1)))
    next_id = (max(ids) + 1) if ids else 1
    return f"F{next_id:03d}"


def archive_old_failures() -> None:
    failures = sorted(FAILURES_DIR.glob("*-F???-*.md"), key=lambda f: f.name)
    if len(failures) <= MAX_FAILURES:
        return
    archive_dir = FAILURES_DIR / "archive"
    archive_dir.mkdir(exist_ok=True)
    for f in failures[: len(failures) - MAX_FAILURES]:
        f.rename(archive_dir / f.name)


def slugify(text: str, max_len: int = 40) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return slug[:max_len] or "api-failure"


def write_failure_record(payload: dict) -> Path:
    FAILURES_DIR.mkdir(parents=True, exist_ok=True)
    error_text = extract_error_text(payload)
    failure_class = classify_failure(error_text)
    task = current_task()
    today = date.today().isoformat()
    fid = next_failure_id()
    filename = f"{today}-{fid}-api-failure-{slugify(task)}.md"

    record = f"""---
id: {fid}
date: {today}
task: "{task}"
task_class: pipeline
complexity: medium
tier: unknown
failure_class: {failure_class}
failure_agent: api
resolved: false
resolution_learning: ""
source: stop-failure-hook
---

## Trajectory

Session ended by CC harness on StopFailure event.

## Error

```
{error_text[:2000]}
```

## Root Cause

Pending analysis — classified as `{failure_class}` based on error text.

## Reflexion

Next session: check `.claude/memory/checkpoint.md` if present; for recurring
`{failure_class}` failures run `/learn-from-failure api` for systematic review.
"""
    path = FAILURES_DIR / filename
    path.write_text(record, encoding="utf-8")
    archive_old_failures()
    return path


def main() -> None:
    try:
        payload = json.loads(sys.stdin.read() or "{}")
    except (json.JSONDecodeError, ValueError):
        payload = {}

    path = write_failure_record(payload)

    print(
        json.dumps(
            {
                "decision": "allow",
                "reason": f"StopFailure recorded: {path.name}",
            }
        )
    )


if __name__ == "__main__":
    try:
        main()
    except Exception:
        pass  # Never block harness recovery on logger failure
