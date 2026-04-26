#!/usr/bin/env python3
"""hybrid-retrieve.py — Unified hybrid search with Reciprocal Rank Fusion.

Combines up to four retrieval signals:
  1. Grep-first (keyword match via learnings YAML frontmatter)
  2. BM25 (memory-search.py full-text scoring)
  3. Graph walk (concept-graph.json 1-hop neighbor expansion)
  4. MemPalace semantic search (ChromaDB embeddings fallback)

Signal 4 triggers only when local signals return <2 results AND tier >= standard.
MemPalace results are injected as virtual learnings with source tag "mempalace".

Reranker boosts applied to fused scores:
  - Maturity boost (core=1.3, validated=1.1, draft=1.0)
  - Mentions boost (Zep-inspired, arXiv:2501.13956): log-dampened boost based on
    how many concept-graph entities reference this learning file. Hub files
    (central to knowledge graph) get up to +20% boost. Generic entities with
    >20 learning_files are excluded as noise.

RRF formula: score = Σ 1 / (k + rank_i),  k=60

Usage:
    python scripts/hybrid-retrieve.py "pipeline error handling"
    python scripts/hybrid-retrieve.py "validation" --top 8 --json
    python scripts/hybrid-retrieve.py "orchestration" --task-tier deep --debug
"""
import argparse
import json
import math
import re
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# Add hooks/lib to import path for associative_engine
STOPA_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(STOPA_ROOT / ".claude" / "hooks" / "lib"))
sys.path.insert(0, str(STOPA_ROOT / "scripts"))

RRF_K = 60  # RRF constant (standard value from Cormack et al.)
LEARNINGS_DIR = STOPA_ROOT / ".claude" / "memory" / "learnings"
METRICS_FILE = STOPA_ROOT / ".claude" / "memory" / "retrieval-metrics.jsonl"

# Files to skip in results
SKIP_FILES = frozenset({
    "critical-patterns.md", "learnings-archive.md",
    "block-manifest.json", ".gitkeep",
})


PALACE_DIR = Path.home() / ".mempalace" / "palace"


# ── Strategy selector (rule-based proxy for RL for RAG) ────────────────
# Ref: arXiv:2510.24652 — RL-trained policy selects retrieval strategy per query.
# We use rule-based heuristics derived from query length + structure as a
# zero-training proxy. Each strategy maps to per-signal weight multipliers
# applied during RRF fusion.
STRATEGY_WEIGHTS: dict[str, dict[str, float]] = {
    "grep_only":      {"grep": 1.0, "bm25": 0.0, "graph": 0.0},
    "bm25_only":      {"grep": 0.0, "bm25": 1.0, "graph": 0.0},
    "hybrid":         {"grep": 1.0, "bm25": 1.0, "graph": 1.0},  # current default
    "grep_priority":  {"grep": 1.5, "bm25": 0.7, "graph": 0.7},
    "bm25_priority":  {"grep": 0.7, "bm25": 1.5, "graph": 0.7},
    "graph_priority": {"grep": 0.8, "bm25": 0.8, "graph": 1.5},
}

_STRATEGY_GRAPH_ENTITIES: set[str] | None = None


def _load_graph_entities() -> set[str]:
    """Load lowercased concept-graph entity names for strategy selection."""
    global _STRATEGY_GRAPH_ENTITIES
    if _STRATEGY_GRAPH_ENTITIES is not None:
        return _STRATEGY_GRAPH_ENTITIES

    graph_path = STOPA_ROOT / ".claude" / "memory" / "concept-graph.json"
    if not graph_path.exists():
        _STRATEGY_GRAPH_ENTITIES = set()
        return _STRATEGY_GRAPH_ENTITIES

    try:
        graph = json.loads(graph_path.read_text(encoding="utf-8"))
        _STRATEGY_GRAPH_ENTITIES = {
            name.lower().strip()
            for name in graph.get("entities", {}).keys()
            if name and len(name.strip()) >= 3  # skip tiny noise entities
        }
    except (json.JSONDecodeError, OSError):
        _STRATEGY_GRAPH_ENTITIES = set()
    return _STRATEGY_GRAPH_ENTITIES


