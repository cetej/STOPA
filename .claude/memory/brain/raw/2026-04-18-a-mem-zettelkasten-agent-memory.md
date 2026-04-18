---
date: 2026-04-18
source: https://arxiv.org/abs/2502.12110
type: paper
title: "A-MEM: Agentic Memory for LLM Agents"
authors: Wujiang Xu, Zujie Liang, Kai Mei, Hang Gao, Juntao Tan, Yongfeng Zhang
venue: NeurIPS 2025
tags: [memory, zettelkasten, agent-memory, dynamic-indexing, knowledge-network]
---

## Summary

A-MEM proposes a dynamic memory system for LLM agents inspired by the Zettelkasten method, organizing information into interconnected knowledge networks rather than flat storage. Each memory note contains contextual descriptions, keywords, and tags; when new memories are added, the system identifies relevant historical connections and establishes links. New memories can trigger updates to existing entries — memory evolves rather than just accumulates. Evaluated on six foundation models, achieves superior improvement over SOTA baselines.

## Key Concepts

- Zettelkasten memory organization for LLM agents
- Interconnected knowledge networks (not flat key-value store)
- Dynamic indexing: new memory → find historical connections → create links
- Memory evolution: adding memory can update/refine existing entries
- Agentic memory management: agent drives its own memory decisions

## Claims

- Memory as interconnected network > flat retrieval store
- Continuous refinement via back-propagation to existing notes
- Evaluated on 6 foundation models, outperforms SOTA baselines on diverse tasks

## Entities

Authors: Wujiang Xu, Zujie Liang, Kai Mei, Hang Gao, Juntao Tan, Yongfeng Zhang
Venue: NeurIPS 2025
