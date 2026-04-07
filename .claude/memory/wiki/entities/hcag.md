---
name: HCAG
type: paper
first_seen: 2026-04-07
last_updated: 2026-04-07
sources: [vertical-scaling-research]
tags: [rag, code-reasoning, hierarchical, cost-optimization]
---

# HCAG

> Hierarchical Code/Architecture-guided Agent Generation — proves that hierarchical code abstraction (project→module→function) is theoretically cost-optimal vs flat and iterative RAG.

## Key Facts

- Paper: arXiv:2603.20299 (ref: sources/vertical-scaling-research.md)
- Problem: flat RAG fails on complex codebases because cross-file dependencies and architectural patterns are invisible at snippet level (ref: sources/vertical-scaling-research.md)
- Solution: offline hierarchical abstraction (LLM recursively parses repo → multi-layer semantic KB) + online top-down retrieval (ref: sources/vertical-scaling-research.md)
- "Architecture-then-module" pattern: set architectural scaffold first, then fill module-level details (ref: sources/vertical-scaling-research.md)
- Theoretical cost-optimality proof for hierarchical abstraction with adaptive node compression (ref: sources/vertical-scaling-research.md)

## Relevance to STOPA

Maps directly to orchestrate→scout→worker chain: macro architecture scan → module scan → specific file edits. Validates the hierarchical scout output format in Varianta A of vertical scaling.

## Mentioned In

- [Vertikální škálování Research](../sources/vertical-scaling-research.md)
