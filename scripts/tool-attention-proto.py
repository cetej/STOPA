#!/usr/bin/env python3
"""Tool Attention Prototype — ISO scoring for STOPA tool catalog.

Demonstrates Intent-Schema Overlap (ISO) scoring from arXiv:2604.21816
"Tool Attention Is All You Need" (Sadani & Kumar, 2026).

Reduces tool schema tokens per turn by filtering irrelevant tools via
TF-IDF cosine similarity between user query and tool descriptions.

Usage:
    python scripts/tool-attention-proto.py                          # demo: 8 sample queries
    python scripts/tool-attention-proto.py "search github issues"   # single query
    python scripts/tool-attention-proto.py --top-k 8 "read file"   # adjust top-k
    python scripts/tool-attention-proto.py --verbose                # show all scores

Issue: cetej/STOPA#25
Paper: https://arxiv.org/abs/2604.21816
"""
import argparse
import math
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# ─────────────────────────────────────────────────────────────────────────────
# STOPA Tool Catalog — representative tools with token cost estimates
# Token costs: name(~5) + description(~50-80) + parameter schema(~30-80)
# Source: CC docs, MCP server READMEs, deferred tool list
# ─────────────────────────────────────────────────────────────────────────────
TOOLS: list[dict] = [
    # ── CC built-in ──────────────────────────────────────────────────────────
    {"name": "Read",        "server": "cc",   "tokens": 70,  "desc": "Read file content from filesystem. Source code config logs memory files. Offset limit for large files. Returns line-numbered content."},
    {"name": "Edit",        "server": "cc",   "tokens": 90,  "desc": "Edit file by replacing exact text. Code changes config updates bug fixes. Requires reading file first. Supports replace_all."},
    {"name": "Write",       "server": "cc",   "tokens": 80,  "desc": "Write complete file content. Create new files or full rewrites. Not for modifying existing files use Edit."},
    {"name": "Glob",        "server": "cc",   "tokens": 70,  "desc": "Find files by glob pattern. Discover files by name extension. Sorted by modification time. Recursive patterns supported."},
    {"name": "Grep",        "server": "cc",   "tokens": 80,  "desc": "Search file content with regex. Find code symbols strings patterns functions. Context lines file type filters case-insensitive."},
    {"name": "Bash",        "server": "cc",   "tokens": 100, "desc": "Execute shell commands. Git operations running tests Python scripts file operations. Background execution timeout."},
    {"name": "Agent",       "server": "cc",   "tokens": 150, "desc": "Spawn sub-agents for parallel or complex tasks. Multi-file changes research validation. Explore Plan koder validator types. Background mode."},
    {"name": "WebFetch",    "server": "cc",   "tokens": 90,  "desc": "Fetch and analyze web page content. Read documentation extract information from URLs. HTML to markdown conversion."},
    {"name": "WebSearch",   "server": "cc",   "tokens": 80,  "desc": "Search the web for information. Current documentation tools papers news. Search result snippets with URLs."},
    {"name": "ToolSearch",  "server": "cc",   "tokens": 60,  "desc": "Find and load deferred tool schemas by keyword. Required before calling deferred tools. Direct lookup or fuzzy search."},
    {"name": "TodoWrite",   "server": "cc",   "tokens": 80,  "desc": "Manage task list for current session. Track progress on multi-step work. Create update complete delete operations."},
    {"name": "Skill",       "server": "cc",   "tokens": 70,  "desc": "Invoke skill from skills library. Run named workflow slash command. Execute specialized capability."},

    # ── brave-search ─────────────────────────────────────────────────────────
    {"name": "brave_web_search",   "server": "brave",  "tokens": 120, "desc": "Search the web using Brave Search. Ranked results titles URLs descriptions. Current events documentation tool discovery news."},
    {"name": "brave_local_search", "server": "brave",  "tokens": 110, "desc": "Search local businesses places services. Locations hours ratings. Geographic queries."},

    # ── filesystem ───────────────────────────────────────────────────────────
    {"name": "fs_list_directory",   "server": "fs",    "tokens": 100, "desc": "List directory contents. Files and subdirectories with metadata. Explore project structure find files check directory."},
    {"name": "fs_read_file",        "server": "fs",    "tokens": 100, "desc": "Read text file content via filesystem MCP. Alternative to built-in Read. Files outside project root."},
    {"name": "fs_write_file",       "server": "fs",    "tokens": 100, "desc": "Write file content via filesystem MCP. Creates or overwrites files UTF-8 encoding."},
    {"name": "fs_create_directory", "server": "fs",    "tokens": 90,  "desc": "Create directory and parent directories. Project scaffolding output directories organizing files."},
    {"name": "fs_search_files",     "server": "fs",    "tokens": 110, "desc": "Search files by name pattern in filesystem. Matching paths across large directory trees."},
    {"name": "fs_move_file",        "server": "fs",    "tokens": 90,  "desc": "Move or rename file. File reorganization archiving renaming."},
    {"name": "fs_get_file_info",    "server": "fs",    "tokens": 90,  "desc": "Get file metadata size permissions modification time. Check file existence size limits timestamps."},
    {"name": "fs_directory_tree",   "server": "fs",    "tokens": 100, "desc": "Get recursive directory tree structure. Nested file folder hierarchy. Project layout documentation."},

    # ── github ───────────────────────────────────────────────────────────────
    {"name": "gh_get_file",           "server": "github", "tokens": 130, "desc": "Get file or directory contents from GitHub repository. Source code config documentation. Refs branches supported."},
    {"name": "gh_list_issues",        "server": "github", "tokens": 130, "desc": "List GitHub issues for repository. Filter by state labels assignee. Task management bug tracking improvement routing."},
    {"name": "gh_get_issue",          "server": "github", "tokens": 120, "desc": "Get GitHub issue details body comments labels. Read issue context before implementing fixes."},
    {"name": "gh_create_issue",       "server": "github", "tokens": 130, "desc": "Create new GitHub issue with title body labels assignees. Improvement routing bug reporting feature requests."},
    {"name": "gh_add_issue_comment",  "server": "github", "tokens": 120, "desc": "Add comment to GitHub issue. Updates progress reports closing notes."},
    {"name": "gh_update_issue",       "server": "github", "tokens": 120, "desc": "Update GitHub issue state title body labels assignees. Close issues change labels reassign."},
    {"name": "gh_create_pr",          "server": "github", "tokens": 140, "desc": "Create GitHub pull request. Code review workflows submitting changes. Title body head base branch."},
    {"name": "gh_list_prs",           "server": "github", "tokens": 130, "desc": "List open pull requests. Filter by state head base branch. CI status review state."},
    {"name": "gh_get_pr",             "server": "github", "tokens": 130, "desc": "Get pull request details diff reviews status checks. Review code changes."},
    {"name": "gh_push_files",         "server": "github", "tokens": 150, "desc": "Push multiple files to GitHub repository in single commit. Batch file updates syncing content to remote."},
    {"name": "gh_search_code",        "server": "github", "tokens": 130, "desc": "Search code across GitHub repositories. Find similar implementations check patterns usage examples."},
    {"name": "gh_search_issues",      "server": "github", "tokens": 130, "desc": "Search GitHub issues across repositories. Find related bugs duplicates existing work."},
    {"name": "gh_list_commits",       "server": "github", "tokens": 120, "desc": "List commits for repository or file. Git history blame changelog generation."},
    {"name": "gh_create_branch",      "server": "github", "tokens": 110, "desc": "Create new git branch in GitHub repository. Before making changes for PR workflow."},
    {"name": "gh_merge_pr",           "server": "github", "tokens": 130, "desc": "Merge pull request. Merge squash rebase strategies. CI checks required."},

    # ── playwright ───────────────────────────────────────────────────────────
    {"name": "pw_navigate",    "server": "playwright", "tokens": 110, "desc": "Navigate browser to URL. Web automation testing scraping dynamic pages JavaScript execution."},
    {"name": "pw_click",       "server": "playwright", "tokens": 100, "desc": "Click element on web page by selector. Form submission button clicks navigation browser automation."},
    {"name": "pw_fill_form",   "server": "playwright", "tokens": 110, "desc": "Fill form fields on web page. Login search data entry automation."},
    {"name": "pw_screenshot",  "server": "playwright", "tokens": 100, "desc": "Take screenshot of browser page. Visual verification capturing UI state."},
    {"name": "pw_snapshot",    "server": "playwright", "tokens": 100, "desc": "Get accessibility snapshot of browser page. Structured content for analysis."},
    {"name": "pw_evaluate",    "server": "playwright", "tokens": 120, "desc": "Execute JavaScript in browser. Extract data manipulate DOM test JavaScript functionality."},
    {"name": "pw_wait_for",    "server": "playwright", "tokens": 100, "desc": "Wait for element URL or network condition in browser. Async pages dynamic content."},
    {"name": "pw_type",        "server": "playwright", "tokens": 100, "desc": "Type text into input field. Search boxes text inputs browser typing."},
    {"name": "pw_console",     "server": "playwright", "tokens": 100, "desc": "Get browser console messages. Debugging JavaScript errors monitoring logs."},
    {"name": "pw_network",     "server": "playwright", "tokens": 110, "desc": "Monitor browser network requests. API debugging checking request response status."},

    # ── Chrome MCP ───────────────────────────────────────────────────────────
    {"name": "chrome_navigate",  "server": "chrome", "tokens": 110, "desc": "Navigate Chrome browser to URL. Chrome automation authenticated web sessions interactive browsing."},
    {"name": "chrome_read_page", "server": "chrome", "tokens": 110, "desc": "Read current Chrome page content. Text and structure from logged-in sessions authenticated scraping."},
    {"name": "chrome_find",      "server": "chrome", "tokens": 100, "desc": "Find elements on Chrome page by text or selector. Locate specific content in browser."},
    {"name": "chrome_form",      "server": "chrome", "tokens": 110, "desc": "Fill and submit forms in Chrome. Authenticated form submission login."},
    {"name": "chrome_js",        "server": "chrome", "tokens": 120, "desc": "Execute JavaScript in Chrome page. DOM manipulation data extraction web automation."},
    {"name": "chrome_batch",     "server": "chrome", "tokens": 130, "desc": "Execute multiple browser actions as batch in Chrome. More efficient than individual tool calls."},

    # ── Gmail ────────────────────────────────────────────────────────────────
    {"name": "gmail_search",  "server": "gmail", "tokens": 120, "desc": "Search Gmail messages by query sender subject date range. Find emails check inbox monitor notifications."},
    {"name": "gmail_read",    "server": "gmail", "tokens": 110, "desc": "Read Gmail message content body headers attachments. Process emails extract information."},
    {"name": "gmail_draft",   "server": "gmail", "tokens": 110, "desc": "Create Gmail draft message recipients subject body. Compose emails prepare outreach."},
    {"name": "gmail_labels",  "server": "gmail", "tokens": 100, "desc": "List Gmail labels and categories. Email organization filtering."},

    # ── Calendar ─────────────────────────────────────────────────────────────
    {"name": "cal_list_events",  "server": "calendar", "tokens": 110, "desc": "List calendar events in time range. Meetings deadlines reminders availability scheduling."},
    {"name": "cal_create_event", "server": "calendar", "tokens": 120, "desc": "Create calendar event with title time location attendees. Schedule meetings set reminders block time."},
    {"name": "cal_suggest_time", "server": "calendar", "tokens": 110, "desc": "Suggest available meeting times based on calendar availability. Scheduling coordination."},
    {"name": "cal_update_event", "server": "calendar", "tokens": 110, "desc": "Update or delete existing calendar event. Reschedule cancel meetings."},

    # ── Google Drive ─────────────────────────────────────────────────────────
    {"name": "drive_list_recent", "server": "gdrive", "tokens": 110, "desc": "List recently accessed Google Drive files. Recent documents shared files Drive activity."},
    {"name": "drive_search",      "server": "gdrive", "tokens": 120, "desc": "Search Google Drive files by name or content. Documents spreadsheets presentations."},
    {"name": "drive_read",        "server": "gdrive", "tokens": 120, "desc": "Read content of Google Drive file. Docs Sheets text files extract document content."},

    # ── Telegram ─────────────────────────────────────────────────────────────
    {"name": "telegram_reply",  "server": "telegram", "tokens": 100, "desc": "Send reply to Telegram chat. User notifications progress updates alerting about completed tasks findings."},
    {"name": "telegram_react",  "server": "telegram", "tokens": 90,  "desc": "Add emoji reaction to Telegram message. Acknowledge messages."},
    {"name": "telegram_edit",   "server": "telegram", "tokens": 100, "desc": "Edit existing Telegram message. Progress updates without ping notification."},

    # ── scheduled-tasks ──────────────────────────────────────────────────────
    {"name": "sched_create", "server": "sched", "tokens": 120, "desc": "Create scheduled task to run Claude Code remotely on schedule. Automation recurring reports periodic maintenance."},
    {"name": "sched_list",   "server": "sched", "tokens": 100, "desc": "List all scheduled tasks and their status. Monitor automation active schedules."},
    {"name": "sched_update", "server": "sched", "tokens": 110, "desc": "Update or disable scheduled task. Modify automation schedules."},

    # ── context7 ─────────────────────────────────────────────────────────────
    {"name": "ctx7_query",   "server": "ctx7", "tokens": 120, "desc": "Query documentation for libraries frameworks APIs. Current library docs API reference SDK usage examples."},
    {"name": "ctx7_resolve", "server": "ctx7", "tokens": 110, "desc": "Resolve library name to context7 ID. Required before querying documentation."},

    # ── claude-preview ───────────────────────────────────────────────────────
    {"name": "preview_start",      "server": "preview", "tokens": 110, "desc": "Start dev server preview for web application. UI development testing frontend changes visual verification."},
    {"name": "preview_screenshot", "server": "preview", "tokens": 100, "desc": "Take screenshot of running preview. Visual verification of UI changes."},
    {"name": "preview_snapshot",   "server": "preview", "tokens": 100, "desc": "Get HTML snapshot of running preview. Content structure verification."},
    {"name": "preview_click",      "server": "preview", "tokens": 100, "desc": "Click element in running preview. Test interactions user flows."},

    # ── mcp-registry ─────────────────────────────────────────────────────────
    {"name": "reg_search",  "server": "registry", "tokens": 110, "desc": "Search MCP registry for servers by keyword. Discover new MCP tools integrations connectors."},
    {"name": "reg_suggest", "server": "registry", "tokens": 110, "desc": "Get connector suggestions based on use case. Find relevant MCP servers."},

    # ── youtube-transcript ───────────────────────────────────────────────────
    {"name": "yt_transcript", "server": "youtube", "tokens": 110, "desc": "Extract transcript from YouTube video. Subtitles transcription video content analysis summarization."},
    {"name": "yt_languages",  "server": "youtube", "tokens": 100, "desc": "Get available transcript languages for YouTube video. Language options for transcription."},
]


