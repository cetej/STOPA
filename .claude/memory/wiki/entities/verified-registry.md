---
name: VerifiedRegistry
type: concept
first_seen: 2026-04-07
last_updated: 2026-04-07
sources: [autoresearchclaw-research]
tags: [code-quality, testing, pipeline]
---

# VerifiedRegistry

> Architektonický (ne post-hoc) přístup k anti-fabricaci v AI research pipeline: číselný whitelist z experimentálních dat, budovaný PŘED psaním, s 1% tolerancí fuzzy matching a section-level enforcement.

## Key Facts

- Dataclass: `values: dict[float, str]` (numeric → provenance), primary_metric, metric_direction (ref: sources/autoresearchclaw-research.md)
- 7-step registration pipeline: best-run metrics → condition summaries → metrics summary → primary metric → per-condition stats → pairwise differences → refinement log (ref: sources/autoresearchclaw-research.md)
- Variant registration: automaticky registruje rounding variants (1-4 decimal places), percentage conversions (×100), fractional conversions (÷100) (ref: sources/autoresearchclaw-research.md)
- `is_verified(number, tolerance=0.01)` — 1% relative tolerance (ref: sources/autoresearchclaw-research.md)
- Paper verifier: strict sections (Results, Experiments, Tables) → rejection; lenient (Introduction, Related Work) → warnings (ref: sources/autoresearchclaw-research.md)
- BUG-222 fix: `best_only=True` prevents regressed refinement iterations from polluting whitelist (ref: sources/autoresearchclaw-research.md)

## Relevance to STOPA

Přímá inspirace pro STOPA eval a harness systém. Pattern: build whitelist from ground-truth data BEFORE running verification. Aplikace: v `/verify` skill ověřovat metriky oproti whitelist z předchozích runs.

## Mentioned In

- [AutoResearchClaw Architecture Research](../sources/autoresearchclaw-research.md)
