---
name: Progressive Knowledge Routing
type: concept
first_seen: 2026-04-08
last_updated: 2026-04-08
sources: [seedance-shot-design-skill-patterns]
tags: [skill-design, knowledge-loading, context-engineering, reference-files]
---

# Progressive Knowledge Routing

> A 3-layer pattern for loading reference knowledge in skills: always-on baseline, semantic-inference auto-load, and explicit-override — ensuring quality floor without token waste.

## Key Facts

- **Layer 1 — Always-On**: Critical reference files loaded unconditionally (e.g., camera dictionary + quality anchors in Seedance skill). These set the quality baseline for every invocation. (ref: sources/seedance-shot-design-skill-patterns.md)
- **Layer 2 — Semantic Inference**: Agent infers which additional knowledge bases are needed from natural language signals in user input — without the user naming them explicitly. "Chase scene" → load action physics vocabulary. (ref: sources/seedance-shot-design-skill-patterns.md)
- **Layer 3 — Explicit Override**: When user directly names a style/template/reference, load that content immediately. Highest priority. (ref: sources/seedance-shot-design-skill-patterns.md)
- **Design principle**: "Cost of loading a knowledge base << cost of generating a low-quality output." Bias toward loading. (ref: sources/seedance-shot-design-skill-patterns.md)
- Related to SKILL0-inspired dynamic curriculum: first invocation = full context, subsequent = compact variant. (ref: skill-files.md rule set)

## Relevance to STOPA

Directly applicable to any STOPA skill with reference files (e.g., `/klip`, `/nano`, `/deepresearch`). The 3-layer pattern prevents both token waste (blind loading of all refs) and quality collapse (missing key refs). Implements the "context engineering, not prompt engineering" principle already in skill-files.md.

## Mentioned In

- [Seedance 2.0 Shot Design — Skill Architecture Patterns](../sources/seedance-shot-design-skill-patterns.md)
