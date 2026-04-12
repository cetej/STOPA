#!/usr/bin/env python3
"""hybrid-retrieve.py — Unified hybrid search with Reciprocal Rank Fusion.

Combines up to four retrieval signals:
  1. Grep-first (keyword match via learnings YAML frontmatter)
  2. BM25 (memory-search.py full-text scoring)
  3. Graph walk (concept-graph.json 1-hop neighbor expansion)
  4. MemPalace semantic search (ChromaDB embeddings fallback)

Signal 4 triggers only when local signals return <2 results AND tier >= standard.
MemPalace results are injected as virtual learnings with source tag "mempalace".

RRF formula: score = Σ 1 / (k + rank_i),  k=60

Usage:
    python scripts/hybrid-retrieve.py "pipeline error handling"
    python scripts/hybrid-retrieve.py "validation" --top 8 --json
    python scripts/hybrid-retrieve.py "orchestration" --task-tier deep --debug
"""
import argparse
import json
import re
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# Add hooks/lib to import path for associative_engine
STOPA_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(STOPA_ROOT / ".claude" / "hooks" / "lib"))
sys.path.insert(0, str(STOPA_ROOT / "scripts"))

RRF_K = 60  # RRF constant (standard value from Cormack et al.)
LEARNINGS_DIR = STOPA_ROOT / ".claude" / "memory" / "learnings"

# Files to skip in results
SKIP_FILES = frozenset({
    "critical-patterns.md", "learnings-archive.md",
    "block-manifest.json", ".gitkeep",
})


PALACE_DIR = Path.home() / ".mempalace" / "palace"


@dataclass
class RankedFile:
    """A learning file with scores from each signal."""
    filename: str
    grep_rank: int | None = None
    bm25_rank: int | None = None
    graph_rank: int | None = None
    mempalace_rank: int | None = None
    rrf_score: float = 0.0
    sources: list[str] = field(default_factory=list)
    mempalace_content: str | None = None  # verbatim snippet from MemPalace


# ── Signal 1: Grep-first (keyword match in YAML frontmatter) ────────────

def grep_search(query: str, max_results: int = 15) -> list[str]:
    """Fast keyword scan across learning filenames, tags, component, summary."""
    if not LEARNINGS_DIR.exists():
        return []

    terms = [t.lower() for t in re.findall(r"[a-zA-Z0-9_-]{3,}", query)]
    if not terms:
        return []

    scored: dict[str, int] = {}  # filename → match count

    for fp in LEARNINGS_DIR.glob("*.md"):
        if fp.name in SKIP_FILES or fp.name.startswith("index-"):
            continue
        try:
            head = fp.read_text(encoding="utf-8", errors="replace")[:1500].lower()
        except OSError:
            continue

        hits = sum(1 for t in terms if t in head)
        if hits > 0:
            scored[fp.name] = hits

    ranked = sorted(scored.items(), key=lambda x: -x[1])
    return [name for name, _ in ranked[:max_results]]


# ── Signal 2: BM25 (import from memory-search.py) ──────────────────────

def bm25_search(query: str, max_results: int = 15) -> list[str]:
    """Run BM25 search via memory-search.py."""
    try:
        from importlib.util import spec_from_file_location, module_from_spec
        spec = spec_from_file_location(
            "memory_search",
            str(STOPA_ROOT / "scripts" / "memory-search.py"),
        )
        mod = module_from_spec(spec)
        spec.loader.exec_module(mod)
        results = mod.search(query, top_n=max_results, expand_synonyms=True)
        return [r.doc.path.name for r in results if r.doc.source_type == "learning"]
    except Exception as e:
        print(f"[WARN] BM25 signal unavailable: {e}", file=sys.stderr)
        return []


# ── Signal 3: Graph walk (concept-graph.json 1-hop) ────────────────────

def graph_search(seed_files: list[str], max_results: int = 10) -> list[str]:
    """Expand seed files via 1-hop graph walk in concept-graph.json."""
    try:
        from associative_engine import graph_walk_from_files, load_graph

        graph = load_graph()
        if not graph.get("entities"):
            return []

        # Check staleness (>7 days = skip)
        last_build = graph.get("meta", {}).get("last_build", "")
        if last_build:
            try:
                build_time = time.mktime(time.strptime(last_build[:19], "%Y-%m-%dT%H:%M:%S"))
                if (time.time() - build_time) > 7 * 86400:
                    print("[WARN] concept-graph.json older than 7 days, skipping graph walk", file=sys.stderr)
                    return []
            except (ValueError, OverflowError):
                pass

        return graph_walk_from_files(seed_files, graph, max_new=max_results)
    except Exception as e:
        print(f"[WARN] Graph signal unavailable: {e}", file=sys.stderr)
        return []


