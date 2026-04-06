#!/usr/bin/env python3
"""Associative Memory Engine — file-based spreading activation.

Hippocampus-inspired (Phase 2): concept graph stored as JSON,
spreading activation for contextual recall, no external DB required.

Architecture:
  concept-graph.json  →  in-memory load  →  keyword seed  →  spread activation
       (entities + edges)                     (2 hops)        →  ranked results
                                                               →  map to learnings

Key constants (from hippocampus, tuned for file-based):
  MAX_SEEDS = 7, MAX_HOPS = 2, SPREAD_DECAY = 0.3
  ACTIVATION_THRESHOLD = 0.15, MAX_NEIGHBORS = 20
  RECENCY_LAMBDA = 0.03 (half-life ~23 days)
"""
import json
import math
import re
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# --- Constants (hippocampus-aligned) ---
MAX_SEEDS = 7
MAX_SPREAD_HOPS = 2
SPREAD_DECAY = 0.3
ACTIVATION_THRESHOLD = 0.15
MIN_EDGE_WEIGHT = 0.5
MAX_NEIGHBORS_PER_HOP = 20
MAX_ACTIVATED = 15
CONTEXT_PACKET_MAX_TOKENS = 1200
RECENCY_LAMBDA = 0.03  # half-life ~23 days

GRAPH_PATH = Path(".claude/memory/concept-graph.json")
LEARNINGS_DIR = Path(".claude/memory/learnings")

# Entity name noise filters (from hippocampus)
SKIP_PREFIXES = ("/Users/", "/tmp/", "/private/", "/var/",
                 "http://", "https://", "/workspace/", "C:\\")

STOPWORDS = frozenset({
    "the", "a", "an", "is", "are", "was", "were", "be", "been",
    "have", "has", "had", "do", "does", "did", "will", "would",
    "could", "should", "may", "might", "shall", "can", "need",
    "and", "or", "but", "if", "then", "else", "when", "where",
    "how", "what", "which", "who", "this", "that", "these",
    "not", "no", "so", "too", "very", "just", "also",
    "for", "from", "with", "about", "into", "through", "during",
    "to", "in", "on", "at", "by", "of", "up", "it", "its",
    "my", "your", "his", "her", "our", "their", "me", "him",
    "use", "using", "used", "make", "get", "set", "run", "add",
    # Czech
    "je", "jsou", "byl", "jak", "kde", "kdy", "co", "na", "ve",
    "za", "do", "od", "po", "pro", "ten", "ta", "to", "ale", "nebo",
})

# Tech patterns for concept extraction (from hippocampus)
TECH_PATTERNS = re.compile(
    r"\b(Rust|Python|JavaScript|TypeScript|Go|Java|Ruby|Swift|C\+\+|"
    r"React|Vue|Angular|FastAPI|Flask|Django|Express|Next\.js|Svelte|"
    r"Redis|Neo4j|PostgreSQL|SQLite|MongoDB|MySQL|"
    r"Docker|Kubernetes|CI/CD|GitHub|GitLab|npm|pip|cargo|"
    r"JWT|OAuth|CORS|SSL|TLS|REST|GraphQL|gRPC|WebSocket|"
    r"SVG|Canvas|WebGL|Three\.js|D3\.js|"
    r"WASM|WebAssembly|Terraform|Ansible|Nginx|Apache)\b",
    re.IGNORECASE,
)


@dataclass
class ActivatedNode:
    """Result of spreading activation."""
    entity_id: str
    name: str
    activation: float
    source: str = ""  # "seed" or "spread"
    entity_type: str = "concept"
    learning_files: list = field(default_factory=list)


# --- Concept Extraction ---

