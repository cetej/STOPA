---
date: 2026-04-11
type: architecture
severity: medium
component: orchestration
tags: [multi-agent, context-sharing, noise, speculation, orchestration]
summary: "Orchestrator's speculative reasoning (dead-end hypotheses, exploration trails) degrades worker accuracy. Aggressive filtering of speculation on hard tasks improves accuracy by +3pp. Workers need clean, focused signal — not the orchestrator's full thought process."
source: external_research
uses: 0
harmful_uses: 0
successful_uses: 0
confidence: 0.7
verify_check: "manual"
related: [2026-04-11-task-guided-context-beats-raw-sharing.md]
skill_scope: [orchestrate]
---

# Speculative Orchestrator Reasoning Degrades Worker Performance

## Finding

Latent Briefing (LongBench v2): on hard questions, aggressive compaction (79% removal of orchestrator trajectory) IMPROVES worker accuracy by +3pp vs baseline. The removed content = orchestrator's speculative reasoning, dead ends, and hypothesis exploration.

## Mechanism

Orchestrator explores many hypotheses across multiple worker calls, accumulating speculative reasoning. When this trajectory is shared with workers, the speculative content dilutes the signal — worker attention spreads across irrelevant exploration instead of focusing on task-relevant facts. Compaction acts as a relevance filter: keeping only what the worker's attention naturally scores high.

## Analogy

Like note-taking: when exploring a hard problem, most notes are scratch work. Sharing raw scratch notes with a colleague forces them to parse your exploration. Sharing a clean summary of relevant findings lets them work effectively.

## Impact on STOPA

STOPA orchestrate passes context to worker agents via Agent tool prompt. Currently no distinction between:
- Established facts from scout/prior workers (high signal)
- Orchestrator's plan-level reasoning (mixed signal)  
- Failed approaches and dead ends (noise)

**Action:** In orchestrate, structure agent prompts as:
1. **Facts** (confirmed by scout/prior workers) — always include
2. **Current subtask** (specific assignment) — always include
3. **Orchestrator reasoning** (why this approach) — include only high-level, strip exploration
4. **Failed approaches** (what didn't work) — include ONLY if directly relevant to subtask (prevents worker from repeating)

**Why:** Workers need clean signal, not orchestrator's full cognitive trail. More context ≠ better context.
**How to apply:** Before spawning worker agent, mentally partition context into facts/task/reasoning/failures. Default: include (1) and (2), selectively include (3) and (4).
