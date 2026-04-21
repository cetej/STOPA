---
title: "ByteRover: Agent-Native Memory Through LLM-Curated Hierarchical Context"
arxiv: "2604.01599"
fetched: 2026-04-21
source: https://arxiv.org/abs/2604.01599
authors: [Andy Nguyen, Danh Doan, Hoang Pham, et al.]
tags: [agent-memory, hierarchical-context, memory-augmented-generation, maturity-tiers, rag]
---

# Raw Extraction

## Key Concepts
- Memory-Augmented Generation (MAG): LLMs + external memory for extended reasoning
- Agent-Native: same LLM that reasons also curates and structures knowledge
- Context Tree: Domain → Topic → Subtopic → Entry hierarchy
- Adaptive Knowledge Lifecycle (AKL): importance scoring, maturity tiers, recency decay

## Main Claims
- Traditional memory: "system that stores doesn't understand" → semantic misalignment
- ByteRover inverts this: reasoning LLM = curation LLM
- 5-tier progressive retrieval: resolves most queries sub-100ms without LLM calls
- File-based markdown storage: zero external infrastructure (no vectors, no graph DBs)

## Results
- SOTA on LoCoMo benchmark
- Competitive on LongMemEval
- Maturity tiers: draft → validated → core (already adopted by STOPA memory-files.md rules)

## Architecture
- Hierarchical Context Tree with explicit relations + provenance
- 5-tier progressive retrieval (keyword → semantic → hierarchical → graph → LLM)
- Local filesystem markdown — human-readable, no server needed
- arXiv:2604.01599
