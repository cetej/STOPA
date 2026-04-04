#!/usr/bin/env python3
"""UserPromptSubmit hook: inject relevant memory context before each user prompt.

Keyword-matches user prompt against learnings, feedback, and patterns.
Outputs additionalContext JSON with memory snippets within a token budget.
Must complete in <3s — no LLM calls, pure keyword matching.

DeerFlow-inspired improvements (2026-03-28):
- Token-budget injection (1500 tokens) instead of fixed top-3
- Confidence scoring: keyword_score × confidence for ranking
- Confidence derived from severity, recency, and source quality
"""
import json
import os
import re
import sys
import time
from pathlib import Path

import sys, os
_levels = {'minimal': 1, 'standard': 2, 'strict': 3}
if _levels.get(os.environ.get('STOPA_HOOK_PROFILE', 'standard'), 2) < _levels.get('standard', 2):
    sys.exit(0)

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

MEMORY_DIR = Path(".claude/memory")
LEARNINGS_DIR = MEMORY_DIR / "learnings"
PATTERNS_PATH = MEMORY_DIR / "patterns.md"
DECISIONS_PATH = MEMORY_DIR / "decisions.md"
CACHE_PATH = MEMORY_DIR / "intermediate" / "learnings-index.json"

# Token budget for memory injection (DeerFlow-inspired)
TOKEN_BUDGET = 1500  # ~1500 tokens max injected per prompt
WORD_TO_TOKEN_RATIO = 1.3  # rough estimate: 1 word ≈ 1.3 tokens

# Confidence mappings
SEVERITY_CONFIDENCE = {
    "critical": 0.95,
    "high": 0.80,
    "medium": 0.60,
    "low": 0.40,
}
SOURCE_CONFIDENCE = {
    "critical": 0.95,  # critical-patterns.md — battle-tested
    "learning": 0.75,  # learnings/ — verified during session
    "decision": 0.85,  # decisions.md — explicit choices
    "feedback": 0.90,  # user corrections — high signal
    "pattern": 0.50,   # auto-detected patterns — lower confidence
}

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
# Synonym expansion table — maps keywords to additional search terms
# Covers: CZ↔EN pairs, technical aliases, conceptual synonyms
# Each key maps to a list of synonyms that will be searched alongside the original
SYNONYM_MAP: dict[str, list[str]] = {
    # CZ↔EN pairs
    "skill": ["dovednost", "command", "příkaz"],
    "dovednost": ["skill", "command"],
    "memory": ["paměť", "context", "kontext"],
    "paměť": ["memory", "context"],
    "hook": ["háček", "trigger", "event"],
    "háček": ["hook", "trigger"],
    "budget": ["cost", "rozpočet", "token", "náklady"],
    "rozpočet": ["budget", "cost", "token"],
    "cost": ["budget", "rozpočet", "náklady"],
    "pipeline": ["workflow", "proces", "tok"],
    "workflow": ["pipeline", "proces"],
    "error": ["chyba", "bug", "failure", "selhání"],
    "chyba": ["error", "bug", "failure"],
    "bug": ["error", "chyba", "defect"],
    "test": ["ověření", "verify", "validace"],
    "verify": ["test", "ověření", "validate"],
    # Technical aliases
    "trigger": ["description", "matcher", "activation"],
    "description": ["trigger", "popis", "frontmatter"],
    "retrieval": ["search", "recall", "vyhledávání", "matching"],
    "search": ["retrieval", "grep", "hledání", "find"],
    "deploy": ["distribute", "sync", "nasazení", "distribuce"],
    "orchestrate": ["plan", "decompose", "rozložit"],
    "checkpoint": ["save", "resume", "snapshot", "uložení"],
    "compact": ["compress", "summarize", "context"],
    "agent": ["subagent", "worker", "teammate"],
    "learning": ["poznatek", "lesson", "pattern", "vzor"],
    "pattern": ["vzor", "learning", "convention"],
    "decision": ["rozhodnutí", "choice", "volba"],
    "confidence": ["score", "ranking", "důvěra"],
    "decay": ["recency", "staleness", "stárnutí"],
    "embedding": ["vector", "semantic", "similarity"],
    "semantic": ["embedding", "meaning", "význam"],
    "consolidation": ["merge", "dedup", "sloučení"],
    "episode": ["history", "log", "event", "záznam"],
    # Domain-specific
    "critic": ["review", "quality", "kontrola"],
    "scout": ["explore", "map", "průzkum"],
    "scribe": ["record", "capture", "zapiš"],
    "watch": ["news", "novinky", "scan"],
    "harness": ["deterministic", "pipeline", "runner"],
}

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


