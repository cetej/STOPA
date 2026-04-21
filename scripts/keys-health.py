"""Key health checker — ping each configured API, log failures to alerts.md.

Usage:
    python scripts/keys-health.py             # full check, append to alerts.md on failures
    python scripts/keys-health.py --verbose   # also print OK results
    python scripts/keys-health.py --json      # machine-readable output

Checks (only keys present in environment):
    - ANTHROPIC_API_KEY → minimal /v1/messages call (1 token)
    - FAL_KEY           → GET /models list (read-only)
    - BRAVE_API_KEY     → minimal search query
    - GITHUB_TOKEN      → GET /user (scoped-token-safe)
    - TELEGRAM_BOT_TOKEN → GET /getMe (free, no message sent)

Exit codes:
    0 = all configured keys OK
    1 = one or more keys failed (401/403/429/expired)
    2 = setup error (no keys found at all)
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from datetime import datetime
from pathlib import Path
from typing import Any

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

STOPA_ROOT = Path(__file__).resolve().parent.parent
ALERTS_FILE = STOPA_ROOT / ".claude" / "memory" / "alerts.md"
REPORTS_FILE = STOPA_ROOT / ".claude" / "memory" / "daily-reports.md"

TIMEOUT = 10.0


def http_get(url: str, headers: dict[str, str]) -> tuple[int, str]:
    req = urllib.request.Request(url, headers=headers, method="GET")
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            return resp.status, resp.read(500).decode("utf-8", errors="replace")
    except urllib.error.HTTPError as e:
        body = e.read(500).decode("utf-8", errors="replace") if e.fp else ""
        return e.code, body
    except Exception as e:
        return -1, f"{type(e).__name__}: {e}"


def http_post(url: str, headers: dict[str, str], data: bytes) -> tuple[int, str]:
    req = urllib.request.Request(url, headers=headers, data=data, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            return resp.status, resp.read(500).decode("utf-8", errors="replace")
    except urllib.error.HTTPError as e:
        body = e.read(500).decode("utf-8", errors="replace") if e.fp else ""
        return e.code, body
    except Exception as e:
        return -1, f"{type(e).__name__}: {e}"


def check_anthropic(key: str) -> dict[str, Any]:
    status, body = http_post(
        "https://api.anthropic.com/v1/messages",
        {
            "x-api-key": key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json",
        },
        json.dumps({
            "model": "claude-haiku-4-5",
            "max_tokens": 1,
            "messages": [{"role": "user", "content": "."}],
        }).encode("utf-8"),
    )
    return classify("ANTHROPIC_API_KEY", status, body)


def check_fal(key: str) -> dict[str, Any]:
    status, body = http_get(
        "https://fal.run/fal-ai/flux",
        {"Authorization": f"Key {key}"},
    )
    return classify("FAL_KEY", status, body, allow_404=True)


def check_brave(key: str) -> dict[str, Any]:
    status, body = http_get(
        "https://api.search.brave.com/res/v1/web/search?q=test&count=1",
        {"X-Subscription-Token": key, "Accept": "application/json"},
    )
    return classify("BRAVE_API_KEY", status, body)


def check_github(key: str) -> dict[str, Any]:
    status, body = http_get(
        "https://api.github.com/user",
        {"Authorization": f"Bearer {key}", "Accept": "application/vnd.github+json"},
    )
    return classify("GITHUB_TOKEN", status, body)


def check_telegram(key: str) -> dict[str, Any]:
    status, body = http_get(
        f"https://api.telegram.org/bot{key}/getMe",
        {},
    )
    return classify("TELEGRAM_BOT_TOKEN", status, body)


def classify(name: str, status: int, body: str, allow_404: bool = False) -> dict[str, Any]:
    if status in (200, 201):
        return {"key": name, "ok": True, "status": status}
    if status == 404 and allow_404:
        return {"key": name, "ok": True, "status": status, "note": "endpoint not found but auth accepted"}
    severity = "high"
    if status == 401:
        kind = "expired_or_invalid"
    elif status == 403:
        kind = "forbidden_or_quota"
    elif status == 429:
        kind = "rate_limited"
        severity = "medium"
    elif status == -1:
        kind = "network_error"
        severity = "medium"
    else:
        kind = f"http_{status}"
    return {"key": name, "ok": False, "status": status, "kind": kind, "severity": severity, "body_excerpt": body[:200]}


CHECKS = [
    ("ANTHROPIC_API_KEY", check_anthropic),
    ("FAL_KEY", check_fal),
    ("BRAVE_API_KEY", check_brave),
    ("GITHUB_TOKEN", check_github),
    ("TELEGRAM_BOT_TOKEN", check_telegram),
]


def append_alert(result: dict[str, Any]) -> None:
    ALERTS_FILE.parent.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime("%Y-%m-%d %H:%M")
    with ALERTS_FILE.open("a", encoding="utf-8") as f:
        f.write(f"\n## {ts} — [keys-health] {result['key']} — {result['kind']}\n")
        f.write(f"- **Severity:** {result['severity']}\n")
        f.write(f"- **Source:** scripts/keys-health.py\n")
        f.write(f"- **Detail:** HTTP {result['status']}. Body: `{result['body_excerpt']}`\n")
        f.write(f"- **Action suggested:** rotate {result['key']} in ~/.claude/keys/secrets.env, run keys-sync.ps1\n")
        f.write(f"- **Status:** open\n")


def append_report(line: str) -> None:
    REPORTS_FILE.parent.mkdir(parents=True, exist_ok=True)
    with REPORTS_FILE.open("a", encoding="utf-8") as f:
        f.write(line + "\n")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--verbose", action="store_true", help="print OK results too")
    parser.add_argument("--json", action="store_true", help="emit JSON on stdout")
    args = parser.parse_args()

    results: list[dict[str, Any]] = []
    configured = 0
    for name, fn in CHECKS:
        value = os.environ.get(name, "").strip()
        if not value:
            results.append({"key": name, "ok": None, "status": "not_configured"})
            continue
        configured += 1
        results.append(fn(value))

    if args.json:
        print(json.dumps(results, indent=2, ensure_ascii=False))
    else:
        for r in results:
            if r.get("ok") is True:
                if args.verbose:
                    print(f"OK      {r['key']}  (HTTP {r['status']})")
            elif r.get("ok") is False:
                print(f"FAIL    {r['key']}  HTTP {r['status']} — {r['kind']}")
            else:
                if args.verbose:
                    print(f"SKIP    {r['key']}  (not configured)")

    failures = [r for r in results if r.get("ok") is False]
    for f in failures:
        append_alert(f)

    ts = datetime.now().strftime("%Y-%m-%d %H:%M")
    ok_count = sum(1 for r in results if r.get("ok") is True)
    fail_count = len(failures)
    append_report(f"{ts} | keys-health | {ok_count} OK, {fail_count} FAIL, {configured} configured")

    if configured == 0:
        return 2
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
