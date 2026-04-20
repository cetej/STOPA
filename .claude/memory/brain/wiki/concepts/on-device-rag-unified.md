---
title: On-Device RAG — Unified Model and Document Representation
type: concept
category: concepts
source: https://arxiv.org/abs/2604.14403
date: 2026-04-19
tags: [rag, on-device, context-compression, retrieval, edge-computing, privacy, unified-model]
related: [ecphory-rag, memory-augmented-routing, agent-memory-taxonomy]
---

# On-Device RAG s Unified Model (arXiv:2604.14403)

## Přehled
"A Unified Model and Document Representation for On-Device Retrieval-Augmented Generation" (Killingback, Meshi, Li, Zamani, Karimzadehgan, 2026). **První model unifikující retrieval + context compression** přes shared model a reprezentaci.

## Klíčový výsledek
RAG na edge zařízení dosahuje parity s tradičním server-side RAG při použití **~1/10 kontextu**. Bez navýšení storage oproti multi-vector retrieval modelům.

## Architektura
Single unified model, který simultánně:
- Komprimuje RAG kontext pro generativní komponentu
- Generuje document representations pro retrieval
- Sdílí underlying reprezentace mezi oběma funkcemi

Tension: quality vs hardware constraints → řešeno shared representation space.

## Motivace — Privacy a Latency
Citlivá data (finanční záznamy, zdravotní záznamy) nemohou opustit zařízení. Edge deployment eliminuje:
- Server-side latency
- Privacy rizika při cloud RAG
- Dependency na konektivitu

## Srovnání s existujícími přístupy
| Přístup | Context | Storage | Quality |
|---------|---------|---------|---------|
| Tradicionální RAG | 1× | multi-vector overhead | baseline |
| Unified On-Device | 1/10× | parity | parity |

## Implikace pro 2BRAIN
- Template pro osobní AI: medical, financial, private knowledge bez cloud exposure
- Shared representation = méně komponent k ladění než pipeline RAG
- 10× token reduction → direct applicability na context-limited local LLM setups
