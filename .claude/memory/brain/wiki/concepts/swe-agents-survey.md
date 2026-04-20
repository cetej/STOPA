---
title: LLM-Empowered SWE Agents — Comprehensive Survey
date: 2026-04-20
sources:
  - https://arxiv.org/abs/2510.09721
tags: [ai, survey, software-engineering, multi-agent, benchmarks, agentic-systems]
related:
  - agentforge.md
  - agentic-engineering-patterns.md
  - verifiability-sw2.md
---

# LLM-Empowered SWE Agents — Comprehensive Survey

## Core Contribution

A two-dimensional taxonomy connecting 150+ papers and 50+ benchmarks for LLM-based software engineering. The key insight: prior surveys treated solutions and benchmarks separately; this work maps them together so researchers can find the right approach for a given evaluation target.

## Two Dimensions

| Dimension | Categories |
|-----------|-----------|
| **Solutions** | Prompt-based → Fine-tuning-based → Agent-based |
| **Benchmarks** | Code generation, Code translation, Code repair |

## Evolution Narrative

**Prompt engineering** → **Fine-tuning** → **Agentic systems** with:
- Planning & reasoning
- Memory mechanisms
- Tool augmentation
- Multi-agent collaboration

## Key Findings

1. **Progression is real**: agentic systems substantially outperform prompt-only and fine-tuning-only on complex, multi-file tasks
2. **Benchmark coverage gaps**: existing benchmarks underrepresent real-world complexity (distributed systems, legacy code, cross-language)
3. **Research frontiers**:
   - Multi-agent collaboration patterns
   - Self-evolving systems (agent updates own code/strategy)
   - Formal verification integration

## Practical Significance

For STOPA: the survey validates the agent-based approach as state of the art for non-trivial SWE tasks. The "self-evolving systems" frontier maps directly to STOPA's `/self-evolve` and `/autoloop` skills.

The benchmark → solution mapping is also useful for STOPA skill design: if the task type is known (code repair vs. generation), use the survey to identify the solution paradigm that performs best.

## Connections

- [agentforge](agentforge.md): concrete implementation of agent-based SWE — exactly the paradigm this survey shows is state of the art
- [agentic-engineering-patterns](agentic-engineering-patterns.md): Willison's practitioner perspective complements the academic survey
- [verifiability-sw2](verifiability-sw2.md): survey results confirm: verifiable tasks (code generation + test execution) see the largest gains from agentic approaches
