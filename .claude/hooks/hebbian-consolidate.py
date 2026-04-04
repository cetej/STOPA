#!/usr/bin/env python3
"""Stop hook: Hebbian consolidation from session activity.

Hippocampus Phase 3a: "Neurons that fire together, wire together."
Extracts concepts from session activity (activity-log, traces) and
strengthens co-occurrence edges in concept-graph.json.

Unlike graph-consolidate.sh (full rebuild from learnings), this hook
performs *incremental* edge strengthening based on what was used together
in the current session — genuine Hebbian learning.

Design:
  1. Read activity-log.md for this session's tool usage (file paths, commands)
  2. Read trace JSONL if active (richer data: inputs, outputs)
  3. Extract concepts from session activity
  4. Build session co-occurrence pairs
  5. Strengthen existing edges / create new ones in concept-graph.json
  6. Apply exponential decay to all edges (consolidation pass)

Runs at Stop, after graph-consolidate.sh. Max 10s.
"""
import json
import math
import re
import sys
import time
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# Add hooks/lib to path
sys.path.insert(0, str(Path(__file__).parent / "lib"))

try:
    from associative_engine import (
        extract_concepts,
        load_graph,
        save_graph,
        RECENCY_LAMBDA,
    )
except ImportError:
    sys.exit(0)

ACTIVITY_LOG = Path(".claude/memory/activity-log.md")
TRACE_MARKER = Path(".claude/memory/intermediate/trace-active.json")

# Hebbian learning constants
SESSION_EDGE_BOOST = 0.5       # Weight boost for session co-occurrence
MAX_SESSION_CONCEPTS = 50      # Cap to avoid combinatorial explosion
DECAY_ALL_EDGES = True         # Apply decay to entire graph during consolidation
MIN_EDGE_WEIGHT_PRUNE = 0.05   # Edges below this get pruned (3e optimization)


def read_activity_log() -> str:
    """Read today's activity log entries."""
    if not ACTIVITY_LOG.exists():
        return ""
    try:
        content = ACTIVITY_LOG.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""

    # Extract today's entries (lines starting with today's date)
    today = time.strftime("%Y-%m-%d")
    lines = []
    for line in content.split("\n"):
        if line.startswith(f"| {today}"):
            lines.append(line)
    return "\n".join(lines)


def read_trace_data() -> str:
    """Read trace JSONL from active trace run (if any)."""
    if not TRACE_MARKER.exists():
        return ""
    try:
        marker = json.loads(TRACE_MARKER.read_text(encoding="utf-8"))
        trace_dir = Path(marker.get("trace_dir", ""))
        tools_path = trace_dir / "tools.jsonl"
        if not tools_path.exists():
            return ""
        content = tools_path.read_text(encoding="utf-8", errors="replace")
        # Extract input_snippets and output_snippets for concept extraction
        parts = []
        for line in content.strip().split("\n"):
            try:
                record = json.loads(line)
                if record.get("input_snippet"):
                    parts.append(record["input_snippet"])
                if record.get("input_path"):
                    parts.append(record["input_path"])
                if record.get("input_cmd"):
                    parts.append(record["input_cmd"][:200])
            except json.JSONDecodeError:
                continue
        return "\n".join(parts)
    except (json.JSONDecodeError, OSError):
        return ""


def extract_session_concepts(activity_text: str, trace_text: str) -> list[str]:
    """Extract unique concepts from session activity."""
    combined = f"{activity_text}\n{trace_text}"
    if not combined.strip():
        return []

    concepts = extract_concepts(combined)

    # Also extract file-path-derived concepts (e.g. "critic" from .claude/skills/critic/SKILL.md)
    for m in re.finditer(r"[/\\]([\w-]+)(?:\.(?:py|md|ts|js|sh))?", combined):
        name = m.group(1)
        if len(name) >= 4 and name.lower() not in {"claude", "hooks", "memory", "skills",
                                                     "docs", "scripts", "lib", "node_modules"}:
            concepts.append(name.lower())

    # Deduplicate, cap
    seen = set()
    unique = []
    for c in concepts:
        key = c.lower()
        if key not in seen:
            seen.add(key)
            unique.append(c)
    return unique[:MAX_SESSION_CONCEPTS]


