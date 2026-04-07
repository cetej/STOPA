---
title: "Implicit Patterns in LLM-Based Binary Analysis (arXiv:2603.19138)"
slug: llm-binary-patterns-research
source_type: research_output
date_ingested: 2026-04-07
entities_extracted: 5
claims_extracted: 5
---
# Implicit Patterns in LLM-Based Binary Analysis (arXiv:2603.19138)

> **TL;DR**: První systematická trace-level analýza způsobu, jakým LLM organizují průzkum při multi-pass analýze binárních zranitelností. 521 ELF32 binárních souborů, 4 modely (DeepSeek-V3, GPT-5, Claude 3.5 Sonnet, Gemini 3.0), 99563 reasoning kroků. Čtyři emergentní vzory (P1–P4) bez explicitního programování, přičemž P2↔P1 smyčka tvoří 79.4% všech přechodů. Přímá analogie s STOPA circuit breakery a orchestračními primitivy.

## Key Claims

1. LLM binary analysis je strukturována 4 emergentními vzory bez explicitního programování: P1 Early Pruning, P2 Path Lock-in, P3 Targeted Backtracking, P4 Knowledge-Guided Prioritization — `[verified]`
2. P2↔P1 bidirektivní smyčka tvoří 79.4% všech pattern přechodů (P2→P1: 40.0%, P1→P2: 39.4%) — jde o core reasoning routine LLM binary analýzy — `[verified]`
3. P2 (Lock-in) dominuje v early phase (24% v phase 1), P3 (Backtracking) se koncentruje v late phase (46.5% v phase 10) — recovery prompting by měl být injektován ke konci session, ne na začátku — `[verified]`
4. P2 a P4 jsou silně negativně korelované (r = -0.845) — jsou komplementární mechanismy alokace reasoning bandwidth — `[verified]`
5. Neexistuje přímá kauzální vazba mezi frekvencí vzorů a úspěšností detekce zranitelností — vzory reflektují reasoning dynamics, ne performance — `[verified]`

## Entities

| Entity | Type | Status |
|--------|------|--------|
| arXiv:2603.19138 | paper | new |
| Early Pruning (P1) | concept | new |
| Path-Dependent Lock-in (P2) | concept | new |
| Targeted Backtracking (P3) | concept | new |
| Knowledge-Guided Prioritization (P4) | concept | new |

## Relations

- P2 `bidirectional-loop-with` P1 `(79.4% of transitions)`
- P3 `triggers-after` P2 `reaches impasse`
- P4 `competes-with` P2 `for reasoning bandwidth (r=-0.845)`
- arXiv:2603.19138 `maps-to-stopa` circuit-breaker-pattern
- P4 `analogous-to` LEARNINGS.md-informed task ordering
