---
title: "ByteRover vs STOPA Memory — Deep Analysis & Upgrade Proposals"
slug: byterover-memory-analysis
source_type: research_output
date_ingested: 2026-04-07
entities_extracted: 8
claims_extracted: 5
---

# ByteRover vs STOPA Memory — Deep Analysis & Upgrade Proposals

> **TL;DR**: ByteRover (arXiv:2604.01599) is a hierarchical memory system achieving SOTA on LoCoMo (96.1%) and LongMemEval-S (92.8%) without embeddings — validating STOPA's markdown-on-disk approach. Analysis proposes 5 concrete STOPA upgrades: topic clustering, tiered retrieval cache, exponential decay with hysteresis, formal curation operations, and auto-generated context summaries.

## Key Claims

1. ByteRover achieves SOTA on LoCoMo (96.1%) and LongMemEval-S (92.8%) using only BM25 + LLM reasoning — no vector embeddings. — `[verified]`
2. Tiered retrieval is ByteRover's most critical component: ablation shows −29.4pp without it. — `[verified]`
3. STOPA has structural advantages ByteRover lacks: write-time admission control, impact scoring, source credibility weighting, machine-checkable verify_check fields. — `[argued]`
4. Exponential decay with hysteresis prevents oscillation at maturity tier boundaries — superior to STOPA's current linear decay. — `[argued]`
5. 2-level topic hierarchy (not full 4-level) is sufficient for STOPA's scale — relations have only marginal impact (−0.4pp in ablation). — `[argued]`

## Relations

- ByteRover `achieves SOTA on` LoCoMo and LongMemEval-S
- ByteRover `validates` STOPA's markdown-on-disk memory approach
- Tiered Retrieval `is most critical component of` ByteRover
- STOPA `should adopt` keyword index cache from ByteRover
- STOPA `should NOT adopt` BM25 full-text index (overkill at <500 entries)

## Entities

| Entity | Type | Status |
|--------|------|--------|
| ByteRover | paper | new |
| LoCoMo benchmark | concept | new |
| LongMemEval-S | concept | new |
| Hierarchical Context Tree | concept | new |
| 5-Tier Progressive Retrieval | concept | new |
| Maturity Tiers with Hysteresis | concept | new |
| BM25 | concept | new |
| Mem0 | tool | new |