def extract_concepts(text: str) -> list[str]:
    """Extract concepts from text using regex patterns (no LLM).

    Patterns from hippocampus:
    1. Multi-word capitalized phrases (Named Entities)
    2. Hyphenated terms (wasm-pack, docker-compose)
    3. CamelCase identifiers
    4. Known tech patterns
    5. Error types (ValueError, TypeError)
    """
    concepts = set()

    # 1. Multi-word capitalized (2-4 words)
    for m in re.finditer(r"[A-Z][a-z]+(?:\s+[A-Z][a-z]+){1,3}", text):
        concepts.add(m.group())

    # 2. Hyphenated terms
    for m in re.finditer(r"[a-zA-Z]+-[a-zA-Z]+(?:-[a-zA-Z]+)*", text):
        term = m.group()
        if len(term) > 4 and term.lower() not in STOPWORDS:
            concepts.add(term.lower())

    # 3. CamelCase
    for m in re.finditer(r"[A-Z][a-z]+[A-Z][a-zA-Z]+", text):
        concepts.add(m.group())

    # 4. Tech patterns
    for m in TECH_PATTERNS.finditer(text):
        concepts.add(m.group())

    # 5. Error types
    for m in re.finditer(r"\w+Error|\w+Exception", text):
        concepts.add(m.group())

    # Filter noise
    filtered = set()
    for c in concepts:
        if len(c) < 3 or len(c) > 80:
            continue
        if any(c.startswith(p) for p in SKIP_PREFIXES):
            continue
        if c.lower() in STOPWORDS:
            continue
        filtered.add(c)

    return sorted(filtered)


def extract_keywords(text: str, max_keywords: int = 7) -> list[str]:
    """Extract search keywords from user prompt.

    Returns singles (longest first) + bigrams, like hippocampus.
    """
    words = re.findall(r"[a-zA-Z0-9_-]{3,}", text.lower())
    words = [w for w in words if w not in STOPWORDS and len(w) >= 3]

    # Deduplicate preserving order
    seen = set()
    unique = []
    for w in words:
        if w not in seen:
            seen.add(w)
            unique.append(w)

    # Singles: top 5 longest (prefer specificity)
    singles = sorted(unique, key=len, reverse=True)[:5]

    # Bigrams: adjacent meaningful tokens
    bigrams = []
    for i in range(len(unique) - 1):
        bg = f"{unique[i]} {unique[i+1]}"
        if bg not in seen:
            bigrams.append(bg)
            seen.add(bg)
    bigrams = bigrams[:3]

    result = list(dict.fromkeys(singles + bigrams))  # deduplicated
    return result[:max_keywords]


# --- Graph I/O ---

