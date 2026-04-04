#!/usr/bin/env python3
"""Learnings retrieval helper with synonym fallback and confidence decay.

Usage (as module):
    from learnings_retrieval import retrieve_learnings, run_confidence_decay

Usage (CLI):
    python learnings_retrieval.py search "validation" "skill"
    python learnings_retrieval.py decay          # run confidence decay on all learnings
    python learnings_retrieval.py graduates      # list graduation candidates
"""
import os
import re
import sys
from datetime import datetime, timedelta
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

LEARNINGS_DIR = Path(".claude/memory/learnings")

# Synonym map: keyword -> related terms to retry on zero grep results
# Covers the most common semantic gaps in STOPA learnings
SYNONYM_MAP = {
    "validation": ["sanitization", "input checking", "verify", "constraint"],
    "sanitization": ["validation", "input checking", "escaping"],
    "security": ["auth", "vulnerability", "injection", "OWASP"],
    "auth": ["authentication", "authorization", "security", "token", "JWT"],
    "performance": ["latency", "speed", "optimization", "bottleneck", "cache"],
    "error": ["exception", "failure", "crash", "bug", "fault"],
    "test": ["testing", "assertion", "coverage", "spec", "verify"],
    "memory": ["state", "persistence", "storage", "checkpoint"],
    "prompt": ["instruction", "system message", "template"],
    "skill": ["command", "workflow", "pipeline"],
    "hook": ["trigger", "automation", "event", "callback"],
    "orchestration": ["coordination", "pipeline", "multi-step", "agent"],
    "review": ["critic", "audit", "quality", "check"],
    "deploy": ["CI/CD", "release", "build", "publish"],
    "refactor": ["cleanup", "restructure", "simplify", "reorganize"],
    "config": ["settings", "configuration", "environment", "env"],
    "budget": ["cost", "tokens", "spending", "tier"],
}

# Source weights for time-weighted relevance scoring
SOURCE_WEIGHTS = {
    "user_correction": 1.5,
    "critic_finding": 1.2,
    "auto_pattern": 1.0,
    "external_research": 0.9,
    "agent_generated": 0.8,
}

SEVERITY_WEIGHTS = {
    "critical": 4,
    "high": 3,
    "medium": 2,
    "low": 1,
}


def parse_yaml_frontmatter(content: str) -> dict:
    """Extract YAML frontmatter as flat string dict."""
    if not content.startswith("---"):
        return {}
    end = content.find("---", 3)
    if end == -1:
        return {}
    yaml_block = content[3:end].strip()
    result = {}
    for line in yaml_block.split("\n"):
        if ":" in line:
            key, _, val = line.partition(":")
            result[key.strip()] = val.strip()
    return result


def get_synonyms(keyword: str) -> list[str]:
    """Get synonym list for a keyword. Returns empty if no synonyms known."""
    kw = keyword.lower().strip()
    synonyms = SYNONYM_MAP.get(kw, [])
    # Also check reverse: if keyword appears as a synonym value
    if not synonyms:
        for key, vals in SYNONYM_MAP.items():
            if kw in [v.lower() for v in vals]:
                synonyms = [key] + [v for v in vals if v.lower() != kw]
                break
    return synonyms[:3]  # Max 3 synonyms per retry


def grep_learnings(keywords: list[str]) -> list[Path]:
    """Grep learnings directory for files matching any keyword."""
    if not LEARNINGS_DIR.exists():
        return []
    matched = set()
    for f in LEARNINGS_DIR.glob("*.md"):
        if f.name in ("critical-patterns.md", "index-general.md"):
            continue
        try:
            content = f.read_text(encoding="utf-8", errors="replace").lower()
        except OSError:
            continue
        for kw in keywords:
            if kw.lower() in content:
                matched.add(f)
                break
    return sorted(matched, key=lambda p: p.name, reverse=True)  # newest first


def score_learning(meta: dict) -> float:
    """Compute time-weighted relevance score for a learning."""
    severity = SEVERITY_WEIGHTS.get(meta.get("severity", "medium"), 2)
    source = SOURCE_WEIGHTS.get(meta.get("source", "auto_pattern"), 1.0)
    confidence = float(meta.get("confidence", "0.7"))

    # Parse date for recency
    date_str = meta.get("date", "")
    try:
        learning_date = datetime.strptime(date_str, "%Y-%m-%d")
        days_since = (datetime.now() - learning_date).days
    except (ValueError, TypeError):
        days_since = 90  # default for unparseable dates

    recency = 1 / (1 + days_since / 60)
    return severity * source * confidence * recency