_FILENAME_RE = re.compile(r"\.(md|py|json|sh|yaml|yml|jsonl|toml)\b")
_QUESTION_RE = re.compile(r"^(how|why|when|what|which|where|kdy|proč|jak|co|kde)\b")


def select_strategy(query: str) -> str:
    """Pick retrieval strategy from query characteristics. Defaults to 'hybrid'.

    Heuristics (all rule-based, zero training):
      1. Query <= 2 words → grep_only (BM25 saturation adds nothing)
      2. Filename/path pattern (.md, .py, slug-style) → grep_priority
      3. Question word prefix (how/why/jak/proč) → hybrid (semantic + keyword)
      4. Known concept name from concept-graph → graph_priority
      5. Long query (>= 15 words, often auto-generated context dump) → bm25_priority
      6. Otherwise → hybrid (conservative default = current behavior)

    Returns one of: grep_only | bm25_only | hybrid | grep_priority |
                    bm25_priority | graph_priority
    """
    q = query.strip().lower()
    if not q:
        return "hybrid"

    words = re.findall(r"[a-záčďéěíňóřšťúůýž0-9_-]{2,}", q)
    n_words = len(words)

    if n_words == 0:
        return "hybrid"

    if n_words <= 2:
        return "grep_only"

    if _FILENAME_RE.search(q) or "/" in q:
        return "grep_priority"

    if _QUESTION_RE.match(q):
        return "hybrid"

    if n_words >= 15:
        return "bm25_priority"

    entities = _load_graph_entities()
    if entities:
        for word in words:
            if word in entities:
                return "graph_priority"

    return "hybrid"


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
    mentions_boost: float = 1.0  # multiplier from concept-graph mentions reranker
    # Outcome-aware retrieval (Hippo-inspired, RCL Phase 2)
    uses: int = 0
    successful_uses: int = 0
    harmful_uses: int = 0
    success_rate: float | None = None  # successful_uses / uses, None if uses == 0


# ── Mentions reranker (Zep-inspired, arXiv:2501.13956) ─────────────────
# Module-level cache — graph loaded once per process.
_MENTIONS_INDEX: dict[str, int] | None = None
_MENTIONS_MAX_FILES = 20  # entities with more learning_files than this = noise


