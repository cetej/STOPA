---
name: QuickJS WASM
type: concept
first_seen: 2026-04-07
last_updated: 2026-04-07
sources: [dev-browser-research]
tags: [security, browser-automation, sandboxing]
---

# QuickJS WASM

> A WebAssembly-compiled JavaScript engine (QuickJS) used as an execution sandbox — scripts run without host filesystem access, network access, or native modules.

## Key Facts

- Used by dev-browser to isolate agent-written scripts from host OS (ref: sources/dev-browser-research.md)
- Limitations: no `require()`, no native Node.js modules, no direct network access (ref: sources/dev-browser-research.md)
- Security model: sandbox escape = full host access; one confirmed RCE resolved in v0.2.0 (ref: sources/dev-browser-research.md)
- File I/O confined to `~/.dev-browser/tmp/` only (ref: sources/dev-browser-research.md)

## Relevance to STOPA

Enables pre-approval of `Bash(dev-browser *)` in settings.json without per-invocation prompts. Security boundary that justifies STOPA's `/browse` skill pre-approval pattern.

## Mentioned In

- [dev-browser Research](../sources/dev-browser-research.md)
