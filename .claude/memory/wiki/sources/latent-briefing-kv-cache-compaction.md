---
title: "Latent Briefing: Efficient Memory Sharing for Multi-Agent Systems via KV Cache Compaction"
slug: latent-briefing-kv-cache-compaction
source_type: paper
url: ""
date_ingested: 2026-04-11
date_published: "2026"
entities_extracted: 2
claims_extracted: 7
---

# Latent Briefing: Efficient Memory Sharing for Multi-Agent Systems via KV Cache Compaction

> **TL;DR**: Task-guided KV cache compaction for cross-agent memory sharing. Orchestrator's trajectory is compressed based on worker's task relevance signal, then passed as latent briefing. 49-65% worker token savings, +3pp accuracy at optimal threshold, ~1.7s overhead. Key insight: speculative orchestrator reasoning is noise that degrades worker accuracy — compaction acts as relevance filter.

## Key Claims

1. Up to 49% median token savings on medium-length (32k-100k) documents — `verified`
2. 65% reduction in worker model token consumption across conditions — `verified`
3. ~1.7s median compaction overhead, 20× faster than sequential AM, 10-30× faster than LLM summarization — `verified`
4. +3pp accuracy gain at optimal threshold vs vanilla RLM baseline — `verified`
5. Optimal threshold varies systematically: longer docs → light compaction (t=-1.0), harder questions → aggressive (t=2.0), short/easy → moderate (t=1.0) — `verified`
6. Speculative orchestrator reasoning (dead-end hypotheses, exploration) is noise that degrades worker performance — `argued`
7. Standard cross-agent context solutions (LLM summarization, RAG, pass everything) all have significant tradeoffs — `argued`

## Entities

| Entity | Type | Status |
|--------|------|--------|
| [Latent Briefing](../entities/latent-briefing.md) | concept | new |
| [Attention Matching Framework](../entities/attention-matching-framework.md) | concept | new |

## Relations

- Latent Briefing `extends` Attention Matching — adds task-guided queries, global mask, MAD thresholding
- Latent Briefing `uses` RLM framework — Zhang et al. 2025, base multi-agent architecture
- Latent Briefing `competes_with` LLM summarization — 10-30× faster, lossless at representation level

## Cross-References

- Related learnings: [2026-04-10-rlm-architectural-principles](../learnings/2026-04-10-rlm-architectural-principles.md) — RLM framework that Latent Briefing extends; STOPA already uses RLM principles
- Related learnings: [2026-04-09-triattention-pre-rope-kv-compression](../learnings/2026-04-09-triattention-pre-rope-kv-compression.md) — complementary KV compression (single-model vs cross-agent)
- Related wiki: [orchestration-multi-agent](../orchestration-multi-agent.md) — multi-agent coordination patterns
- Contradictions: none
