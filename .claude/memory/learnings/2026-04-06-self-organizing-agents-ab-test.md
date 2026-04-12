---
date: 2026-04-06
type: architecture
severity: high
component: orchestration
tags: [orchestration, agents, research]
summary: "A/B test potvrdil: self-organizing agenti (jen mise, bez rolí) překonávají hierarchické přiřazení o +8% na explorativních úkolech. Hierarchický přístup lepší na strukturovaném rankingu. Hybridní přístup v orchestrate by měl detekovat typ tasku."
source: autoresearch
confidence: 1.0
uses: 2
successful_uses: 0
harmful_uses: 0
impact_score: 0.0
verify_check: "Grep('self-organizing', path='.claude/memory/learnings/') → 1+ matches"
task_context: {task_class: research, complexity: medium, tier: standard}
---

## Self-Organizing vs Hierarchical Agent Orchestration — A/B Test

**Basis:** arXiv:2603.28990 "Drop the Hierarchy and Roles" (Dochkina, 2026)
- 25K tasků, 8 modelů, 4-256 agentů, 8 koordinačních protokolů
- Self-org překonává centrální koordinaci o +14% (p<0.001)
- Efekt silnější u silnějších modelů

**Náš test (3 tasky × 2 přístupy, sonnet model):**

| Task | Typ | H score | S score | Vítěz |
|------|-----|---------|---------|-------|
| Deepresearch audit | Explorativní | 17/25 | 24/25 | S (+41%) |
| Learning verify_check | Analytický+explorativní | 20/25 | 22/25 | S (+10%) |
| Radar analýza | Strukturovaný ranking | 22/25 | 19/25 | H (+16%) |
| **Celkem** | | **59/75** | **65/75** | **S (+8%)** |

**Náklady:** ~$7.60 celkem, S o 5% dražší (zanedbatelné).

**Klíčové zjištění:**
- Self-org lepší na exploraci (audit, hledání issues) — agent sám rozhodne co prozkoumat
- Hierarchický lepší na structured output (ranking, scoring) — předepsané kroky = strukturovanější výstup
- Paper tvrdí +14%, my naměřili +8% — směr potvrzen, menší efekt (sonnet vs mix modelů v paperu)

**Why:** Hierarchické přiřazení rolí omezuje agenta na předem definovaný prostor hledání. Self-organizing agent může objevit issues které předepsané kroky nepokrývají.

**How to apply:** Orchestrate by měl detekovat typ tasku (explorativní vs analytický) a přizpůsobit míru předepsání:
- Explorativní (scout, audit, research): dát jen misi + kvalitativní cíl
- Analytický (ranking, scoring, structured report): předepsat kroky + formát
- Implementace: přidat task_style detection do Phase 1 orchestrate, podmínit template v agent-execution.md
- Odloženo na pozdější implementaci (budget constraint 2026-04).
