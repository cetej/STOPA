---
title: Agentic Engineering Patterns — Simon Willison's Guide
category: concepts
tags: [agentic-engineering, tdd, coding-agents, vibe-coding, software-engineering]
sources: [raw/2026-04-18-simon-willison-agentic-engineering.md]
updated: 2026-04-18
---

# Agentic Engineering Patterns — Simon Willison's Guide

**Source**: Simon Willison (@simonw), simonwillison.net, February 23, 2026 (220K views)

## The Core Distinction

**Agentic engineering** ≠ **vibe coding**

| | Vibe coding | Agentic engineering |
|---|---|---|
| Who | Non-programmers using LLMs | Professional software engineers using coding agents |
| Expertise | No engineering foundation | Deep engineering expertise + AI augmentation |
| Output quality | Variable, often fragile | Production-grade with proper verification |
| Control | "It works, I don't know why" | Full understanding + verification |

## Chapter 1: Writing Code is Cheap Now

Code generation cost has dropped dramatically. Consequences:
- More code is economically viable to write
- Exploratory implementations worth trying
- Test coverage becomes cheaper to achieve
- Refactoring has lower cost ceiling

The skill shift: from "write good code efficiently" to "direct agents to write good code with verification."

## Chapter 2: Red/Green TDD with Agents

Test-first development works better with coding agents than prompt engineering alone:

1. Write failing test (Red)
2. Agent reads test → has clear, machine-verifiable success criterion
3. Agent generates implementation
4. Test passes (Green)
5. Minimal prompting needed because **the test IS the specification**

Tests provide:
- Unambiguous success criteria
- Automatic verification loop
- Regression detection on next change

**Result**: more succinct code, less hallucination drift, lower prompting overhead.

## STOPA Relevance

Willison's TDD insight is already encoded in STOPA's `/tdd` skill (RED-GREEN-REFACTOR enforcer). This confirms the pattern is worth preserving and teaching. The broader "agentic engineering vs vibe coding" framing is useful for explaining STOPA's approach: STOPA is for engineers who know what they want, not for users who want AI to decide for them.

## Related Concepts

→ [vibe-coding.md](vibe-coding.md)  
→ [verifiability-sw2.md](verifiability-sw2.md)  
→ [karpathy.md](../people/karpathy.md) — related AI capability framing
