---
title: "Seedance 2.0 Shot Design — Skill Architecture Patterns"
slug: seedance-shot-design-skill-patterns
source_type: url
url: "https://github.com/woodfantasy/Seedance2.0-ShotDesign-Skills"
date_ingested: 2026-04-08
date_published: "2026-04-08 (v1.8.3)"
entities_extracted: 4
claims_extracted: 7
---

# Seedance 2.0 Shot Design — Skill Architecture Patterns

> **TL;DR**: Production-grade Claude Code skill for AI video prompt generation (Seedance 2.0 platform). Primary value for STOPA: 4 transferable skill design patterns — 3-layer knowledge routing, LLM-native structured validation, descriptive-over-narrative principle, and style conflict matrix. Platform-specific content (Chinese review system, @引用 syntax) is irrelevant to STOPA.

## Key Claims

1. 3-layer knowledge routing (always-on/semantic-inference/explicit-override) prevents quality collapse without token waste — `[argued]`
2. LLM-native validation replaced Python execution after security platform flagged shell patterns; identical coverage, no execution risk — `[verified]` (v1.8.1 changelog)
3. Descriptive over narrative: AI renderers process visuals not psychology — emotion words produce worse output than observable physical descriptions — `[argued]`
4. One-shot-one-move: combining camera movements in a single time segment causes jitter — `[asserted]`
5. 60–100 word sweet spot for generative prompts: below = vague, above = concept drift + instruction conflicts — `[argued]`
6. Semantic intensity words (gentle/gradual/smooth) outperform technical parameters (24fps/f2.8) because models parse semantics not numeric specs — `[argued]`
7. Style conflict matrix (precomputed mutually exclusive pairs) catches physically impossible combinations before generation — `[argued]`

## Entities

| Entity | Type | Status |
|--------|------|--------|
| [Progressive Knowledge Routing](../entities/progressive-knowledge-routing.md) | concept | new |
| [LLM-Native Validation](../entities/llm-native-validation.md) | concept | new |
| [Descriptive Over Narrative](../entities/descriptive-over-narrative.md) | concept | new |
| [Style Conflict Matrix](../entities/style-conflict-matrix.md) | concept | new |

## Relations

- `progressive-knowledge-routing` `inspired_by` skill-design (STOPA skill-files.md context-engineering principle)
- `llm-native-validation` `supersedes` python-based-validation (in agent execution path; Python retained for CI/CD)
- `descriptive-over-narrative` `part_of` prompt-engineering (generative media domain)
- `style-conflict-matrix` `part_of` `llm-native-validation` (rule ⑥ in the 7-rule checklist)
- `seedance-shot-design` `uses` `progressive-knowledge-routing` + `llm-native-validation`

## Cross-References

- Related learnings: none directly matched (new patterns not yet in learnings/)
- Related wiki articles: [skill-design](../skill-design.md) (description=routing trigger, body=context)
- Related entities: `schema-utility-decoupling` (existing entity — LLM-native validation is runtime complement)
- Contradictions: none detected
