---
name: Knowledge Graph Visualization
type: concept
first_seen: 2026-04-07
last_updated: 2026-04-07
sources: [second-brain-gap-analysis]
tags: [knowledge-management, memory, exploration]
---

# Knowledge Graph Visualization

> Vizualizace concept-graph.json jako interaktivní HTML graf nebo Mermaid fallback — umožňuje procházet propojení mezi entitami, learningsmí a wiki články.

## Key Facts

- Problém: concept-graph.json (547 KB, stovky entit a edges) viditelný jen jako raw JSON (ref: sources/second-brain-gap-analysis.md)
- Cesta A — Obsidian export: skript konvertuje wiki/ + learnings/ + concept-graph na Obsidian vault s `[[wiki links]]`; jednosměrný export (ref: sources/second-brain-gap-analysis.md)
- Cesta B — Interaktivní HTML (doporučeno): D3.js force-directed nebo Cytoscape.js, filtrování podle entity type/recency/activation level, click → learning snippets (~300 řádků HTML/JS) (ref: sources/second-brain-gap-analysis.md)
- Cesta C — Hybrid: `/compile` generuje statický `wiki/GRAPH.md` s Mermaid top 30 konceptů + volitelný `--html` flag pro D3.js verzi (ref: sources/second-brain-gap-analysis.md)
- Implementace v `/compile` jako Phase 9 (Fáze 4 roadmapy) (ref: sources/second-brain-gap-analysis.md)
- Effort Cesta B: ~300 řádků HTML/JS + 50 řádků Python generátor (ref: sources/second-brain-gap-analysis.md)

## Relevance to STOPA

Fáze 4 implementačního plánu. Nízká priorita vs ingest pipeline, ale vysoká hodnota pro orientaci v rostoucím znalostním grafu. Doporučeno jako součást `/compile --html`.

## Mentioned In

- [Second Brain Gap Analysis](../sources/second-brain-gap-analysis.md)
