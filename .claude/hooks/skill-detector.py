#!/usr/bin/env python3
"""SessionStart hook: auto-detect skill crystallization candidates.

Hippocampus Phase 3b: When concept clusters in the graph form tight
communities (high internal edge weight, repeated across sessions),
they may represent an emergent workflow worth crystallizing into a skill.

Detection is passive — outputs suggestions as additionalContext,
never creates skills automatically.

Archetype patterns (from hippocampus, adapted):
  1. Tool chain: A→B→C appears 5+ times across sessions
  2. Concept cluster: 4+ concepts with avg edge weight > 3.0
  3. Cross-project: same pattern in 3+ workspace contexts
  4. Error→fix pair: error concept strongly linked to fix concept

Runs at SessionStart. Max 5s.
"""
import json
import os
import sys
import time
from collections import defaultdict
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# Profile gate
_levels = {"minimal": 1, "standard": 2, "strict": 3}
if _levels.get(os.environ.get("STOPA_HOOK_PROFILE", "standard"), 2) < _levels.get("standard", 2):
    sys.exit(0)

GRAPH_PATH = Path(".claude/memory/concept-graph.json")
SKILLS_DIR = Path(".claude/skills")
SUGGESTIONS_PATH = Path(".claude/memory/intermediate/skill-suggestions.json")

# Detection thresholds
MIN_CLUSTER_SIZE = 4          # Minimum concepts in a cluster
MIN_AVG_EDGE_WEIGHT = 3.0     # Average edge weight within cluster
MIN_CROSS_PROJECT = 3          # Contexts for cross-project pattern
MIN_EDGE_COUNT = 5             # Minimum co-occurrences for strong edge
MAX_SUGGESTIONS = 3            # Don't overwhelm with suggestions
COOLDOWN_DAYS = 7              # Don't re-suggest same cluster within 7 days


