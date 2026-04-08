---
name: autoreason
variant: compact
description: Condensed autoreason for repeat invocations within session. Use full SKILL.md for first invocation.
---

# AutoReason — Compact (Session Re-invocation)

Adversarial debate loop for subjective text improvement. Extends auto-research to domains without numeric metrics.

## Setup

1. Parse: target (file/text), domain (auto-detect: prompt|argument|copy|text), rounds (3), judges (3, odd)
2. Precondition: text ≥100 words (shorter → /critic instead)
3. Generate 5-dimension scoring rubric per domain. Present to user for approval.
4. Save to `outputs/autoreason-<slug>/`

## Debate Loop (per round)

| Step | Agent | Key rule |
|------|-------|---------|
| Critic | Sonnet, cold-start | Sees ONLY current text + rubric. No history. Find 3-5 weaknesses. Don't suggest fixes. |
| Early exit | — | 0 critical + ≤1 important → converged |
| Rewriter | Sonnet, cold-start | Sees original + current + critique + rubric. Surgical improvements, not wholesale rewrite. |
| Synthesizer | Sonnet, cold-start | Sees current + rewrite ONLY. Merge best of both. ±20% length. |
| Judge Panel | Haiku × N, parallel, cold-start | Randomized labels (X/Y not A/B), randomized order per judge. Blind evaluation against rubric. |
| Tally | — | Majority wins. Tie → current holds (conservative). |

## Convergence Exits

- Current_best won 2 consecutive rounds
- Critic found 0 critical + ≤1 important
- All rubric dimensions ≥4 from all judges
- Round limit reached

## Critical Rules

- Cold-start isolation — each agent gets fresh context, no history bleed
- Structured critique > binary preference
- Panel (3+) > single judge
- Randomized labels prevent position bias
- Cap at 5 rounds — diminishing returns
