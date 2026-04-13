#!/usr/bin/env python3
"""
brain-telegram-capture.py — Auto-detect brain capture requests from Telegram.

Runs as UserPromptSubmit hook. When incoming message contains a Telegram channel
block with a URL and trigger keyword (brain, capture, ulož, zapamatuj),
appends the URL to brain/inbox.md for processing by brain-ingest scheduled task.

This enables async capture: user sends URL via Telegram at any time,
it gets queued even if no active session is processing it immediately.
"""
import json
import re
import sys
from datetime import datetime
from pathlib import Path

BRAIN_DIR = Path(__file__).parent.parent / "memory" / "brain"
INBOX = BRAIN_DIR / "inbox.md"

# Trigger keywords (case-insensitive)
TRIGGERS = {"brain", "capture", "ulož", "zapamatuj", "mozek", "2brain"}

def main():
    try:
        data = json.loads(sys.stdin.read())
    except (json.JSONDecodeError, EOFError):
        return

    message = data.get("message", "")
    if not message:
        return

    # Check if message is from Telegram channel
    if '<channel source="telegram"' not in message:
        return

    # Extract message text (after the channel tag)
    text_match = re.search(r'</channel>\s*(.*)', message, re.DOTALL)
    if not text_match:
        return

    text = text_match.group(1).strip()
    text_lower = text.lower()

    # Check for trigger keywords
    has_trigger = any(kw in text_lower for kw in TRIGGERS)
    if not has_trigger:
        return

    # Extract URLs from the text
    urls = re.findall(r'https?://[^\s<>"]+', text)

    # Extract non-URL text (potential IDEA)
    clean_text = re.sub(r'https?://[^\s<>"]+', '', text).strip()
    # Remove trigger keywords from idea text
    for kw in TRIGGERS:
        clean_text = re.sub(rf'\b{kw}\b', '', clean_text, flags=re.IGNORECASE).strip()
    clean_text = re.sub(r'\s+', ' ', clean_text).strip()
    clean_text = clean_text.strip(':').strip()

    if not urls and not clean_text:
        return

    # Ensure inbox exists
    if not INBOX.exists():
        return

    # Read current inbox
    content = INBOX.read_text(encoding="utf-8")

    # Find insertion point (after "## Queue" line)
    queue_marker = "## Queue"
    if queue_marker not in content:
        return

    # Build entries
    entries = []
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    for url in urls:
        entries.append(f"URL: {url}  <!-- telegram {now} -->")
    if clean_text and len(clean_text) > 5:
        entries.append(f"IDEA: {clean_text}  <!-- telegram {now} -->")

    if not entries:
        return

    # Insert after ## Queue marker
    lines = content.split("\n")
    insert_idx = None
    for i, line in enumerate(lines):
        if line.strip() == queue_marker:
            insert_idx = i + 1
            break

    if insert_idx is None:
        return

    # Skip empty lines after marker
    while insert_idx < len(lines) and not lines[insert_idx].strip():
        insert_idx += 1

    for entry in reversed(entries):
        lines.insert(insert_idx, entry)

    INBOX.write_text("\n".join(lines), encoding="utf-8")

    # Signal to Claude that items were queued
    result = {"message": f"2BRAIN: {len(entries)} item(s) queued in inbox from Telegram"}
    print(json.dumps(result))

if __name__ == "__main__":
    main()
