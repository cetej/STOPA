---
title: "Persistent Identity in AI Agents: A Multi-Anchor Architecture for Resilient Memory and Continuity"
arxiv: "2604.09588"
fetched: 2026-04-21
source: https://arxiv.org/abs/2604.09588
authors: [Prahlad G. Menon]
tags: [agent-identity, persistent-memory, catastrophic-forgetting, multi-anchor, rag-rlm]
---

# Raw Extraction

## Key Concepts
- Identity persistence when conversation history is summarized/truncated
- Distributed identity anchors (episodic, procedural, emotional, embodied — like human memory)
- Multi-anchor resilience: no single point of failure
- soul.py: open-source implementation
- Hybrid RAG+RLM retrieval routing

## Main Claims
- AI identity is "centralized in a single memory store" = single point of failure
- Human identity survives memory damage because it's distributed across multiple systems
- Context-limited agents suffer identity collapse during compaction/summarization
- Separable identity components enable resilient continuity

## Architecture
- Identity files: stable, long-lived (facts about the agent's goals/values/persona)
- Memory logs: temporal, append-only experience traces
- Hybrid RAG+RLM: routes queries to appropriate memory pattern
- soul.py open-source codebase

## Submitted: 2026-03-02, cs.AI + cs.ET + cs.LG
