#!/usr/bin/env python3
"""HTTP webhook proxy for Claude Code HTTP hooks → Slack.

Workaround for TLS SNI bug (anthropics/claude-code#30613):
CC v2.1.63+ supports "type": "http" hooks, but HTTPS to external domains
fails due to SNI. This proxy listens on localhost and forwards to Slack.

Usage:
    python scripts/webhook-proxy.py

Config (env vars):
    SLACK_WEBHOOK_URL  — Slack incoming webhook URL (required)
    PROXY_PORT         — Port to listen on (default: 9090)

CC sends POST to http://localhost:9090/webhook with JSON body:
    {
        "hook_event_name": "TaskCompleted" | "StopFailure" | ...,
        "tool_name": str,
        "session_id": str,
        "cwd": str
    }
"""
import json
import logging
import os
import sys
import urllib.error
import urllib.request
from http.server import BaseHTTPRequestHandler, HTTPServer

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    stream=sys.stdout,
)
log = logging.getLogger(__name__)

SLACK_WEBHOOK_URL = os.environ.get("SLACK_WEBHOOK_URL", "")
PORT = int(os.environ.get("PROXY_PORT", "9090"))
SLACK_TIMEOUT = 5

# Map CC hook event names to Slack message config
EVENT_TEMPLATES: dict[str, dict] = {
    "TaskCompleted": {
        "emoji": ":white_check_mark:",
        "text": "Task completed",
    },
    "StopFailure": {
        "emoji": ":rotating_light:",
        "text": "API error — session killed",
    },
    "SessionStart": {
        "emoji": ":rocket:",
        "text": "Session started",
    },
    "Stop": {
        "emoji": ":stop_sign:",
        "text": "Session ended",
    },
    "PostCompact": {
        "emoji": ":compression:",
        "text": "Context compacted",
    },
}


def build_slack_payload(event: dict) -> dict:
    """Build Slack Block Kit payload from CC hook event body."""
    hook_event = event.get("hook_event_name", "UnknownEvent")
    session_id = event.get("session_id", "?")[:8]
    cwd = event.get("cwd", "")
    project = os.path.basename(cwd) if cwd else "?"

    tmpl = EVENT_TEMPLATES.get(hook_event, {"emoji": ":bell:", "text": hook_event})
    header = f"{tmpl['emoji']}  *{tmpl['text']}*  — _{project}_"

    fields = [f"*Session:* `{session_id}`"]
    tool = event.get("tool_name")
    if tool:
        fields.append(f"*Tool:* `{tool}`")

    blocks = [
        {"type": "section", "text": {"type": "mrkdwn", "text": header}},
        {"type": "section", "text": {"type": "mrkdwn", "text": "\n".join(fields)}},
    ]
    return {"blocks": blocks, "text": f"{tmpl['emoji']} {tmpl['text']}"}


def send_to_slack(payload: dict) -> bool:
    """POST payload to Slack. Returns True on success."""
    if not SLACK_WEBHOOK_URL:
        return False
    data = json.dumps(payload).encode("utf-8")
    try:
        req = urllib.request.Request(
            SLACK_WEBHOOK_URL,
            data=data,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=SLACK_TIMEOUT) as resp:
            return resp.status == 200
    except (urllib.error.URLError, urllib.error.HTTPError, OSError) as exc:
        log.warning("Slack delivery failed: %s", exc)
        return False


class WebhookHandler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):  # suppress default access log
        pass

    def do_POST(self):
        if self.path != "/webhook":
            self.send_response(404)
            self.end_headers()
            return

        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length) if length else b""

        try:
            event = json.loads(body) if body else {}
        except json.JSONDecodeError:
            event = {}

        hook_event = event.get("hook_event_name", "?")
        log.info("← %s  session=%s", hook_event, event.get("session_id", "?")[:8])

        payload = build_slack_payload(event)
        ok = send_to_slack(payload)
        log.info("→ Slack %s", "OK" if ok else "SKIP (no URL)" if not SLACK_WEBHOOK_URL else "FAIL")

        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'{"ok":true}')

    def do_GET(self):
        if self.path == "/health":
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'{"status":"ok"}')
        else:
            self.send_response(404)
            self.end_headers()


def main():
    if not SLACK_WEBHOOK_URL:
        log.warning("SLACK_WEBHOOK_URL not set — events will be received but NOT forwarded")

    server = HTTPServer(("localhost", PORT), WebhookHandler)
    log.info("Webhook proxy listening on http://localhost:%d/webhook", PORT)
    log.info("Press Ctrl+C to stop")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        log.info("Shutting down")
        server.server_close()


if __name__ == "__main__":
    main()
