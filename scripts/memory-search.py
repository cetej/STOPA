#!/usr/bin/env python3
"""
memory-search.py — BM25-inspired retrieval across STOPA memory system.

Unified search over learnings/, critical-patterns.md, decisions.md, key-facts.md.
Zero dependencies beyond stdlib. Zero embeddings. Zero training.

Usage:
    python scripts/memory-search.py "pipeline error handling"
    python scripts/memory-search.py "orchestration budget" --top 10
    python scripts/memory-search.py "validation" --debug
    python scripts/memory-search.py "validation" --json
"""

import argparse
import json
import math
import os
import re
import sys
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path
from typing import Optional

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# ── Config ──────────────────────────────────────────────────────────────────

MEMORY_DIR = Path(__file__).resolve().parent.parent / ".claude" / "memory"
LEARNINGS_DIR = MEMORY_DIR / "learnings"
SYNONYMS_PATH = MEMORY_DIR / "synonyms.yaml"

# BM25 parameters (tuned for short documents ~20-200 lines)
K1 = 1.2   # term frequency saturation
B = 0.75   # length normalization strength

# Metadata weight multipliers
SEVERITY_WEIGHTS = {"critical": 4.0, "high": 3.0, "medium": 2.0, "low": 1.0}
SOURCE_WEIGHTS = {
    "user_correction": 1.5,
    "critic_finding": 1.2,
    "auto_pattern": 1.0,
    "external_research": 0.9,
    "agent_generated": 0.8,
}

# Stop words — common terms that add no retrieval value
STOP_WORDS = frozenset({
    "the", "a", "an", "is", "are", "was", "were", "be", "been", "being",
    "have", "has", "had", "do", "does", "did", "will", "would", "could",
    "should", "may", "might", "shall", "can", "need", "must",
    "in", "on", "at", "to", "for", "of", "with", "by", "from", "as",
    "into", "through", "during", "before", "after", "above", "below",
    "and", "or", "but", "not", "no", "nor", "so", "yet", "both",
    "this", "that", "these", "those", "it", "its",
    "if", "then", "else", "when", "where", "how", "what", "which", "who",
    # Czech stop words
    "je", "jsou", "byl", "byla", "bylo", "být", "pro", "při", "pod", "nad",
    "tak", "ale", "ani", "nebo", "když", "aby", "že", "jak", "kde",
    "ten", "ta", "to", "toto", "tyto", "jeho", "její", "jejich",
})

# ── Synonym map (inline, expandable) ───────────────────────────────────────

SYNONYMS: dict[str, list[str]] = {
    "validation": ["sanitization", "input checking", "guard", "verify"],
    "pipeline": ["workflow", "processing chain", "batch", "harness"],
    "retrieval": ["search", "lookup", "query", "fetch", "ranking"],
    "orchestration": ["coordination", "routing", "dispatch", "decomposition"],
    "error": ["failure", "exception", "crash", "bug", "broken"],
    "memory": ["state", "checkpoint", "persistence", "context"],
    "budget": ["cost", "tokens", "pricing", "spending"],
    "skill": ["command", "slash command", "capability"],
    "agent": ["sub-agent", "subagent", "worker", "delegate"],
    "security": ["vulnerability", "trust boundary", "injection", "secrets"],
    "performance": ["optimization", "speed", "latency", "efficiency"],
    "test": ["testing", "verification", "assertion", "proof"],
    "debug": ["debugging", "diagnosis", "root cause", "troubleshoot"],
    "review": ["audit", "critic", "quality check", "inspection"],
    "config": ["configuration", "settings", "environment"],
    "deploy": ["deployment", "ship", "release", "ci/cd"],
}


# ── Data structures ────────────────────────────────────────────────────────

@dataclass
class Document:
    """A searchable document from the memory system."""
    path: Path
    source_type: str          # "learning", "critical-pattern", "decision", "key-fact"
    title: str
    content: str              # full text (frontmatter stripped)
    words: list[str] = field(default_factory=list)
    word_count: int = 0
    # Metadata (learnings only)
    severity: str = "medium"
    source: str = "auto_pattern"
    confidence: float = 0.7
    uses: int = 0
    harmful_uses: int = 0
    date: str = ""
    component: str = ""
    tags: list[str] = field(default_factory=list)
    summary: str = ""
    supersedes: str = ""
    superseded_by: Optional[str] = None  # set during loading