def estimate_tokens(text: str) -> float:
    """Estimate token count from text (word count × 1.3)."""
    return len(text.split()) * WORD_TO_TOKEN_RATIO


def compute_confidence(source: str, severity: str = "", date_str: str = "") -> float:
    """Compute confidence score (0.0-1.0) combining source quality, severity, and recency.

    Inspired by DeerFlow's confidence scoring but adapted for STOPA's
    structured memory (severity levels, dated learnings).
    """
    # Base confidence from source type
    base = SOURCE_CONFIDENCE.get(source, 0.60)

    # Severity boost (for learnings)
    if severity:
        severity_factor = SEVERITY_CONFIDENCE.get(severity, 0.60)
        # Blend: 60% source, 40% severity
        base = base * 0.6 + severity_factor * 0.4

    # Recency decay: facts older than 60 days lose confidence
    if date_str:
        try:
            days_ago = (time.time() - time.mktime(time.strptime(date_str, "%Y-%m-%d"))) / 86400
            if days_ago > 60:
                decay = max(0.7, 1.0 - (days_ago - 60) / 300)  # slow decay, floor at 0.7
                base *= decay
        except (ValueError, OverflowError):
            pass

    return round(min(1.0, max(0.1, base)), 2)


def expand_synonyms(keywords: list[str], max_expanded: int = 8) -> list[str]:
    """Expand keywords with synonyms from SYNONYM_MAP.

    Original keywords come first (higher priority), synonyms appended.
    Total capped at max_expanded to avoid noise.
    """
    expanded = list(keywords)  # originals first
    seen = set(keywords)
    for kw in keywords:
        for syn in SYNONYM_MAP.get(kw, []):
            if syn not in seen and syn not in STOPWORDS:
                expanded.append(syn)
                seen.add(syn)
    return expanded[:max_expanded]


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

            entry = {"file": f.name, "tags": [], "component": "", "description": "", "summary": "", "severity": ""}
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
                elif line.startswith("severity:"):
                    entry["severity"] = line.split(":", 1)[1].strip()
                elif line.startswith("summary:"):
                    entry["summary"] = line.split(":", 1)[1].strip().strip("'\"")[:200]

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


def _screening_boost(keywords: list[str], index: list[dict]) -> dict[str, float]:
    """Get screening scores for blending, if available. Returns {filename: score}."""
    if os.environ.get("STOPA_SCREENING") != "1":
        return {}
    try:
        from lib.learning_embedder import ScreeningScorer
        scorer = ScreeningScorer.load(timeout_ms=300)
        if scorer is None:
            return {}
        raw = scorer.score_keywords(keywords, max_results=20)
        return {r["filename"]: r["score"] for r in raw}
    except Exception:
        return {}


