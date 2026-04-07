---
title: "Idea File: Nový primitiv pro sdílení znalostí s AI agenty"
slug: idea-file-research
source_type: research_output
date_ingested: 2026-04-07
entities_extracted: 10
claims_extracted: 5
---
# Idea File: Nový primitiv pro sdílení znalostí s AI agenty

> **TL;DR**: Karpathy 4. dubna 2026 pojmenoval "idea file" — Markdown dokument popisující záměr (co postavit), nikoli implementaci. OpenClaw/Monica demonstruje koordinaci 6 agentů přes sdílené .md soubory. Klíčová mezera: compilation layer — přeměna denních raw signálů na strukturované znalosti. Akademický mainstream konverguje na 3-fázový lifecycle (ingest → consolidate → reflect), ale phase 3 (reflection) nemá ověřenou open-source implementaci.

## Key Claims

1. Karpathy's idea file je meta-pojmenování principu existujícího v autoresearch (program.md, 2026-03-06), AGENTS.md (2025-08) a SKILL.md (2025-12) — `[verified]`
2. DEV.to explicitně: "RAG performs information retrieval; Karpathy's workflow performs knowledge compilation" — fundamentálně odlišná operace — `[verified]`
3. AGENTS.md je standardizován přes Linux Foundation AAIF (12/2025) s AWS, Anthropic, OpenAI, Google, Microsoft jako platinum members — `[verified]`
4. Context Engineering → Intent Engineering → Specification Engineering hierarchie (arXiv:2603.09619v2) — "whoever controls specifications controls scale" — `[argued]`
5. Fáze 3 (reflection) memory lifecycle — cross-temporal pattern detection — nemá ověřenou open-source implementaci navzdory claimům Letta, AWS AgentCore, Supermemory — `[inferred]`

## Entities

| Entity | Type | Status |
|--------|------|--------|
| Karpathy idea file | concept | new |
| OpenClaw | tool | existing |
| EverMemOS | tool | new |
| MAGMA | paper | new |
| Letta sleep-time compute | concept | new |
| A-MEM | paper | new |
| AAIF | company | new |
| Specification Engineering | concept | new |
| Birgitta Böckeler | person | new |
| AWS Kiro | tool | new |

## Relations

- Karpathy idea file `generalizes` autoresearch program.md
- AGENTS.md `standardized-by` AAIF
- EverMemOS `implements` 3-phase memory lifecycle
- Letta `implements` sleep-time consolidation `as phase 2`
- OpenClaw `coordinates` agents `via shared markdown files`
