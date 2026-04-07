---
name: claude-agent-sdk
type: tool
first_seen: 2026-04-07
last_updated: 2026-04-07
sources: [radar-claude-code-sdk-python]
tags: [orchestration, session, devops, python]
---

# claude-agent-sdk

> Oficiální Python SDK od Anthropic pro programatické řízení Claude Code CLI přes bidirektivní IPC protokol — umožňuje headless CC sessions, custom AgentDefinition, Python hook callbacks a přesnou budget kontrolu.

## Key Facts

- PyPI: `pip install claude-agent-sdk`, verze 0.1.55, MIT licence (ref: sources/radar-claude-code-sdk-python.md)
- Architektura: spouští `claude` CLI subprocess, komunikuje přes JSON/stdio IPC — nevolá Anthropic API přímo (ref: sources/radar-claude-code-sdk-python.md)
- Dva vstupní body: `query()` (async iterator, jednosměrný) a `ClaudeSDKClient` (bidirektivní, umožňuje follow-up bez nového procesu) (ref: sources/radar-claude-code-sdk-python.md)
- ClaudeAgentOptions klíčové fieldy: `max_budget_usd`, `permission_mode`, `setting_sources`, `hooks`, `agents`, `mcp_servers` (ref: sources/radar-claude-code-sdk-python.md)
- 6111 stars, 55+ releases za 10 měsíců, průměrný release každé 2-4 dny (ref: sources/radar-claude-code-sdk-python.md)
- Bug #768: `bypassPermissions` + settings.json hooks nefungují dohromady (ref: sources/radar-claude-code-sdk-python.md)
- Bug #425: SDK MCP tools selhávají pod background subagenty (ref: sources/radar-claude-code-sdk-python.md)
- Windows: funguje s anyio, cesty přes pathlib.Path() (ref: sources/radar-claude-code-sdk-python.md)

## Relevance to STOPA

Klíčový nástroj pro implementaci autonomních scheduled agentů mimo CC session. Umožňuje `spawn_subagent_sdk()` jako alternativu k Agent tool s přesnou budget kontrolou per tier. Python hook callbacks mohou nahradit shell hook skripty (až po opravě bug #768). Pro `/schedule` skill: SDK je přímý implementační základ.

Doporučení: INTEGROVAT s prioritou vysoká. Čekat na fix #768 před nahrazením hook skriptů, fix #425 před heavy orchestrací.

## Mentioned In

- [Radar: claude-code-sdk-python](../sources/radar-claude-code-sdk-python.md)
