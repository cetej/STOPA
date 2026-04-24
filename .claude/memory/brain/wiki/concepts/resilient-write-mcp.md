---
title: Resilient Write — Six-Layer Durable Write Surface for LLM Agents
category: concepts
tags: [mcp, file-operations, write-safety, error-recovery, coding-agents]
sources: [raw/processed/2026-04-24-resilient-write-mcp.md]
updated: 2026-04-24
---

# Resilient Write — Six-Layer Durable Write Surface for LLM Agents

**Paper**: arXiv:2604.10842  
**Authors**: Justice Owusu Agyemang, Jerry John Kponyo et al. (April 2026)

## Core Problem

Write failures in LLM coding agent workflows are underestimated. Content-safety filters can silently reject writes — the agent believes the write succeeded but the file was never updated. This was observed in a real April 2026 incident where API key prefixes in redacted form triggered silent rejections.

## Six-Layer Architecture

Each layer addresses a distinct failure mode independently:

| Layer | Failure addressed |
|-------|------------------|
| 1. Pre-validation | Content safety checks BEFORE write attempt |
| 2. Chunk preview | Validates partial content before full write |
| 3. Format-aware validation | Checks encoding/structure compatibility |
| 4. Atomic write | Ensures file state integrity on partial failure |
| 5. Journal analytics | Tracks write attempts and recovery paths |
| 6. Structured error signals | Returns recoverable vs unrecoverable error info |

## Results

- **5× reduction** in recovery time vs baseline
- **13× improvement** in agent self-correction rate
- 186-test validation suite
- Three emergent tools: chunk preview, format-aware validation, journal analytics

## MCP Integration

Implemented as an open-source MCP server (MIT License). The six layers are **orthogonal and independently adoptable** — teams can add individual layers without the full stack.

## STOPA Relevance

Relevant to any STOPA skill that writes files (Edit, Write tool calls). The silent rejection pattern is a real risk: STOPA hooks already include some write protection, but the journal analytics pattern (tracking write attempts per run) is worth adopting for failure debugging. The "structured error signals" pattern aligns with core-invariants I4 (syntax regression detection).

## Related Concepts

→ [semaclaw-harness-engineering.md](semaclaw-harness-engineering.md)  
→ [externalization-llm-agents.md](externalization-llm-agents.md)  
→ [artifacts-as-memory.md](artifacts-as-memory.md)
