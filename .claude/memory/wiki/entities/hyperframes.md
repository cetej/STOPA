---
name: HyperFrames
type: tool
first_seen: 2026-04-18
last_updated: 2026-04-18
sources: [heygen-hyperframes-agentic-video, hyperframes-github-repo]
last_updated: 2026-04-18
tags: [video, agent-native, html, skill, media, gsap, rendering, typescript, deterministic]
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
- **Deterministic output**: identical inputs always produce identical video — supports reliable automated pipelines (ref: sources/hyperframes-github-repo.md)
- **Frame Adapter Pattern**: pluggable animation runtime integration (GSAP, Lottie, CSS, Three.js, WebGL shaders) (ref: sources/hyperframes-github-repo.md)
- Monorepo: CLI (create/preview/lint/render), core parser+runtime, Puppeteer+FFmpeg capture, audio mixing, browser editor UI, embeddable player, WebGL transitions (ref: sources/hyperframes-github-repo.md)
- CLI designed non-interactive for agent automation; `npx hyperframes init` for manual init (ref: sources/hyperframes-github-repo.md)
- 4.5k stars, 322 forks, 34 releases — TypeScript 97.5%; docs: hyperframes.heygen.com (ref: sources/hyperframes-github-repo.md)

## Relevance to STOPA

Concrete implementation of agent-native tooling philosophy — matches STOPA's latent/deterministic boundary (skill as thin harness over rich HTML/JS capabilities). Potential complement/alternative to `/klip` skill for programmatic video composition (klip = text-to-video via Kling, HyperFrames = code-to-video via HTML).

## Mentioned In

- [Agentic Video is HTML: Open Sourcing HyperFrames](../sources/heygen-hyperframes-agentic-video.md)
- [HyperFrames GitHub Repository](../sources/hyperframes-github-repo.md)