@dataclass
class SearchResult:
    """Ranked search result."""
    doc: Document
    bm25_score: float
    metadata_score: float
    combined_score: float
    matched_terms: list[str] = field(default_factory=list)


# ── Tokenization ───────────────────────────────────────────────────────────

def tokenize(text: str) -> list[str]:
    """Split text into lowercase tokens, strip stop words."""
    words = re.findall(r"[a-záčďéěíňóřšťúůýž0-9_-]{2,}", text.lower())
    return [w for w in words if w not in STOP_WORDS]


# ── Document loading ───────────────────────────────────────────────────────

def parse_yaml_frontmatter(text: str) -> tuple[dict, str]:
    """Extract YAML frontmatter and body from markdown."""
    if not text.startswith("---"):
        return {}, text
    end = text.find("---", 3)
    if end == -1:
        return {}, text
    fm_text = text[3:end].strip()
    body = text[end + 3:].strip()

    meta = {}
    for line in fm_text.split("\n"):
        if ":" not in line:
            continue
        key, _, val = line.partition(":")
        key = key.strip()
        val = val.strip().strip('"').strip("'")
        # Parse arrays
        if val.startswith("[") and val.endswith("]"):
            val = [v.strip().strip('"').strip("'") for v in val[1:-1].split(",") if v.strip()]
        # Parse numbers
        elif re.match(r"^-?\d+(\.\d+)?$", val):
            val = float(val) if "." in val else int(val)
        meta[key] = val
    return meta, body


def load_learnings(supersedes_map: dict[str, str]) -> list[Document]:
    """Load all learning files."""
    docs = []
    if not LEARNINGS_DIR.exists():
        return docs

    for path in LEARNINGS_DIR.glob("*.md"):
        if path.name.startswith("index-") or path.name == "critical-patterns.md":
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        meta, body = parse_yaml_frontmatter(text)
        if not body.strip():
            continue

        # Skip expired learnings
        valid_until = meta.get("valid_until", "")
        if valid_until:
            try:
                if date.fromisoformat(str(valid_until)) < date.today():
                    continue
            except (ValueError, TypeError):
                pass

        # Track supersedes relationships
        sup = meta.get("supersedes", "")
        if sup:
            supersedes_map[sup] = path.name

        tags = meta.get("tags", [])
        if isinstance(tags, str):
            tags = [t.strip() for t in tags.split(",")]

        words = tokenize(body)
        docs.append(Document(
            path=path,
            source_type="learning",
            title=path.stem,
            content=body,
            words=words,
            word_count=len(words),
            severity=meta.get("severity", "medium"),
            source=meta.get("source", "auto_pattern"),
            confidence=float(meta.get("confidence", 0.7)),
            uses=int(meta.get("uses", 0)),
            harmful_uses=int(meta.get("harmful_uses", 0)),
            date=str(meta.get("date", "")),
            component=meta.get("component", ""),
            tags=tags,
            summary=meta.get("summary", ""),
            supersedes=sup,
        ))
    return docs


def load_critical_patterns() -> list[Document]:
    """Load critical-patterns.md as individual section documents."""
    path = LEARNINGS_DIR / "critical-patterns.md"
    if not path.exists():
        return []

    text = path.read_text(encoding="utf-8", errors="replace")
    docs = []
    sections = re.split(r"\n## \d+\.\s+", text)
    for i, section in enumerate(sections[1:], 1):
        lines = section.strip().split("\n")
        title = lines[0].strip() if lines else f"Pattern {i}"
        body = "\n".join(lines)
        words = tokenize(body)
        docs.append(Document(
            path=path,
            source_type="critical-pattern",
            title=f"Critical: {title}",
            content=body,
            words=words,
            word_count=len(words),
            severity="critical",
            source="user_correction",
            confidence=0.95,
        ))
    return docs


def load_section_file(path: Path, source_type: str) -> list[Document]:
    """Load a markdown file split by ## headings."""
    if not path.exists():
        return []
    text = path.read_text(encoding="utf-8", errors="replace")
    docs = []
    sections = re.split(r"\n## ", text)
    for section in sections:
        section = section.strip()
        if not section or len(section) < 20:
            continue
        lines = section.split("\n")
        title = lines[0].strip().lstrip("#").strip()
        body = "\n".join(lines)
        words = tokenize(body)
        if len(words) < 3:
            continue
        docs.append(Document(
            path=path,
            source_type=source_type,
            title=title,
            content=body,
            words=words,
            word_count=len(words),
        ))
    return docs


