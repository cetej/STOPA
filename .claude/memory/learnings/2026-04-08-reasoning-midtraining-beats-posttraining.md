---
date: 2026-04-08
type: best_practice
severity: high
component: orchestration
tags: [reasoning, training-methodology, model-selection, curriculum, mid-training]
summary: "Front-loading reasoning structure (mid-training or curriculum-hints) yields 3-9× gains vs adding it only at post-training/call-time. Meta's thinking mid-training: 9× solo, 3.2× combined. Validates teach-early pattern."
source: external_research
maturity: draft
uses: 1
harmful_uses: 0
successful_uses: 0
confidence: 1.0
verify_check: "manual"
related: []
task_context:
  task_class: research
  complexity: medium
  tier: light
---

## Detail

Meta AI (RAM blog, 2026-04): inserting a dedicated "thinking mid-training" phase between pretraining and post-training produces:
- 9× improvement over base Llama-3-8B (mid-training alone)
- 3.2× improvement vs direct RL post-training when combined
- RL phase (8.7B tokens) more efficient than extended SFT (10.5B tokens)

Core mechanism: annotator inserts interleaved thoughts into pretraining data → SFT teaches thought generation → RL (DrGRPO) refines via binary LLM-judge rewards.

**STOPA implication**: `curriculum-hints` in SKILL.md is the closest analogy — structured reasoning sequence injected as context at call time rather than as reward signal at the end. This research validates the principle: reasoning structure should be present *before* the task requires it, not appended after failure. When selecting models for orchestration tiers, prefer models trained with mid-training / extended reasoning (they'll require fewer repair iterations = lower actual cost even if list-price higher).