def screening_score_learnings(
    keywords: list[str], max_results: int = 5
) -> list[dict] | None:
    """Score learnings using trained Multiscreen RetrievalScreener.

    Returns list of dicts matching retrieve_learnings format, or None if unavailable.
    Requires: STOPA_SCREENING=1 env var and trained model checkpoint.
    """
    if os.environ.get("STOPA_SCREENING") != "1":
        return None
    try:
        from lib.learning_embedder import ScreeningScorer
        scorer = ScreeningScorer.load(timeout_ms=500)
        if scorer is None:
            return None
        raw = scorer.score_keywords(keywords, max_results)
        # Convert to standard format
        results = []
        for r in raw:
            path = LEARNINGS_DIR / r["filename"]
            results.append({
                "path": str(path),
                "filename": r["filename"],
                "meta": r["meta"],
                "score": r["score"],
                "body": r["body"],
            })
        return results
    except Exception:
        return None


def retrieve_learnings(keywords: list[str], max_results: int = 5) -> list[dict]:
    """Retrieve learnings with synonym fallback and relevance scoring.

    Returns list of dicts: {path, meta, score, body}

    When STOPA_SCREENING=1 and model available, uses trained Multiscreen
    RetrievalScreener for better ranking. Falls back to heuristic otherwise.
    """
    # Try screening-based scoring first
    screening_results = screening_score_learnings(keywords, max_results)
    if screening_results is not None:
        return screening_results

    # Round 1: direct grep
    matches = grep_learnings(keywords)

    # Round 2: synonym fallback if no matches (max 2 retry rounds)
    if not matches:
        for kw in keywords:
            synonyms = get_synonyms(kw)
            if synonyms:
                matches = grep_learnings(synonyms)
                if matches:
                    break
        # Round 3: try synonyms of all keywords combined
        if not matches:
            all_synonyms = []
            for kw in keywords:
                all_synonyms.extend(get_synonyms(kw))
            if all_synonyms:
                matches = grep_learnings(list(set(all_synonyms)))

    # Score and rank
    results = []
    for path in matches:
        try:
            content = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        meta = parse_yaml_frontmatter(content)

        # Skip superseded learnings
        superseded_by = None
        for other in matches:
            if other == path:
                continue
            try:
                other_meta = parse_yaml_frontmatter(
                    other.read_text(encoding="utf-8", errors="replace")
                )
                if other_meta.get("supersedes", "") == path.name:
                    superseded_by = other.name
                    break
            except OSError:
                continue
        if superseded_by:
            continue

        score = score_learning(meta)
        # Body = everything after frontmatter
        body_start = content.find("---", 3)
        body = content[body_start + 3:].strip() if body_start != -1 else content

        results.append({
            "path": str(path),
            "filename": path.name,
            "meta": meta,
            "score": round(score, 3),
            "body": body[:500],  # truncate for preview
        })

    # Sort by score descending
    results.sort(key=lambda x: x["score"], reverse=True)
    return results[:max_results]


def run_confidence_decay() -> list[dict]:
    """Apply confidence decay to learnings unused for 60+ days.

    Returns list of decayed learnings with old/new confidence.
    """
    if not LEARNINGS_DIR.exists():
        return []
    decayed = []
    now = datetime.now()

    for f in LEARNINGS_DIR.glob("*.md"):
        if f.name in ("critical-patterns.md", "index-general.md",
                       "block-manifest.json", "ecosystem-scan.md"):
            continue
        try:
            content = f.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue

        meta = parse_yaml_frontmatter(content)
        if not meta.get("date"):
            continue

        try:
            learning_date = datetime.strptime(meta["date"], "%Y-%m-%d")
        except ValueError:
            continue

        days_old = (now - learning_date).days
        if days_old < 60:
            continue

        uses = int(meta.get("uses", "0"))
        confidence = float(meta.get("confidence", "0.7"))

        # Decay: -0.1 per 30 days of inactivity beyond 60 days
        # But uses boost: +0.05 per use
        decay_periods = (days_old - 60) // 30
        old_confidence = confidence
        new_confidence = max(0.1, confidence - (decay_periods * 0.1) + (uses * 0.05))
        new_confidence = min(1.0, new_confidence)

        if abs(new_confidence - old_confidence) > 0.01:
            # Update the file
            old_line = f"confidence: {meta.get('confidence', '0.7')}"
            new_line = f"confidence: {new_confidence:.1f}"
            new_content = content.replace(old_line, new_line, 1)
            if new_content != content:
                f.write_text(new_content, encoding="utf-8")
                decayed.append({
                    "file": f.name,
                    "old": round(old_confidence, 2),
                    "new": round(new_confidence, 2),
                    "days_old": days_old,
                    "uses": uses,
                })

    return decayed


