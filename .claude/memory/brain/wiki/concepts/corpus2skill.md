---
title: Corpus2Skill — Navigate, Don't Retrieve
date: 2026-04-21
sources:
  - https://arxiv.org/abs/2604.14572
tags: [ai, rag, knowledge-navigation, hierarchical-rag, enterprise-qa, agent-skills, corpus-compilation]
related:
  - context-awareness-gate.md
  - knowledge-drift-chronos.md
  - adr-context-strategies.md
  - agentforge.md
---

# Corpus2Skill — Navigate, Don't Retrieve

## Core Idea

Traditional RAG treats LLMs as **passive consumers of search results** — the model receives retrieved chunks without understanding corpus structure. Corpus2Skill inverts this: the agent receives a **"bird's-eye view"** of the corpus and actively navigates it like a skilled researcher.

**Don't retrieve → navigate.**

## Two-Phase Architecture

### Phase 1: Offline Compilation
```
Document corpus
    → iterative clustering
    → LLM summaries at each hierarchical level
    → materialized skill file tree
```
The corpus becomes a navigable tree of summaries, not a flat chunk index.

### Phase 2: Serve-Time Navigation
```
Query → bird's-eye summary → drill into topic branch
     → progressive detail → retrieve document by ID
```
At each level, the agent can *backtrack* from unproductive branches — impossible with standard retrieval.

## Why Navigation Beats Retrieval

| Capability | Standard RAG | Corpus2Skill |
|-----------|-------------|--------------|
| Corpus structure visibility | ❌ | ✓ |
| Backtracking | ❌ | ✓ |
| Cross-branch synthesis | Poor | ✓ |
| Progressive refinement | ❌ | ✓ |

## Results on WixQA

Outperforms: dense retrieval, RAPTOR, agentic RAG across quality metrics on enterprise customer-support benchmark.

## Relevance to STOPA

Corpus2Skill formalizes what 2BRAIN is doing informally:
- 2BRAIN wiki = the "skill file tree" from offline compilation
- `/ingest` = the compilation step (raw source → structured summaries)
- `/compile` = hierarchical synthesis (subtopics → topic summaries)
- LLM navigates wiki/index.md as bird's-eye view, then drills into relevant articles

The key missing piece in STOPA: explicit **backtracking** when a wiki branch doesn't contain the answer. Currently `/scout` returns early; it could instead navigate siblings.

## Connections

- [context-awareness-gate](context-awareness-gate.md): CAG decides whether to retrieve; Corpus2Skill assumes retrieval is needed but does it smarter
- [adr-context-strategies](adr-context-strategies.md): both find that selective, structured context beats exhaustive retrieval
- [agentforge](agentforge.md): AgentForge uses execution grounding (Docker); Corpus2Skill uses knowledge grounding — both reject passive retrieval
