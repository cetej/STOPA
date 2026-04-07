---
title: "dev-browser — Browser Automation for Claude Code"
slug: dev-browser-research
source_type: research_output
date_ingested: 2026-04-07
entities_extracted: 8
claims_extracted: 5
---

# dev-browser — Browser Automation for Claude Code

> **TL;DR**: dev-browser is a code-execution bridge tool (not MCP server) where the agent writes TypeScript/JS scripts that run in a QuickJS WASM sandbox controlling a Playwright-backed browser. Created by Sawyer Hood (ex-Figma/Facebook), it uses 29 turns vs Playwright MCP's 51 turns for equivalent tasks, at $0.88 vs $1.45 cost. It is the most-installed Claude Code browser skill with 264 installations.

## Key Claims

1. Agent writes scripts → QuickJS WASM sandbox → Playwright daemon; no MCP tool schema overhead (~0 tokens vs 13,700 for Playwright MCP) — `[verified]`
2. Self-published benchmark: 3m53s/$0.88/29 turns vs Playwright MCP 4m31s/$1.45/51 turns — `[argued]` (conflict of interest: author-run benchmark)
3. A critical RCE-via-prompt-injection vulnerability was resolved by the v0.2.0 architectural rewrite; PoC never publicly disclosed — `[verified]`
4. Named persistent pages survive across script invocations; `page.snapshotForAI()` returns token-optimized DOM — `[verified]`
5. Windows x64 support added in v0.2.3 (March 2026); MIT license — `[verified]`

## Entities

| Entity | Type | Status |
|--------|------|--------|
| dev-browser | tool | new |
| Sawyer Hood | person | new |
| QuickJS WASM | concept | new |
| Playwright MCP | tool | new |
| agent-browser (Vercel) | tool | new |
| browser-use | tool | new |
| PinchTab | tool | new |
| Smooth Brain LLC | company | new |

## Relations

- Sawyer Hood `created` dev-browser
- dev-browser `uses` QuickJS WASM (sandbox isolation)
- dev-browser `uses` Playwright (browser control daemon)
- dev-browser `competes_with` Playwright MCP (code-first vs action-by-action)
- Sawyer Hood `operates` Smooth Brain LLC
