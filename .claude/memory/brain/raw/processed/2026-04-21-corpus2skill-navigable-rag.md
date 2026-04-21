---
title: "Don't Retrieve, Navigate: Distilling Enterprise Knowledge into Navigable Agent Skills for QA and RAG"
arxiv: "2604.14572"
fetched: 2026-04-21
source: https://arxiv.org/abs/2604.14572
authors: [Yiqun Sun, Pengfei Wei, Lawrence B. Hsieh]
tags: [rag, knowledge-navigation, hierarchical-rag, enterprise-qa, agent-skills, corpus2skill]
---

# Raw Extraction

## Key Concepts
- Corpus2Skill: offline compilation of document corpora into navigable skill file trees
- Navigation > retrieval: agents reason about evidence location, backtrack from unproductive paths
- Two-phase: offline compilation (cluster → summarize → tree) + serve-time navigation
- "Bird's-eye view" of corpus organization

## Main Claims
- Traditional RAG: LLM is "passive consumer of search results" — no corpus structure visibility
- Navigation enables synthesis across multiple document branches
- Outperforms: dense retrieval, RAPTOR, agentic RAG on WixQA (enterprise customer-support benchmark)
- Agents can backtrack, adjust search strategy, drill progressively

## Architecture
- Offline: iterative clustering → LLM summaries at hierarchical levels → skill file tree
- Online: bird's-eye view → drill into topic branches → retrieve by document ID

## Application: Enterprise QA, Information Retrieval
## arXiv:2604.14572
