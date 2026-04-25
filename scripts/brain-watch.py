#!/usr/bin/env python3
"""brain-watch — local Python replacement for cloud agent scheduled task.

Scans 2BRAIN watchlist sources for new content and queues URLs into inbox.md.

Coverage (MVP):
  - arXiv topics: direct arXiv API (free, no rate limits)
  - Blogs & Personal Sites: Brave Search API (`site:URL after:date`)
  - Frequency-aware: skips sources scanned within their cadence

Not yet covered (TODO — require OAuth/scraping setup):
  - Gmail Labels & Senders → needs google-api-python-client + OAuth flow
  - X/Twitter handles → no public search API, scraping fragile

Output:
  - New URLs appended to `.claude/memory/brain/inbox.md` Queue section
  - Scan dates in watchlist.md updated
  - Summary line in daily-reports.md
  - Errors in alerts.md

Runs via Windows Task Scheduler daily. No CC permissions needed.

Usage:
    python scripts/brain-watch.py [--dry-run] [--source arxiv|blogs|all]
"""
from __future__ import annotations

import argparse
import re
import sys
import time
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from xml.etree import ElementTree as ET

import requests

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.keyring import get_secret  # noqa: E402

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")

PROJECT_ROOT = Path("C:/Users/stock/Documents/000_NGM/STOPA")
BRAIN_DIR = PROJECT_ROOT / ".claude/memory/brain"
INBOX = BRAIN_DIR / "inbox.md"
WATCHLIST = BRAIN_DIR / "watchlist.md"
DAILY_REPORT = PROJECT_ROOT / ".claude/memory/daily-reports.md"
ALERTS = PROJECT_ROOT / ".claude/memory/alerts.md"
LOG_FILE = PROJECT_ROOT / ".claude/memory/brain-watch.log"

ARXIV_API = "http://export.arxiv.org/api/query"
BRAVE_API = "https://api.search.brave.com/res/v1/web/search"

FREQUENCY_DAYS = {"daily": 1, "weekly": 7, "monthly": 30}
ARXIV_MAX_PER_QUERY = 3
BLOG_MAX_PER_SITE = 3
ARXIV_LOOKBACK_DAYS = 7
BLOG_LOOKBACK_DAYS = 7


# ---------- Logging ----------

def log_debug(msg: str) -> None:
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    LOG_FILE.open("a", encoding="utf-8").write(f"{ts} {msg}\n")


# ---------- Watchlist parsing ----------

def _parse_table(section_text: str) -> list[dict]:
    """Parse markdown table into list of dicts with column→value mapping."""
    rows = []
    lines = [line.strip() for line in section_text.splitlines() if line.strip().startswith("|")]
    if len(lines) < 2:
        return rows
    headers = [h.strip() for h in lines[0].strip("|").split("|")]
    # lines[1] is the divider --- ; data starts at lines[2]
    for line in lines[2:]:
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) != len(headers):
            continue
        rows.append(dict(zip(headers, cells)))
    return rows


def parse_watchlist() -> dict:
    """Parse watchlist.md into structured dict by section name."""
    text = WATCHLIST.read_text(encoding="utf-8")
    sections = {}
    section_pattern = re.compile(r"^## (.+?)$", re.MULTILINE)
    matches = list(section_pattern.finditer(text))
    for i, m in enumerate(matches):
        name = m.group(1).strip()
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        sections[name] = _parse_table(text[start:end])
    return sections


def days_since(scan_date_str: str) -> int:
    """Days between today and given YYYY-MM-DD scan date (large number if invalid)."""
    try:
        scanned = datetime.strptime(scan_date_str.strip(), "%Y-%m-%d").date()
        return (date.today() - scanned).days
    except ValueError:
        return 999


# ---------- arXiv ----------

def search_arxiv(query: str, max_results: int = 3) -> list[dict]:
    """Query arXiv API. Returns list of {url, title, summary}."""
    params = {
        "search_query": f"all:{query}",
        "sortBy": "submittedDate",
        "sortOrder": "descending",
        "max_results": max_results,
    }
    try:
        resp = requests.get(ARXIV_API, params=params, timeout=15)
        resp.raise_for_status()
    except Exception as e:
        log_debug(f"arxiv: query={query!r} err={e}")
        return []

    # Parse Atom XML
    ns = {"atom": "http://www.w3.org/2005/Atom"}
    try:
        root = ET.fromstring(resp.content)
    except ET.ParseError as e:
        log_debug(f"arxiv: parse err={e}")
        return []

    cutoff = datetime.now(timezone.utc).replace(tzinfo=None) - timedelta(days=ARXIV_LOOKBACK_DAYS)
    results = []
    for entry in root.findall("atom:entry", ns):
        link = entry.find("atom:id", ns)
        title = entry.find("atom:title", ns)
        published = entry.find("atom:published", ns)
        if link is None or published is None:
            continue
        try:
            pub_dt = datetime.strptime(published.text[:10], "%Y-%m-%d")
        except ValueError:
            continue
        if pub_dt < cutoff:
            continue
        results.append({
            "url": link.text.strip(),
            "title": (title.text or "").strip().replace("\n", " "),
        })
    return results


