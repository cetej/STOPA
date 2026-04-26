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
RADAR_FILE = PROJECT_ROOT / ".claude/memory/radar.md"
RADAR_PROPOSALS = PROJECT_ROOT / ".claude/memory/radar-proposals.md"
NEWS_PROPOSALS = PROJECT_ROOT / ".claude/memory/news-proposals.md"

JINA_PREFIX = "https://r.jina.ai/"
MODEL = "claude-sonnet-4-5-20250929"
MAX_CONTENT_CHARS = 15000

# Action classes that trigger bridge to STOPA action memory.
# Issue #24 G7: brain-watch findings need a controlled path into radar.md/news.md
# without silent drift. Classes that map to radar (tool evaluation):
RADAR_ACTION_CLASSES = {"tool", "library", "mcp-server", "cli"}
# Classes that map to news (research signal, not a tool):
NEWS_ACTION_CLASSES = {"paper"}
# Anything else ("none", "blog-post", "thread", ...): archive only, no bridge.

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
  "slug": "short-lowercase-slug-for-filename",
  "action_class": "tool|library|mcp-server|cli|paper|none",
  "tool_name": "Pokud action_class != none, jméno toolu/library/paperu (např. 'context-mode', 'TACO'). Jinak null.",
  "primary_url": "Kanonická URL toolu/repa/paperu pokud existuje (GitHub URL pro tool, arXiv abs URL pro paper). Jinak {url}."
}}

Pravidla pro action_class:
- "tool" — interaktivní software (CLI app, desktop app, web app pro vývojáře)
- "library" — Python/JS/TS package, framework, knihovna k importu
- "mcp-server" — server implementující MCP protokol (Model Context Protocol)
- "cli" — command-line tool (často podmnožina "tool", používej "cli" když je primárně CLI)
- "paper" — výzkumný paper (arXiv, OpenReview, conference proceedings)
- "none" — blog post, thread, novinka, opinion, dokumentace existujícího toolu, anything else

Pokud článek POUZE zmiňuje tool jako side reference (ale primárně je o něčem jiném), vrať action_class="none".
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


# ---------- Brain → STOPA bridge (issue #24, G7) ----------

def canonicalize_url(url: str) -> str:
    """Normalize URL for dedup comparison.

    Strips trailing slash, lowercases scheme+host, removes www., ignores fragment.
    Keeps query string (e.g., arxiv abs URLs stay distinguishable).
    """
    if not url:
        return ""
    url = url.strip()
    # Remove fragment
    url = url.split("#", 1)[0]
    # Lowercase scheme+host portion
    m = re.match(r"^(https?://)([^/]+)(/.*)?$", url, re.IGNORECASE)
    if not m:
        return url.lower().rstrip("/")
    scheme, host, path = m.group(1).lower(), m.group(2).lower(), (m.group(3) or "")
    if host.startswith("www."):
        host = host[4:]
    path = path.rstrip("/")
    return f"{scheme}{host}{path}"


def is_already_known(tool_name: str, url: str) -> tuple[bool, str]:
    """Check if a tool/url is already tracked in radar.md or any *-proposals.md.

    Returns (is_known, reason). Reason is empty if not known.
    """
    canon = canonicalize_url(url)
    name_lower = (tool_name or "").strip().lower()

    targets = [RADAR_FILE, RADAR_PROPOSALS, NEWS_PROPOSALS]
    for target in targets:
        if not target.exists():
            continue
        try:
            text = target.read_text(encoding="utf-8")
        except Exception:
            continue
        text_lower = text.lower()

        # URL match (canonical form, but also check raw URL substring as fallback)
        if canon and canon in text_lower:
            return True, f"URL already in {target.name}"
        if url and url.lower() in text_lower:
            return True, f"URL already in {target.name}"

        # Name match — only if name is reasonably specific (>=4 chars, not generic)
        if name_lower and len(name_lower) >= 4:
            # Match `[name](` (markdown link) or `| name |` (table cell) or `**name**`
            patterns = [
                f"[{name_lower}](",
                f"| {name_lower} |",
                f"**{name_lower}**",
                f"`{name_lower}`",
            ]
            if any(p in text_lower for p in patterns):
                return True, f"Name already in {target.name}"
    return False, ""


PROPOSAL_HEADER = """# Radar Proposals — Brain-sourced findings awaiting review

Items here came from `brain-ingest` LLM classification (action_class ∈ {tool, library, mcp-server, cli}).
They are NOT yet in radar.md. Reviewed during `/radar` runs — user accepts/rejects per row.

**Audit invariants (issue #24):**
- Every entry has `source: brain-watch` (or equivalent ingest pipeline)
- Dedup checked against radar.md + this file before append
- Hook never writes to brain/* — no recursion possible

| Date | Tool | Action class | URL | Source | Key idea | Status |
|------|------|--------------|-----|--------|----------|--------|

## Resolved

| Date resolved | Tool | Decision | Notes |
|---------------|------|----------|-------|
"""

