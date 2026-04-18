---
name: In-Place TTT as conceptual analog for STOPA learning maturity
date: 2026-04-18
type: architecture
severity: low
component: memory
tags: [research, ttt, fast-weights, maturity, confidence, analog]
summary: In-Place TTT (ICLR 2026) updates MLP projection matrices during inference as "fast weights" for 128k contexts. STOPA's confidence/uses/maturity counters are the agent-level analog — learning files behave like fast weights on the agent layer instead of the model layer. No direct implementation, but the framing validates our maturity tier design (draft→validated→core) as a discrete equivalent of continuous gradient-based adaptation.
source: external_research
uses: 0
successful_uses: 0
harmful_uses: 0
confidence: 0.6
maturity: draft
verify_check: manual
---

## Paper
- **Title**: In-Place Test-Time Training (arXiv:2604.06169)
- **Authors**: Feng, Luo, Hua, Zhang, He, Huang, Cai
- **Venue**: ICLR 2026 Oral (2026-04-07)
- **Core**: LLM adapts final MLP projection matrices during inference via task-aligned next-token objective. 4B model with drop-in TTT beats baselines on 128k contexts. Chunk-wise updates maintain context parallelism.

## Conceptual bridge to STOPA

| In-Place TTT | STOPA learnings |
|---|---|
| MLP projection matrices = fast weights | Learning files = fast weights on agent layer |
| Gradient update per chunk | `uses++`, `confidence += 0.05`, `harmful_uses--` per application |
| Continuous adaptation | Discrete maturity tiers (draft→validated→core) |
| 128k context scaling | Learning corpus scales past single-session context |
| Task-aligned objective | Critic score + outcome credit (RCL) |

## Why this is NOT directly actionable

- STOPA already does the *agent-level* version of what TTT does at *model level*
- We don't train models — we update learning files and retrieval scores
- No architectural change recommended from this paper alone

## Why it's worth keeping as reference

- Validates the framing: "learnings as fast weights" is a defensible design pattern, not an ad-hoc hack
- If Anthropic ever exposes MLP-level adaptation API, this paper becomes the blueprint
- Counter-argument to anyone pushing for continuous RL over discrete maturity: In-Place TTT shows chunk-wise discrete updates can match continuous approaches

## Related STOPA files
- `.claude/rules/memory-files.md` — maturity tier semantics
- `.claude/memory/learnings/2026-04-05-self-improving-harness.md` — impact-tracker parallels helpfulness-driven credit
- RCL outcome records (arXiv:2604.03189) — already our chosen framework