def search_learnings(keywords: list[str], index: list[dict]) -> list[dict]:
    """Search learnings index by keywords. Returns scored matches.

    When STOPA_SCREENING=1: blends keyword score with screening score
    (0.6 * keyword_norm + 0.4 * screening_score) for better ranking.
    """
    # Get screening scores upfront (empty dict if disabled)
    screening_scores = _screening_boost(keywords, index)

    matches = []
    for entry in index:
        score = 0
        tags_lower = [t.lower() for t in entry.get("tags", [])]
        component = entry.get("component", "").lower()
        slug = entry.get("slug", "")
        desc = entry.get("description", "").lower()
        summary = entry.get("summary", "").lower()

        for kw in keywords:
            if kw in tags_lower:
                score += 3
            elif kw == component:
                score += 2
            elif kw in slug:
                score += 2
            elif kw in summary:
                score += 2  # summary match: higher than desc, equal to slug
            elif kw in desc:
                score += 1

        if score > 0:
            # Prefer summary over first-line description
            display = entry.get("summary") or entry.get("description") or entry.get("slug", "?")
            confidence = compute_confidence("learning", entry.get("severity", ""), entry.get("date", ""))
            matches.append({
                "source": "learning",
                "file": entry.get("file", ""),  # track filename for uses increment
                "text": display,
                "date": entry.get("date", ""),
                "score": score,
                "confidence": confidence,
            })

    # Blend with screening scores if available
    if screening_scores:
        max_kw_score = max((m["score"] for m in matches), default=1) or 1
        seen_files = set()
        for m in matches:
            fname = m.get("file", "")
            seen_files.add(fname)
            kw_norm = m["score"] / max_kw_score
            scr = screening_scores.get(fname, 0.0)
            m["score"] = 0.6 * kw_norm + 0.4 * scr

        # Add screening-only matches (keyword search missed)
        for fname, scr_score in screening_scores.items():
            if fname not in seen_files and scr_score > 0.1:
                # Find entry in index
                entry = next((e for e in index if e.get("file") == fname), None)
                if entry:
                    display = entry.get("summary") or entry.get("description") or fname
                    confidence = compute_confidence("learning", entry.get("severity", ""), entry.get("date", ""))
                    matches.append({
                        "source": "learning",
                        "file": fname,
                        "text": display,
                        "date": entry.get("date", ""),
                        "score": 0.4 * scr_score,  # screening-only (no keyword contribution)
                        "confidence": confidence,
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
                    "confidence": compute_confidence("feedback"),
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
                        "confidence": compute_confidence("pattern"),
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
                "confidence": compute_confidence("pattern"),
            })

    return sorted(matches, key=lambda x: -x["score"])


def search_decisions(keywords: list[str]) -> list[dict]:
    """Search decisions.md entries by title, context, and decision text."""
    if not DECISIONS_PATH.exists():
        return []

    try:
        text = DECISIONS_PATH.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return []

    matches = []
    current_title = ""
    current_date = ""
    current_text = []

    for line in text.split("\n"):
        if line.startswith("### "):
            # Score previous decision block
            if current_title:
                searchable = (current_title + " " + " ".join(current_text)).lower()
                score = sum(2 for kw in keywords if kw in searchable)
                if score > 0:
                    matches.append({
                        "source": "decision",
                        "text": f"{current_title}"[:120],
                        "date": current_date,
                        "score": score,
                        "confidence": compute_confidence("decision", date_str=current_date),
                    })
            # Parse new header: ### 2026-03-27 — Title
            header = line[4:].strip()
            parts = header.split("—", 1) if "—" in header else header.split("-", 1)
            current_date = parts[0].strip() if len(parts) > 1 else ""
            current_title = parts[1].strip() if len(parts) > 1 else header
            current_text = []
        elif line.startswith("- **"):
            # Capture Decision/Context/Rationale lines
            current_text.append(line.split(":", 1)[1].strip() if ":" in line else line)

    # Don't forget last entry
    if current_title:
        searchable = (current_title + " " + " ".join(current_text)).lower()
        score = sum(2 for kw in keywords if kw in searchable)
        if score > 0:
            matches.append({
                "source": "decision",
                "text": f"{current_title}"[:120],
                "date": current_date,
                "score": score,
                "confidence": compute_confidence("decision", date_str=current_date),
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
                    "confidence": compute_confidence("critical"),
                })

    return sorted(matches, key=lambda x: -x["score"])


