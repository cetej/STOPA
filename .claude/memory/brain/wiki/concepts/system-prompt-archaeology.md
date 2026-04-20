---
title: System Prompt Archaeology — Git Timeline Methodology
date: 2026-04-20
sources:
  - https://simonwillison.net/2026/Apr/18/extract-system-prompts/
tags: [system-prompts, git, version-control, research-methodology, anthropic, claude]
related:
  - claude-opus-47.md
  - claude-code-design-space.md
  - agentic-engineering-patterns.md
---

# System Prompt Archaeology — Git Timeline Methodology

## Core Idea

Simon Willison's approach to tracking Claude's evolving system instructions: convert Anthropic's published system prompt documentation into a **git repository with timestamped commits**, one file per model/version, enabling standard git tooling for research.

## Why This Matters

Anthropic publishes Claude system prompts as monolithic markdown docs. The problem: a single file gives no visibility into *what changed, when, and why*. Git disaggregation turns static documentation into a **temporal database**.

## Method

1. Parse Anthropic's published system prompt markdown
2. Split into individual files per model + model family
3. Assign fake git commit dates matching actual release dates
4. Result: full git log/diff/blame history over the prompt corpus

## What It Enables

| Tool | Use |
|------|-----|
| `git log` | Chronological change history |
| `git diff` | Exact line-level changes between model versions |
| `git blame` | Attribution of specific instructions to model generations |

**Applied example:** Willison used this to analyze differences between Claude Opus 4.6 and 4.7 system prompts.

## Significance for STOPA / Context Engineering

System prompts are the primary context engineering artifact for Claude. Git archaeology reveals the *design trajectory* — what problems prompted each change. This is the external equivalent of STOPA's behavioral-genome.md evolution.

## Repository

`https://github.com/simonw/research/tree/main/extract-system-prompts`

## Connections

- Complements [claude-code-design-space](claude-code-design-space.md): the design space paper analyzes architecture; this tool surfaces the prompt-level behavioral record
- Extends [agentic-engineering-patterns](agentic-engineering-patterns.md): Willison applies the same "treat everything as engineering artifact" discipline to prompts
- Directly applicable to [claude-opus-47](claude-opus-47.md) analysis
