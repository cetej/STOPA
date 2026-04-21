---
title: SemaClaw — General-Purpose Personal AI Agents via Harness Engineering
date: 2026-04-21
sources:
  - https://arxiv.org/abs/2604.11548
tags: [ai, harness-engineering, personal-ai-agent, multi-agent, orchestration, safety, knowledge-management]
related:
  - externalization-llm-agents.md
  - multi-agent-orchestration-protocols.md
  - claude-code-design-space.md
  - context-kubernetes.md
---

# SemaClaw — General-Purpose Personal AI Agents via Harness Engineering

## Positioning

SemaClaw is an open-source multi-agent application framework emerging from the "OpenClaw ecosystem" (early 2026). Its design thesis: **harness engineering** is the dominant architectural differentiator for production-ready personal AI agents — not model size, not prompting.

## Four Infrastructure Pillars

| Pillar | Component | What It Solves |
|--------|-----------|----------------|
| **Orchestration** | DAG-based two-phase hybrid | Task decomposition with dependency tracking |
| **Safety** | PermissionBridge | Behavioral guardrails, auditable permission grants |
| **Context** | Three-tier architecture | Immediate / working / long-term memory separation |
| **Knowledge** | Agentic wiki skill | Automated personal KB construction from agent work |

## Harness Engineering Definition

> The transition from prompt/context engineering to designing **complete infrastructure** for controllable, auditable, production-ready agent systems.

This is the same shift STOPA represents — from "better prompts" to "better runtime."

## Three-Tier Context Architecture

| Tier | Scope | STOPA Analog |
|------|-------|-------------|
| Immediate | Current task window | Active conversation context |
| Working | Session-level state | `state.md`, `intermediate/` post-its |
| Long-term | Persistent knowledge | `memory/learnings/`, `key-facts.md`, 2BRAIN |

## PermissionBridge

Behavioral safety via explicit permission grants — similar to STOPA's Guardian L2 sentinel and permission hooks. Key property: auditable (every grant is logged).

## Relevance to STOPA

SemaClaw is a close parallel to what STOPA builds. Key differences:
- SemaClaw: DAG-based orchestration; STOPA: budget-tier + circuit breakers
- SemaClaw: PermissionBridge; STOPA: Guardian L2 + settings.json permissions
- SemaClaw: Agentic wiki skill → 2BRAIN serves the same function

## Connections

- [externalization-llm-agents](externalization-llm-agents.md): SemaClaw = concrete implementation of the three externalization pillars
- [context-kubernetes](context-kubernetes.md): both address declarative context management; CK uses YAML manifests, SemaClaw uses three-tier architecture
- [claude-code-design-space](claude-code-design-space.md): CC's 98.4% operational infra = harness engineering realized