def increment_learning_uses(filenames: list[str]) -> None:
    """Increment uses: counter in YAML frontmatter of retrieved learning files.

    This is the critical feedback loop: tracks which learnings actually get surfaced,
    enabling graduation (uses >= 10 → critical-patterns) and pruning (unused → stale).
    Inspired by Hebbian learning: "retrieved together, strengthened together".
    """
    if not filenames or not LEARNINGS_DIR.exists():
        return

    for fname in filenames:
        fpath = LEARNINGS_DIR / fname
        if not fpath.exists():
            continue
        try:
            content = fpath.read_text(encoding="utf-8", errors="replace")
            # Find and increment uses: field
            uses_match = re.search(r"^uses:\s*(\d+)", content, re.MULTILINE)
            if uses_match:
                old_val = int(uses_match.group(1))
                new_val = old_val + 1
                new_content = content[:uses_match.start()] + f"uses: {new_val}" + content[uses_match.end():]
            else:
                # Insert uses: 1 after the last frontmatter field (before closing ---)
                # Find second --- that closes frontmatter
                first = content.find("---")
                if first == -1:
                    continue
                second = content.find("---", first + 3)
                if second == -1:
                    continue
                new_content = content[:second] + "uses: 1\n" + content[second:]
                new_val = 1

            fpath.write_text(new_content, encoding="utf-8")
        except OSError:
            continue


def log_retrieval_event(prompt_keywords: list[str], selected_matches: list[dict]) -> None:
    """Log retrieval event to sessions.jsonl for analytics.

    Tracks: which keywords triggered which learnings, enabling
    co-occurrence analysis and retrieval effectiveness measurement.
    """
    log_path = MEMORY_DIR / "sessions.jsonl"
    try:
        record = {
            "ts": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "event": "memory_retrieval",
            "keywords": prompt_keywords[:5],
            "matches": [
                {"source": m.get("source", ""), "file": m.get("file", ""), "score": m.get("effective_score", 0)}
                for m in selected_matches[:10]
            ],
            "match_count": len(selected_matches),
        }
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")
    except OSError:
        pass


def format_snippet(match: dict) -> str:
    """Format a match into a concise snippet line."""
    source_label = {
        "critical": "critical",
        "learning": "learning",
        "decision": "decision",
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

    # Expand with synonyms for broader recall (originals score higher naturally)
    search_keywords = expand_synonyms(keywords)

    # Search all sources
    all_matches = []
    all_matches.extend(search_critical_patterns(search_keywords))
    all_matches.extend(search_learnings(search_keywords, build_learnings_index()))
    all_matches.extend(search_decisions(search_keywords))
    all_matches.extend(search_feedback(search_keywords))
    all_matches.extend(search_patterns(search_keywords))

    if not all_matches:
        return

    # Sort by effective score: keyword_score × confidence (DeerFlow-inspired)
    for m in all_matches:
        m["effective_score"] = m["score"] * m.get("confidence", 0.60)
    all_matches.sort(key=lambda x: -x["effective_score"])

    # Only output if best match has raw score >= 2 (avoid noise)
    if all_matches[0]["score"] < 2:
        return

    # Token-budget injection: fill up to TOKEN_BUDGET tokens (DeerFlow-inspired)
    selected = []
    tokens_used = 0.0
    for m in all_matches:
        snippet = format_snippet(m)
        snippet_tokens = estimate_tokens(snippet)
        if tokens_used + snippet_tokens > TOKEN_BUDGET:
            if not selected:
                # Always include at least one result
                selected.append(snippet)
            break
        selected.append(snippet)
        tokens_used += snippet_tokens

    # Phase 1a: Track which learnings were surfaced (Hebbian feedback loop)
    surfaced_learning_files = [
        m.get("file") for m in all_matches
        if m.get("source") == "learning" and m.get("file")
        and format_snippet(m) in selected
    ]
    if surfaced_learning_files:
        increment_learning_uses(surfaced_learning_files)

    # Log retrieval event for co-occurrence analytics
    log_retrieval_event(keywords, [m for m in all_matches if format_snippet(m) in selected])

    output = "\n".join(selected)
    print(json.dumps({"additionalContext": output}))


if __name__ == "__main__":
    main()
