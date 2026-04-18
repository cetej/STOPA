---
name: HyperFrames
type: tool
first_seen: 2026-04-18
last_updated: 2026-04-18
sources: [heygen-hyperframes-agentic-video]
tags: [video, agent-native, html, skill, media, gsap, rendering]
---

# HyperFrames

> HTML-based video toolchain by HeyGen that turns agent-written HTML+CSS+JS into rendered MP4/MOV/WebM, distributed as a Claude Code skill.

## Key Facts

- Converts HTML + `data-` attributes (`data-composition-id`, `data-start`, `data-duration`, `data-track-index`) into video timeline definitions (ref: sources/heygen-hyperframes-agentic-video.md)
- Install as skill: `npx skills add heygen-com/hyperframes` — one-command integration (ref: sources/heygen-hyperframes-agentic-video.md)
- Works with any agent/LLM, zero API keys, all rendering done locally (ref: sources/heygen-hyperframes-agentic-video.md)
- Inspired by openclaw and Remotion; built on GSAP for JS animation (ref: sources/heygen-hyperframes-agentic-video.md)
- Apache 2.0 license — core engine + studio + renderer + skills + examples (ref: sources/heygen-hyperframes-agentic-video.md)
- Anything that works in a browser works in HyperFrames: CSS animations, GSAP timelines, Lottie, Three.js, D3, Google Fonts, Canvas, SVG (ref: sources/heygen-hyperframes-agentic-video.md)

## Relevance to STOPA

Concrete implementation of agent-native tooling philosophy — matches STOPA's latent/deterministic boundary (skill as thin harness over rich HTML/JS capabilities). Potential complement/alternative to `/klip` skill for programmatic video composition (klip = text-to-video via Kling, HyperFrames = code-to-video via HTML).

## Mentioned In

- [Agentic Video is HTML: Open Sourcing HyperFrames](../sources/heygen-hyperframes-agentic-video.md)
