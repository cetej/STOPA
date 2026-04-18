---
date: 2026-04-18
type: architecture
severity: medium
component: orchestration
tags: [subagent, context-isolation, delegation, memory, multi-agent]
summary: CC subagent sidechains never return full history to parent — only final response text. STOPA agents already do this via Agent() tool, but agent instructions often don't explicitly mandate concise response summarization before return, causing context bloat.
source: external_research
uses: 0
successful_uses: 0
harmful_uses: 0
confidence: 0.6
maturity: draft
skill_scope: [orchestrate, deepresearch, scout]
verify_check: manual
---

## Detail

From arXiv:2604.14228. Each CC subagent writes a separate `.jsonl` file. Only final response text (+ minimal metadata) returns to parent. Parent context window is never inflated by the subagent's full reasoning trace — that stays in the sidechain for audit but is NOT injected into parent.

**STOPA current state**: Agent() tool already isolates subagent context. But: worker agents return large unstructured outputs (e.g., full grep results, file diffs) without summarization, and orchestrators inject them directly into parent context.

**Why:** Context explosion in nested multi-agent runs degrades quality and increases cost. The 98.4% operational infrastructure insight says: contain output at the boundary.

**How to apply:** Worker agent prompts should include explicit instruction: "Return a concise summary (max 300 words) + structured outputs. Do NOT return raw file contents or full grep output — extract only what is needed." This enforces sidechain isolation at the prompt level.