# ─────────────────────────────────────────────────────────────────────────────
# ISO Scoring — TF-IDF cosine similarity (no external deps required)
# ─────────────────────────────────────────────────────────────────────────────

def tokenize(text: str) -> list[str]:
    """Lowercase word tokenizer."""
    return re.findall(r"[a-z0-9]+", text.lower())


def build_idf(corpus: list[list[str]]) -> dict[str, float]:
    """Compute IDF weights from tool description corpus."""
    n = len(corpus)
    df: dict[str, int] = {}
    for doc in corpus:
        for term in set(doc):
            df[term] = df.get(term, 0) + 1
    return {term: math.log((n + 1) / (cnt + 1)) for term, cnt in df.items()}


def tfidf_vector(tokens: list[str], idf: dict[str, float]) -> dict[str, float]:
    """Compute TF-IDF vector for a list of tokens."""
    tf: dict[str, int] = {}
    for t in tokens:
        tf[t] = tf.get(t, 0) + 1
    total = len(tokens) or 1
    return {term: (cnt / total) * idf.get(term, 0.0) for term, cnt in tf.items()}


def cosine_sim(v1: dict[str, float], v2: dict[str, float]) -> float:
    """Cosine similarity between two TF-IDF vectors."""
    dot = sum(v1.get(t, 0.0) * v2.get(t, 0.0) for t in v2)
    norm1 = math.sqrt(sum(x**2 for x in v1.values()))
    norm2 = math.sqrt(sum(x**2 for x in v2.values()))
    if norm1 == 0 or norm2 == 0:
        return 0.0
    return dot / (norm1 * norm2)


