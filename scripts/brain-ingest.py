#!/usr/bin/env python3
"""brain-ingest — local Python replacement for cloud agent scheduled task.

Processes URL and WATCH items from `.claude/memory/brain/inbox.md`:
- URL: fetch via Jina Reader → Claude summarize → save to brain/raw/
- WATCH: append to brain/watchlist.md
- Move processed items from Queue to Processed table
- Log to daily-reports.md, errors to alerts.md

Runs via Windows Task Scheduler. No CC permissions needed — direct file I/O.

Usage:
    python scripts/brain-ingest.py [--dry-run] [--limit N]
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from datetime import date, datetime
from pathlib import Path

import anthropic
import requests

# Add scripts/ to path so we can import lib.secrets
sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.keyring import get_secret  # noqa: E402

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")

PROJECT_ROOT = Path("C:/Users/stock/Documents/000_NGM/STOPA")
BRAIN_DIR = PROJECT_ROOT / ".claude/memory/brain"
INBOX = BRAIN_DIR / "inbox.md"
WATCHLIST = BRAIN_DIR / "watchlist.md"
RAW_DIR = BRAIN_DIR / "raw"
DAILY_REPORT = PROJECT_ROOT / ".claude/memory/daily-reports.md"
ALERTS = PROJECT_ROOT / ".claude/memory/alerts.md"
LOG_FILE = PROJECT_ROOT / ".claude/memory/brain-ingest.log"

JINA_PREFIX = "https://r.jina.ai/"
MODEL = "claude-sonnet-4-5-20250929"
MAX_CONTENT_CHARS = 15000

EXTRACT_PROMPT = """Extrahuj strukturované shrnutí článku (v češtině).

URL: {url}

Obsah:
{content}

Vrať JSON s přesně touto strukturou, bez markdown wrapperu:
{{
  "title": "Krátký popisný titul (max 80 znaků)",
  "key_idea": "1-2 věty jádra článku",
  "concepts": ["koncept1", "koncept2", "koncept3"],
  "entities": ["osoba/organizace1", "osoba/organizace2"],
  "claims": ["Tvrzení 1", "Tvrzení 2", "Tvrzení 3"],
  "relevance_for_stopa": "Proč je to relevantní pro STOPA orchestraci (1-2 věty)",
  "slug": "short-lowercase-slug-for-filename"
}}
"""


# ---------- I/O helpers ----------

def log_debug(msg: str) -> None:
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    LOG_FILE.open("a", encoding="utf-8").write(f"{ts} {msg}\n")


def read_inbox() -> tuple[list[dict], str]:
    text = INBOX.read_text(encoding="utf-8")
    m = re.search(r"## Queue\n(.*?)\n## Processed", text, re.DOTALL)
    if not m:
        return [], text
    queue_raw = m.group(1).strip()
    items = []
    for line in queue_raw.splitlines():
        line = line.strip()
        if line.startswith("URL:"):
            items.append({"type": "URL", "value": line[4:].strip()})
        elif line.startswith("WATCH:"):
            items.append({"type": "WATCH", "value": line[6:].strip()})
    return items, text


def fetch_url(url: str, timeout: int = 30) -> str | None:
    try:
        resp = requests.get(JINA_PREFIX + url, timeout=timeout)
        if resp.status_code == 200 and resp.text.strip():
            return resp.text
        log_debug(f"fetch_url: status={resp.status_code} url={url}")
    except Exception as e:
        log_debug(f"fetch_url: exception url={url} err={e}")
    return None


def extract_summary(client: anthropic.Anthropic, url: str, content: str) -> dict | None:
    content_trim = content[:MAX_CONTENT_CHARS]
    try:
        msg = client.messages.create(
            model=MODEL,
            max_tokens=1024,
            messages=[{"role": "user", "content": EXTRACT_PROMPT.format(url=url, content=content_trim)}],
        )
        txt = msg.content[0].text.strip()
        # Strip code fences if present
        txt = re.sub(r"^```(?:json)?\s*\n?", "", txt)
        txt = re.sub(r"\n?```\s*$", "", txt)
        return json.loads(txt)
    except json.JSONDecodeError as e:
        log_debug(f"extract_summary: JSON parse failed url={url} err={e}")
        return None
    except Exception as e:
        log_debug(f"extract_summary: API error url={url} err={e}")
        return None


def slugify(text: str, max_len: int = 40) -> str:
    slug = re.sub(r"[^a-z0-9-]+", "-", text.lower()).strip("-")
    return slug[:max_len] or "untitled"


def write_raw(summary: dict, url: str) -> Path:
    today = date.today().isoformat()
    slug = slugify(summary.get("slug") or summary.get("title", "untitled"))
    filename = RAW_DIR / f"{today}-{slug}.md"
    counter = 2
    while filename.exists():
        filename = RAW_DIR / f"{today}-{slug}-{counter}.md"
        counter += 1

    concepts_json = json.dumps(summary.get("concepts", []), ensure_ascii=False)
    entities_json = json.dumps(summary.get("entities", []), ensure_ascii=False)
    claims_md = "\n".join(f"- {c}" for c in summary.get("claims", [])) or "- (žádné)"

    content = f"""---
title: {summary.get('title', 'Untitled')}
url: {url}
date: {today}
concepts: {concepts_json}
entities: {entities_json}
source: brain-ingest-local
---

# {summary.get('title', 'Untitled')}

**URL**: {url}

## Key Idea

{summary.get('key_idea', 'N/A')}

## Claims

{claims_md}

## Relevance for STOPA