def load_graph() -> dict:
    """Load concept graph."""
    if not GRAPH_PATH.exists():
        return {}
    try:
        return json.loads(GRAPH_PATH.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {}


def get_existing_skill_concepts() -> set[str]:
    """Extract concepts already covered by existing skills."""
    concepts = set()
    if not SKILLS_DIR.exists():
        return concepts
    for skill_dir in SKILLS_DIR.iterdir():
        if skill_dir.is_dir():
            skill_file = skill_dir / "SKILL.md"
            if skill_file.exists():
                try:
                    content = skill_file.read_text(encoding="utf-8", errors="replace")
                    # Extract key terms from skill name and description
                    concepts.add(skill_dir.name.lower())
                    for word in skill_dir.name.lower().replace("-", " ").split():
                        if len(word) >= 4:
                            concepts.add(word)
                except OSError:
                    continue
    return concepts


def find_dense_clusters(graph: dict) -> list[dict]:
    """Find dense concept clusters that might be emergent skills.

    Uses simple greedy clustering: start from highest-weight edges,
    expand cluster while average internal weight stays above threshold.
    """
    entities = graph.get("entities", {})
    edges = graph.get("edges", {})
    if not edges:
        return []

    # Build adjacency list with strong edges only
    adjacency = defaultdict(list)
    for edge_key, edge in edges.items():
        parts = edge_key.split("|")
        if len(parts) != 2:
            continue
        if edge.get("count", 0) < MIN_EDGE_COUNT:
            continue
        weight = edge.get("weight", 0)
        if weight < 1.0:
            continue
        eid1, eid2 = parts
        adjacency[eid1].append((eid2, weight, edge))
        adjacency[eid2].append((eid1, weight, edge))

    # Sort edges by weight for greedy expansion
    sorted_edges = sorted(
        edges.items(),
        key=lambda x: x[1].get("weight", 0),
        reverse=True,
    )

    clusters = []
    used_nodes = set()

    for edge_key, edge in sorted_edges[:100]:  # Check top 100 edges
        parts = edge_key.split("|")
        if len(parts) != 2:
            continue
        if edge.get("count", 0) < MIN_EDGE_COUNT:
            continue

        seed1, seed2 = parts
        if seed1 in used_nodes and seed2 in used_nodes:
            continue

        # Try to grow a cluster from this edge
        cluster = {seed1, seed2}
        cluster_edges = [(edge_key, edge)]

        # Expand: add neighbors that maintain high avg weight
        candidates = set()
        for node in cluster:
            for neighbor, weight, e in adjacency.get(node, []):
                if neighbor not in cluster:
                    candidates.add(neighbor)

        for candidate in candidates:
            # Check how many cluster members this candidate connects to
            connections = []
            for node in cluster:
                ek = f"{min(node, candidate)}|{max(node, candidate)}"
                if ek in edges:
                    connections.append(edges[ek])

            if len(connections) >= 2:  # Connected to 2+ cluster members
                avg_w = sum(e.get("weight", 0) for e in connections) / len(connections)
                if avg_w >= MIN_AVG_EDGE_WEIGHT * 0.5:
                    cluster.add(candidate)
                    cluster_edges.extend(
                        (f"{min(node, candidate)}|{max(node, candidate)}", edges[f"{min(node, candidate)}|{max(node, candidate)}"])
                        for node in list(cluster) if f"{min(node, candidate)}|{max(node, candidate)}" in edges
                    )

        if len(cluster) < MIN_CLUSTER_SIZE:
            continue

        # Calculate cluster quality metrics
        internal_weights = []
        all_contexts = set()
        for eid1 in cluster:
            for eid2 in cluster:
                if eid1 >= eid2:
                    continue
                ek = f"{min(eid1, eid2)}|{max(eid1, eid2)}"
                if ek in edges:
                    internal_weights.append(edges[ek].get("weight", 0))
                    for ctx in edges[ek].get("contexts", []):
                        all_contexts.add(ctx)

        if not internal_weights:
            continue

        avg_weight = sum(internal_weights) / len(internal_weights)
        if avg_weight < MIN_AVG_EDGE_WEIGHT:
            continue

        # Get entity names
        names = [entities.get(eid, {}).get("name", eid) for eid in cluster]

        clusters.append({
            "concepts": sorted(names),
            "eids": sorted(cluster),
            "size": len(cluster),
            "avg_weight": round(avg_weight, 2),
            "contexts": sorted(all_contexts),
            "cross_project": len(all_contexts) >= MIN_CROSS_PROJECT,
        })

        used_nodes.update(cluster)
        if len(clusters) >= MAX_SUGGESTIONS * 2:
            break

    # Sort by quality (size × avg_weight × cross-project bonus)
    clusters.sort(
        key=lambda c: c["size"] * c["avg_weight"] * (1.5 if c["cross_project"] else 1.0),
        reverse=True,
    )

    return clusters[:MAX_SUGGESTIONS]


def load_previous_suggestions() -> dict:
    """Load previously made suggestions to avoid repeats."""
    if not SUGGESTIONS_PATH.exists():
        return {}
    try:
        return json.loads(SUGGESTIONS_PATH.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {}


def save_suggestions(suggestions: dict) -> None:
    """Save suggestions for cooldown tracking."""
    SUGGESTIONS_PATH.parent.mkdir(parents=True, exist_ok=True)
    SUGGESTIONS_PATH.write_text(
        json.dumps(suggestions, ensure_ascii=False, indent=1),
        encoding="utf-8",
    )


def filter_suggestions(clusters: list[dict], existing_skills: set[str],
                        previous: dict) -> list[dict]:
    """Filter out clusters already covered by skills or recently suggested."""
    today = time.strftime("%Y-%m-%d")
    filtered = []

    for cluster in clusters:
        # Check if mostly covered by existing skills
        concept_set = {c.lower() for c in cluster["concepts"]}
        overlap = concept_set & existing_skills
        if len(overlap) > len(concept_set) * 0.6:
            continue  # >60% overlap with existing skill

        # Check cooldown
        cluster_key = "|".join(cluster["eids"][:5])
        last_suggested = previous.get(cluster_key, "")
        if last_suggested:
            try:
                last_dt = time.mktime(time.strptime(last_suggested, "%Y-%m-%d"))
                days_ago = (time.time() - last_dt) / 86400
                if days_ago < COOLDOWN_DAYS:
                    continue
            except (ValueError, OverflowError):
                pass

        # Mark as suggested
        previous[cluster_key] = today
        filtered.append(cluster)

    return filtered


def main():
    # Consume stdin
    try:
        json.load(sys.stdin)
    except (json.JSONDecodeError, EOFError):
        pass

    graph = load_graph()
    if not graph.get("entities") or not graph.get("edges"):
        return

    clusters = find_dense_clusters(graph)
    if not clusters:
        return

    existing_skills = get_existing_skill_concepts()
    previous = load_previous_suggestions()

    suggestions = filter_suggestions(clusters, existing_skills, previous)
    if not suggestions:
        return

    save_suggestions(previous)

    # Format output
    lines = ["[Skill detector] Emergent workflow patterns found:"]
    for i, cluster in enumerate(suggestions, 1):
        concepts_str = ", ".join(cluster["concepts"][:8])
        ctx_str = f" (cross-project: {', '.join(cluster['contexts'][:3])})" if cluster["cross_project"] else ""
        lines.append(
            f"  {i}. [{cluster['size']} concepts, w={cluster['avg_weight']}] "
            f"{concepts_str}{ctx_str}"
        )
    lines.append("  Consider crystallizing into a skill with /skill-generator if pattern is recurring.")

    print(json.dumps({"additionalContext": "\n".join(lines)}))


if __name__ == "__main__":
    try:
        main()
    except Exception:
        pass  # Never block session start
