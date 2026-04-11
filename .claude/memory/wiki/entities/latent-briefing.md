---
name: Latent Briefing
type: concept
first_seen: 2026-04-11
last_updated: 2026-04-11
sources: [latent-briefing-kv-cache-compaction]
tags: [multi-agent, kv-cache, token-efficiency, orchestration, context-sharing]
---

# Latent Briefing

> Cross-agent memory sharing via task-guided KV cache compaction — 49-65% token savings while maintaining or improving accuracy in multi-agent systems.

## Key Facts

- Builds on RLM framework (Zhang et al., 2025) and Attention Matching (Zweiger et al., 2026) (ref: sources/latent-briefing-kv-cache-compaction.md)
- Three innovations over base AM: task-guided query vectors (compress based on subtask relevance), shared global token mask (batched execution), MAD-normalized thresholding (adaptive compression level) (ref: sources/latent-briefing-kv-cache-compaction.md)
- Results on LongBench v2 (126 questions, 0-100k tokens): +3pp accuracy at optimal threshold, 42-57% median worker token reduction, ~1.7s compaction overhead (ref: sources/latent-briefing-kv-cache-compaction.md)
- Compaction overhead: ~1.7s (20× faster than sequential AM, 10-30× faster than LLM summarization) (ref: sources/latent-briefing-kv-cache-compaction.md)
- Uses Claude Sonnet 4 as orchestrator, Qwen3-14B as worker (ref: sources/latent-briefing-kv-cache-compaction.md)
- Key insight: speculative orchestrator reasoning is noise for workers — aggressive compaction on hard tasks filters out exploration trail, improving accuracy (ref: sources/latent-briefing-kv-cache-compaction.md)

## Relevance to STOPA

Directly addresses STOPA's token explosion in multi-agent orchestrate. Even without KV cache access (Claude API), the core principle applies: send task-relevant context to workers, not raw orchestrator trajectory. Maps to budget tiers: deep tier (long trajectory) → lighter compaction, hard subtasks → aggressive context filtering.

## Mentioned In

- [Latent Briefing: KV Cache Compaction for Multi-Agent Systems](../sources/latent-briefing-kv-cache-compaction.md)
