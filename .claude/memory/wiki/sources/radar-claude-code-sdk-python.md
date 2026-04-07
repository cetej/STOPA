---
title: "Radar: claude-code-sdk-python (claude-agent-sdk) — 2026-04-03"
slug: radar-claude-code-sdk-python
source_type: research_output
date_ingested: 2026-04-07
entities_extracted: 6
claims_extracted: 5
---
# Radar: claude-code-sdk-python (claude-agent-sdk)

> **TL;DR**: Oficiální Python SDK od Anthropic pro programatické řízení Claude Code CLI přes IPC protokol (JSON přes stdio). Verze 0.1.55, 6111 stars, MIT licence. SDK umožňuje spouštět CC sessions headless, definovat custom agenty s AgentDefinition, Python hook callbacks, in-process MCP servery a přesnou budget kontrolu. Pro STOPA je klíčový jako základ autonomních scheduled agentů mimo CC session.

## Key Claims

1. SDK nevolá Anthropic API přímo — obaluje `claude` CLI subprocess přes bidirektivní IPC protokol; všechny CC funkce (skills, CLAUDE.md, hooks, memory) jsou dostupné programaticky — `[verified]`
2. ClaudeSDKClient umožňuje za-běhovou úpravu chování (set_permission_mode, interrupt, set_model) — kvalitativní skok oproti hook skriptům — `[argued]`
3. Bug #768: `bypassPermissions` mode ignoruje hooks ze settings.json — vyžaduje opravu před nahrazením hook skriptů Python callbacky — `[verified]`
4. Bug #425: SDK MCP tools selhávají pod background subagenty (message-queue backpressure) — limituje heavy orchestraci — `[verified]`
5. Pro STOPA je claude-agent-sdk jediná volba; LangGraph a CrewAI abstrahují CC-specifické funkce (skills, CLAUDE.md, memory) — `[argued]`

## Entities

| Entity | Type | Status |
|--------|------|--------|
| claude-agent-sdk | tool | new |
| ClaudeAgentOptions | concept | new |
| AgentDefinition | concept | new |
| Strands SDK | tool | new |
| LangGraph | tool | new |
| anyio | tool | new |

## Relations

- claude-agent-sdk `wraps` Claude Code CLI `via IPC`
- AgentDefinition `configures` claude-agent-sdk `sub-agents`
- claude-agent-sdk `competes-with` Strands SDK
- claude-agent-sdk `competes-with` LangGraph
- anyio `enables` claude-agent-sdk `cross-platform async on Windows`
