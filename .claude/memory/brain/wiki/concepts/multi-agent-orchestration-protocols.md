---
title: Multi-Agent Orchestration — Protocols and Enterprise Architecture
category: concepts
tags: [multi-agent, orchestration, mcp, agent2agent, enterprise, protocols, governance]
sources: [raw/2026-04-18-multi-agent-orchestration-survey.md]
updated: 2026-04-18
---

# Multi-Agent Orchestration — Protocols and Enterprise Architecture

**Paper**: arXiv:2601.13671  
**Authors**: Apoorva Adimulam, Rajesh Gupta, Sumit Kumar (January 2026)

## Architectural Layer

The paper proposes a unified orchestration layer integrating four concerns:

| Concern | What it covers |
|---------|---------------|
| Planning | Task decomposition, agent assignment |
| Policy enforcement | Access control, permission boundaries |
| State management | Shared context, memory, handoffs |
| Quality operations | Monitoring, evaluation, observability |

## Two Key Protocols

### Model Context Protocol (MCP)

Standardizes how agents access external tools and context:
- Adopted by Anthropic and increasingly by others
- Enables plug-and-play tool integration
- Abstracts away provider-specific API differences

STOPA uses MCP extensively (filesystem, playwright, github MCPs).

### Agent2Agent Protocol

Governs peer-to-peer coordination between agents:
- Negotiation: agents agree on task division
- Delegation: structured handoffs with explicit contracts
- Feedback loops: progress signals between peers

Currently more aspirational in most frameworks — STOPA's orchestrate skill implements delegation but not negotiation.

## Enterprise Gap

Research architectures → enterprise deployment requires three additions the paper highlights:

1. **Governance**: who authorized what action, audit trails
2. **Observability**: what are agents doing right now
3. **Accountability**: which agent caused which outcome

These map directly to STOPA's: decisions.md (governance), status skill (observability), failures/agent-accountability.md (accountability).

## Related Concepts

→ [agentforge.md](agentforge.md)  
→ [gaama.md](gaama.md)  
→ [multi-agent-hpc.md](multi-agent-hpc.md)
