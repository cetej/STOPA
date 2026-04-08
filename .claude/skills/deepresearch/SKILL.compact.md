---
name: deepresearch
variant: compact
description: Condensed deepresearch for repeat invocations within session. Use full SKILL.md for first invocation.
---

# Deep Research — Compact (Session Re-invocation)

Multi-agent evidence pipeline: plan → discover → read → synthesize → verify → deliver.

## Integrity (non-negotiable)

Never fabricate sources. URL or it didn't happen. Read before summarize. Mark uncertainty: `[VERIFIED]` / `[INFERRED]` / `[UNVERIFIED]` / `[SINGLE-SOURCE]`.

## Scale Decision

| Query type | Scale | Discovery (Haiku) | Reading (Sonnet) | Verifier? |
|-----------|-------|-------------------|------------------|-----------|
| Narrow factual | direct | 0 (search directly) | 0 | No |
| Comparison (2-3) | comparison | 2-3 × 5 calls | 2 × 8 calls | Top 5 |
| Broad survey | survey | 4-5 × 5 calls | 3 × 8 calls | Top 10 |
| Complex multi-domain | complex | 5 × 5 calls | 3 × 8 calls | Full |

## Pipeline

1. **Plan** → sub-questions (flat for direct/comparison, tree for survey/complex). Present to user.
2. **Discovery** (Haiku, parallel) → WebSearch only, URL lists. 3 min cap.
3. **Reading** (Sonnet, parallel) → top 8-12 URLs via Jina Reader. Self-RAG per source. 10 min cap.
4. **Synthesis** → merge evidence, deduplicate, identify consensus/disagreements/gaps.
5. **Verification** → verifier sub-agent for comparison+. Claim inventory: >30% unresolved → re-gather.
6. **Brief** → outputs/<slug>-research.md with Executive Summary, Detailed Findings, Evidence Table, Sources.
7. **Deliver** → present summary, point to files. Auto-ingest to wiki (skip with --no-ingest).

## Critical Rules

- Hard cap: 8 tool calls per agent. Split wider scope into more agents.
- Time caps: discovery 3 min, reading 10 min, total ~16 min.
- Three-phase pipeline (discover/read/synthesize) saves ~65% vs monolithic agent.
- Never spawn subagents for work doable in 5 tool calls.
- Default to comparison scale when unsure.
