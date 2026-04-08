---
name: SimpleStream
type: concept
first_seen: 2026-04-08
last_updated: 2026-04-08
sources: [simplestream-streaming-video-baseline]
tags: [memory, context, recency, evaluation, architecture]
---

# SimpleStream

> Sliding-window baseline that feeds only the N most recent frames to an off-the-shelf VLM — matches or exceeds complex streaming memory models.

## Key Facts

- Achieves 67.7% on OVO-Bench with just 4 recent frames; 80.59% on StreamingBench (ref: sources/simplestream-streaming-video-baseline.md)
- Outperforms 13 baseline models with sophisticated memory mechanisms (ref: sources/simplestream-streaming-video-baseline.md)
- Core insight: adding historical context improves recall but weakens real-time perception — recency window trades off differently from long-range memory (ref: sources/simplestream-streaming-video-baseline.md)
- Context value scales with backbone architecture, not uniformly with model size (ref: sources/simplestream-streaming-video-baseline.md)
- Authors recommend benchmarks separate "recent-scene perception" from "long-range memory recall" to prevent evaluations that reward spurious complexity (ref: sources/simplestream-streaming-video-baseline.md)

## Relevance to STOPA

The recency-wins finding applies to STOPA context engineering: for time-sensitive skills (real-time fetch, streaming analysis), a sliding window of the N most recent items often outperforms complex retrieval; long-range memory adds value only when the task requires historical recall, not recency perception.

## Mentioned In

- [SimpleStream — A Simple Baseline for Streaming Video Understanding](../sources/simplestream-streaming-video-baseline.md)
