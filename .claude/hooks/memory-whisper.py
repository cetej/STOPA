#!/usr/bin/env python3
"""UserPromptSubmit hook: inject relevant memory context before each user prompt.

Keyword-matches user prompt against learnings, feedback, and patterns.
Outputs additionalContext JSON with top 3 relevant memory snippets.
Must complete in <3s — no LLM calls, pure keyword matching.
"""
import json
import os
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

MEMORY_DIR = Path(".claude/memory")
LEARNINGS_DIR = MEMORY_DIR / "learnings"
PATTERNS_PATH = MEMORY_DIR / "patterns.md"
CACHE_PATH = MEMORY_DIR / "intermediate" / "learnings-index.json"

# Resolve auto-memory feedback dir (project-scoped)
# Claude Code stores per-project memory in ~/.claude/projects/<mangled-path>/memory/
# Mangling: C:\ → C--, then \ and _ → -, path separators normalized
_home = Path.home()
_projects_dir = _home / ".claude" / "projects"
AUTOMEMORY_DIR = None
if _projects_dir.exists():
    # Find project dir by matching the last path component (most reliable)
    _cwd_name = Path.cwd().resolve().name
    for d in _projects_dir.iterdir():
        if d.is_dir() and d.name.endswith(f"-{_cwd_name}") and "worktree" not in d.name:
            candidate = d / "memory"
            if candidate.exists():
                AUTOMEMORY_DIR = candidate
                break
if AUTOMEMORY_DIR is None:
    AUTOMEMORY_DIR = _projects_dir / "nonexistent"  # will fail exists() check gracefully

# Stopwords to filter from prompt keywords
STOPWORDS = frozenset({
    "the", "a", "an", "is", "are", "was", "were", "be", "been", "being",
    "have", "has", "had", "do", "does", "did", "will", "would", "could",
    "should", "may", "might", "shall", "can", "need", "must",
    "and", "or", "but", "if", "then", "else", "when", "where", "how",
    "what", "which", "who", "whom", "this", "that", "these", "those",
    "not", "no", "nor", "so", "too", "very", "just", "also",
    "for", "from", "with", "about", "into", "through", "during",
    "before", "after", "above", "below", "between", "out", "off", "over",
    "to", "in", "on", "at", "by", "of", "up", "it", "its",
    "my", "your", "his", "her", "our", "their", "me", "him", "them", "we",
    "all", "each", "every", "both", "few", "more", "most", "some", "any",
    "use", "using", "used", "make", "made", "get", "got", "set",
    "let", "try", "run", "add", "new", "see", "now", "here", "there",
    # Czech stopwords
    "je", "jsou", "byl", "byla", "bylo", "jak", "kde", "kdy", "co",
    "na", "ve", "za", "do", "od", "po", "pro", "pri", "nad", "pod",
    "ten", "ta", "to", "ty", "tato", "tyto", "ale", "nebo", "ani",
    "tak", "jiz", "jen", "mit", "mam", "chci", "zkus", "udelej",
})


def extract_keywords(text: str, max_keywords: int = 5) -> list[str]:
    """Extract meaningful keywords from user prompt."""
    # Split on non-alphanumeric, lowercase
    words = re.findall(r"[a-zA-Z0-9_-]{3,}", text.lower())
    # Filter stopwords and short words
    keywords = [w for w in words if w not in STOPWORDS and len(w) >= 3]
    # Deduplicate preserving order
    seen = set()
    unique = []
    for w in keywords:
        if w not in seen:
            seen.add(w)
            unique.append(w)
    return unique[:max_keywords]


def extract_prompt(hook_input: dict) -> str:
    """Extract user prompt text from hook input JSON."""
    message = hook_input.get("message", {})
    if isinstance(message, dict):
        content = message.get("content", "")
        if isinstance(content, list):
            content = " ".join(
                c.get("text", "") for c in content if isinstance(c, dict)
            )
    elif isinstance(message, str):
        content = message
    else:
        content = str(message)
    return content


