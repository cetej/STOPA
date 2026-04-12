#!/usr/bin/env python3
"""kg-sync.py — Bidirectional sync between STOPA concept-graph and MemPalace KG.

Direction A (STOPA → MemPalace):
  - Typed entities (tool, paper, person, company) → kg.add_entity()
  - High-weight co-occurrence edges (weight >= 3) → "related_to" triples
  - Entity-learning links → "mentioned_in" triples with temporal validity

Direction B (MemPalace → STOPA):
  - New MemPalace triples from session drawers → concept-graph edges
  - Invalidated triples → edge annotations in concept-graph

Usage:
    python scripts/kg-sync.py                    # bidirectional sync
    python scripts/kg-sync.py --direction a      # STOPA → MemPalace only
    python scripts/kg-sync.py --direction b      # MemPalace → STOPA only
    python scripts/kg-sync.py --dry-run          # preview changes
    python scripts/kg-sync.py --debug            # verbose output

Designed as Stop hook (runs after graph-consolidate.sh).
"""
import argparse
import json
import re
import sys
import time
from datetime import datetime
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

STOPA_ROOT = Path(__file__).resolve().parent.parent
CONCEPT_GRAPH = STOPA_ROOT / ".claude" / "memory" / "concept-graph.json"
PALACE_DIR = Path.home() / ".mempalace" / "palace"
SYNC_STATE_FILE = STOPA_ROOT / ".claude" / "memory" / "intermediate" / "kg-sync-state.json"

# Only sync entities with these types (skip generic 'concept' — too noisy)
SYNC_ENTITY_TYPES = frozenset({"tool", "paper", "person", "company"})

# Minimum co-occurrence weight to export as a triple
MIN_EDGE_WEIGHT = 3

# Predicates for different edge types
PREDICATE_MAP = {
    "co-occurrence": "related_to",
    "learning-link": "mentioned_in",
}


