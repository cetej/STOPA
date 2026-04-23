---
title: Qwen3.6-27B — Flagship Coding in a Dense 27B Model
category: concepts
tags: [models, open-source, local-inference, coding, efficiency]
sources: [simonwillison.net/2026/Apr/22/qwen36-27b/]
updated: 2026-04-23
---

# Qwen3.6-27B — Flagship Coding in a Dense 27B Model

**Source**: Simon Willison, simonwillison.net, April 22, 2026  
**Organization**: Alibaba / Qwen team

## Core Claim

A 27B dense model matches or exceeds a 397B MoE predecessor on coding benchmarks, enabling powerful coding capability on consumer hardware without cloud dependency.

## Key Numbers

| Metric | Value |
|--------|-------|
| Parameter count | 27B |
| Full model size | 55.6 GB |
| Quantized (GGUF) | 16.8 GB |
| Previous model size | 807 GB (397B-A17B) |
| Read speed | 54.32 tokens/s |
| Generation speed | ~25 tokens/s |

## Why It Matters

**Dense vs MoE tradeoff**: MoE models activate only a fraction of parameters per token (hence "397B-A17B" = 397B total, 17B active). A dense 27B model activating all parameters may still match MoE on specialized tasks where depth > breadth.

**Local deployment**: 16.8 GB quantized fits in consumer GPU VRAM, enabling offline agentic coding without API dependency.

**SVG generation** is highlighted as a specific capability — relevant for agentic UI scaffolding and design-to-code workflows.

## Tooling

- llama.cpp + llama-server for local inference
- GGUF format for quantization
- Hugging Face for model hosting

## STOPA Relevance

Local models as fallback or specialized worker nodes in STOPA's agent pool. Qwen3.6-27B at 16.8 GB = viable Haiku alternative for coding tasks when:
- API costs prohibitive (farm tier)
- Offline operation required
- Specialized coding workload where 27B dense can match API models

## Related Concepts

→ [claude-opus-47.md](claude-opus-47.md)  
→ [paramanager-orchestrator.md](paramanager-orchestrator.md)  
→ [agentforge.md](agentforge.md)
