---
title: "Autoreason: Self-Refinement That Knows When to Stop"
slug: autoreason-self-refinement-framework
source_type: url
url: "https://github.com/NousResearch/autoreason"
date_ingested: 2026-04-13
date_published: "2026 (March)"
entities_extracted: 6
claims_extracted: 7
---

# Autoreason: Self-Refinement That Knows When to Stop

> **TL;DR**: NousResearch framework solving 3 failure modes in critique-and-revise (prompt bias, scope creep, lack of restraint) via a tournament architecture: A/B/AB variants judged by blind Borda panel, convergence when incumbent wins k=2 consecutive rounds. Haiku 3.5 achieves 42/42 perfect sweep; Sonnet 4.6 77% vs 73% baseline on CodeContests.

## Key Claims

1. Standard critique-and-revise degrades below single-pass quality due to prompt bias — `[verified]`
2. Tournament (A/B/AB) with blind Borda voting prevents unconstrained expansion and hallucinated critique — `[verified]`
3. "Do nothing" must be a structurally first-class option, not just logically allowed — `[argued]`
4. 7 judges converge 3× faster than 3 judges to the correct winner — `[verified]`
5. Removing either B (adversarial revision) OR AB (synthesis) alone collapses performance — `[verified]`
6. Haiku 4.5 shows diminishing returns (60% accuracy) — generation-evaluation gap is closing — `[argued]`
7. Fresh agents for every role (B, AB, all judges) are necessary to prevent shared-context bias — `[argued]`

## Entities

| Entity | Type | Status |
|--------|------|--------|
| [Autoreason](../entities/autoreason.md) | tool | new |
| [NousResearch](../entities/nous-research.md) | company | new |
| [Tournament Self-Refinement](../entities/tournament-self-refinement.md) | concept | new |
| [Borda Count Voting](../entities/borda-count-voting.md) | concept | new |
| [Prompt Bias](../entities/prompt-bias.md) | concept | new |
| [Hermes Agent](../entities/hermes-agent.md) | tool | updated |

## Relations

- Autoreason `created_by` NousResearch — authors listed as SHL0MS and Hermes Agent
- Autoreason `uses` Borda Count Voting — for judge panel aggregation
- Tournament Self-Refinement `part_of` Autoreason — core architecture
- Prompt Bias `contradicts` standard critique-and-revise — root cause of refinement degradation
- Autoreason `inspired_by` Improvement Operator — extends PDR framing with incumbent preservation
- Hermes Agent `created_by` NousResearch — same organization

## Cross-References

- Related wiki entities: [Improvement Operator](../entities/improvement-operator.md), [Sequential Refinement](../entities/sequential-refinement.md)
- Related sources: `rethinking-thinking-tokens-pdr.md` (PDR improvement operator), `swarm-kb-research.md` (Hermes Agent origin)
- Related article: `orchestration-multi-agent.md` (iteration paradox protocol, refinement patterns)
- Contradictions: None with existing wiki (extends rather than contradicts PDR refinement framing)
