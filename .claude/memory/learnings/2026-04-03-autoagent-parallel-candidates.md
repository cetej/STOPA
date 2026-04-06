---
date: 2026-04-03
type: architecture
severity: medium
component: orchestration
tags: [autoloop, autoresearch, parallel, sandbox, future]
summary: "AutoAgent evaluates multiple candidates in parallel via Docker sandboxes. STOPA skills are sequential — known limitation, not worth solving until CC gets native parallel execution."
source: external_research
uses: 0
harmful_uses: 0
confidence: 0.6
verify_check: manual
related: [2026-04-03-autoagent-overfitting-guard.md]
successful_uses: 0
---

## Parallel Candidate Evaluation Gap

AutoAgent (kevinrgu/autoagent) proposes multiple harness candidates per iteration and evaluates them in parallel via Harbor's Docker sandbox system. This dramatically speeds up exploration.

STOPA's optimization skills (autoloop, autoresearch, self-evolve) are all sequential: one hypothesis → one eval → keep/discard → next.

**Why this matters:** Sequential exploration is O(n) where parallel is O(1) per batch. For 24+ hour optimization runs, this is a significant throughput difference.

**Why NOT to solve now:**
- Requires sandbox infrastructure (Docker, Harbor, or CC worktrees)
- CC worktrees are read-only for agents currently
- Sequential approach works well for STOPA's typical run lengths (5-20 iterations)

**When to revisit:** When CC gets native parallel agent execution or when optimization runs exceed 50 iterations routinely.