def score_tools(
    query: str,
    tools: list[dict],
    idf: dict[str, float],
    top_k: int = 10,
    threshold: float = 0.05,
) -> tuple[list[tuple[float, dict]], list[tuple[float, dict]]]:
    """Return (active, filtered_out) sorted by ISO score descending."""
    q_vec = tfidf_vector(tokenize(query), idf)
    scored = []
    for tool in tools:
        # Include tool name tokens in description for better matching
        desc_tokens = tokenize(tool["name"] + " " + tool["server"] + " " + tool["desc"])
        t_vec = tfidf_vector(desc_tokens, idf)
        score = cosine_sim(q_vec, t_vec)
        scored.append((score, tool))
    scored.sort(key=lambda x: -x[0])

    active = [(s, t) for s, t in scored[:top_k] if s >= threshold]
    filtered = [(s, t) for s, t in scored if (s, t) not in active]
    return active, filtered, scored


# ─────────────────────────────────────────────────────────────────────────────
# Demo queries covering typical STOPA workflows
# ─────────────────────────────────────────────────────────────────────────────
SAMPLE_QUERIES = [
    "read skill file and search for matching pattern in codebase",
    "search github issues and create a fix branch",
    "send notification to telegram after task completes",
    "browse web page extract product information scraping",
    "schedule automated daily report for project",
    "search emails and create calendar meeting event",
    "take screenshot of dev server UI preview",
    "query library documentation for API usage examples",
]


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Tool Attention ISO scoring — STOPA tool catalog benchmark"
    )
    parser.add_argument("query", nargs="?", help="Query to score (omit for 8-query demo)")
    parser.add_argument("--top-k", type=int, default=10, help="Max tools in active set (default: 10)")
    parser.add_argument("--threshold", type=float, default=0.04, help="Min ISO score (default: 0.04)")
    parser.add_argument("--verbose", action="store_true", help="Show all scores including filtered")
    args = parser.parse_args()

    # Build IDF from tool corpus (include name + server in each doc)
    corpus = [tokenize(t["name"] + " " + t["server"] + " " + t["desc"]) for t in TOOLS]
    idf = build_idf(corpus)

    total_tokens = sum(t["tokens"] for t in TOOLS)
    queries = [args.query] if args.query else SAMPLE_QUERIES

    print(f"\n{'═' * 72}")
    print(f"  Tool Attention ISO — STOPA ({len(TOOLS)} tools, {total_tokens:,} tokens/turn baseline)")
    print(f"  Algorithm: TF-IDF cosine (arXiv:2604.21816 proxy) | top-k={args.top_k} | θ={args.threshold}")
    print(f"{'═' * 72}\n")

    savings_all: list[float] = []

    for query in queries:
        active, filtered, all_scores = score_tools(query, TOOLS, idf, args.top_k, args.threshold)

        active_tokens = sum(t["tokens"] for _, t in active)
        pct_reduction = 100.0 * (1 - active_tokens / total_tokens)
        savings_all.append(pct_reduction)

        print(f"  ▸ \"{query}\"")
        print(f"    Active: {len(active)} tools / {active_tokens} tokens — {pct_reduction:.0f}% reduction")
        for score, tool in active:
            print(f"      ✓ [{score:.3f}] {tool['name']} ({tool['server']})")
        if args.verbose:
            print(f"    Filtered out ({len(filtered)} tools):")
            for score, tool in filtered[:8]:
                print(f"      ✗ [{score:.3f}] {tool['name']}")
            if len(filtered) > 8:
                print(f"      ... and {len(filtered) - 8} more")
        print()

    # Summary
    avg_reduction = sum(savings_all) / len(savings_all)
    avg_active_tokens = int(total_tokens * (1 - avg_reduction / 100))

    print(f"{'─' * 72}")
    print(f"  SUMMARY")
    print(f"  ├─ Full catalog:        {total_tokens:,} tokens/turn ({len(TOOLS)} tools)")
    print(f"  ├─ ISO-filtered avg:    {avg_active_tokens:,} tokens/turn ({args.top_k} tools max)")
    print(f"  ├─ Average reduction:   {avg_reduction:.0f}%")
    print(f"  └─ Est. savings/100k:   ~{int((total_tokens - avg_active_tokens) * 100000 / 1000):,}k tokens")
    print()
    print(f"  NEXT STEPS (arXiv:2604.21816 roadmap for STOPA):")
    print(f"  1. Replace TF-IDF with all-MiniLM-L6-v2 embeddings (+15% precision)")
    print(f"     → pip install sentence-transformers && python scripts/tool-attention-embed.py")
    print(f"  2. Wire intent cache into UserPromptSubmit hook:")
    print(f"     → .claude/hooks/tool-intent-cache.py (writes intermediate/current-intent.json)")
    print(f"  3. MCP proxy server for real schema filtering:")
    print(f"     → Only works at session level (Anthropic doesn't expose per-turn schema hook)")
    print(f"  4. Per-skill allowed-tools auto-generation from ISO scores:")
    print(f"     → python scripts/tool-attention-proto.py <skill_desc> --generate-allowlist")
    print()


if __name__ == "__main__":
    main()
