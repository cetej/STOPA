#!/usr/bin/env python3
"""Error classification utility for STOPA orchestration.

Classifies error messages into three types for the 3-fix escalation system:
- infrastructure: unrecoverable environment failures → immediate stop
- transient: temporary failures → 1 retry with delay
- logic: semantic/code errors → normal 3-fix escalation

Usage:
    from error_classifier import classify_error
    error_type = classify_error("FileNotFoundError: No such file: foo.py")
    # Returns: "infrastructure"

Not a hook — imported by orchestration skills and other hooks.
"""
import re
from typing import Literal

ErrorType = Literal["infrastructure", "transient", "logic"]

# Patterns matched case-insensitively against error messages
INFRASTRUCTURE_PATTERNS: list[re.Pattern[str]] = [
    re.compile(p, re.IGNORECASE) for p in [
        r"ENOENT|FileNotFoundError|No such file or directory",
        r"EACCES|PermissionError|Permission denied|Access is denied",
        r"ENOSPC|No space left on device|disk full",
        r"MemoryError|OutOfMemoryError|OOM|out of memory|killed",
        r"ENOMEM|Cannot allocate memory",
        r"ModuleNotFoundError|ImportError.*No module named",
        r"command not found|is not recognized as",
        r"EPIPE|Broken pipe",
        r"IOError.*\[Errno 28\]",  # No space left
        r"OSError.*\[WinError 112\]",  # No space left (Windows)
        r"OSError.*\[WinError 5\]",  # Access denied (Windows)
    ]
]

TRANSIENT_PATTERNS: list[re.Pattern[str]] = [
    re.compile(p, re.IGNORECASE) for p in [
        r"timeout|timed?\s*out|ETIMEDOUT",
        r"rate.?limit|429|too many requests|RateLimitError",
        r"temporarily unavailable|503|Service Unavailable",
        r"502|Bad Gateway",
        r"Connection refused|ECONNREFUSED",
        r"Connection reset|ECONNRESET",
        r"network.*unreachable|ENETUNREACH",
        r"SSL.*error|certificate.*error",
        r"overloaded|OverloadedError",
        r"APIStatusError.*529",  # Anthropic overloaded
    ]
]


def classify_error(error_msg: str) -> ErrorType:
    """Classify an error message into infrastructure/transient/logic.

    Args:
        error_msg: The error message or traceback string

    Returns:
        "infrastructure" — unrecoverable, stop immediately
        "transient" — temporary, retry once
        "logic" — semantic error, normal 3-fix escalation
    """
    if not error_msg:
        return "logic"

    for pattern in INFRASTRUCTURE_PATTERNS:
        if pattern.search(error_msg):
            return "infrastructure"

    for pattern in TRANSIENT_PATTERNS:
        if pattern.search(error_msg):
            return "transient"

    return "logic"


def format_classification(error_msg: str) -> str:
    """Return a human-readable classification string for context injection."""
    error_type = classify_error(error_msg)
    labels = {
        "infrastructure": "INFRASTRUCTURE ERROR — do NOT retry, escalate immediately",
        "transient": "TRANSIENT ERROR — retry once with 5s delay",
        "logic": "LOGIC ERROR — normal 3-fix escalation applies",
    }
    return f"[Error Classification: {labels[error_type]}]"


if __name__ == "__main__":
    # Self-test
    import sys
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    tests = [
        ("FileNotFoundError: No such file: foo.py", "infrastructure"),
        ("PermissionError: [Errno 13] Permission denied", "infrastructure"),
        ("MemoryError", "infrastructure"),
        ("ModuleNotFoundError: No module named 'nonexistent'", "infrastructure"),
        ("429 Too Many Requests", "transient"),
        ("Connection refused", "transient"),
        ("OverloadedError: service overloaded", "transient"),
        ("AssertionError: expected 5 got 3", "logic"),
        ("TypeError: unsupported operand", "logic"),
        ("", "logic"),
    ]
    passed = 0
    for msg, expected in tests:
        result = classify_error(msg)
        status = "OK" if result == expected else f"FAIL (got {result})"
        if result == expected:
            passed += 1
        print(f"  {status}: {msg[:50]} → {result}")
    print(f"\n{passed}/{len(tests)} tests passed")
