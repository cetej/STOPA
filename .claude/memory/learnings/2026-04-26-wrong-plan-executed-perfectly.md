---
date: 2026-04-26
type: architecture
severity: high
component: orchestration
tags: [orchestration, planning, evaluation, critic, scout]
summary: "Pokud agenti reportují 100% subtask completion ale verify FAILuje, root cause je v plan quality (špatný plán proveden perfektně), ne v execution. Re-run scout místo retry agentů."
source: external_research
uses: 0
harmful_uses: 0
successful_uses: 0
confidence: 0.8
maturity: draft
verify_check: "manual"
skill_scope: [orchestrate, critic]
task_context:
  task_class: multi_file
  complexity: high
  tier: standard
---

# Wrong Plan Executed Perfectly

## Pattern

Full-Plan-in-Advance agent v arXiv:2603.12710 má 89% Element Accuracy (provádí plán perfektně) ale pouze 36.29% task success vs 38.41% Step-by-Step.

Interpretace: agent perfektně provádí špatný plán. Špatný výsledek není způsoben špatnou exekucí, ale špatným plánováním.

## STOPA aplikace

Když orchestrátor reportuje: všechny subtasky completed = 100%, ale `/verify` FAILuje → příčina je v plan quality, ne execution.

**Diagnostická heuristika pro `/critic`:**
- Agenti reportují 100% subtask completion
- `verify` nebo final output FAILuje
- **→ re-run scout, přeplánuj, NE retry agentů**

Retry agentů na stejném plánu = zbytečné; je to Element Accuracy situation.

## Evidence

- arXiv:2603.12710, Table 4: Full-Plan Element Accuracy 0.89±0.03, Overall Success 36.29%
- Formulace "agent perfektně provádí špatný plán" nenalezena v literatuře — possibly novel framing

## Source evidence

Extrahováno z deepresearch briefu `outputs/arxiv-2603.12710-research.md`, [VERIFIED] markers, přímý read paperu via Jina Reader.