# ── Signal 4: MemPalace semantic search (fallback) ────────────────────

def mempalace_search(query: str, max_results: int = 5) -> list[tuple[str, str]]:
    """Search MemPalace for semantically similar content.

    Returns list of (virtual_filename, content_snippet) tuples.
    Virtual filenames use 'mp:' prefix to distinguish from local learnings.
    """
    if not PALACE_DIR.exists():
        return []

    try:
        from mempalace.palace import get_collection

        collection = get_collection(str(PALACE_DIR))
        if collection.count() == 0:
            return []

        # Detect project wing from cwd
        wing = Path.cwd().name.lower()

        # Query with wing filter first, fallback to unfiltered
        where_filter = {"wing": wing}
        try:
            results = collection.query(
                query_texts=[query],
                n_results=min(max_results, collection.count()),
                where=where_filter,
            )
        except Exception:
            # Wing filter failed (no matches for wing) — try without filter
            results = collection.query(
                query_texts=[query],
                n_results=min(max_results, collection.count()),
            )

        if not results or not results.get("documents") or not results["documents"][0]:
            return []

        output = []
        docs = results["documents"][0]
        ids = results["ids"][0] if results.get("ids") else [f"mp-{i}" for i in range(len(docs))]
        distances = results["distances"][0] if results.get("distances") else [0.5] * len(docs)

        for doc_id, doc, dist in zip(ids, docs, distances):
            # Skip low-similarity results (distance > 1.2 = very dissimilar)
            if dist > 1.2:
                continue
            # Truncate content to ~500 chars for context efficiency
            snippet = doc[:500] + "..." if len(doc) > 500 else doc
            virtual_name = f"mp:{doc_id}"
            output.append((virtual_name, snippet))

        return output
    except ImportError:
        return []
    except Exception as e:
        print(f"[WARN] MemPalace signal unavailable: {e}", file=sys.stderr)
        return []


# ── Supersedes filtering ────────────────────────────────────────────────

def load_superseded_set() -> set[str]:
    """Load set of superseded filenames from block-manifest or direct scan."""
    manifest_path = LEARNINGS_DIR / "block-manifest.json"
    if manifest_path.exists():
        try:
            data = json.loads(manifest_path.read_text(encoding="utf-8"))
            return set(data.get("superseded_ids", []))
        except (json.JSONDecodeError, OSError):
            pass

    # Fallback: scan for supersedes: fields
    superseded = set()
    for fp in LEARNINGS_DIR.glob("*.md"):
        try:
            head = fp.read_text(encoding="utf-8", errors="replace")[:800]
            m = re.search(r"^supersedes:\s*[\"']?(.+?)[\"']?\s*$", head, re.MULTILINE)
            if m:
                superseded.add(m.group(1).strip())
        except OSError:
            pass
    return superseded


# ── RRF Fusion ──────────────────────────────────────────────────────────

def fuse_rrf(
    grep_results: list[str],
    bm25_results: list[str],
    graph_results: list[str],
    superseded: set[str],
    top_n: int = 8,
    mempalace_results: list[tuple[str, str]] | None = None,
) -> list[RankedFile]:
    """Reciprocal Rank Fusion across up to four signal lists."""
    files: dict[str, RankedFile] = {}

    def ensure(name: str) -> RankedFile:
        if name not in files:
            files[name] = RankedFile(filename=name)
        return files[name]

    # Assign ranks per signal
    for rank, name in enumerate(grep_results, 1):
        if name in superseded:
            continue
        rf = ensure(name)
        rf.grep_rank = rank
        rf.sources.append("grep")

    for rank, name in enumerate(bm25_results, 1):
        if name in superseded:
            continue
        rf = ensure(name)
        rf.bm25_rank = rank
        rf.sources.append("bm25")

    for rank, name in enumerate(graph_results, 1):
        if name in superseded:
            continue
        rf = ensure(name)
        rf.graph_rank = rank
        rf.sources.append("graph")

    # Signal 4: MemPalace (virtual entries, not subject to supersedes)
    if mempalace_results:
        for rank, (vname, snippet) in enumerate(mempalace_results, 1):
            rf = ensure(vname)
            rf.mempalace_rank = rank
            rf.mempalace_content = snippet
            rf.sources.append("mempalace")

    # Compute RRF score
    for rf in files.values():
        score = 0.0
        if rf.grep_rank is not None:
            score += 1.0 / (RRF_K + rf.grep_rank)
        if rf.bm25_rank is not None:
            score += 1.0 / (RRF_K + rf.bm25_rank)
        if rf.graph_rank is not None:
            score += 1.0 / (RRF_K + rf.graph_rank)
        if rf.mempalace_rank is not None:
            score += 1.0 / (RRF_K + rf.mempalace_rank)
        rf.rrf_score = score

    ranked = sorted(files.values(), key=lambda x: -x.rrf_score)
    return ranked[:top_n]