def build_learnings_index() -> list[dict]:
    """Build or load cached index of learnings YAML frontmatter."""
    if not LEARNINGS_DIR.exists():
        return []

    # Check cache validity
    dir_mtime = LEARNINGS_DIR.stat().st_mtime
    if CACHE_PATH.exists():
        try:
            cache = json.loads(CACHE_PATH.read_text(encoding="utf-8"))
            if cache.get("mtime") == dir_mtime:
                return cache.get("entries", [])
        except (json.JSONDecodeError, KeyError):
            pass

    # Rebuild index from YAML frontmatter
    entries = []
    for f in LEARNINGS_DIR.glob("*.md"):
        try:
            text = f.read_text(encoding="utf-8", errors="replace")
            # Parse YAML frontmatter (first 10 lines)
            lines = text.split("\n", 12)
            if not lines or lines[0].strip() != "---":
                continue

            entry = {"file": f.name, "tags": [], "component": "", "description": ""}
            for line in lines[1:10]:
                if line.strip() == "---":
                    break
                if line.startswith("tags:"):
                    # Parse [tag1, tag2] or - tag1
                    tags_str = line.split(":", 1)[1].strip()
                    tags_str = tags_str.strip("[]")
                    entry["tags"] = [t.strip().strip("'\"") for t in tags_str.split(",") if t.strip()]
                elif line.startswith("component:"):
                    entry["component"] = line.split(":", 1)[1].strip()
                elif line.startswith("date:"):
                    entry["date"] = line.split(":", 1)[1].strip()

            # Extract first meaningful content line after frontmatter
            # Need to find second --- (closing frontmatter), then first non-empty non-heading line
            fence_count = 0
            for line in text.split("\n"):
                if line.strip() == "---":
                    fence_count += 1
                    continue
                if fence_count >= 2 and line.strip() and not line.startswith("#"):
                    entry["description"] = line.strip()[:120]
                    break

            # Also use filename as searchable text
            entry["slug"] = f.stem.lower()
            entries.append(entry)
        except OSError:
            continue

    # Save cache
    try:
        CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
        CACHE_PATH.write_text(
            json.dumps({"mtime": dir_mtime, "entries": entries}, ensure_ascii=False),
            encoding="utf-8",
        )
    except OSError:
        pass

    return entries


def search_learnings(keywords: list[str], index: list[dict]) -> list[dict]:
    """Search learnings index by keywords. Returns scored matches."""
    matches = []
    for entry in index:
        score = 0
        tags_lower = [t.lower() for t in entry.get("tags", [])]
        component = entry.get("component", "").lower()
        slug = entry.get("slug", "")
        desc = entry.get("description", "").lower()

        for kw in keywords:
            if kw in tags_lower:
                score += 3
            elif kw == component:
                score += 2
            elif kw in slug:
                score += 2
            elif kw in desc:
                score += 1

        if score > 0:
            matches.append({
                "source": "learning",
                "text": entry.get("description", entry.get("slug", "?")),
                "date": entry.get("date", ""),
                "score": score,
            })

    return sorted(matches, key=lambda x: -x["score"])


def search_feedback(keywords: list[str]) -> list[dict]:
    """Search auto-memory feedback files by description."""
    if not AUTOMEMORY_DIR.exists():
        return []

    matches = []
    for f in AUTOMEMORY_DIR.glob("feedback_*.md"):
        try:
            text = f.read_text(encoding="utf-8", errors="replace")
            lines = text.split("\n", 8)

            description = ""
            for line in lines:
                if line.startswith("description:"):
                    description = line.split(":", 1)[1].strip()
                    break

            if not description:
                continue

            desc_lower = description.lower()
            score = 0
            for kw in keywords:
                if kw in desc_lower:
                    score += 2

            if score > 0:
                matches.append({
                    "source": "feedback",
                    "text": description[:120],
                    "score": score,
                })
        except OSError:
            continue

    return sorted(matches, key=lambda x: -x["score"])