def load_all_documents() -> list[Document]:
    """Load all memory documents, filter superseded."""
    supersedes_map: dict[str, str] = {}  # old_file -> new_file

    docs = load_learnings(supersedes_map)

    # Mark superseded docs
    for doc in docs:
        if doc.path.name in supersedes_map:
            doc.superseded_by = supersedes_map[doc.path.name]

    # Filter superseded
    docs = [d for d in docs if d.superseded_by is None]

    # Add other memory sources
    docs.extend(load_critical_patterns())
    docs.extend(load_section_file(MEMORY_DIR / "decisions.md", "decision"))
    docs.extend(load_section_file(MEMORY_DIR / "key-facts.md", "key-fact"))

    return docs


# ── BM25 scoring ───────────────────────────────────────────────────────────

def compute_idf(term: str, docs: list[Document]) -> float:
    """Inverse document frequency — how rare is this term across corpus."""
    n = len(docs)
    df = sum(1 for d in docs if term in d.words)
    if df == 0:
        return 0.0
    # BM25 IDF formula (Robertson-Sparck Jones)
    return math.log((n - df + 0.5) / (df + 0.5) + 1.0)


def bm25_score_doc(query_terms: list[str], doc: Document,
                   idf_cache: dict[str, float], avgdl: float) -> tuple[float, list[str]]:
    """Compute BM25 score for a single document against query terms."""
    score = 0.0
    matched = []
    dl = doc.word_count

    for term in query_terms:
        idf = idf_cache.get(term, 0.0)
        if idf == 0.0:
            continue

        # Term frequency in document
        tf = doc.words.count(term)
        if tf == 0:
            # Check partial match (prefix) for compound terms
            tf = sum(1 for w in doc.words if w.startswith(term) or term.startswith(w))
            if tf == 0:
                continue
            tf *= 0.5  # partial match penalty

        matched.append(term)

        # BM25 TF component with saturation and length normalization
        numerator = tf * (K1 + 1)
        denominator = tf + K1 * (1 - B + B * (dl / avgdl)) if avgdl > 0 else tf + K1
        score += idf * (numerator / denominator)

    return score, matched


MATURITY_BOOSTS = {"core": 1.3, "validated": 1.1}


def metadata_score(doc: Document) -> float:
    """Compute metadata-based score multiplier (existing STOPA formula)."""
    if doc.source_type != "learning":
        # Non-learning docs get neutral metadata score
        return 1.0

    severity_w = SEVERITY_WEIGHTS.get(doc.severity, 2.0)
    source_w = SOURCE_WEIGHTS.get(doc.source, 1.0)
    confidence = doc.confidence

    # Time decay (halves relevance every 60 days)
    days_old = 0
    if doc.date:
        try:
            d = date.fromisoformat(doc.date)
            days_old = (date.today() - d).days
        except (ValueError, TypeError):
            days_old = 30  # default

    time_factor = 1.0 / (1.0 + days_old / 60.0)

    # Maturity boost (read directly from file to avoid adding field to Document)
    maturity_boost = 1.0
    try:
        head = doc.path.read_text(encoding="utf-8", errors="replace")[:800]
        m = re.search(r"^maturity:\s*[\"']?(\w+)[\"']?", head, re.MULTILINE)
        if m:
            maturity_boost = MATURITY_BOOSTS.get(m.group(1).lower(), 1.0)
    except OSError:
        pass

    return severity_w * source_w * confidence * time_factor * maturity_boost


# ── Query expansion ────────────────────────────────────────────────────────

def expand_query(terms: list[str]) -> list[str]:
    """Expand query with synonyms. Original terms get priority (handled in scoring)."""
    expanded = list(terms)
    for term in terms:
        if term in SYNONYMS:
            for syn in SYNONYMS[term]:
                syn_tokens = tokenize(syn)
                for st in syn_tokens:
                    if st not in expanded:
                        expanded.append(st)
    return expanded


# ── Main search ────────────────────────────────────────────────────────────

