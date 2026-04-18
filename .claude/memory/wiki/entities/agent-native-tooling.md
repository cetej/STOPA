---
name: Agent-Native Tooling
type: concept
first_seen: 2026-04-18
last_updated: 2026-04-18
sources: [heygen-hyperframes-agentic-video]
tags: [skill-design, agent, tools, philosophy, training-data]
---

# Agent-Native Tooling

> Design principle: tools for LLM agents should use media/formats from agents' training data (HTML, Markdown, plain code), not formats designed for humans (GUI timelines, XML, proprietary binary).

## Key Facts

- LLMs were trained on billions of HTML pages, millions of CSS/JS animations, hundreds of thousands of GSAP/SVG/Canvas snippets — web is the largest creative medium in training data by orders of magnitude (ref: sources/heygen-hyperframes-agentic-video.md)
- "AI Agents shouldn't be learning After Effects or DaVinci Resolve — JSON/XML based tools are built for humans, not agents" (HeyGen argument) (ref: sources/heygen-hyperframes-agentic-video.md)
- Pre-Nov 2025 (Gemini 3, Opus 4.5): even agent-native code generation for video was unreliable; model capability inflection enabled consistent quality output (ref: sources/heygen-hyperframes-agentic-video.md)
- Thin abstraction pattern: HeyGen added only a handful of `data-` attributes on top of standard HTML — rest is vanilla web tech (ref: sources/heygen-hyperframes-agentic-video.md)

## Relevance to STOPA

Aligns with and validates STOPA's latent/deterministic boundary (Garry Tan) and fat-skills philosophy. Also principle for STOPA skill design: prefer markdown + plain Python/Bash over YAML DSLs or GUI-configured tools. Extends beyond video — applies to any creative or operational tool given to an agent.

## Mentioned In

- [Agentic Video is HTML: Open Sourcing HyperFrames](../sources/heygen-hyperframes-agentic-video.md)
