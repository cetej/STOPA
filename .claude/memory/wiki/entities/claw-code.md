---
name: Claw Code
type: tool
first_seen: 2026-04-07
last_updated: 2026-04-07
sources: [claw-code-architecture]
tags: [orchestration, security, mcp, multi-agent]
---

# Claw Code

> Fork Claude Code (instructkr/claw-code → ultraworkers/claw-code) s rozšířenou security architekturou, 6 MCP transporty a multi-agent orchestrací přes QueryEngine.

## Key Facts

- 3-tier permission model: ReadOnly / WorkspaceWrite / DangerFullAccess (ref: sources/claw-code-architecture.md)
- COORDINATOR_MODE omezuje koordinátora na [Agent, SendMessage, TaskStop] — nutí delegaci (ref: sources/claw-code-architecture.md)
- 5 built-in agent typů: explore (Haiku, read-only), plan, general, verification, guide (ref: sources/claw-code-architecture.md)
- BashTool má 8vrstvý security stack — nejkomplexněji gated tool v systému
- Agent Teams (Fork/Teammate/Worktree spawn módy) — jen Opus 4.6

## Relevance to STOPA

COORDINATOR_MODE pattern je přímou inspirací pro refaktoring /orchestrate skill: orchestrátor by měl mít `allowed-tools: [Agent, Read, Grep, Glob]` a delegovat veškerou práci. QueryEngine budget control (max_turns, max_budget_tokens) odpovídá STOPA tier systému.

## Mentioned In

- [Claw Code — Architektonická analýza pro STOPA](../sources/claw-code-architecture.md)