def search(query: str, top_n: int = 5, debug: bool = False,
           expand_synonyms: bool = True) -> list[SearchResult]:
    """Execute BM25 search across all memory documents."""
    docs = load_all_documents()
    if not docs:
        return []

    # Tokenize and expand query
    query_terms = tokenize(query)
    if not query_terms:
        return []

    original_terms = set(query_terms)
    if expand_synonyms:
        query_terms = expand_query(query_terms)

    if debug:
        print(f"[DEBUG] Query terms: {query_terms}")
        print(f"[DEBUG] Original: {original_terms}")
        print(f"[DEBUG] Corpus: {len(docs)} documents")

    # Pre-compute IDF for all query terms
    idf_cache = {term: compute_idf(term, docs) for term in query_terms}

    if debug:
        print(f"[DEBUG] IDF scores: {json.dumps({k: round(v, 3) for k, v in idf_cache.items() if v > 0}, indent=2)}")

    # Average document length
    avgdl = sum(d.word_count for d in docs) / len(docs) if docs else 1.0

    # Score all documents
    results = []
    for doc in docs:
        bm25, matched = bm25_score_doc(query_terms, doc, idf_cache, avgdl)
        if bm25 == 0.0:
            continue

        # Boost for matches on original (non-synonym) terms
        original_match_count = sum(1 for m in matched if m in original_terms)
        if original_match_count > 0:
            bm25 *= 1.0 + 0.2 * original_match_count

        meta = metadata_score(doc)
        combined = bm25 * meta

        results.append(SearchResult(
            doc=doc,
            bm25_score=bm25,
            metadata_score=meta,
            combined_score=combined,
            matched_terms=matched,
        ))

    # Sort by combined score
    results.sort(key=lambda r: r.combined_score, reverse=True)

    # Related expansion (1-hop)
    if results and results[0].doc.source_type == "learning":
        related_files = results[0].doc.tags  # could also use `related:` field
        # Already included via corpus — no extra action needed

    return results[:top_n]


# ── Output formatting ──────────────────────────────────────────────────────

def format_results(results: list[SearchResult], debug: bool = False,
                   as_json: bool = False) -> str:
    """Format search results for display."""
    if not results:
        return "No matches found."

    if as_json:
        data = []
        for r in results:
            data.append({
                "path": str(r.doc.path.relative_to(MEMORY_DIR)),
                "title": r.doc.title,
                "type": r.doc.source_type,
                "score": round(r.combined_score, 3),
                "bm25": round(r.bm25_score, 3),
                "meta": round(r.metadata_score, 3),
                "matched": r.matched_terms,
                "summary": r.doc.summary or r.doc.content[:120].replace("\n", " "),
                "severity": r.doc.severity,
                "confidence": r.doc.confidence,
                "tags": r.doc.tags,
            })
        return json.dumps(data, indent=2, ensure_ascii=False)

    lines = []
    lines.append(f"{'─' * 60}")
    lines.append(f" Memory Search — {len(results)} results")
    lines.append(f"{'─' * 60}")

    for i, r in enumerate(results, 1):
        rel_path = r.doc.path.relative_to(MEMORY_DIR)
        lines.append(f"\n  #{i}  [{r.doc.source_type}] {r.doc.title}")
        lines.append(f"      Path: {rel_path}")
        lines.append(f"      Score: {r.combined_score:.3f}  (BM25={r.bm25_score:.3f} x Meta={r.metadata_score:.3f})")
        lines.append(f"      Matched: {', '.join(r.matched_terms)}")

        if r.doc.summary:
            summary = r.doc.summary[:150]
            lines.append(f"      Summary: {summary}")
        else:
            snippet = r.doc.content[:150].replace("\n", " ").strip()
            lines.append(f"      Snippet: {snippet}")

        if debug:
            lines.append(f"      Severity={r.doc.severity} Source={r.doc.source} "
                         f"Confidence={r.doc.confidence} "
                         f"Uses={r.doc.uses} Date={r.doc.date}")
            lines.append(f"      Tags: {r.doc.tags}")
            lines.append(f"      Words: {r.doc.word_count}")

    lines.append(f"\n{'─' * 60}")
    return "\n".join(lines)


# ── CLI ────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="BM25-inspired search across STOPA memory system"
    )
    parser.add_argument("query", help="Search query (natural language)")
    parser.add_argument("--top", type=int, default=5, help="Number of results (default: 5)")
    parser.add_argument("--debug", action="store_true", help="Show scoring details")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument("--no-synonyms", action="store_true", help="Disable synonym expansion")

    args = parser.parse_args()

    results = search(
        query=args.query,
        top_n=args.top,
        debug=args.debug,
        expand_synonyms=not args.no_synonyms,
    )

    output = format_results(results, debug=args.debug, as_json=args.json)
    print(output)

    # Exit code: 0 if results found, 1 if empty
    sys.exit(0 if results else 1)


if __name__ == "__main__":
    main()
