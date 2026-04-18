---
title: "HyperFrames GitHub Repository"
slug: hyperframes-github-repo
source_type: url
url: "https://github.com/heygen-com/hyperframes"
date_ingested: 2026-04-18
date_published: "ongoing"
authors: "HeyGen team"
entities_extracted: 0
claims_extracted: 4
---

# HyperFrames GitHub Repository

> **TL;DR**: Technical repo details — monorepo with CLI, Puppeteer+FFmpeg render pipeline, Frame Adapter Pattern for pluggable animation runtimes, deterministic output guarantee. 4.5k stars, 34 releases, TypeScript 97.5%. Complements blog-post source with architecture specifics.

## Key Claims

1. Identical inputs always produce identical video outputs — deterministic pipeline — `asserted`
2. Frame Adapter Pattern: pluggable integration of GSAP, Lottie, CSS, Three.js, WebGL shaders — `asserted`
3. CLI designed non-interactive for agent automation (`npx hyperframes init`, preview, lint, render) — `asserted`
4. 4.5k stars, 322 forks, 34 releases — TypeScript 97.5%, Apache 2.0 — `verified` (GitHub stats)

## Entities

| Entity | Type | Status |
|--------|------|--------|
| [HyperFrames](../entities/hyperframes.md) | tool | updated (+5 facts) |

## Relations

- HyperFrames `uses` Puppeteer — capture engine
- HyperFrames `uses` FFmpeg — rendering pipeline

## Cross-References

- Related learnings: `2026-04-18-html-as-agent-native-medium.md` (agent-native tooling)
- Critical pattern: #4 Harness > Skill for Deterministic — HyperFrames' deterministic guarantee aligns with this
- Related memory: `reference_agent_friendly_cli.md` — CLI non-interactive design matches agent-friendly pattern
- Contradictions: none
