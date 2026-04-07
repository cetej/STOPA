---
name: dev-browser
type: tool
first_seen: 2026-04-07
last_updated: 2026-04-07
sources: [dev-browser-research]
tags: [web, browser-automation, claude-code, security]
---

# dev-browser

> CLI tool where the agent writes TypeScript/JS scripts that run in a QuickJS WASM sandbox controlling a Playwright browser — no MCP server, no tool schema overhead.

## Key Facts

- Created by Sawyer Hood (ex-Figma/Facebook); MIT license; 4.4k GitHub stars, 264 Claude Code installs (ref: sources/dev-browser-research.md)
- Architecture: Rust CLI → QuickJS WASM sandbox → Playwright Node.js daemon (ref: sources/dev-browser-research.md)
- Benchmark (self-published): 29 turns / $0.88 vs Playwright MCP 51 turns / $1.45 for same task (ref: sources/dev-browser-research.md)
- Named persistent pages survive across script invocations; `page.snapshotForAI()` for token-optimized DOM (ref: sources/dev-browser-research.md)
- v0.2.0 (March 2026): major rewrite resolved critical RCE-via-prompt-injection vulnerability (ref: sources/dev-browser-research.md)
- Two modes: `--headless` (fresh Chromium) and `--connect` (attach to existing Chrome with cookies/auth) (ref: sources/dev-browser-research.md)
- Pre-approve in settings.json: `"allow": ["Bash(dev-browser *)"]` (ref: sources/dev-browser-research.md)

## Relevance to STOPA

Primary candidate for `/browse` skill backend. Code-first approach aligns with STOPA's Bash-tool model — no MCP config needed. Security model (QuickJS sandbox) justifies pre-approval. Use `--connect` for authenticated sessions, `--headless` for isolated scraping.

## Mentioned In

- [dev-browser Research](../sources/dev-browser-research.md)