def load_concept_graph() -> dict:
    """Load STOPA concept-graph.json."""
    if not CONCEPT_GRAPH.exists():
        return {"entities": {}, "edges": {}, "meta": {}}
    try:
        return json.loads(CONCEPT_GRAPH.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as e:
        print(f"[WARN] Cannot load concept-graph: {e}", file=sys.stderr)
        return {"entities": {}, "edges": {}, "meta": {}}


def save_concept_graph(graph: dict) -> None:
    """Save STOPA concept-graph.json."""
    CONCEPT_GRAPH.write_text(
        json.dumps(graph, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def load_sync_state() -> dict:
    """Load last sync timestamp and counters."""
    if SYNC_STATE_FILE.exists():
        try:
            return json.loads(SYNC_STATE_FILE.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            pass
    return {"last_sync": None, "a_exported": 0, "b_imported": 0}


def save_sync_state(state: dict) -> None:
    """Persist sync state."""
    SYNC_STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    SYNC_STATE_FILE.write_text(
        json.dumps(state, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def get_mempalace_kg():
    """Get MemPalace KnowledgeGraph instance."""
    try:
        from mempalace.knowledge_graph import KnowledgeGraph
        return KnowledgeGraph()
    except ImportError:
        print("kg-sync: mempalace not installed, skipping", file=sys.stderr)
        return None
    except Exception as e:
        print(f"kg-sync: cannot init MemPalace KG: {e}", file=sys.stderr)
        return None


def extract_date_from_learning(filename: str) -> str | None:
    """Extract date from learning filename (2026-04-12-xxx.md → 2026-04-12)."""
    m = re.match(r"(\d{4}-\d{2}-\d{2})", filename)
    return m.group(1) if m else None


# ── Direction A: STOPA → MemPalace ────────────────────────────────────

def sync_stopa_to_mempalace(
    graph: dict,
    kg,
    dry_run: bool = False,
    debug: bool = False,
) -> int:
    """Export typed entities and high-weight edges to MemPalace KG."""
    entities = graph.get("entities", {})
    edges = graph.get("edges", {})
    exported = 0

    # 1. Export typed entities
    for name, data in entities.items():
        etype = data.get("type", "unknown")
        if etype not in SYNC_ENTITY_TYPES:
            continue

        if debug:
            print(f"  [A] Entity: {name} ({etype})")

        if not dry_run:
            kg.add_entity(name, entity_type=etype)

        # Add learning-link triples
        for lf in data.get("learning_files", []):
            valid_from = extract_date_from_learning(lf)
            if debug:
                print(f"    → mentioned_in {lf} (from {valid_from})")
            if not dry_run:
                kg.add_triple(
                    subject=name,
                    predicate="mentioned_in",
                    obj=lf,
                    valid_from=valid_from,
                    source_file=lf,
                )
            exported += 1

    # 2. Export high-weight co-occurrence edges
    for edge_key, edge_data in edges.items():
        weight = edge_data.get("weight", 0)
        if weight < MIN_EDGE_WEIGHT:
            continue

        parts = edge_key.split("|")
        if len(parts) != 2:
            continue

        src, dst = parts
        # Only export edges where at least one entity is typed
        src_type = entities.get(src, {}).get("type", "concept")
        dst_type = entities.get(dst, {}).get("type", "concept")
        if src_type == "concept" and dst_type == "concept":
            continue

        last_ts = edge_data.get("last_ts", "")
        valid_from = last_ts[:10] if last_ts else None

        if debug:
            print(f"  [A] Edge: {src} → related_to → {dst} (w={weight})")

        if not dry_run:
            kg.add_triple(
                subject=src,
                predicate="related_to",
                obj=dst,
                valid_from=valid_from,
                confidence=min(weight / 10.0, 1.0),
            )
        exported += 1

    return exported


# ── Direction B: MemPalace → STOPA ────────────────────────────────────

def sync_mempalace_to_stopa(
    graph: dict,
    kg,
    last_sync: str | None,
    dry_run: bool = False,
    debug: bool = False,
) -> int:
    """Import new MemPalace triples into STOPA concept-graph."""
    imported = 0
    entities = graph.setdefault("entities", {})
    edges = graph.setdefault("edges", {})

    # Query all triples — filter by date if we have last_sync
    try:
        timeline = kg.timeline()
    except Exception as e:
        print(f"[WARN] Cannot query MemPalace timeline: {e}", file=sys.stderr)
        return 0

    if not timeline:
        return 0

    now_str = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

    for triple in timeline:
        # triple is typically (subject, predicate, object, valid_from, valid_to, confidence, source)
        if not isinstance(triple, (tuple, list)) or len(triple) < 3:
            continue

        subj = str(triple[0])
        pred = str(triple[1])
        obj = str(triple[2])
        valid_from = str(triple[3]) if len(triple) > 3 and triple[3] else None
        valid_to = str(triple[4]) if len(triple) > 4 and triple[4] else None

        # Skip triples older than last sync
        if last_sync and valid_from and valid_from < last_sync:
            continue

        # Skip invalidated triples
        if valid_to:
            # Mark as invalidated in concept-graph if edge exists
            edge_key = f"{subj}|{obj}"
            if edge_key in edges:
                if debug:
                    print(f"  [B] Invalidate edge: {edge_key}")
                if not dry_run:
                    edges[edge_key]["invalidated"] = valid_to
                imported += 1
            continue

        # Add/update entity nodes
        for name in (subj, obj):
            if name not in entities:
                if debug:
                    print(f"  [B] New entity: {name}")
                if not dry_run:
                    entities[name] = {
                        "name": name,
                        "type": "concept",
                        "mentions": 1,
                        "last_seen": now_str,
                        "learning_files": [],
                    }

        # Add/update edge
        edge_key = f"{subj}|{obj}"
        if edge_key not in edges:
            if debug:
                print(f"  [B] New edge: {subj} → {pred} → {obj}")
            if not dry_run:
                edges[edge_key] = {
                    "weight": 1,
                    "count": 1,
                    "last_ts": now_str,
                    "mempalace_predicate": pred,
                }
            imported += 1
        else:
            # Reinforce existing edge
            if not dry_run:
                edges[edge_key]["count"] = edges[edge_key].get("count", 1) + 1
                edges[edge_key]["weight"] = edges[edge_key].get("weight", 1) + 1
                edges[edge_key]["last_ts"] = now_str
                if "mempalace_predicate" not in edges[edge_key]:
                    edges[edge_key]["mempalace_predicate"] = pred

    return imported


# ── Main ──────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Bidirectional sync between STOPA concept-graph and MemPalace KG"
    )
    parser.add_argument(
        "--direction", choices=["a", "b", "both"], default="both",
        help="a=STOPA→MemPalace, b=MemPalace→STOPA, both=bidirectional (default)"
    )
    parser.add_argument("--dry-run", action="store_true", help="Preview changes without writing")
    parser.add_argument("--debug", action="store_true", help="Verbose output")
    args = parser.parse_args()

    # Skip subagent invocations (when run as hook)
    try:
        stdin_data = sys.stdin.read() if not sys.stdin.isatty() else ""
        if stdin_data and '"agent_type"' in stdin_data:
            return
    except Exception:
        pass

    graph = load_concept_graph()
    if not graph.get("entities"):
        print("kg-sync: no concept-graph data, skipping")
        return

    kg = get_mempalace_kg()
    if kg is None:
        return

    sync_state = load_sync_state()
    results = {"a_exported": 0, "b_imported": 0}

    try:
        # Direction A: STOPA → MemPalace
        if args.direction in ("a", "both"):
            prefix = "[DRY-RUN] " if args.dry_run else ""
            results["a_exported"] = sync_stopa_to_mempalace(
                graph, kg, dry_run=args.dry_run, debug=args.debug
            )
            print(f"{prefix}kg-sync A: {results['a_exported']} triples exported to MemPalace")

        # Direction B: MemPalace → STOPA
        if args.direction in ("b", "both"):
            prefix = "[DRY-RUN] " if args.dry_run else ""
            results["b_imported"] = sync_mempalace_to_stopa(
                graph, kg, last_sync=sync_state.get("last_sync"),
                dry_run=args.dry_run, debug=args.debug,
            )
            if not args.dry_run and results["b_imported"] > 0:
                save_concept_graph(graph)
            print(f"{prefix}kg-sync B: {results['b_imported']} triples imported to concept-graph")

        # Update sync state
        if not args.dry_run:
            sync_state["last_sync"] = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
            sync_state["a_exported"] += results["a_exported"]
            sync_state["b_imported"] += results["b_imported"]
            save_sync_state(sync_state)

    finally:
        kg.close()


if __name__ == "__main__":
    main()
