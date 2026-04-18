---
name: R-KV
type: concept
first_seen: 2026-04-18
last_updated: 2026-04-18
sources: [triattention-alphsignal-practitioner]
tags: [kv-cache, compression, attention, recency-bias]
---

# R-KV

> Recurrent KV cache compression baseline — extends SnapKV with recurrence but inherits post-RoPE instability and collapses at reasoning depth >14.

## Key Facts

- Uses narrow recent-query window to score KV cache importance (post-RoPE space) (ref: sources/triattention-alphsignal-practitioner.md)
- Depth collapse: 61% accuracy at DFS depth 14 → 31% at depth 16; TriAttention maintains accuracy throughout (ref: sources/triattention-alphsignal-practitioner.md)
- Root cause: post-RoPE queries rotate with position → importance scores unstable for distant tokens

## Relevance to STOPA

Illustrates recency-biased retrieval depth collapse — same failure mode as STOPA BM25-only retrieval on long-horizon sessions: recent query terms dominate scoring, distant-but-relevant learnings get pruned.

## Mentioned In

- [TriAttention — AlphaSignal Practitioner Summary](../sources/triattention-alphsignal-practitioner.md)
