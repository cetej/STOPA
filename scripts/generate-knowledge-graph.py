#!/usr/bin/env python3
"""Generate interactive HTML knowledge graph from concept-graph.json.

Usage:
    python scripts/generate-knowledge-graph.py [--output path] [--min-weight 0.5] [--max-nodes 80]

Reads .claude/memory/concept-graph.json and produces a standalone HTML file
with D3.js force-directed graph visualization. No external dependencies needed.
"""
from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def load_graph(path: Path) -> dict:
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def filter_graph(graph: dict, min_weight: float, max_nodes: int) -> tuple[list, list]:
    """Filter entities and edges for visualization."""
    entities = graph.get("entities", {})
    edges = graph.get("edges", {})

    # Filter edges by weight
    filtered_edges = []
    connected_ids: set[str] = set()
    for edge_key, edge_data in edges.items():
        w = edge_data.get("weight", 0)
        if w < min_weight:
            continue
        parts = edge_key.split("|")
        if len(parts) != 2:
            continue
        filtered_edges.append({
            "source": parts[0],
            "target": parts[1],
            "weight": round(w, 2),
            "count": edge_data.get("count", 1),
        })
        connected_ids.add(parts[0])
        connected_ids.add(parts[1])

    # Filter entities — only connected ones, sorted by mentions
    filtered_entities = []
    for eid, edata in entities.items():
        if eid not in connected_ids:
            continue
        filtered_entities.append({
            "id": eid,
            "name": edata.get("name", eid),
            "type": edata.get("type", "concept"),
            "mentions": edata.get("mentions", 1),
            "files": len(edata.get("learning_files", [])),
            "last_seen": edata.get("last_seen", ""),
        })

    # Sort by mentions descending, take top N
    filtered_entities.sort(key=lambda e: e["mentions"], reverse=True)
    if len(filtered_entities) > max_nodes:
        keep_ids = {e["id"] for e in filtered_entities[:max_nodes]}
        filtered_entities = filtered_entities[:max_nodes]
        filtered_edges = [
            e for e in filtered_edges
            if e["source"] in keep_ids and e["target"] in keep_ids
        ]

    return filtered_entities, filtered_edges