def _build_mentions_index() -> dict[str, int]:
    """Build reverse index: filename → count of entities that reference it.

    Excludes overly generic entities (>20 learning_files) as noise — those are
    index/meta concepts that appear everywhere and carry no discriminative signal.
    """
    global _MENTIONS_INDEX
    if _MENTIONS_INDEX is not None:
        return _MENTIONS_INDEX

    graph_path = STOPA_ROOT / ".claude" / "memory" / "concept-graph.json"
    if not graph_path.exists():
        _MENTIONS_INDEX = {}
        return _MENTIONS_INDEX

    try:
        graph = json.loads(graph_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        _MENTIONS_INDEX = {}
        return _MENTIONS_INDEX

    index: dict[str, int] = {}
    for entity_data in graph.get("entities", {}).values():
        learning_files = entity_data.get("learning_files", [])
        if len(learning_files) > _MENTIONS_MAX_FILES:
            continue  # skip generic/noise entities
        for lf in learning_files:
            index[lf] = index.get(lf, 0) + 1

    _MENTIONS_INDEX = index
    return _MENTIONS_INDEX


def _mentions_boost(filename: str) -> float:
    """Return log-dampened boost multiplier based on entity mention count.

    Files referenced by many concept-graph entities are 'hubs' in the knowledge
    graph. Max boost +20% at count >= 20. No penalty for low counts.
    """
    count = _build_mentions_index().get(filename, 0)
    if count <= 0:
        return 1.0
    return 1.0 + min(0.2, math.log1p(count) / math.log1p(20) * 0.2)


# ── Signal 1: Grep-first (keyword match in YAML frontmatter) ────────────

def _is_expired(head: str) -> bool:
    """Return True if YAML frontmatter contains valid_until before today."""
    m = re.search(r"^valid_until:\s*[\"']?(\d{4}-\d{2}-\d{2})[\"']?", head, re.MULTILINE)
    if not m:
        return False
    try:
        return date.fromisoformat(m.group(1)) < date.today()
    except (ValueError, TypeError):
        return False


def _maturity_boost(head: str) -> float:
    """Return maturity boost multiplier from YAML frontmatter."""
    m = re.search(r"^maturity:\s*[\"']?(\w+)[\"']?", head, re.MULTILINE)
    if not m:
        return 1.0
    maturity = m.group(1).lower()
    return {"core": 1.3, "validated": 1.1}.get(maturity, 1.0)


def _parse_outcome_counters(head: str) -> tuple[int, int, int]:
    """Parse uses, successful_uses, harmful_uses from YAML frontmatter.

    Returns (uses, successful_uses, harmful_uses). Missing fields default to 0.
    Used for outcome-aware retrieval (Hippo-inspired): agent sees empirical
    success rate alongside the learning, informing trust decisions.
    """
    def _read(field: str) -> int:
        m = re.search(rf"^{field}:\s*(\d+)", head, re.MULTILINE)
        return int(m.group(1)) if m else 0
    return _read("uses"), _read("successful_uses"), _read("harmful_uses")


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
            head = fp.read_text(encoding="utf-8", errors="replace")[:1500]
        except OSError:
            continue

        if _is_expired(head):
            continue

        hits = sum(1 for t in terms if t in head.lower())
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
    signal_weights: dict[str, float] | None = None,
) -> list[RankedFile]:
    """Reciprocal Rank Fusion across up to four signal lists.

    signal_weights: optional per-signal multipliers (keys: grep, bm25, graph).
    Defaults to {grep:1, bm25:1, graph:1} (standard equal-weighted RRF).
    """
    if signal_weights is None:
        signal_weights = {"grep": 1.0, "bm25": 1.0, "graph": 1.0}
    w_grep = signal_weights.get("grep", 1.0)
    w_bm25 = signal_weights.get("bm25", 1.0)
    w_graph = signal_weights.get("graph", 1.0)

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

    # Compute weighted RRF score with maturity boost.
    # MemPalace stays at weight 1.0 — it's a fallback channel orthogonal to
    # the strategy decision (triggered by sparsity, not by query type).
    for rf in files.values():
        score = 0.0
        if rf.grep_rank is not None:
            score += w_grep / (RRF_K + rf.grep_rank)
        if rf.bm25_rank is not None:
            score += w_bm25 / (RRF_K + rf.bm25_rank)
        if rf.graph_rank is not None:
            score += w_graph / (RRF_K + rf.graph_rank)
        if rf.mempalace_rank is not None:
            score += 1.0 / (RRF_K + rf.mempalace_rank)

        # Apply maturity + mentions boost (local files only — virtual mp: entries skip)
        if not rf.filename.startswith("mp:"):
            fp = LEARNINGS_DIR / rf.filename
            try:
                head = fp.read_text(encoding="utf-8", errors="replace")[:1500]
                score *= _maturity_boost(head)
                # Outcome-aware retrieval: surface empirical success rate to caller
                rf.uses, rf.successful_uses, rf.harmful_uses = _parse_outcome_counters(head)
                if rf.uses > 0:
                    rf.success_rate = round(rf.successful_uses / rf.uses, 2)
            except OSError:
                pass
            rf.mentions_boost = _mentions_boost(rf.filename)
            score *= rf.mentions_boost

        rf.rrf_score = score

    ranked = sorted(files.values(), key=lambda x: -x.rrf_score)
    return ranked[:top_n]


# ── Context Awareness Gate (arXiv:2411.16133) ───────────────────────────

# Pure expression: digits, whitespace, basic math/comparison ops, parens.
_NUMERIC_RE = re.compile(r"^[\d\s+\-*/().=<>!^%]+$")


def context_awareness_gate(query: str) -> tuple[bool, str]:
    """Pre-filter: decide whether retrieval is likely to help this query.

    Conservative — defaults to retrieve. Skips only on strong signals that
    past learnings cannot help (trivial queries, pure arithmetic, code-only
    snippets without natural language).

    Returns (should_retrieve, reason). The reason is logged to metrics so
    skip rate vs. accuracy can be tuned later from real data.

    Reference: arXiv:2411.16133 — Context Awareness Gate for conditional RAG.
    """
    q = query.strip()

    if len(q) < 3:
        return False, "trivial query (<3 chars)"

    if _NUMERIC_RE.match(q):
        return False, "pure numeric/arithmetic"

    # Code-like density heuristic: queries dominated by punctuation/symbols
    # and lacking natural language alpha runs are usually self-contained
    # transformations (regex tweaks, JSON snippets) where learnings won't help.
    if len(q) >= 12:
        alpha_chars = sum(1 for c in q if c.isalpha())
        if alpha_chars / len(q) < 0.35:
            return False, "code-like (low alpha density)"

    return True, "proceed"


