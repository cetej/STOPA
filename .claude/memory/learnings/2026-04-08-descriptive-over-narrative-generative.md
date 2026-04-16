---
date: 2026-04-08
type: best_practice
severity: medium
component: skill
tags: [prompt-engineering, generative-media, klip, nano, anti-pattern]
summary: "For generative media prompts (image/video): only describe observable outputs (what the renderer sees), never internal states (emotions, intentions). Converts to: 'tears streaming down her cheeks' not 'she feels sad'. Rhythm words > technical params — models parse semantics, not numbers."
source: external_research
uses: 1
successful_uses: 0
harmful_uses: 0
confidence: 0.95
verify_check: "manual"
---

# Descriptive Over Narrative — Generative Media Prompt Principle

## Context

From Seedance 2.0 Shot Design skill (v1.8.3 — added as core rule #12). Based on observation that AI video/image models render physical reality, not psychological states.

## Rules

1. **Only write what the renderer can render** — visual/physical descriptions only
2. **Convert emotions to observable signals**:
   - `She is sad` → `Tears streaming down her cheeks, lips trembling slightly`
   - `He is angry` → `Jaw clenched, fists tightening, veins visible on neck`
   - `They feel hope` → `Eyes lift toward light, shoulders relax, breath slows`
3. **Semantic intensity > technical parameters**:
   - `gentle, gradual, smooth` > `24fps, f/2.8, slow-motion`
   - Models parse language semantics, not numeric specs
4. **I2V extension**: In image-to-video, only describe CHANGES from first frame — not static content already visible. Add anchor phrase `preserve composition and colors`.

## Generalization

This principle extends beyond video:
- `/nano` (image): describe textures, lighting conditions, physical arrangements — not "a peaceful scene" but "morning light through thin curtains casting long shadows on wooden floor"
- Agent outputs: describe what you observed in tool output, not what you "feel" is correct. `"The tests passed — pytest reported 47 PASSED, 0 FAILED"` not `"The tests should be passing now"`

**Connection**: This reinforces critical-pattern #10 (anti-hallucination) — both rules say: describe observable reality, not assumed/internal states.
