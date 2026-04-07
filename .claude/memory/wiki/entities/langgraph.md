---
name: LangGraph
type: tool
first_seen: 2026-04-07
last_updated: 2026-04-07
sources: [radar-claude-code-sdk-python]
tags: [orchestration, python]
---

# LangGraph

> Graph-based multi-agent workflow framework od LangChain — nejvyšší flexibilita pro komplexní orchestraci, ale overkill pro CC-specific use cases.

## Key Facts

- Graph-based workflow: nejvyšší flexibilita, ale vysoký overhead a složitý setup (ref: sources/radar-claude-code-sdk-python.md)
- Nevyužívá CC specifické funkce: skills, CLAUDE.md, hooks, memory — abstrahuje je pryč (ref: sources/radar-claude-code-sdk-python.md)
- Srovnání vs. claude-agent-sdk: LangGraph je obecnější, claude-agent-sdk je CC-native (ref: sources/radar-claude-code-sdk-python.md)
- Pro STOPA: overkill, nevhodný — claude-agent-sdk zachovává CC-specific výhody (ref: sources/radar-claude-code-sdk-python.md)

## Relevance to STOPA

Explicitně vyloučen pro STOPA orchestraci — abstrahovalo by CC-specific funkce (skills, CLAUDE.md, memory). Dokumentováno jako referenční porovnání pro rozhodnutí použít claude-agent-sdk.

## Mentioned In

- [Radar: claude-code-sdk-python](../sources/radar-claude-code-sdk-python.md)
