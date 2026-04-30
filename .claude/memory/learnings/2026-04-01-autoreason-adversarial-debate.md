---
date: 2026-04-01
type: architecture
severity: medium
component: skill
tags: [autoreason, debate, subjective-optimization, multi-agent]
summary: "AutoReason pattern (SHL0MS) extends AutoResearch to subjective domains via adversarial debate loop. Key: cold-start agent isolation prevents confirmation bias, randomized judge labels prevent position bias, structured critique > binary preference."
source: external_research
maturity: draft
uses: 1
harmful_uses: 0
confidence: 1.0
verify_check: "Glob('.claude/commands/autoreason.md') → 1+ matches"
related: [2026-03-30-society-of-thought-orchestration.md, 2026-04-26-autoreason-mid-tier-sweet-spot.md]
successful_uses: 0
---

## AutoReason — Adversarial Debate for Subjective Text Optimization

**Pattern**: Writer → Critic → Rewriter → Synthesizer → Blind Judge Panel → loop until convergence

**Key design principles (validated by literature):**
1. **Cold-start isolation** — each agent gets fresh context, no history bleed (prevents confirmation bias)
2. **Structured critique > binary preference** — critique text is directional information (Feedback Descent, Stanford arXiv:2511.07919)
3. **Panel of small judges > single large judge** — 3+ diverse Haiku judges cheaper and less biased than 1 Opus (PoLL, arXiv:2404.18796)
4. **Randomized labels** — X/Y not A/B, order randomized per judge (Chatbot Arena methodology)
5. **Convergence via judging, not consensus** — Wynn et al. ICML 2025 showed naive consensus DEGRADES quality

**When debate helps vs hurts:**
- HELPS: Genuinely ambiguous subjective tasks, texts >100 words, multiple valid approaches
- HURTS: Simple factual tasks, when agents share systematic bias, short texts
- CRITICAL WARNING: "Talk Isn't Always Cheap" (ICML 2025) — agents favor agreement over truth. Must enforce dissent.

**Cost model**: ~6 sub-agent calls per round (4 Sonnet + 3 Haiku judges = equivalent of ~5 Sonnet calls)

**Implementation**: `/autoreason` skill in STOPA, Tier 2. Fills gap between `/critic` (single-pass, no revision) and `/autoresearch` (numeric metrics only).