def search_patterns(keywords: list[str]) -> list[dict]:
    """Search patterns.md by pattern names and descriptions."""
    if not PATTERNS_PATH.exists():
        return []

    try:
        text = PATTERNS_PATH.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return []

    matches = []
    current_name = ""
    current_desc = ""

    for line in text.split("\n"):
        if line.startswith("### "):
            if current_name:
                # Score previous pattern
                searchable = (current_name + " " + current_desc).lower()
                score = sum(2 for kw in keywords if kw in searchable)
                if score > 0:
                    matches.append({
                        "source": "pattern",
                        "text": f"{current_name}: {current_desc}"[:120],
                        "score": score,
                    })
            current_name = line[4:].strip()
            current_desc = ""
        elif line.startswith("- **Description**:"):
            current_desc = line.split(":", 1)[1].strip()

    # Don't forget last pattern
    if current_name:
        searchable = (current_name + " " + current_desc).lower()
        score = sum(2 for kw in keywords if kw in searchable)
        if score > 0:
            matches.append({
                "source": "pattern",
                "text": f"{current_name}: {current_desc}"[:120],
                "score": score,
            })

    return sorted(matches, key=lambda x: -x["score"])


def search_critical_patterns(keywords: list[str]) -> list[dict]:
    """Search critical-patterns.md titles/content."""
    cp_path = LEARNINGS_DIR / "critical-patterns.md"
    if not cp_path.exists():
        return []

    try:
        text = cp_path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return []

    matches = []
    for line in text.split("\n"):
        line_stripped = line.strip()
        if not line_stripped or line_stripped.startswith("#"):
            continue
        # Each critical pattern is a bullet point
        if line_stripped.startswith(("- ", "* ", "1.", "2.", "3.", "4.", "5.", "6.", "7.", "8.", "9.")):
            line_lower = line_stripped.lower()
            score = sum(3 for kw in keywords if kw in line_lower)
            if score > 0:
                # Trim bullet prefix
                text_clean = re.sub(r"^[-*\d.]+\s*\*\*", "", line_stripped)
                text_clean = re.sub(r"\*\*", "", text_clean).strip()
                matches.append({
                    "source": "critical",
                    "text": text_clean[:120],
                    "score": score,
                })

    return sorted(matches, key=lambda x: -x["score"])


def format_snippet(match: dict) -> str:
    """Format a match into a concise snippet line."""
    source_label = {
        "critical": "critical",
        "learning": "learning",
        "feedback": "feedback",
        "pattern": "pattern",
    }.get(match["source"], match["source"])

    date_suffix = f", {match['date']}" if match.get("date") else ""
    text = match["text"]
    if len(text) > 100:
        text = text[:97] + "..."
    return f"[Memory:{source_label}] {text}{date_suffix}"


def main():
    try:
        hook_input = json.load(sys.stdin)
    except (json.JSONDecodeError, EOFError):
        return

    prompt = extract_prompt(hook_input)
    if not prompt or len(prompt) < 5:
        return

    keywords = extract_keywords(prompt)
    if not keywords:
        return

    # Search all sources
    all_matches = []
    all_matches.extend(search_critical_patterns(keywords))
    all_matches.extend(search_learnings(keywords, build_learnings_index()))
    all_matches.extend(search_feedback(keywords))
    all_matches.extend(search_patterns(keywords))

    if not all_matches:
        return

    # Sort by score, take top 3
    all_matches.sort(key=lambda x: -x["score"])
    top = all_matches[:3]

    # Only output if best match has score >= 2 (avoid noise)
    if top[0]["score"] < 2:
        return

    snippets = [format_snippet(m) for m in top]
    output = "\n".join(snippets)

    print(json.dumps({"additionalContext": output}))


if __name__ == "__main__":
    main()
