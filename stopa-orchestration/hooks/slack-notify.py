#!/usr/bin/env python3
"""Slack webhook proxy for STOPA hooks.

Fire-and-forget notifications to Slack for session lifecycle events.
Config: SLACK_WEBHOOK_URL env var (silent no-op if missing).
Usage: python slack-notify.py <event_type> [key=value ...]
"""
import json
import os
import sys
import urllib.error
import urllib.request

WEBHOOK_URL = os.environ.get("SLACK_WEBHOOK_URL", "")
TIMEOUT = 5  # seconds per request
MAX_RETRIES = 2

# --- Message Templates (Slack Block Kit) ---

TEMPLATES = {
    "session_start": {
        "emoji": ":rocket:",
        "text": "Session started",
        "fields": lambda kv: [
            f"*Branch:* `{kv.get('branch', '?')}`",
            f"*Task:* {kv.get('task', 'unknown')}",
        ],
    },
    "task_completed": {
        "emoji": ":white_check_mark:",
        "text": "Task completed",
        "fields": lambda kv: [
            f"*Task:* {kv.get('task', 'unknown')}",
        ],
    },
    "session_stop": {
        "emoji": ":stop_sign:",
        "text": "Session ended",
        "fields": lambda kv: [
            f"*Active task:* {kv.get('task', 'none')}",
        ],
    },
    "stop_failure": {
        "emoji": ":rotating_light:",
        "text": "API error — session killed",
        "fields": lambda kv: [
            f"*Checkpoint:* {kv.get('checkpoint', 'unknown')}",
            f"*Active task:* {kv.get('task', 'none')}",
        ],
    },
    "post_compact": {
        "emoji": ":compression:",
        "text": "Context compacted",
        "fields": lambda kv: [
            f"*Branch:* `{kv.get('branch', '?')}`",
            f"*Task:* {kv.get('task', 'unknown')}",
        ],
    },
}


def build_payload(event_type: str, kv: dict[str, str]) -> dict:
    """Build Slack Block Kit payload for the given event."""
    template = TEMPLATES.get(event_type)
    if not template:
        # Fallback: plain text for unknown events
        return {"text": f"{event_type}: {json.dumps(kv)}"}

    emoji = template["emoji"]
    text = template["text"]
    fields = template["fields"](kv)

    project = kv.get("project", "STOPA")
    header = f"{emoji}  *{text}*  — _{project}_"

    blocks = [
        {"type": "section", "text": {"type": "mrkdwn", "text": header}},
    ]

    if fields:
        field_text = "\n".join(fields)
        blocks.append(
            {"type": "section", "text": {"type": "mrkdwn", "text": field_text}}
        )

    return {"blocks": blocks, "text": f"{emoji} {text}"}


def send(payload: dict) -> bool:
    """POST payload to Slack webhook with retry. Returns True on success."""
    data = json.dumps(payload).encode("utf-8")

    for attempt in range(MAX_RETRIES):
        try:
            req = urllib.request.Request(
                WEBHOOK_URL,
                data=data,
                headers={"Content-Type": "application/json"},
                method="POST",
            )
            with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
                if resp.status == 200:
                    return True
        except (urllib.error.URLError, urllib.error.HTTPError, OSError):
            if attempt == MAX_RETRIES - 1:
                return False
    return False


def parse_args(args: list[str]) -> tuple[str, dict[str, str]]:
    """Parse CLI args: event_type key=value key=value ..."""
    if not args:
        return "", {}

    event_type = args[0]
    kv = {}
    for arg in args[1:]:
        if "=" in arg:
            k, v = arg.split("=", 1)
            kv[k] = v
    return event_type, kv


def main():
    if not WEBHOOK_URL:
        sys.exit(0)  # Silent no-op when not configured

    event_type, kv = parse_args(sys.argv[1:])
    if not event_type:
        sys.exit(0)

    payload = build_payload(event_type, kv)
    send(payload)  # Fire-and-forget — ignore result


if __name__ == "__main__":
    main()
