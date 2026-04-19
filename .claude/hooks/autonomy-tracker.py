#!/usr/bin/env python3
"""UserPromptSubmit hook — detect "approval-only" user messages.

Friction signal: if the user sends a short message that's just confirmation
("ano", "ok", "pokračuj"), the assistant probably asked a redundant question
in the previous turn. Log it so /evolve can surface the pattern and the
assistant can self-correct on next session.

Silent: writes to .claude/memory/autonomy-friction.jsonl, no stdout.
"""
from __future__ import annotations

import json
import re
import sys
import time
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

LOG = Path(__file__).resolve().parent.parent / "memory" / "autonomy-friction.jsonl"

# Short approval phrases — Czech + English. Case-insensitive, trimmed.
# Only flag if the ENTIRE message matches (stripped of punctuation).
APPROVAL_PATTERNS = [
    r"ano",
    r"yes",
    r"ok",
    r"okay",
    r"jasn[eě]",
    r"sure",
    r"pokracuj",
    r"pokračuj",
    r"pokracujte",
    r"jdi (do toho|na to)",
    r"tak d[eě]lej",
    r"d[eě]lej",
    r"go",
    r"go (ahead|for it)",
    r"do it",
    r"proceed",
    r"souhlas[ií]m?",
    r"jo",
    r"jop",
    r"jasn[eě]\s*že",
    r"samoz[řr]ejm[eě]",
    r"ur[čc]it[eě]",
    r"jdeme",
    r"bomba",
    r"super\s*tak",
    r"pokra[čc]uj\s*pros[ií]m",
    r"ano\s*pros[ií]m",
    r"přesně\s*tak",
    r"tak\s*jo",
    r"d[ií]ky\s*pokra[čc]uj",
]

COMBINED = re.compile(r"^\s*(" + "|".join(APPROVAL_PATTERNS) + r")[\s\.\!\?]*$", re.IGNORECASE)


def main() -> int:
    try:
        payload = json.loads(sys.stdin.read() or "{}")
    except Exception:
        return 0

    msg = (payload.get("prompt") or payload.get("user_message") or payload.get("message") or "").strip()
    if not msg or len(msg) > 60:
        # Long messages aren't "just approvals"; skip to keep signal pure.
        return 0

    if not COMBINED.match(msg):
        return 0

    # Match — log friction event.
    try:
        LOG.parent.mkdir(parents=True, exist_ok=True)
        entry = {
            "ts": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "session_id": payload.get("session_id"),
            "message": msg,
            "message_len": len(msg),
        }
        with LOG.open("a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    except Exception:
        pass

    return 0


if __name__ == "__main__":
    sys.exit(main())
