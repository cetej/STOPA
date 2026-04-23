---
title: RAG-DIVE — Dynamic Multi-Turn Dialogue Evaluation for RAG
category: concepts
tags: [rag, evaluation, benchmarking, multi-turn, dialogue]
sources: [arXiv:2604.16310]
updated: 2026-04-23
---

# RAG-DIVE — Dynamic Multi-Turn Dialogue Evaluation for RAG

**Paper**: arXiv:2604.16310  
**Authors**: Lorenz Brehme, Benedikt Dornauer, Jan-Henrik Böttcher, Klaus Schmid, Mircea-Cristian Racasan, Ruth Breu

## Core Problem

Static multi-turn datasets fail to capture the dynamic nature of real-world RAG dialogues. Fixed benchmarks don't test how RAG systems handle context drift, follow-up questions, and evolving user intent across a conversation.

## Solution: Dynamic Interactive Validation

RAG-DIVE simulates real user interactions through LLM-generated multi-turn conversations. Three components:

| Component | Role |
|-----------|------|
| **Conversation Generator** | Simulates users with evolving intent |
| **Conversation Validator** | Quality control for generated conversations |
| **Conversation Evaluator** | Per-turn + aggregated performance measurement |

## Key Capability

Detects system modifications that static benchmarks miss — if you change chunk size or retrieval strategy, RAG-DIVE shows the degradation; a static dataset may not.

## Evaluation Dimensions

- Per-turn accuracy
- Aggregated dialogue coherence
- Context retention across turns
- Recovery from retrieval failures within a conversation

## STOPA Relevance

Limited direct applicability — STOPA doesn't build RAG systems per se. Indirect relevance:
- **2BRAIN hybrid-retrieve.py**: multi-turn research sessions (deepresearch skill) rely on retrieval across conversation context. RAG-DIVE methodology could evaluate this.
- **Harness evaluation**: STOPA `/harness` skill could benefit from dynamic test generation rather than fixed JSONL test cases.

The concept of LLM-as-evaluator generating test conversations (not static datasets) = applicable to skill harness design.

## Related Concepts

→ [context-awareness-gate.md](context-awareness-gate.md)  
→ [memory-augmented-routing.md](memory-augmented-routing.md)  
→ [knowledge-drift-chronos.md](knowledge-drift-chronos.md)
