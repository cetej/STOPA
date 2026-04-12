---
name: Reasoning Model Pricing Reversals
description: Listed API prices mislead — 21.8% of model pairs show cost reversal due to thinking token heterogeneity (up to 28x). Benchmark actual costs, not list prices.
type: reference
---

**Paper:** arXiv:2603.23971 — "When Cheaper Reasoning Models End Up Costing More"

**Key findings:**
- 8 frontier reasoning models, 9 tasks, 21.8% pricing reversals
- Magnitude up to 28x
- Gemini 3 Flash listed 78% cheaper than GPT-5.2, actually 22% higher
- Claude Opus 4.6 listed at 2x Gemini 3.1 Pro, actually 35% less
- Root cause: thinking token usage varies up to 900% on same query
- Removing thinking token costs reduces reversals by 70%

**How to apply:** When selecting models for production or sub-agents, benchmark actual token consumption per task type — don't rely on listed $/Mtok. Use ccusage for real cost tracking. STOPA's task-complexity-based model selection (haiku→sonnet→opus) naturally aligns with thinking token efficiency.