# ── Main entry point ────────────────────────────────────────────────────

def hybrid_search(
    query: str,
    task_tier: str = "standard",
    top_n: int = 8,
    debug: bool = False,
) -> list[RankedFile]:
    """Run hybrid retrieval with tiered triggering.

    light tier + grep >= 3 hits → grep only (fast path)
    standard/deep → full hybrid (grep + BM25 + graph → RRF)
    """
    # Signal 1: grep (always runs)
    grep_results = grep_search(query)

    if debug:
        print(f"[GREP] {len(grep_results)} results: {grep_results[:5]}")

    # Fast path: light tier with enough grep hits
    if task_tier == "light" and len(grep_results) >= 3:
        superseded = load_superseded_set()
        return [
            RankedFile(filename=f, grep_rank=i + 1, rrf_score=1.0 / (RRF_K + i + 1), sources=["grep"])
            for i, f in enumerate(grep_results[:top_n])
            if f not in superseded
        ]

    # Signal 2: BM25
    bm25_results = bm25_search(query)
    if debug:
        print(f"[BM25] {len(bm25_results)} results: {bm25_results[:5]}")

    # Signal 3: Graph walk (seeded from grep + BM25 union)
    seed_files = list(dict.fromkeys(grep_results + bm25_results))  # deduplicated, order preserved
    graph_results = graph_search(seed_files[:10])
    if debug:
        print(f"[GRAPH] {len(graph_results)} results: {graph_results[:5]}")

    # Signal 4: MemPalace semantic fallback
    # Triggers when local signals are sparse (<2 unique results) AND tier >= standard
    local_unique = len(set(grep_results + bm25_results + graph_results))
    mp_results: list[tuple[str, str]] | None = None

    if local_unique < 2 and task_tier in ("standard", "deep", "farm"):
        mp_results = mempalace_search(query)
        if debug:
            print(f"[MEMPALACE] {len(mp_results)} results (fallback triggered, local={local_unique})")
    elif task_tier == "deep":
        # Deep tier always queries MemPalace for maximum recall
        mp_results = mempalace_search(query)
        if debug:
            print(f"[MEMPALACE] {len(mp_results)} results (deep tier, always-on)")
    elif debug:
        print(f"[MEMPALACE] skipped (local={local_unique}, tier={task_tier})")

    # Fuse with RRF
    superseded = load_superseded_set()
    fused = fuse_rrf(grep_results, bm25_results, graph_results, superseded, top_n, mp_results)

    if debug:
        print(f"[RRF] {len(fused)} fused results:")
        for rf in fused:
            extra = f" [{rf.mempalace_content[:60]}...]" if rf.mempalace_content else ""
            print(f"  {rf.rrf_score:.5f} [{'+'.join(rf.sources)}] {rf.filename}{extra}")

    return fused


# ── CLI ──────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Hybrid memory retrieval with Reciprocal Rank Fusion"
    )
    parser.add_argument("query", help="Search query (natural language)")
    parser.add_argument("--top", type=int, default=8, help="Number of results (default: 8)")
    parser.add_argument("--task-tier", default="standard",
                        choices=["light", "standard", "deep", "farm"],
                        help="Task tier (affects triggering)")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument("--debug", action="store_true", help="Show per-signal details")

    args = parser.parse_args()

    results = hybrid_search(
        query=args.query,
        task_tier=args.task_tier,
        top_n=args.top,
        debug=args.debug,
    )

    if args.json:
        data = []
        for rf in results:
            entry = {
                "filename": rf.filename,
                "rrf_score": round(rf.rrf_score, 6),
                "sources": rf.sources,
                "grep_rank": rf.grep_rank,
                "bm25_rank": rf.bm25_rank,
                "graph_rank": rf.graph_rank,
                "mempalace_rank": rf.mempalace_rank,
            }
            if rf.mempalace_content:
                entry["mempalace_snippet"] = rf.mempalace_content[:300]
            data.append(entry)
        print(json.dumps(data, ensure_ascii=False, indent=2))
    else:
        if not results:
            print("No matches found.")
        else:
            print(f"Hybrid search: {len(results)} results (RRF k={RRF_K})\n")
            for i, rf in enumerate(results, 1):
                signals = "+".join(rf.sources)
                print(f"  {i}. [{rf.rrf_score:.5f}] ({signals}) {rf.filename}")

    sys.exit(0 if results else 1)


if __name__ == "__main__":
    main()