{summary.get('relevance_for_stopa', 'N/A')}
"""
    filename.write_text(content, encoding="utf-8")
    return filename


def append_watchlist(url: str) -> None:
    """Append to Manual Watches section (create if missing)."""
    today = date.today().isoformat()
    line = f"- {url}  (added {today})\n"
    text = WATCHLIST.read_text(encoding="utf-8") if WATCHLIST.exists() else "# Watchlist\n"
    # Append to end — user can reorganize manually
    if not text.endswith("\n"):
        text += "\n"
    text += line
    WATCHLIST.write_text(text, encoding="utf-8")


def update_inbox(items: list[dict], processed_summaries: dict[str, str]) -> None:
    """Remove processed items from Queue, append rows to Processed table."""
    text = INBOX.read_text(encoding="utf-8")
    queue_m = re.search(r"(## Queue\n)(.*?)(\n## Processed)", text, re.DOTALL)
    if not queue_m:
        return

    # Rebuild Queue section
    new_queue_lines = []
    processed_values = {v for v in processed_summaries.keys()}
    for line in queue_m.group(2).splitlines():
        stripped = line.strip()
        if stripped.startswith(("URL:", "WATCH:")):
            val = stripped.split(":", 1)[1].strip()
            if val in processed_values:
                continue
        new_queue_lines.append(line)

    new_queue_body = "\n".join(new_queue_lines).rstrip()
    new_queue_section = f"{queue_m.group(1)}{new_queue_body}" + ("\n" if new_queue_body else "")

    # Build new processed rows (one per processed item)
    today = date.today().isoformat()
    new_rows_parts = []
    for item in items:
        v = item["value"]
        if v in processed_summaries:
            new_rows_parts.append(f"| {today} | {item['type']}: {v} — {processed_summaries[v]} |")
    new_rows = "\n".join(new_rows_parts)

    # Replace Queue section
    new_text = text[:queue_m.start()] + new_queue_section + text[queue_m.end(3) - len(queue_m.group(3)):]

    # Insert rows under Processed table header
    table_m = re.search(r"(## Processed\n\n?\| Date \| Item \|\n\|------\|------\|\n)", new_text)
    if table_m and new_rows:
        insert_pos = table_m.end()
        new_text = new_text[:insert_pos] + new_rows + "\n" + new_text[insert_pos:]

    INBOX.write_text(new_text, encoding="utf-8")


def log_daily_report(processed_count: int, watch_count: int, errors: list[str]) -> None:
    ts = datetime.now().strftime("%Y-%m-%d %H:%M")
    status_parts = []
    if processed_count:
        status_parts.append(f"{processed_count} URLs")
    if watch_count:
        status_parts.append(f"{watch_count} watches")
    if errors:
        status_parts.append(f"{len(errors)} errors")
    status = ", ".join(status_parts) or "inbox empty"
    line = f"{ts} | brain-ingest | {status}\n"
    DAILY_REPORT.open("a", encoding="utf-8").write(line)


def log_alerts(errors: list[str]) -> None:
    if not errors:
        return
    ts = datetime.now().strftime("%Y-%m-%d %H:%M")
    entry = f"\n### {ts} | brain-ingest errors\n\n" + "\n".join(f"- {e}" for e in errors) + "\n"
    ALERTS.open("a", encoding="utf-8").write(entry)


# ---------- Main ----------

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true", help="parse inbox but don't call API or write")
    parser.add_argument("--limit", type=int, default=0, help="process at most N items (0 = no limit)")
    args = parser.parse_args()

    api_key = get_secret("ANTHROPIC_API_KEY")
    if not api_key and not args.dry_run:
        print("ERROR: ANTHROPIC_API_KEY not found (env or ~/.claude/keys/secrets.env)", file=sys.stderr)
        return 2

    items, _ = read_inbox()
    if not items:
        print("Inbox empty")
        log_daily_report(0, 0, [])
        return 0

    if args.limit > 0:
        items = items[:args.limit]

    print(f"Found {len(items)} items in inbox")

    if args.dry_run:
        for item in items:
            print(f"  [{item['type']}] {item['value']}")
        return 0

    client = anthropic.Anthropic(api_key=api_key)
    RAW_DIR.mkdir(parents=True, exist_ok=True)

    processed: dict[str, str] = {}
    url_count = 0
    watch_count = 0
    errors: list[str] = []

    for item in items:
        if item["type"] == "WATCH":
            try:
                append_watchlist(item["value"])
                processed[item["value"]] = "přidáno do watchlistu"
                watch_count += 1
                print(f"[WATCH] {item['value']}")
            except Exception as e:
                errors.append(f"WATCH {item['value']}: {e}")
            continue

        url = item["value"]
        print(f"[URL] {url}")
        content = fetch_url(url)
        if not content:
            errors.append(f"fetch failed: {url}")
            continue

        summary = extract_summary(client, url, content)
        if not summary:
            errors.append(f"summarize failed: {url}")
            continue

        try:
            raw_file = write_raw(summary, url)
            processed[url] = f"raw/{raw_file.name}"
            url_count += 1
            print(f"  → raw/{raw_file.name}")
        except Exception as e:
            errors.append(f"write failed: {url}: {e}")

    # Update inbox (move processed items to Processed table)
    if processed:
        update_inbox(items, processed)

    log_daily_report(url_count, watch_count, errors)
    log_alerts(errors)

    print(f"\n=== Done: {url_count} URLs, {watch_count} watches, {len(errors)} errors ===")
    return 0 if not errors else 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\nInterrupted", file=sys.stderr)
        sys.exit(130)
    except Exception as e:
        log_debug(f"FATAL: {e}")
        print(f"FATAL: {e}", file=sys.stderr)
        sys.exit(1)
