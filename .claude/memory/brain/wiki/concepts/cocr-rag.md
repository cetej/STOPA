---
title: CoCR-RAG — Concept-Oriented Context Reconstruction
category: concepts
tags: [rag, context-reconstruction, amr, multi-source, retrieval, context-engineering]
sources: [raw/processed/2026-04-22-cocr-rag.md]
updated: 2026-04-22
---

# CoCR-RAG — Concept-Oriented Context Reconstruction

**Paper**: arXiv:2603.23989  
**Authors**: Kaize Shi, Xueyao Sun, Qika Lin, Firoj Alam, Qing Li, Xiaohui Tao, Guandong Xu

## Problem

Multi-source RAG: retrieved documents have inconsistent formats, styles, redundancy. Direct concatenation degrades coherence and increases noise. Standard solution (chunk-then-retrieve) loses cross-document relationships.

## Solution: Three-Stage Pipeline

### Stage 1: Concept Distillation (AMR)
Abstract Meaning Representation (AMR) converts each document into a semantic logical graph. Core concepts extracted from graph — format/style noise eliminated at the representation layer, not the text layer.

### Stage 2: Unified Context Reconstruction
LLM synthesizes distilled concepts into a single coherent context. Only necessary sentence elements are added — no raw document text copied verbatim.

### Stage 3: Plug-and-Play Delivery
Reconstructed context replaces raw retrieved chunks. Works across different LLM backbones.

## Key Insight

**Reconstruct from concepts, not from text.**

AMR as intermediate semantic layer:
- Removes style/format divergence
- Preserves knowledge structure
- Enables true multi-source fusion

## Results

- Significant improvement on PopQA and EntityQuestions benchmarks
- Outperforms competing multi-source RAG methods
- Backbone-agnostic (plug-and-play)

## STOPA Relevance

2BRAIN's learnings retrieval currently does text-level fusion (multiple learning files concatenated). CoCR-RAG suggests: extract key concepts from each matched learning, then reconstruct a unified context before presenting to the reasoning model. Would reduce redundancy when multiple learnings cover overlapping topics.

The AMR intermediate representation is complex to implement directly, but the principle (concept extraction → synthesis) is adoptable with simpler NLP tools.

## Related Concepts

→ [ecphory-rag.md](ecphory-rag.md)  
→ [context-awareness-gate.md](context-awareness-gate.md)  
→ [knowledge-compounding.md](knowledge-compounding.md)  
→ [memory-augmented-routing.md](memory-augmented-routing.md)
