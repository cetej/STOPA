---
name: clean-writing
variant: compact
description: "Use when editing text to remove AI writing patterns ('AI-isms'). Trigger on 'clean writing', 'remove AI-isms', 'uprav text', 'odstraň AI patterny', 'zní to jako AI'."
version: 1.0.0
---

# Clean Writing — Compact

Audit & rewrite text to remove AI-isms. Two modes: `rewrite` (default) or `detect` (flag only).

## Quick Reference

1. Detect language → load `word-table-cs.md` or `word-table-en.md` from skill dir
2. Auto-detect context profile: social | blog | technical | email | docs | casual
3. Audit ALL patterns (P0/P1/P2)
4. Rewrite mode: fix → second pass → output 4 sections
5. Detect mode: flag → assess → output 2 sections

## Severity

- **P0**: chatbot artifacts, sycophancy, cutoff disclaimers, vague attributions, significance inflation
- **P1**: word-table Tier 1, templates, "pojďme/let's", synonym cycling, formulaic openings, bold/em-dash excess
- **P2**: generic conclusions, rule-of-three, uniform length, copula, transitions

## Critical Rules

- Structure > vocabulary (rhythm uniformity is #1 signal)
- Load word table for detected language ALWAYS
- Second pass catches over-polishing (rewrite becoming MORE uniform)
- 5+ vocab + 3+ patterns + uniform rhythm → full rewrite, not patch
- Keep author's voice — don't over-sanitize
- CZ: em dash limit 2-3/1000w (not 0-1 like EN)
- CZ-specific: pasivum, nominalizace, "daný", řetězení předložek, infinitivní řetězce
- Profile tolerance overrides apply (technical gets exceptions)

## Output Format

**Rewrite**: 1. Issues found → 2. Rewritten → 3. What changed → 4. Second-pass
**Detect**: 1. Issues found (by P0/P1/P2) → 2. Assessment