def hebbian_strengthen(graph: dict, session_concepts: list[str]) -> tuple[int, int]:
    """Strengthen edges for concepts that co-occurred in this session.

    Returns (new_edges, strengthened_edges).
    """
    entities = graph.get("entities", {})
    edges = graph.get("edges", {})
    today = time.strftime("%Y-%m-%d")
    now_ts = time.time()
    new_count = 0
    strength_count = 0

    # Map concepts to entity IDs (only those in graph)
    session_eids = []
    for concept in session_concepts:
        eid = concept.lower().replace(" ", "-")
        if eid in entities:
            session_eids.append(eid)
            # Update last_seen
            entities[eid]["last_seen"] = today
        # Also check if concept is a substring of any entity
        else:
            for existing_eid in entities:
                if concept.lower() in existing_eid or existing_eid in concept.lower():
                    session_eids.append(existing_eid)
                    entities[existing_eid]["last_seen"] = today
                    break

    # Deduplicate
    session_eids = list(dict.fromkeys(session_eids))

    # Build co-occurrence edges (Hebbian: fire together, wire together)
    for i, eid1 in enumerate(session_eids):
        for eid2 in session_eids[i + 1:]:
            edge_key = f"{min(eid1, eid2)}|{max(eid1, eid2)}"

            if edge_key not in edges:
                edges[edge_key] = {
                    "weight": 0.0,
                    "count": 0,
                    "last_ts": "",
                    "contexts": [],
                    "source": "hebbian",
                }
                new_count += 1
            else:
                strength_count += 1

            edge = edges[edge_key]
            edge["count"] += 1
            edge["last_ts"] = today

            # Add workspace context
            cwd_name = Path.cwd().name.lower()
            if cwd_name and cwd_name not in edge.get("contexts", []):
                edge.setdefault("contexts", []).append(cwd_name)
                edge["contexts"] = edge["contexts"][-5:]  # Keep last 5

            # Recalculate weight with Hebbian boost
            try:
                days = (now_ts - time.mktime(
                    time.strptime(edge["last_ts"], "%Y-%m-%d")
                )) / 86400
                edge["weight"] = (edge["count"] + SESSION_EDGE_BOOST) * math.exp(-RECENCY_LAMBDA * days)
            except (ValueError, OverflowError):
                edge["weight"] = float(edge["count"])

    graph["entities"] = entities
    graph["edges"] = edges
    return new_count, strength_count


def decay_and_prune(graph: dict) -> int:
    """Apply exponential decay to all edges and prune weak ones.

    Returns number of pruned edges.
    """
    edges = graph.get("edges", {})
    now_ts = time.time()
    to_prune = []

    for edge_key, edge in edges.items():
        last_ts = edge.get("last_ts", "")
        if not last_ts:
            to_prune.append(edge_key)
            continue
        try:
            days = (now_ts - time.mktime(
                time.strptime(last_ts, "%Y-%m-%d")
            )) / 86400
            edge["weight"] = edge["count"] * math.exp(-RECENCY_LAMBDA * days)
        except (ValueError, OverflowError):
            edge["weight"] = float(edge.get("count", 0))

        if edge["weight"] < MIN_EDGE_WEIGHT_PRUNE:
            to_prune.append(edge_key)

    for key in to_prune:
        del edges[key]

    graph["edges"] = edges
    return len(to_prune)


def main():
    # Consume stdin (Stop hook receives session data); skip for subagents
    try:
        stdin_data = sys.stdin.read()
        hook_data = json.loads(stdin_data) if stdin_data.strip() else {}
        if hook_data.get("agent_type"):
            return  # Subagent Stop — skip Hebbian consolidation
    except Exception:
        pass

    # 1. Gather session activity
    activity_text = read_activity_log()
    trace_text = read_trace_data()

    if not activity_text and not trace_text:
        return

    # 2. Extract concepts
    session_concepts = extract_session_concepts(activity_text, trace_text)
    if len(session_concepts) < 2:
        return  # Need at least 2 concepts for edges

    # 3. Load graph and apply Hebbian strengthening
    graph = load_graph()
    if not graph.get("entities"):
        return  # No graph to work with

    new_edges, strengthened = hebbian_strengthen(graph, session_concepts)

    # 4. Decay and prune
    pruned = 0
    if DECAY_ALL_EDGES:
        pruned = decay_and_prune(graph)

    # 5. Save
    graph.setdefault("meta", {})["last_hebbian"] = time.strftime("%Y-%m-%dT%H:%M:%S")
    graph["meta"]["session_concepts"] = len(session_concepts)
    save_graph(graph)

    # 6. Report
    if new_edges or strengthened or pruned:
        parts = []
        if new_edges:
            parts.append(f"{new_edges} new edges")
        if strengthened:
            parts.append(f"{strengthened} strengthened")
        if pruned:
            parts.append(f"{pruned} pruned")
        print(f"[Hebbian] {', '.join(parts)} ({len(session_concepts)} session concepts)")


if __name__ == "__main__":
    try:
        main()
    except Exception:
        pass  # Never fail the session stop