NEWS_PROPOSAL_HEADER = """# News Proposals — Brain-sourced papers awaiting review

Items here came from `brain-ingest` LLM classification (action_class = paper).
Reviewed during `/watch` runs — user accepts/rejects per row.

| Date | Title | URL | Source | Key idea | Status |
|------|-------|-----|--------|----------|--------|

## Resolved

| Date resolved | Title | Decision | Notes |
|---------------|-------|----------|-------|
"""


def _ensure_proposal_file(path: Path, header: str) -> None:
    if not path.exists():
        path.write_text(header, encoding="utf-8")


def propose_to_radar(action_class: str, tool_name: str, url: str, summary: dict) -> str:
    """Append a brain-sourced finding to radar-proposals.md or news-proposals.md.

    Returns one of: "proposed", "deduplicated", "skipped" (no action_class match).
    Never raises — bridge failures must not break ingest.
    """
    try:
        if action_class in RADAR_ACTION_CLASSES:
            target = RADAR_PROPOSALS
            header = PROPOSAL_HEADER
            row_kind = "radar"
        elif action_class in NEWS_ACTION_CLASSES:
            target = NEWS_PROPOSALS
            header = NEWS_PROPOSAL_HEADER
            row_kind = "news"
        else:
            return "skipped"

        if not tool_name or not tool_name.strip():
            return "skipped"

        # Use primary_url from summary if provided, else the original URL
        primary_url = summary.get("primary_url") or url

        known, reason = is_already_known(tool_name, primary_url)
        if known:
            log_debug(f"bridge: dedup skip tool={tool_name!r} reason={reason}")
            return "deduplicated"

        _ensure_proposal_file(target, header)

        today = date.today().isoformat()
        # Sanitize cells (strip newlines, escape pipes)
        def _cell(s: str) -> str:
            return (s or "").replace("\n", " ").replace("|", "\\|").strip()

        title = summary.get("title", tool_name)
        key_idea = summary.get("key_idea", "")

        if row_kind == "radar":
            row = (
                f"| {today} | [{_cell(tool_name)}]({primary_url}) | {action_class} "
                f"| {primary_url} | brain-watch | {_cell(key_idea)[:200]} | pending |\n"
            )
        else:
            row = (
                f"| {today} | [{_cell(title)}]({primary_url}) | {primary_url} "
                f"| brain-watch | {_cell(key_idea)[:200]} | pending |\n"
            )

        # Insert under the active table (between the table header and `## Resolved`)
        text = target.read_text(encoding="utf-8")
        resolved_idx = text.find("## Resolved")
        if resolved_idx == -1:
            # Defensive: append at end with separator
            text = text.rstrip() + "\n" + row + "\n"
        else:
            text = text[:resolved_idx].rstrip() + "\n" + row + "\n\n" + text[resolved_idx:]

        target.write_text(text, encoding="utf-8")
        log_debug(f"bridge: proposed {row_kind} tool={tool_name!r} class={action_class}")
        return "proposed"
    except Exception as e:
        log_debug(f"bridge: error tool={tool_name!r}: {e}")
        return "skipped"


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


def log_daily_report(
    processed_count: int,
    watch_count: int,
    errors: list[str],
    proposed_count: int = 0,
    dedup_count: int = 0,
) -> None:
    ts = datetime.now().strftime("%Y-%m-%d %H:%M")
    status_parts = []
    if processed_count:
        status_parts.append(f"{processed_count} URLs")
    if watch_count:
        status_parts.append(f"{watch_count} watches")
    if proposed_count:
        status_parts.append(f"{proposed_count} radar/news proposals")
    if dedup_count:
        status_parts.append(f"{dedup_count} dedup")
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
    proposed_count = 0
    dedup_count = 0
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
            note = f"raw/{raw_file.name}"
            url_count += 1

            # Bridge to STOPA action memory (issue #24, G7)
            action_class = (summary.get("action_class") or "none").strip().lower()
            tool_name = (summary.get("tool_name") or "").strip()
            if action_class != "none" and tool_name:
                bridge_result = propose_to_radar(action_class, tool_name, url, summary)
                if bridge_result == "proposed":
                    proposed_count += 1
                    note += f" → proposed ({action_class})"
                elif bridge_result == "deduplicated":
                    dedup_count += 1
                    note += " → dedup"

            processed[url] = note
            print(f"  → {note}")
        except Exception as e:
            errors.append(f"write failed: {url}: {e}")

    # Update inbox (move processed items to Processed table)
    if processed:
        update_inbox(items, processed)

    log_daily_report(url_count, watch_count, errors, proposed_count, dedup_count)
    log_alerts(errors)

    print(
        f"\n=== Done: {url_count} URLs, {watch_count} watches, "
        f"{proposed_count} proposals, {dedup_count} dedup, {len(errors)} errors ==="
    )
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