# ── Main entry point ────────────────────────────────────────────────────

def hybrid_search(
    query: str,
    task_tier: str = "standard",
    top_n: int = 8,
    debug: bool = False,
    mode: str = "standard",
    use_gate: bool = True,
    use_strategy: bool = False,
) -> list[RankedFile]:
    """Run hybrid retrieval with tiered triggering.

    light tier + grep >= 3 hits → grep only (fast path)
    standard/deep → full hybrid (grep + BM25 + graph → RRF)
    mode='aggregate' → return ALL matching results (ignores top_n)
    use_gate=True → run context-awareness pre-filter (arXiv:2411.16133)
    use_strategy=True → run rule-based strategy selector (arXiv:2510.24652 proxy)
    """
    # Signal 0: Context awareness gate (arXiv:2411.16133)
    # Skip retrieval entirely for queries where it cannot help (trivial,
    # arithmetic, code-only). Conservative — defaults to retrieve.
    if use_gate:
        proceed, gate_reason = context_awareness_gate(query)
        if not proceed:
            if debug:
                print(f"[GATE] skip: {gate_reason}")
            return []
        elif debug:
            print(f"[GATE] proceed: {gate_reason}")

    # Strategy selection (rule-based proxy for arXiv:2510.24652)
    # When enabled, picks per-signal weights AND skips signals with weight 0.
    strategy = "hybrid"
    weights = {"grep": 1.0, "bm25": 1.0, "graph": 1.0}
    if use_strategy:
        strategy = select_strategy(query)
        weights = STRATEGY_WEIGHTS[strategy]
        if debug:
            print(f"[STRATEGY] {strategy} weights={weights}")

    skip_grep = use_strategy and weights["grep"] == 0.0
    skip_bm25 = use_strategy and weights["bm25"] == 0.0
    skip_graph = use_strategy and weights["graph"] == 0.0

    # Signals 1-2 run in parallel (Combee-inspired, arXiv:2604.04247)
    # Signal 3 (graph) depends on 1+2 seeds, so runs after.
    t0 = time.monotonic()
    grep_results: list[str] = []
    bm25_results: list[str] = []
    if skip_grep and skip_bm25:
        pass  # nothing to run
    elif skip_grep:
        bm25_results = bm25_search(query)
    elif skip_bm25:
        grep_results = grep_search(query)
    else:
        with ThreadPoolExecutor(max_workers=2, thread_name_prefix="sig") as pool:
            fut_grep = pool.submit(grep_search, query)
            fut_bm25 = pool.submit(bm25_search, query)
            grep_results = fut_grep.result()
            bm25_results = fut_bm25.result()

    if debug:
        dt = (time.monotonic() - t0) * 1000
        print(f"[GREP] {len(grep_results)} results: {grep_results[:5]}")
        print(f"[BM25] {len(bm25_results)} results: {bm25_results[:5]}")
        print(f"[PARALLEL] signals 1+2 in {dt:.0f}ms")

    # Fast path: light tier with enough grep hits
    if task_tier == "light" and len(grep_results) >= 3:
        superseded = load_superseded_set()
        limit = len(grep_results) if mode == "aggregate" else top_n
        ranked = []
        for i, f in enumerate(grep_results[:limit]):
            if f in superseded:
                continue
            rf = RankedFile(
                filename=f, grep_rank=i + 1,
                rrf_score=1.0 / (RRF_K + i + 1), sources=["grep"],
            )
            # Outcome-aware retrieval: parse counters even on fast path
            try:
                head = (LEARNINGS_DIR / f).read_text(encoding="utf-8", errors="replace")[:1500]
                rf.uses, rf.successful_uses, rf.harmful_uses = _parse_outcome_counters(head)
                if rf.uses > 0:
                    rf.success_rate = round(rf.successful_uses / rf.uses, 2)
            except OSError:
                pass
            ranked.append(rf)
        return ranked

    # Signal 3: Graph walk (seeded from grep + BM25 union).
    # Skipped when strategy weight = 0 (perf bonus for grep_only / bm25_only).
    seed_files = list(dict.fromkeys(grep_results + bm25_results))  # deduplicated, order preserved
    graph_results: list[str] = [] if skip_graph else graph_search(seed_files[:10])
    if debug:
        if skip_graph:
            print(f"[GRAPH] skipped (strategy={strategy})")
        else:
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

    # Fuse with RRF (weighted when strategy is active)
    superseded = load_superseded_set()
    effective_top_n = 9999 if mode == "aggregate" else top_n
    fused = fuse_rrf(
        grep_results, bm25_results, graph_results, superseded,
        effective_top_n, mp_results,
        signal_weights=weights if use_strategy else None,
    )

    if debug:
        print(f"[RRF] {len(fused)} fused results:")
        for rf in fused:
            extra = f" [{rf.mempalace_content[:60]}...]" if rf.mempalace_content else ""
            mb = f" m×{rf.mentions_boost:.2f}" if rf.mentions_boost != 1.0 else ""
            print(f"  {rf.rrf_score:.5f} [{'+'.join(rf.sources)}]{mb} {rf.filename}{extra}")

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
    parser.add_argument("--mode", default="standard", choices=["standard", "aggregate"],
                        help="standard: apply --top limit; aggregate: return all matches")
    parser.add_argument("--no-gate", action="store_true",
                        help="Disable context-awareness gate (arXiv:2411.16133)")
    parser.add_argument("--use-strategy", action="store_true",
                        help="Enable rule-based strategy selector (arXiv:2510.24652 proxy)")

    args = parser.parse_args()

    # Run gate first so we can log skip decisions even when retrieval is bypassed
    use_gate = not args.no_gate
    gate_proceed, gate_reason = (True, "disabled") if not use_gate else context_awareness_gate(args.query)

    # Compute strategy upfront so we can log it even when retrieval is bypassed
    strategy_label = "disabled"
    if args.use_strategy and gate_proceed:
        strategy_label = select_strategy(args.query)

    t_start = time.perf_counter()
    results = hybrid_search(
        query=args.query,
        task_tier=args.task_tier,
        top_n=args.top,
        debug=args.debug,
        mode=args.mode,
        use_gate=use_gate,
        use_strategy=args.use_strategy,
    )
    duration_ms = int((time.perf_counter() - t_start) * 1000)

    # Phase C instrumentation (ADR 0016) — log per-query metrics for
    # threshold evaluation (re-evaluate July 2026: miss rate > 8% or p95 > 300ms → vectors)
    try:
        signal_set: set[str] = set()
        for rf in results:
            signal_set.update(rf.sources)
        metrics_entry = {
            "ts": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "query": args.query[:120],
            "task_tier": args.task_tier,
            "result_count": len(results),
            "miss": len(results) == 0,
            "duration_ms": duration_ms,
            "top_score": round(results[0].rrf_score, 6) if results else 0.0,
            "signals": sorted(signal_set),
            "gate_proceed": gate_proceed,
            "gate_reason": gate_reason,
            "strategy": strategy_label,
        }
        METRICS_FILE.parent.mkdir(parents=True, exist_ok=True)
        with METRICS_FILE.open("a", encoding="utf-8") as f:
            f.write(json.dumps(metrics_entry, ensure_ascii=False) + "\n")
    except Exception:
        # Metrics logging must never break retrieval
        pass

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
                "mentions_boost": round(rf.mentions_boost, 3),
                "uses": rf.uses,
                "successful_uses": rf.successful_uses,
                "harmful_uses": rf.harmful_uses,
                "success_rate": rf.success_rate,
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
                # Outcome suffix: empirical success rate when uses > 0
                outcome = ""
                if rf.uses > 0:
                    outcome = f" [{rf.successful_uses}/{rf.uses} succ"
                    if rf.harmful_uses > 0:
                        outcome += f", {rf.harmful_uses} harm"
                    outcome += "]"
                print(f"  {i}. [{rf.rrf_score:.5f}] ({signals}){outcome} {rf.filename}")

    sys.exit(0 if results else 1)


if __name__ == "__main__":
    main()
