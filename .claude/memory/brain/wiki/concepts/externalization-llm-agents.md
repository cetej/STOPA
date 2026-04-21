---
title: Externalization in LLM Agents — Unified Review
date: 2026-04-21
sources:
  - https://arxiv.org/abs/2604.08224
tags: [ai, agent, harness-engineering, memory, orchestration, externalization]
related:
  - harness-engineering.md
  - agent-memory-taxonomy.md
  - multi-agent-orchestration-protocols.md
  - agentic-engineering-patterns.md
---

# Externalization in LLM Agents — Unified Review

## Core Claim

Modern LLM agents progress **"less by changing model weights than by reorganizing the runtime around them."** Agent infrastructure matters because it transforms difficult cognitive tasks into forms models can handle reliably.

## Three Forms of Externalization

| Form | What Gets Externalized | Why It Matters |
|------|----------------------|----------------|
| **Memory** | State management across time | Agent can reason across sessions, long contexts |
| **Skills** | Procedural expertise | Reusable behavioral modules outside weights |
| **Protocols** | Interaction structure | Formalized contracts between agents and tools |

The three forms are **coupled** — their combination enables emergent behaviors that no single form produces alone.

## Harness Engineering

The **harness** is the coordination layer that unifies all three external components. Key insight: prompt engineering and context engineering are insufficient; you need *harness engineering* — the deliberate design of the infrastructure around the model.

This parallels the paper's use of **cognitive artifacts** from cognitive science: the infrastructure isn't just scaffolding, it actively shapes what cognition is possible.

## Evolution of Architectures

```
Weights-based → Context-aware → Harness-based
   (model is       (careful         (dedicated
   everything)     prompting)       runtime infra)
```

## Emerging Direction: Self-Evolving Harnesses

The paper identifies self-evolving harnesses as a frontier direction — infrastructure that improves itself through use. STOPA's `/self-evolve` and `/evolve` skills are direct implementations of this pattern.

## Relevance to STOPA

This paper provides the theoretical unification for what STOPA is building:
- Memory externalization → `.claude/memory/` system
- Skills externalization → `.claude/skills/` + `.claude/commands/`
- Protocols externalization → hooks, orchestration rules, circuit breakers
- Harness engineering → STOPA as a whole

The 3-phase STOPA restructure (sensors + STOPA/KODER split + feedback loop) is exactly the harness engineering paradigm applied to Claude Code.

## Connections

- [agent-memory-taxonomy](agent-memory-taxonomy.md): taxonomy of memory forms — Maps to the "memory externalization" pillar
- [multi-agent-orchestration-protocols](multi-agent-orchestration-protocols.md): MCP + Agent2Agent = protocol externalization
- [agentic-engineering-patterns](agentic-engineering-patterns.md): Willison's pattern — harness is the answer to "agentic engineering ≠ vibe coding"
- [claude-code-design-space](claude-code-design-space.md): Liu et al. 1.6%/98.4% split — the 98.4% is the harness
