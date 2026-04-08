---
name: Descriptive Over Narrative
type: concept
first_seen: 2026-04-08
last_updated: 2026-04-08
sources: [seedance-shot-design-skill-patterns]
tags: [prompt-engineering, generative-media, skill-design, anti-pattern]
---

# Descriptive Over Narrative

> Principle for generative media prompts: only describe what is *observable* (what the camera/renderer sees), never what is *internal* (emotions, thoughts, intentions).

## Key Facts

- **Rule**: "Only write what the camera SEES (visual words), never what characters FEEL (emotion words). AI renders visuals, not psychology." (ref: sources/seedance-shot-design-skill-patterns.md)
- **Conversion**: All emotions must be translated into visible physical expressions — facial micro-expressions, body language, breathing rhythm, gaze direction. (ref: sources/seedance-shot-design-skill-patterns.md)
- **Bad**: `She feels heartbroken` — not renderable
- **Good**: `Tears streaming down her cheeks, lips trembling slightly` — physically observable (ref: sources/seedance-shot-design-skill-patterns.md)
- **Related I2V rule**: In image-to-video mode, only describe *changes* from the first frame — not static content already visible. Prevents redundancy drift. (ref: sources/seedance-shot-design-skill-patterns.md)
- Extends to "rhythm words over technical params": `gentle/gradual/smooth` > `24fps/f2.8` — models parse semantics, not numeric specs. (ref: sources/seedance-shot-design-skill-patterns.md)

## Relevance to STOPA

Applicable to `/klip`, `/nano` prompt generation — and to any agent output rule where the model should describe observable tool outputs rather than claimed internal states. Generalizes: "describe what you can verify, not what you assume." Cross-links to anti-hallucination pattern (#10 in critical-patterns.md).

## Mentioned In

- [Seedance 2.0 Shot Design — Skill Architecture Patterns](../sources/seedance-shot-design-skill-patterns.md)
