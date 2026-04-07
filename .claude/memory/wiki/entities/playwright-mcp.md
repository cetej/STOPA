---
name: Playwright MCP
type: tool
first_seen: 2026-04-07
last_updated: 2026-04-07
sources: [dev-browser-research]
tags: [web, browser-automation, mcp]
---

# Playwright MCP

> Microsoft's MCP server for browser automation exposing 26+ discrete tools — each browser action is a separate MCP tool call.

## Key Facts

- Tool schema alone costs ~13,700 tokens per session (ref: sources/dev-browser-research.md)
- 51 turns vs dev-browser's 29 turns for equivalent task in author's benchmark (ref: sources/dev-browser-research.md)
- $1.45 vs $0.88 per task in same benchmark (ref: sources/dev-browser-research.md)
- Action-by-action model: one MCP call per browser action (click, fill, goto, etc.) (ref: sources/dev-browser-research.md)
- >10k GitHub stars (ref: sources/dev-browser-research.md)

## Relevance to STOPA

Anti-pattern for STOPA — avoid. 13,700 token overhead per session is unacceptable. dev-browser is the preferred alternative. NEVER add Playwright MCP to Claude Desktop (see behavioral-genome.md anti-patterns).

## Mentioned In

- [dev-browser Research](../sources/dev-browser-research.md)
