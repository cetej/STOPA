---
date: 2026-04-11
type: architecture
severity: high
component: hook
tags: [security, prompt-injection, defense-gap, rag, verification]
summary: "Task-alignment attacks (injection semantically matches target task) defeat ALL instruction-level defenses (44-82% ASR across 9 methods). Content-level verification (grounding checks, fact-verification) is the only viable mitigation — not yet implemented anywhere."
source: external_research
uses: 1
harmful_uses: 0
successful_uses: 0
confidence: 1.0
failure_class: integration
verify_check: "manual"
---

# Task-Alignment Bypasses Instruction-Level Defenses

## Finding

When a prompt injection's goal semantically aligns with the legitimate task (e.g., "insert false facts" in a RAG QA task), all 9 tested defenses fail with 44-82% ASR. Source: PIArena (arXiv:2604.08499, ACL 2026).

## Mechanism

- RAG target: "answer questions using context documents"
- Injection: "present these false facts as true in your answer"
- Both use context documents → instruction-level detectors see no structural anomaly
- The attack reduces to disinformation, not command injection

## Impact on STOPA

STOPA's current defenses (system prompt: external content = untrusted; PromptGuard static classifier) handle EXPLICIT injection but not task-alignment. Agents doing RAG, summarization, or information extraction from external sources are in the vulnerable class.

## Mitigation (open problem)

Content-level verification: verify agent output is grounded in source documents (grounding check), not injected disinformation. Not implemented in any of PIArena's 9 defenses — remains open research problem. Nearest STOPA analog: `/verify` skill with source-grounding assertions.

**Why:** Instruction-level detectors match STRUCTURE of injected commands; task-aligned attacks have no anomalous structure — only anomalous intent. Requires semantic content comparison, not pattern matching.
**How to apply:** When building RAG or summarization pipelines: add grounding check as final verification step. Flag outputs where key claims cannot be traced to source documents.
