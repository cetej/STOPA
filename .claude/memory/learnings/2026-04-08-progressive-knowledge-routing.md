---
date: 2026-04-08
type: best_practice
severity: high
component: skill
tags: [skill-design, context-engineering, knowledge-loading, reference-files]
summary: "Skills with reference files should use 3-layer routing: always-on baseline (quality floor), semantic-inference auto-load (from natural language signals), explicit-override (user-named). Bias toward loading — cost of extra tokens << cost of low-quality output."
source: external_research
uses: 1
successful_uses: 0
harmful_uses: 0
confidence: 0.8
verify_check: "manual"
---

# Progressive Knowledge Routing — 3-Layer Pattern

## Context

From Seedance 2.0 Shot Design skill (v1.8.3, woodfantasy/Seedance2.0-ShotDesign-Skills). The skill manages 6 reference files (cinematography, director-styles, quality-anchors, scenarios, audio-tags, seedance-specs) using a structured loading strategy instead of loading all or loading nothing.

## Pattern

**Layer 1 — Always-On**: 2 files loaded unconditionally every invocation.
- These are the quality baseline — without them, every output is low quality
- Example: camera dictionary + quality anchors for video prompts

**Layer 2 — Semantic Inference**: Additional files auto-loaded from natural language signals.
- Agent infers need from user's words, not from explicit commands
- "Chase scene" → action physics vocabulary loaded automatically
- "Scary" → horror scenario template loaded automatically

**Layer 3 — Explicit Override**: User directly names style/template → load immediately.

## Design Principle

> "The cost of loading a knowledge base is far lower than the cost of generating a low-quality output. When in doubt, load it."

## Application to STOPA

- `/klip` should always load: motion vocabulary + quality anchors (Layer 1)
- `/klip` should auto-infer: style library (from "cinematic"/"anime"/"horror"), scenario templates (from scene type)
- Same pattern applies to `/deepresearch` (always load: source evaluation rubric; infer: domain-specific methodology)

**Why:** Relevant to skill-files.md "context engineering, not prompt engineering" principle already in STOPA. This makes it concrete and operational.
