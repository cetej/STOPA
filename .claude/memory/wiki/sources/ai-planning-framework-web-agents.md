---
title: "AI Planning Framework for LLM-Based Web Agents (arXiv:2603.12710)"
slug: ai-planning-framework-web-agents
source_type: research_output
url: "https://arxiv.org/abs/2603.12710"
date_ingested: 2026-04-26
date_published: "2026-03"
entities_extracted: 12
claims_extracted: 7
---

# AI Planning Framework for LLM-Based Web Agents

> **TL;DR**: Shahnovsky & Dror (2026) mapují web agenty na BFS/Best-First/DFS taxonomii, navrhují 5 trajectory metrik a sbírají 794-trajektorií dataset. Kritická analýza: taxonomie derivativní, metodologie single-annotator, ale Element Accuracy + Recovery Rate jsou genuinely novel, a finding "agent perfektně provádí špatný plán" je diagnosticky cenný.

## Key Claims

1. Full-Plan-in-Advance má 89% Element Accuracy ale 36.29% task success — "agent perfektně provádí špatný plán" — `[verified]`
2. AgentOccam (linear, bez search) 45.7% bije Plan-MCTS 39.2% na WebArena — linear well-tuned > naive tree search — `[verified]`
3. Rule-based WebArena evaluators undercount success; pouze 3.8% tasks solved by ALL 6 agents — `[verified]`
4. BFS/DFS taxonomie derivativní od Yao 2023 (ToT) a Koh 2024 — `[argued]`
5. Element Accuracy a Recovery Rate nemají ekvivalent v 5 konkurenčních 2024-2026 eval frameworks — `[argued]`
6. Tree search wins na tool planning (typed I/O) ale ne na web navigation (noisy actions) — doménová závislost — `[verified]`
7. Plan-space search (subplan units) > action-space search bez ohledu na search algoritmus — `[verified]`

## Entities

| Entity | Type | Status |
|--------|------|--------|
| [arxiv-2603.12710](../entities/arxiv-2603-12710.md) | paper | new |
| [AgentRewardBench](../entities/agentrewardbench.md) | paper | new |
| [WebGraphEval](../entities/webgrapheval.md) | paper | new |
| [TRACE (trajectory)](../entities/trace-trajectory.md) | paper | new |
| [WebArena Verified](../entities/webarena-verified.md) | tool | new |
| [Plan-MCTS](../entities/plan-mcts.md) | paper | new |
| [AgentOccam](../entities/agentoccam.md) | tool | new |
| [ToolTree](../entities/tooltree.md) | paper | new |
| [WebArena](../entities/webarena.md) | tool | new |
| [trajectory-eval-metrics](../entities/trajectory-eval-metrics.md) | concept | new |
| [LATS](../entities/lats.md) | paper | updated |
| [Tree of Thoughts](../entities/tree-of-thoughts.md) | paper | updated |

## Relations

- arxiv-2603.12710 `extends` WebArena (uses dataset, builds on benchmark)
- AgentRewardBench `competes_with` arxiv-2603.12710 (both propose trajectory evaluation frameworks)
- WebGraphEval `competes_with` arxiv-2603.12710 (competing trajectory eval)
- Plan-MCTS `contradicts` arxiv-2603.12710 (AgentOccam finding missing from S&D's comparison)
- ToolTree `inspired_by` Tree-of-Thoughts (BFS/DFS attribution chain)
- AgentOccam `contradicts` LATS (linear beats MCTS on WebArena)
- trajectory-eval-metrics `part_of` skill-evaluation (STOPA wiki article)
- TRACE `competes_with` arxiv-2603.12710 (HTUF subsumes Partial Success)

## Cross-References

- Related learnings: `orchestration-iteration.md` (iterative refinement), `skill-evaluation.md` (eval methods)
- Related wiki articles: `skill-evaluation` (trajectory auditing gap), `orchestration-multi-agent` (plan-space search)
- **GAP ADDRESSED**: INDEX.md lists "trajectory auditing" as open gap — this source directly provides frameworks
- Contradictions: none vs existing learnings
