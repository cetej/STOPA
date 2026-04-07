#!/usr/bin/env python3
"""Update concept-graph.json with entities from wiki/entities/ pages.

Reads all entity pages, extracts entity names and source references,
adds new nodes and co-occurrence edges to the concept graph.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

GRAPH_PATH = Path(".claude/memory/concept-graph.json")
ENTITIES_DIR = Path(".claude/memory/wiki/entities")
SOURCES_DIR = Path(".claude/memory/wiki/sources")


def load_graph() -> dict:
    if GRAPH_PATH.exists():
        with open(GRAPH_PATH, encoding="utf-8") as f:
            return json.load(f)
    return {"entities": {}, "edges": {}, "meta": {}}


def extract_entity_id(name: str) -> str:
    """Normalize entity name to graph ID."""
    return re.sub(r"[^a-z0-9-]", "-", name.lower()).strip("-")


def parse_entity_page(path: Path) -> dict | None:
    """Parse entity .md page for name, type, sources, tags."""
    text = path.read_text(encoding="utf-8", errors="replace")
    meta = {}

    # Parse YAML frontmatter
    if text.startswith("---"):
        end = text.find("---", 3)
        if end > 0:
            fm = text[3:end]
            for line in fm.strip().split("\n"):
                if ":" in line:
                    key, val = line.split(":", 1)
                    key = key.strip()
                    val = val.strip().strip("\"'")
                    if key in ("name", "type", "first_seen", "last_updated"):
                        meta[key] = val
                    elif key == "sources":
                        # Parse YAML array
                        meta["sources"] = [
                            s.strip().strip("\"'")
                            for s in val.strip("[]").split(",")
                            if s.strip()
                        ]
                    elif key == "tags":
                        meta["tags"] = [
                            t.strip().strip("\"'")
                            for t in val.strip("[]").split(",")
                            if t.strip()
                        ]

    if "name" not in meta:
        # Fallback: use filename
        meta["name"] = path.stem

    return meta


def parse_source_page(path: Path) -> list[str]:
    """Extract entity names mentioned in a source summary."""
    text = path.read_text(encoding="utf-8", errors="replace")
    entities = []

    # Find entity table rows: | Name | type | status |
    for match in re.finditer(r"\|\s*\[?([^\]|]+)\]?\s*\|", text):
        name = match.group(1).strip()
        if name and name not in ("Entity", "Name", "---", "type", "Status"):
            entities.append(name)

    return entities


def main():
    graph = load_graph()
    entities_added = 0
    edges_added = 0

    # Step 1: Add entity nodes from wiki/entities/
    entity_pages = list(ENTITIES_DIR.glob("*.md"))
    print(f"Found {len(entity_pages)} entity pages")

    for page in entity_pages:
        meta = parse_entity_page(page)
        if not meta:
            continue

        eid = extract_entity_id(meta["name"])

        if eid not in graph["entities"]:
            graph["entities"][eid] = {
                "name": meta["name"],
                "type": meta.get("type", "concept"),
                "mentions": 1,
                "last_seen": meta.get("last_updated", "2026-04-07"),
                "learning_files": [page.name],
            }
            entities_added += 1
        else:
            # Update existing: increment mentions, update last_seen
            node = graph["entities"][eid]
            node["mentions"] = node.get("mentions", 0) + 1
            node["last_seen"] = meta.get("last_updated", node.get("last_seen", ""))
            if page.name not in node.get("learning_files", []):
                node.setdefault("learning_files", []).append(page.name)

    # Step 2: Build co-occurrence edges from source pages
    source_pages = list(SOURCES_DIR.glob("*.md"))
    print(f"Found {len(source_pages)} source pages")

    for source in source_pages:
        mentioned = parse_source_page(source)
        # Normalize to entity IDs
        entity_ids = []
        for name in mentioned:
            eid = extract_entity_id(name)
            if eid in graph["entities"]:
                entity_ids.append(eid)

        # Create edges between co-occurring entities
        entity_ids = list(set(entity_ids))
        for i in range(len(entity_ids)):
            for j in range(i + 1, len(entity_ids)):
                a, b = sorted([entity_ids[i], entity_ids[j]])
                edge_key = f"{a}|{b}"
                if edge_key not in graph["edges"]:
                    graph["edges"][edge_key] = {
                        "weight": 1.0,
                        "count": 1,
                        "last_ts": "2026-04-07",
                        "contexts": [],
                    }
                    edges_added += 1
                else:
                    edge = graph["edges"][edge_key]
                    edge["count"] = edge.get("count", 0) + 1
                    edge["weight"] = edge["count"] * 1.0
                    edge["last_ts"] = "2026-04-07"

    # Step 3: Write back
    with open(GRAPH_PATH, "w", encoding="utf-8") as f:
        json.dump(graph, f, indent=2, ensure_ascii=False)

    print(f"Updated concept-graph.json: +{entities_added} entities, +{edges_added} edges")
    print(f"Total: {len(graph['entities'])} entities, {len(graph['edges'])} edges")


if __name__ == "__main__":
    main()