def generate_html(nodes: list, edges: list, title: str = "STOPA Knowledge Graph") -> str:
    """Generate standalone HTML with D3.js force-directed graph."""
    nodes_json = json.dumps(nodes)
    edges_json = json.dumps(edges)

    return f"""<!DOCTYPE html>
<html lang="cs">
<head>
<meta charset="utf-8">
<title>{title}</title>
<style>
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{
    background: #0f1117;
    color: #c9d1d9;
    font-family: "JetBrains Mono", "Fira Code", "Cascadia Code", monospace;
    overflow: hidden;
}}
#controls {{
    position: fixed; top: 12px; left: 12px; z-index: 10;
    background: #161b22; border: 1px solid #30363d; border-radius: 6px;
    padding: 12px 16px; font-size: 13px; max-width: 320px;
}}
#controls h2 {{ font-size: 15px; margin-bottom: 8px; color: #e6edf3; }}
#controls label {{ display: block; margin: 4px 0; }}
#controls input[type=range] {{ width: 100%; }}
#info {{
    position: fixed; bottom: 12px; right: 12px; z-index: 10;
    background: #161b22; border: 1px solid #30363d; border-radius: 6px;
    padding: 12px 16px; font-size: 12px; max-width: 360px;
    display: none;
}}
#info h3 {{ font-size: 14px; color: #e6edf3; margin-bottom: 6px; }}
#info .meta {{ color: #8b949e; }}
#info .files {{ color: #58a6ff; margin-top: 4px; }}
#stats {{
    position: fixed; top: 12px; right: 12px; z-index: 10;
    background: #161b22; border: 1px solid #30363d; border-radius: 6px;
    padding: 8px 12px; font-size: 12px; color: #8b949e;
}}
.link {{ stroke-opacity: 0.4; }}
.link:hover {{ stroke-opacity: 1; }}
.node text {{
    font-size: 10px;
    fill: #c9d1d9;
    pointer-events: none;
    text-anchor: middle;
}}
#search {{
    width: 100%; padding: 4px 8px; margin-top: 6px;
    background: #0d1117; border: 1px solid #30363d; border-radius: 4px;
    color: #c9d1d9; font-size: 12px; font-family: inherit;
}}
</style>
</head>
<body>
<div id="controls">
    <h2>STOPA Knowledge Graph</h2>
    <label>Min edge weight: <span id="wv">0.5</span>
        <input type="range" id="weight-slider" min="0" max="5" step="0.1" value="0.5">
    </label>
    <label>Force strength: <span id="fv">-120</span>
        <input type="range" id="force-slider" min="-300" max="-30" step="10" value="-120">
    </label>
    <input type="text" id="search" placeholder="Search entity...">
</div>
<div id="stats"></div>
<div id="info"></div>
<svg id="graph"></svg>

<script src="https://d3js.org/d3.v7.min.js"></script>
<script>
const rawNodes = {nodes_json};
const rawEdges = {edges_json};

const typeColors = {{
    concept: "#58a6ff",
    tool: "#3fb950",
    person: "#d2a8ff",
    company: "#f0883e",
    paper: "#db6d28",
}};

const width = window.innerWidth;
const height = window.innerHeight;

const svg = d3.select("#graph")
    .attr("width", width)
    .attr("height", height);

const g = svg.append("g");

// Zoom
svg.call(d3.zoom()
    .scaleExtent([0.1, 8])
    .on("zoom", (e) => g.attr("transform", e.transform)));

let simulation, linkSel, nodeSel;

function render(minW, forceStr) {{
    const nodes = rawNodes.map(d => ({{...d}}));
    const nodeIds = new Set(nodes.map(d => d.id));
    const edges = rawEdges
        .filter(e => e.weight >= minW && nodeIds.has(e.source) && nodeIds.has(e.target))
        .map(e => ({{...e}}));

    // Update connected set
    const connected = new Set();
    edges.forEach(e => {{ connected.add(e.source); connected.add(e.target); }});
    const visNodes = nodes.filter(n => connected.has(n.id));

    document.getElementById("stats").textContent =
        `${{visNodes.length}} entities | ${{edges.length}} edges`;

    g.selectAll("*").remove();

    const maxMentions = Math.max(...visNodes.map(n => n.mentions), 1);

    // Links
    linkSel = g.append("g")
        .selectAll("line")
        .data(edges)
        .join("line")
        .attr("class", "link")
        .attr("stroke", "#30363d")
        .attr("stroke-width", d => Math.max(0.5, Math.sqrt(d.weight)));

    // Nodes
    nodeSel = g.append("g")
        .selectAll("g")
        .data(visNodes)
        .join("g")
        .attr("class", "node")
        .call(d3.drag()
            .on("start", dragStart)
            .on("drag", dragging)
            .on("end", dragEnd));

    nodeSel.append("circle")
        .attr("r", d => 4 + (d.mentions / maxMentions) * 12)
        .attr("fill", d => typeColors[d.type] || "#58a6ff")
        .attr("stroke", "#0f1117")
        .attr("stroke-width", 1.5)
        .style("cursor", "pointer");

    nodeSel.append("text")
        .attr("dy", d => -(6 + (d.mentions / maxMentions) * 12))
        .text(d => d.name.length > 20 ? d.name.slice(0, 18) + "..." : d.name);

    // Hover info
    nodeSel.on("click", (ev, d) => {{
        const info = document.getElementById("info");
        info.style.display = "block";
        info.innerHTML = `<h3>${{d.name}}</h3>
            <div class="meta">Type: ${{d.type}} | Mentions: ${{d.mentions}} | Last: ${{d.last_seen}}</div>
            <div class="files">Learning files: ${{d.files}}</div>`;
    }});

    simulation = d3.forceSimulation(visNodes)
        .force("link", d3.forceLink(edges).id(d => d.id).distance(60))
        .force("charge", d3.forceManyBody().strength(forceStr))
        .force("center", d3.forceCenter(width / 2, height / 2))
        .force("collision", d3.forceCollide().radius(d => 8 + (d.mentions / maxMentions) * 12))
        .on("tick", () => {{
            linkSel
                .attr("x1", d => d.source.x).attr("y1", d => d.source.y)
                .attr("x2", d => d.target.x).attr("y2", d => d.target.y);
            nodeSel.attr("transform", d => `translate(${{d.x}},${{d.y}})`);
        }});
}}

function dragStart(e, d) {{ if (!e.active) simulation.alphaTarget(0.3).restart(); d.fx = d.x; d.fy = d.y; }}
function dragging(e, d) {{ d.fx = e.x; d.fy = e.y; }}
function dragEnd(e, d) {{ if (!e.active) simulation.alphaTarget(0); d.fx = null; d.fy = null; }}

// Controls
const ws = document.getElementById("weight-slider");
const fs = document.getElementById("force-slider");
ws.addEventListener("input", () => {{
    document.getElementById("wv").textContent = ws.value;
    render(+ws.value, +fs.value);
}});
fs.addEventListener("input", () => {{
    document.getElementById("fv").textContent = fs.value;
    render(+ws.value, +fs.value);
}});

// Search
document.getElementById("search").addEventListener("input", (ev) => {{
    const q = ev.target.value.toLowerCase();
    if (!nodeSel) return;
    nodeSel.select("circle").attr("opacity", d =>
        q === "" || d.name.toLowerCase().includes(q) ? 1 : 0.15
    );
    nodeSel.select("text").attr("opacity", d =>
        q === "" || d.name.toLowerCase().includes(q) ? 1 : 0.1
    );
}});

// Initial render
render(0.5, -120);
</script>
</body>
</html>"""


def main():
    parser = argparse.ArgumentParser(description="Generate interactive knowledge graph HTML")
    parser.add_argument("--output", default="outputs/knowledge-graph.html", help="Output HTML path")
    parser.add_argument("--min-weight", type=float, default=0.3, help="Min edge weight to include")
    parser.add_argument("--max-nodes", type=int, default=80, help="Max number of nodes")
    args = parser.parse_args()

    graph_path = Path(".claude/memory/concept-graph.json")
    if not graph_path.exists():
        print(f"ERROR: {graph_path} not found", file=sys.stderr)
        sys.exit(1)

    graph = load_graph(graph_path)
    nodes, edges = filter_graph(graph, args.min_weight, args.max_nodes)
    html = generate_html(nodes, edges)

    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding="utf-8")
    print(f"Generated {out} — {len(nodes)} nodes, {len(edges)} edges")


if __name__ == "__main__":
    main()
