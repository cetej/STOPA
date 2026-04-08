---
name: Style Conflict Matrix
type: concept
first_seen: 2026-04-08
last_updated: 2026-04-08
sources: [seedance-shot-design-skill-patterns]
tags: [prompt-engineering, validation, generative-media, anti-pattern]
---

# Style Conflict Matrix

> A precomputed set of mutually exclusive style/technique pairs that produce artifacts when combined — enforced as hard errors in prompt validation.

## Key Facts

- **Video conflicts** (Seedance): IMAX vs VHS, film grain vs sharp digital, ink-wash vs UE5 ray-tracing, Cel-Shaded vs realistic PBR, slow motion vs speed ramp. (ref: sources/seedance-shot-design-skill-patterns.md)
- **Optical conflicts**: ultra-wide (14mm) + shallow depth-of-field bokeh (physically impossible), handheld camera + perfect geometric symmetry (contradictory intent). (ref: sources/seedance-shot-design-skill-patterns.md)
- **Motion conflicts**: within a single time segment: push-in + pull-back simultaneously; fast action + slow motion simultaneously. (ref: sources/seedance-shot-design-skill-patterns.md)
- **Validation tier**: ❌ hard error — not a warning. Conflicting styles must be resolved before output is shown to user. (ref: sources/seedance-shot-design-skill-patterns.md)
- **Python implementation exists** (`validate_prompt.py`) for CI/CD use, but LLM-native checklist enforces same rules at runtime. (ref: sources/seedance-shot-design-skill-patterns.md)

## Relevance to STOPA

`/klip` and `/nano` currently have no conflict detection. Adding a conflict matrix (e.g., photorealistic vs cartoon, 8K vs VHS, portrait vs wide-angle + bokeh) would reduce invalid prompts sent to fal.ai. Pattern generalizes: any generative skill benefits from precomputed mutually-exclusive constraint sets.

## Mentioned In

- [Seedance 2.0 Shot Design — Skill Architecture Patterns](../sources/seedance-shot-design-skill-patterns.md)