def find_graduation_candidates() -> list[dict]:
    """Find learnings eligible for promotion to critical-patterns.md or rules/.

    Criteria: uses >= 10 AND confidence >= 0.8 AND harmful_uses < 2
    """
    if not LEARNINGS_DIR.exists():
        return []
    candidates = []

    for f in LEARNINGS_DIR.glob("*.md"):
        if f.name in ("critical-patterns.md", "index-general.md",
                       "block-manifest.json", "ecosystem-scan.md"):
            continue
        try:
            content = f.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue

        meta = parse_yaml_frontmatter(content)
        uses = int(meta.get("uses", "0"))
        confidence = float(meta.get("confidence", "0.7"))
        harmful = int(meta.get("harmful_uses", "0"))

        if uses >= 10 and confidence >= 0.8 and harmful < 2:
            candidates.append({
                "file": f.name,
                "summary": meta.get("summary", ""),
                "uses": uses,
                "confidence": confidence,
                "harmful_uses": harmful,
                "component": meta.get("component", ""),
            })

    # Also flag pruning candidates: confidence < 0.3
    pruning = []
    for f in LEARNINGS_DIR.glob("*.md"):
        if f.name in ("critical-patterns.md", "index-general.md",
                       "block-manifest.json", "ecosystem-scan.md"):
            continue
        try:
            content = f.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        meta = parse_yaml_frontmatter(content)
        confidence = float(meta.get("confidence", "0.7"))
        if confidence < 0.3:
            pruning.append({
                "file": f.name,
                "confidence": confidence,
                "summary": meta.get("summary", ""),
            })

    return {"graduates": candidates, "pruning_candidates": pruning}


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: learnings_retrieval.py search <keyword1> [keyword2] ...")
        print("       learnings_retrieval.py decay")
        print("       learnings_retrieval.py graduates")
        sys.exit(1)

    cmd = sys.argv[1]

    if cmd == "search":
        keywords = sys.argv[2:]
        if not keywords:
            print("Error: provide at least one keyword")
            sys.exit(1)
        results = retrieve_learnings(keywords)
        if not results:
            print(f"No learnings found for: {', '.join(keywords)}")
        else:
            print(f"Found {len(results)} learnings:")
            for r in results:
                print(f"  [{r['score']:.2f}] {r['filename']}")
                if r['meta'].get('summary'):
                    print(f"         {r['meta']['summary'][:100]}")

    elif cmd == "decay":
        decayed = run_confidence_decay()
        if not decayed:
            print("No learnings needed confidence decay.")
        else:
            print(f"Decayed {len(decayed)} learnings:")
            for d in decayed:
                print(f"  {d['file']}: {d['old']} -> {d['new']} ({d['days_old']}d old, {d['uses']} uses)")

    elif cmd == "graduates":
        result = find_graduation_candidates()
        grads = result["graduates"]
        prune = result["pruning_candidates"]
        if grads:
            print(f"Graduation candidates ({len(grads)}):")
            for g in grads:
                print(f"  {g['file']} (uses={g['uses']}, conf={g['confidence']})")
        else:
            print("No graduation candidates yet.")
        if prune:
            print(f"\nPruning candidates ({len(prune)}):")
            for p in prune:
                print(f"  {p['file']} (conf={p['confidence']})")
        else:
            print("No pruning candidates.")

    else:
        print(f"Unknown command: {cmd}")
        sys.exit(1)