# ---------- Brave Search ----------

def search_brave(query: str, count: int = 5) -> list[dict]:
    """Brave Search API. Returns list of {url, title}."""
    api_key = get_secret("BRAVE_API_KEY")
    if not api_key:
        log_debug("brave: no API key")
        return []
    headers = {
        "X-Subscription-Token": api_key,
        "Accept": "application/json",
    }
    params = {"q": query, "count": count}
    try:
        resp = requests.get(BRAVE_API, headers=headers, params=params, timeout=15)
        if resp.status_code == 429:
            log_debug("brave: rate limited")
            time.sleep(2)
            return []
        resp.raise_for_status()
    except Exception as e:
        log_debug(f"brave: query={query!r} err={e}")
        return []

    data = resp.json()
    results = []
    for r in (data.get("web", {}).get("results") or []):
        url = r.get("url")
        if url:
            results.append({"url": url, "title": r.get("title", "")})
    return results


# ---------- Scanning ----------

def scan_arxiv_topics(topics: list[dict]) -> tuple[list[str], list[dict]]:
    """Scan all arXiv queries. Returns (new_urls, scanned_topics_for_date_update)."""
    new_urls = []
    scanned = []
    for topic in topics:
        query = topic.get("Query")
        if not query:
            continue
        last_scan = topic.get("Poslední scan", "")
        if days_since(last_scan) < 1:  # arXiv: daily
            continue
        results = search_arxiv(query, ARXIV_MAX_PER_QUERY)
        for r in results:
            new_urls.append(r["url"])
        scanned.append(topic)
        time.sleep(0.5)  # be polite to arXiv
    return new_urls, scanned


def scan_blogs(blogs: list[dict]) -> tuple[list[str], list[dict]]:
    """Scan blogs via Brave 'site:URL'. Frequency-aware."""
    new_urls = []
    scanned = []
    yesterday = (date.today() - timedelta(days=BLOG_LOOKBACK_DAYS)).isoformat()
    for blog in blogs:
        url = blog.get("URL", "").strip()
        freq = blog.get("Frekvence", "weekly").strip()
        last_scan = blog.get("Poslední scan", "")
        cadence = FREQUENCY_DAYS.get(freq, 7)
        if days_since(last_scan) < cadence:
            continue
        # Strip protocol for site: query
        site_host = re.sub(r"^https?://", "", url).rstrip("/")
        results = search_brave(f"site:{site_host} after:{yesterday}", count=BLOG_MAX_PER_SITE)
        for r in results:
            # Filter: must be from same host (Brave sometimes returns adjacent sites)
            if site_host in r["url"]:
                new_urls.append(r["url"])
        scanned.append(blog)
        time.sleep(0.5)  # rate limit
    return new_urls, scanned


# ---------- Inbox update ----------

def existing_inbox_urls() -> set[str]:
    """Get all URLs already in inbox (Queue + Processed) to avoid duplicates."""
    if not INBOX.exists():
        return set()
    text = INBOX.read_text(encoding="utf-8")
    urls = set()
    # Queue items
    for m in re.finditer(r"^URL:\s*(\S+)", text, re.MULTILINE):
        urls.add(m.group(1).strip())
    # Processed table rows containing URL: prefix
    for m in re.finditer(r"URL:\s*(\S+)", text):
        urls.add(m.group(1).strip())
    return urls


def add_to_inbox(urls: list[str]) -> int:
    """Add new URLs to Queue section. Returns count actually added (deduplicated)."""
    if not urls:
        return 0
    existing = existing_inbox_urls()
    new = [u for u in urls if u not in existing]
    if not new:
        return 0

    text = INBOX.read_text(encoding="utf-8")
    queue_m = re.search(r"(## Queue\n)(.*?)(\n## Processed)", text, re.DOTALL)
    if not queue_m:
        log_debug("add_to_inbox: Queue section not found")
        return 0

    existing_queue = queue_m.group(2).rstrip()
    additions = "\n".join(f"URL: {u}" for u in new)
    if existing_queue:
        new_queue = existing_queue + "\n" + additions
    else:
        new_queue = additions
    new_section = f"{queue_m.group(1)}\n{new_queue}\n"

    new_text = text[:queue_m.start()] + new_section + text[queue_m.end(3) - len(queue_m.group(3)):]
    INBOX.write_text(new_text, encoding="utf-8")
    return len(new)


