---
title: "Agentic Video is HTML: Open Sourcing HyperFrames"
slug: heygen-hyperframes-agentic-video
source_type: url
url: "https://heygen.com/blog/hyperframes (reconstructed from user paste)"
date_ingested: 2026-04-18
date_published: "2026-04-18"
authors: "HeyGen team (Abhay Zala, Jake, James Rames Jusso, Miguel, Vance Ingalls)"
entities_extracted: 3
claims_extracted: 6
---

# Agentic Video is HTML: Open Sourcing HyperFrames

> **TL;DR**: HeyGen open-sourced HyperFrames (Apache 2.0) — an HTML-based video toolchain where agents write HTML+CSS+JS and it renders to MP4/MOV/WebM. Core thesis: agents are fluent in web tech from training data; video tools should match that, not After Effects. Installs as a Claude Code skill via `npx skills add heygen-com/hyperframes`.

## Key Claims

1. HTML + thin `data-` attribute layer (`data-composition-id/start/duration/track-index`) = complete agent-legible video timeline — `verified` (code example shown)
2. LLMs were trained on web content orders of magnitude more than any other creative medium; HTML is their "native tongue" — `argued`
3. Pre-Nov 2025 models could not reliably generate motion graphics via code; Gemini 3 + Opus 4.5 were the capability inflection point — `asserted`
4. HyperFrames works with any agent/LLM, zero API keys, fully local rendering — `asserted`
5. Inspired by openclaw, Remotion, and GSAP — `asserted`
6. Complete 5-second two-scene video composition fits in <70 lines of HTML — `verified` (code shown)

## Entities

| Entity | Type | Status |
|--------|------|--------|
| [HyperFrames](../entities/hyperframes.md) | tool | new |
| [Agent-Native Tooling](../entities/agent-native-tooling.md) | concept | new |
| [HeyGen](../entities/heygen.md) | company | new |
| [OpenClaw](../entities/openclaw.md) | tool | existing (inspiration source) |

## Relations

- HyperFrames `uses` GSAP — JS animation library
- HyperFrames `inspired_by` OpenClaw — cited as inspiration in blog
- HyperFrames `inspired_by` Remotion — cited as inspiration
- HyperFrames `part_of` Agent-Native Tooling — concrete implementation of the design philosophy
- HyperFrames `created_by` HeyGen

## Cross-References

- Related learnings: `2026-04-12-purpose-built-tools-75x-faster.md` (thin harness/fat skill validates this design), `2026-04-08-descriptive-over-narrative-generative.md` (code-gen for creative output)
- Related wiki articles: [skill-design](../skill-design.md) (latent/deterministic boundary)
- Related STOPA skills: `/klip` (video via Kling) — HyperFrames is the code-gen complement to klip's text-to-video
- Contradictions: none