def load_graph() -> dict:
    """Load concept graph from JSON. Returns empty structure if missing."""
    if not GRAPH_PATH.exists():
        return {"entities": {}, "edges": {}, "meta": {"last_build": ""}}
    try:
        return json.loads(GRAPH_PATH.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {"entities": {}, "edges": {}, "meta": {"last_build": ""}}


def save_graph(graph: dict) -> None:
    """Save concept graph to JSON."""
    GRAPH_PATH.parent.mkdir(parents=True, exist_ok=True)
    graph["meta"]["last_build"] = time.strftime("%Y-%m-%dT%H:%M:%S")
    GRAPH_PATH.write_text(
        json.dumps(graph, ensure_ascii=False, indent=1),
        encoding="utf-8",
    )


# --- Graph Building ---

def build_graph_from_learnings() -> dict:
    """Build concept graph from all learnings (one-time + incremental).

    Entities: concepts extracted from learning tags + body.
    Edges: co-occurrence within same learning file (Hebbian).
    """
    graph = load_graph()
    entities = graph.get("entities", {})
    edges = graph.get("edges", {})

    if not LEARNINGS_DIR.exists():
        return graph

    skip_files = {"critical-patterns.md", "index-general.md",
                  "block-manifest.json", "ecosystem-scan.md"}

    for f in LEARNINGS_DIR.glob("*.md"):
        if f.name in skip_files:
            continue
        try:
            content = f.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue

        # Extract concepts from full content
        concepts = extract_concepts(content)

        # Also include YAML tags as concepts
        tags_match = re.search(r"^tags:\s*\[?(.+?)\]?\s*$", content, re.MULTILINE)
        if tags_match:
            tags = [t.strip().strip("'\"") for t in tags_match.group(1).split(",")]
            concepts.extend([t for t in tags if len(t) >= 3])

        # Include component as concept
        comp_match = re.search(r"^component:\s*(.+)$", content, re.MULTILINE)
        if comp_match:
            concepts.append(comp_match.group(1).strip())

        # Deduplicate
        concepts = list(dict.fromkeys(c for c in concepts if c))

        # Parse date for recency
        date_match = re.search(r"^date:\s*(\d{4}-\d{2}-\d{2})", content, re.MULTILINE)
        date_str = date_match.group(1) if date_match else ""

        # Create/update entity nodes
        for concept in concepts:
            eid = concept.lower().replace(" ", "-")
            if eid not in entities:
                entities[eid] = {
                    "name": concept,
                    "type": "concept",
                    "mentions": 0,
                    "last_seen": "",
                    "learning_files": [],
                }
            entities[eid]["mentions"] += 1
            if date_str > entities[eid].get("last_seen", ""):
                entities[eid]["last_seen"] = date_str
            if f.name not in entities[eid].get("learning_files", []):
                entities[eid].setdefault("learning_files", []).append(f.name)
                # Cap at 20 files per entity
                entities[eid]["learning_files"] = entities[eid]["learning_files"][-20:]

        # Build co-occurrence edges (Hebbian: fire together, wire together)
        for i, c1 in enumerate(concepts):
            for c2 in concepts[i + 1:]:
                eid1 = c1.lower().replace(" ", "-")
                eid2 = c2.lower().replace(" ", "-")
                edge_key = f"{min(eid1, eid2)}|{max(eid1, eid2)}"

                if edge_key not in edges:
                    edges[edge_key] = {
                        "weight": 0.0,
                        "count": 0,
                        "last_ts": "",
                        "contexts": [],
                    }

                edge = edges[edge_key]
                edge["count"] += 1
                if date_str > edge.get("last_ts", ""):
                    edge["last_ts"] = date_str

                # Compute weight with recency decay (hippocampus formula)
                if edge["last_ts"]:
                    try:
                        days = (time.time() - time.mktime(
                            time.strptime(edge["last_ts"], "%Y-%m-%d")
                        )) / 86400
                        edge["weight"] = edge["count"] * math.exp(-RECENCY_LAMBDA * days)
                    except (ValueError, OverflowError):
                        edge["weight"] = float(edge["count"])
                else:
                    edge["weight"] = float(edge["count"])

    graph["entities"] = entities
    graph["edges"] = edges
    return graph


# --- Spreading Activation ---

def activate(cue: str, workspace: str = "", graph: dict = None) -> list[ActivatedNode]:
    """Run spreading activation on concept graph.

    1. Extract keywords from cue
    2. Seed: match keywords → entities
    3. Spread: 2 hops, decay 0.3, threshold 0.15
    4. Rank: activation × recency × workspace context
    5. Map back to learning files
    """
    if graph is None:
        graph = load_graph()

    entities = graph.get("entities", {})
    edges = graph.get("edges", {})

    if not entities:
        return []

    keywords = extract_keywords(cue)
    if not keywords:
        return []

    # --- Phase 1: Seed ---
    activation = {}
    entity_data = {}

    for kw in keywords:
        for eid, ent in entities.items():
            if kw in eid or kw in ent.get("name", "").lower():
                if eid not in activation:
                    activation[eid] = 0.0
                    entity_data[eid] = ent
                activation[eid] = min(1.0, activation[eid] + 0.3)

    # Keep top MAX_SEEDS by activation
    if len(activation) > MAX_SEEDS:
        top_seeds = sorted(activation.items(), key=lambda x: -x[1])[:MAX_SEEDS]
        activation = dict(top_seeds)

    if not activation:
        return []

    # --- Phase 2: Spread ---
    visited = set(activation.keys())

    for hop in range(MAX_SPREAD_HOPS):
        frontier = {
            eid: score for eid, score in activation.items()
            if score >= ACTIVATION_THRESHOLD
        }
        if not frontier:
            break

        new_activations = {}
        for eid in frontier:
            # Find edges connected to this entity
            neighbors = []
            for edge_key, edge in edges.items():
                parts = edge_key.split("|")
                if len(parts) != 2:
                    continue
                if eid in parts:
                    neighbor = parts[1] if parts[0] == eid else parts[0]
                    if neighbor in visited:
                        continue
                    if edge.get("weight", 0) < MIN_EDGE_WEIGHT:
                        continue
                    # Workspace context boost (hippocampus pattern)
                    context_boost = 1.0
                    if workspace:
                        ws_name = Path(workspace).name.lower()
                        for ctx in edge.get("contexts", []):
                            if ws_name in ctx.lower():
                                context_boost = 1.5
                                break
                    neighbors.append((neighbor, edge["weight"] * context_boost))

            # Sort by effective weight, take top N
            neighbors.sort(key=lambda x: -x[1])
            max_weight = neighbors[0][1] if neighbors else 1.0

            for neighbor, eff_weight in neighbors[:MAX_NEIGHBORS_PER_HOP]:
                normalized = eff_weight / max_weight if max_weight > 0 else 0
                spread = frontier[eid] * SPREAD_DECAY * normalized

                if spread >= ACTIVATION_THRESHOLD:
                    if neighbor not in new_activations or new_activations[neighbor] < spread:
                        new_activations[neighbor] = spread
                    if neighbor in entities:
                        entity_data[neighbor] = entities[neighbor]

        activation.update(new_activations)
        visited.update(new_activations.keys())

    # --- Phase 3: Rank ---
    results = []
    for eid, score in activation.items():
        if score < ACTIVATION_THRESHOLD:
            continue
        ent = entity_data.get(eid, entities.get(eid, {}))

        # Apply recency factor
        last_seen = ent.get("last_seen", "")
        recency = 1.0
        if last_seen:
            try:
                days = (time.time() - time.mktime(
                    time.strptime(last_seen, "%Y-%m-%d")
                )) / 86400
                recency = math.exp(-RECENCY_LAMBDA * max(0, days))
            except (ValueError, OverflowError):
                pass

        final_score = score * recency

        results.append(ActivatedNode(
            entity_id=eid,
            name=ent.get("name", eid),
            activation=round(final_score, 4),
            source="seed" if eid in {k for k in list(activation.keys())[:MAX_SEEDS]} else "spread",
            entity_type=ent.get("type", "concept"),
            learning_files=ent.get("learning_files", []),
        ))

    # Sort by activation descending, cap at MAX_ACTIVATED
    results.sort(key=lambda x: -x.activation)
    return results[:MAX_ACTIVATED]


# --- Graph Walk (LLM Wiki v2 Gap 1: knowledge graph → retrieval pipeline) ---

def graph_walk_from_files(
    seed_files: list[str],
    graph: dict | None = None,
    max_new: int = 6,
) -> list[str]:
    """1-hop graph walk seeded from matched learning filenames.

    seed_files → reverse lookup entities → 1-hop neighbors (weight desc)
    → return additional learning filenames not in seed set.

    Used by hybrid-retrieve.py to add graph signal to RRF pipeline.
    """
    if graph is None:
        graph = load_graph()

    entities = graph.get("entities", {})
    edges = graph.get("edges", {})
    if not entities or not seed_files:
        return []

    # Normalize seed filenames (strip path, keep basename)
    seed_basenames = {Path(f).name for f in seed_files}

    # Step 1: Reverse index — filename → entity IDs
    file_to_entities: dict[str, list[str]] = {}
    for eid, ent in entities.items():
        for lf in ent.get("learning_files", []):
            basename = Path(lf).name
            file_to_entities.setdefault(basename, []).append(eid)

    # Step 2: Collect seed entity IDs
    seed_eids: set[str] = set()
    for fname in seed_basenames:
        seed_eids.update(file_to_entities.get(fname, []))

    if not seed_eids:
        return []

    # Step 3: 1-hop neighbors sorted by edge weight
    neighbor_scores: dict[str, float] = {}  # eid → best weight
    for edge_key, edge in edges.items():
        parts = edge_key.split("|")
        if len(parts) != 2:
            continue
        w = edge.get("weight", 0)
        if w < MIN_EDGE_WEIGHT:
            continue

        a, b = parts
        if a in seed_eids and b not in seed_eids:
            neighbor_scores[b] = max(neighbor_scores.get(b, 0), w)
        elif b in seed_eids and a not in seed_eids:
            neighbor_scores[a] = max(neighbor_scores.get(a, 0), w)

    # Step 4: Collect learning files from neighbors
    ranked_neighbors = sorted(neighbor_scores.items(), key=lambda x: -x[1])
    new_files: list[str] = []
    seen: set[str] = set(seed_basenames)

    for eid, _weight in ranked_neighbors:
        ent = entities.get(eid, {})
        for lf in ent.get("learning_files", []):
            basename = Path(lf).name
            # Skip index files and already-seen
            if basename in seen or basename.startswith("index-") or basename == "critical-patterns.md":
                continue
            seen.add(basename)
            new_files.append(basename)
            if len(new_files) >= max_new:
                return new_files

    return new_files


# --- Context Packet ---

def compress_to_packet(nodes: list[ActivatedNode], max_tokens: int = CONTEXT_PACKET_MAX_TOKENS) -> str:
    """Compress activated nodes into token-budgeted context packet.

    Tiered presentation (hippocampus pattern):
    - High activation (> 0.5): full concept + learning files
    - Medium (0.2-0.5): concept name + key file
    - Low (< 0.2): names only
    """
    if not nodes:
        return ""

    lines = [f"[Associative recall — {len(nodes)} concepts activated]"]
    tokens_used = 10  # header estimate

    # High activation
    for n in nodes:
        if n.activation <= 0.5:
            continue
        files_str = ", ".join(n.learning_files[:3]) if n.learning_files else ""
        line = f"  [{n.activation:.2f}] {n.name}"
        if files_str:
            line += f" → {files_str}"
        est = len(line) // 4
        if tokens_used + est > max_tokens:
            break
        lines.append(line)
        tokens_used += est

    # Medium activation
    for n in nodes:
        if n.activation > 0.5 or n.activation <= 0.2:
            continue
        line = f"  [{n.activation:.2f}] {n.name}"
        if n.learning_files:
            line += f" → {n.learning_files[0]}"
        est = len(line) // 4
        if tokens_used + est > max_tokens * 0.85:
            break
        lines.append(line)
        tokens_used += est

    # Low activation (names only)
    low_names = [n.name for n in nodes if n.activation <= 0.2]
    if low_names and tokens_used < max_tokens * 0.95:
        line = "  Also: " + ", ".join(low_names[:8])
        lines.append(line)

    return "\n".join(lines)


# --- Graph Optimization (Phase 3e) ---

# Pruning thresholds
PRUNE_EDGE_MIN_WEIGHT = 0.05     # Remove edges below this weight
PRUNE_ENTITY_MIN_MENTIONS = 0    # Remove orphan entities with 0 connections
NORMALIZE_WEIGHT_CAP = 50.0      # Cap max edge weight to prevent runaway

def optimize_graph(graph: dict) -> dict[str, int]:
    """Run full graph optimization: decay, prune, normalize, compact.

    Returns dict with counts of each optimization action.
    """
    stats = {"decayed": 0, "edges_pruned": 0, "entities_pruned": 0, "normalized": 0}

    entities = graph.get("entities", {})
    edges = graph.get("edges", {})
    now_ts = time.time()

    # 1. Decay all edge weights based on last_ts
    for edge_key, edge in edges.items():
        last_ts = edge.get("last_ts", "")
        if not last_ts:
            continue
        try:
            days = (now_ts - time.mktime(
                time.strptime(last_ts, "%Y-%m-%d")
            )) / 86400
            new_weight = edge["count"] * math.exp(-RECENCY_LAMBDA * days)
            if new_weight != edge.get("weight", 0):
                edge["weight"] = round(new_weight, 4)
                stats["decayed"] += 1
        except (ValueError, OverflowError):
            pass

    # 2. Prune weak edges
    to_prune = [
        key for key, edge in edges.items()
        if edge.get("weight", 0) < PRUNE_EDGE_MIN_WEIGHT
    ]
    for key in to_prune:
        del edges[key]
    stats["edges_pruned"] = len(to_prune)

    # 3. Normalize edge weights (cap runaway weights)
    for edge in edges.values():
        w = edge.get("weight", 0)
        if w > NORMALIZE_WEIGHT_CAP:
            edge["weight"] = NORMALIZE_WEIGHT_CAP
            stats["normalized"] += 1

    # 4. Prune orphan entities (no edges and no learning files)
    connected = set()
    for edge_key in edges:
        parts = edge_key.split("|")
        connected.update(parts)

    orphans = [
        eid for eid, ent in entities.items()
        if eid not in connected and not ent.get("learning_files")
    ]
    for eid in orphans:
        del entities[eid]
    stats["entities_pruned"] = len(orphans)

    # 5. Compact entity data (remove empty fields)
    for ent in entities.values():
        if not ent.get("learning_files"):
            ent.pop("learning_files", None)
        if not ent.get("last_seen"):
            ent.pop("last_seen", None)

    # 6. Compact edge data (remove empty contexts)
    for edge in edges.values():
        if not edge.get("contexts"):
            edge.pop("contexts", None)
        if not edge.get("source"):
            edge.pop("source", None)
        # Round weight to 4 decimal places
        edge["weight"] = round(edge.get("weight", 0), 4)

    graph["entities"] = entities
    graph["edges"] = edges
    return stats


def graph_health(graph: dict) -> dict:
    """Compute graph health metrics for monitoring."""
    entities = graph.get("entities", {})
    edges = graph.get("edges", {})

    if not entities:
        return {"status": "empty", "entities": 0, "edges": 0}

    weights = [e.get("weight", 0) for e in edges.values()]
    mentions = [e.get("mentions", 0) for e in entities.values()]

    connected = set()
    for edge_key in edges:
        connected.update(edge_key.split("|"))

    return {
        "entities": len(entities),
        "edges": len(edges),
        "connected_ratio": round(len(connected) / max(1, len(entities)), 2),
        "avg_edge_weight": round(sum(weights) / max(1, len(weights)), 2),
        "max_edge_weight": round(max(weights, default=0), 2),
        "avg_mentions": round(sum(mentions) / max(1, len(mentions)), 1),
        "hebbian_edges": sum(1 for e in edges.values() if e.get("source") == "hebbian"),
        "last_build": graph.get("meta", {}).get("last_build", "never"),
        "last_hebbian": graph.get("meta", {}).get("last_hebbian", "never"),
    }


# --- CLI ---

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage:")
        print("  associative_engine.py build         # Build graph from learnings")
        print("  associative_engine.py activate <q>  # Test activation with query")
        print("  associative_engine.py stats          # Graph statistics")
        print("  associative_engine.py optimize       # Run graph optimization")
        print("  associative_engine.py health         # Graph health metrics")
        sys.exit(1)

    cmd = sys.argv[1]

    if cmd == "build":
        graph = build_graph_from_learnings()
        save_graph(graph)
        ent_count = len(graph["entities"])
        edge_count = len(graph["edges"])
        print(f"Graph built: {ent_count} entities, {edge_count} edges")
        print(f"Saved to {GRAPH_PATH}")

    elif cmd == "activate":
        query = " ".join(sys.argv[2:]) if len(sys.argv) > 2 else "orchestration memory"
        graph = load_graph()
        if not graph["entities"]:
            print("Graph empty — run 'build' first")
            sys.exit(1)
        nodes = activate(query, graph=graph)
        if not nodes:
            print("No activations")
        else:
            packet = compress_to_packet(nodes)
            print(packet)
            print(f"\n--- {len(nodes)} nodes activated ---")

    elif cmd == "stats":
        graph = load_graph()
        ent = graph.get("entities", {})
        edg = graph.get("edges", {})
        print(f"Entities: {len(ent)}")
        print(f"Edges: {len(edg)}")
        print(f"Last build: {graph.get('meta', {}).get('last_build', 'never')}")
        if ent:
            top = sorted(ent.items(), key=lambda x: -x[1].get("mentions", 0))[:10]
            print("\nTop 10 entities by mentions:")
            for eid, e in top:
                print(f"  {e.get('name', eid)}: {e.get('mentions', 0)} mentions, {len(e.get('learning_files', []))} files")

    elif cmd == "optimize":
        graph = load_graph()
        if not graph["entities"]:
            print("Graph empty — run 'build' first")
            sys.exit(1)
        before_ent = len(graph["entities"])
        before_edg = len(graph["edges"])
        stats = optimize_graph(graph)
        save_graph(graph)
        print(f"Before: {before_ent} entities, {before_edg} edges")
        print(f"After:  {len(graph['entities'])} entities, {len(graph['edges'])} edges")
        for k, v in stats.items():
            if v > 0:
                print(f"  {k}: {v}")

    elif cmd == "health":
        graph = load_graph()
        h = graph_health(graph)
        for k, v in h.items():
            print(f"  {k}: {v}")

    else:
        print(f"Unknown command: {cmd}")
        sys.exit(1)