# ---------- Watchlist scan-date update ----------

def update_scan_dates(section_name: str, scanned_rows: list[dict], key_col: str) -> None:
    """Update 'Poslední scan' column in watchlist.md for scanned rows."""
    if not scanned_rows:
        return
    today = date.today().isoformat()
    text = WATCHLIST.read_text(encoding="utf-8")

    section_pattern = re.compile(rf"(## {re.escape(section_name)}.*?)(?=\n## |\Z)", re.DOTALL)
    sec_m = section_pattern.search(text)
    if not sec_m:
        return
    section_text = sec_m.group(1)

    new_section = section_text
    for row in scanned_rows:
        key_val = row.get(key_col, "").strip()
        if not key_val:
            continue
        # Match the entire row line, replace last cell (scan date)
        # Pattern: line starting with `| <key_val>` to end of line
        # Replace everything between last `|` separators (the date cell)
        escaped_key = re.escape(key_val)
        row_pattern = re.compile(rf"(^\|\s*{escaped_key}\s*\|.*?\|)\s*[\d-]+\s*(\|)$", re.MULTILINE)
        new_section = row_pattern.sub(rf"\1 {today} \2", new_section)

    new_text = text[:sec_m.start()] + new_section + text[sec_m.end():]
    WATCHLIST.write_text(new_text, encoding="utf-8")


# ---------- Reporting ----------

def log_daily_report(stats: dict, errors: list[str]) -> None:
    ts = datetime.now().strftime("%Y-%m-%d %H:%M")
    parts = []
    for k, v in stats.items():
        if v:
            parts.append(f"{k}: {v}")
    if errors:
        parts.append(f"{len(errors)} errors")
    summary = ", ".join(parts) or "silent skip"
    line = f"{ts} | brain-watch | {summary}\n"
    DAILY_REPORT.open("a", encoding="utf-8").write(line)


def log_alerts(errors: list[str]) -> None:
    if not errors:
        return
    ts = datetime.now().strftime("%Y-%m-%d %H:%M")
    entry = f"\n### {ts} | brain-watch errors\n\n" + "\n".join(f"- {e}" for e in errors) + "\n"
    ALERTS.open("a", encoding="utf-8").write(entry)


# ---------- Main ----------

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--source", choices=["arxiv", "blogs", "all"], default="all")
    args = parser.parse_args()

    sections = parse_watchlist()

    arxiv_topics = sections.get("arXiv Topics", [])
    blogs = sections.get("Blogs & Personal Sites", [])

    print(f"Loaded watchlist: {len(arxiv_topics)} arXiv topics, {len(blogs)} blogs")

    new_urls = []
    stats = {"arxiv": 0, "blogs": 0}
    errors = []

    if args.source in ("arxiv", "all"):
        try:
            urls, scanned = scan_arxiv_topics(arxiv_topics)
            new_urls.extend(urls)
            stats["arxiv"] = len(urls)
            print(f"arXiv: {len(urls)} new URLs from {len(scanned)} topics scanned")
            if not args.dry_run:
                update_scan_dates("arXiv Topics", scanned, "Query")
        except Exception as e:
            errors.append(f"arxiv scan: {e}")
            log_debug(f"arxiv scan: {e}")

    if args.source in ("blogs", "all"):
        try:
            urls, scanned = scan_blogs(blogs)
            new_urls.extend(urls)
            stats["blogs"] = len(urls)
            print(f"Blogs: {len(urls)} new URLs from {len(scanned)} blogs scanned")
            if not args.dry_run:
                update_scan_dates("Blogs & Personal Sites", scanned, "URL")
        except Exception as e:
            errors.append(f"blogs scan: {e}")
            log_debug(f"blogs scan: {e}")

    if args.dry_run:
        print(f"\n=== DRY RUN: would add {len(new_urls)} URLs ===")
        for u in new_urls[:20]:
            print(f"  {u}")
        if len(new_urls) > 20:
            print(f"  ... and {len(new_urls) - 20} more")
        return 0

    added = add_to_inbox(new_urls) if new_urls else 0
    stats["queued"] = added

    log_daily_report(stats, errors)
    log_alerts(errors)

    print(f"\n=== Done: {added} URLs queued, {len(errors)} errors ===")
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
