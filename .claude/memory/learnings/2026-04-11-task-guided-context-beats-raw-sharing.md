---
date: 2026-04-11
type: architecture
severity: high
component: orchestration
tags: [multi-agent, context-sharing, token-efficiency, kv-cache, orchestration]
summary: "Latent Briefing: task-guided KV cache compaction pro cross-agent memory dosahuje 49-65% token savings + 3pp accuracy gain. Princip platí i na API úrovni: orchestrátor by měl posílat workerům task-relevantní kontext, ne celou trajektorii. Speculative reasoning je šum pro workery."
source: external_research
uses: 0
harmful_uses: 0
successful_uses: 0
confidence: 0.75
verify_check: "manual"
related: [2026-04-10-rlm-architectural-principles.md, 2026-04-09-triattention-pre-rope-kv-compression.md]
skill_scope: [orchestrate]
---

# Task-Guided Context Selection Beats Raw Context Sharing

## Finding

Latent Briefing compresses orchestrator's trajectory using worker's task queries as relevance signal → 49-65% worker token reduction, +3pp accuracy at optimal threshold. Claude Sonnet 4 orchestrator + Qwen3-14B worker, LongBench v2 (126 questions, 0-100k tokens).

## Mechanism

Standard RLM: orchestrator passes (raw document, targeted query) → worker sees narrow view. Latent Briefing: compress orchestrator's full trajectory (prior worker responses, hypotheses, dead ends) using attention between task prompt and trajectory → worker gets relevant accumulated context, not everything.

## Impact on STOPA

STOPA orchestrate currently passes subtask descriptions to worker agents. Orchestrator accumulates context (scout results, prior worker outputs, plan updates) that could help workers but is too expensive to pass raw. Applicable even at API level without KV cache access:

1. **Task-relevant context selection**: before spawning worker agent, grep/filter orchestrator state for subtask-relevant facts (not raw dump)
2. **Strip speculation**: remove orchestrator's hypothesis-testing and dead-end exploration from worker context
3. **Adaptive detail**: simple subtasks → minimal context; complex subtasks → more accumulated context

## Compression Regime Mapping

| Condition | Optimal Approach | Token Savings | STOPA Tier |
|-----------|-----------------|---------------|------------|
| Long docs (32k-100k) | Light compaction (preserve coverage) | 49% median | deep |
| Hard questions | Aggressive (strip speculation) | +3pp accuracy | deep |
| Short/easy docs | Moderate | 42% | light/standard |

**Why:** Raw context sharing compounds tokens across agent calls (N workers × full trajectory). Task-guided selection gives each worker what IT needs, not everything the orchestrator knows.
**How to apply:** In orchestrate Phase 4 (agent assignment): build per-subtask context packet. Include: relevant scout facts, relevant prior results. Exclude: orchestrator's plan-level reasoning, failed hypotheses, unrelated subtask results.
