---
name: CaMeL
type: tool
first_seen: 2026-04-07
last_updated: 2026-04-07
sources: [agent-defense-frameworks]
tags: [security, prompt-injection, dual-llm, capability-tracking]
---

# CaMeL

> Google DeepMind + ETH Zurich (arXiv:2503.18813) — architektonická obrana proti prompt injection přes dual-LLM vzor a capability tracking. Research artifact, ne produkční knihovna.

## Key Facts

- Dual-LLM: P-LLM (trusted planner, restricted Python dialect) + Q-LLM (quarantined data processor) (ref: sources/agent-defense-frameworks.md)
- Capability tags na každé proměnné: trusted user vs untrusted external source
- 77% task success s provable security vs 84% baseline (7% utility trade-off)
- Explicitní varování v repo: "likely contains bugs and not a Google product"
- Instalace přes uv, ne pip — nelze použít jako standalone library

## Relevance to STOPA

Plná implementace nepraktická. Capability tagging vzor lze approximovat: označit tool outputs jako [UNTRUSTED] v memory state, PreToolUse hook blokuje použití untrusted dat v privilegovaných tools. Agent zpracovávající external data by neměl vypsat přímé příkazy — pouze data do state.md.

## Mentioned In

- [AI Agent Defense Frameworks Research](../sources/agent-defense-frameworks.md)
