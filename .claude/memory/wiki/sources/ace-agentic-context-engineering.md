---
title: "ACE — Agentic Context Engineering"
slug: ace-agentic-context-engineering
source_type: research_output
date_ingested: 2026-04-07
entities_extracted: 8
claims_extracted: 5
---

# ACE — Agentic Context Engineering

> **TL;DR**: ACE je self-improving systém, který aktualizuje kontext přes append-only delta updates s bullet IDs a helpful/harmful countery. Klíčový mechanismus: Reflector (co se pokazilo) je oddělen od Curatoru (co zapsat) — zabraňuje šumu při self-update. Context collapse v Dynamic Cheatsheet: 18 282 → 122 tokenů v jednom kroku = 57.1% accuracy pod baseline.

## Key Claims

1. Context collapse je měřitelné selhání: Dynamic Cheatsheet degradoval z 18 282 na 122 tokenů, accuracy 57.1% pod no-adaptation baseline 63.7% — `[verified]`
2. Append-only ADD operace je primární prevence context collapse — Curator nikdy nepřepisuje existující bullets — `[verified]`
3. BulletpointAnalyzer používá sentence-transformers (all-mpnet-base-v2) + FAISS, cosine ≥ 0.90 pro merge near-duplicates — `[verified]`
4. ACE dosahuje 86.9% nižší adaptation latenci a 83.6% nižší token cost vs Dynamic Cheatsheet — `[verified]`
5. UPDATE/MERGE/DELETE operace jsou definovány v kódu ale nejsou implementovány — pouze ADD funguje na main branch — `[verified]`

## Entities

| Entity | Type | Status |
|--------|------|--------|
| ACE (Agentic Context Engineering) | tool | new |
| Dynamic Cheatsheet | concept | new |
| BulletpointAnalyzer | concept | new |
| Reflector (ACE) | concept | new |
| Curator (ACE) | concept | new |
| Context Collapse | concept | new |
| AppWorld benchmark | concept | new |
| Bullet wire format | concept | new |

## Relations

- ACE `prevents` Context Collapse via append-only updates
- Reflector (ACE) `feeds` Curator (ACE) with structured error analysis
- BulletpointAnalyzer `deduplicates` bullet entries via FAISS cosine similarity
- Bullet wire format `tracks` helpful/harmful counters per entry
- ACE `outperforms` Dynamic Cheatsheet on AppWorld benchmark
