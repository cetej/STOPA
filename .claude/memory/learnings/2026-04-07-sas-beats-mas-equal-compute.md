---
date: 2026-04-07
type: architecture
severity: high
component: orchestration
tags: [multi-agent, compute-budget, single-agent, orchestration, reasoning]
summary: "Při rovném thinking token budgetu single-agent systémy dosahují stejného nebo lepšího výkonu než multi-agent systémy. MAS výhoda = nekontrolovaný compute, ne architektura. MAS zbývá zdůvodnění: paralelizace, specializace, fault isolation."
source: external_research
uses: 0
harmful_uses: 0
confidence: 0.8
successful_uses: 0
failure_class: assumption
verify_check: "manual"
task_context:
  task_class: research
  complexity: medium
  tier: light
---

## Situace

Tran & Kiela (arXiv:2604.02460, 2026-04) testovali SAS vs MAS na multi-hop reasoning (FRAMES, MuSiQue 4-hop) s kontrolovaným thinking token budgetem. Výsledky konzistentní napříč Qwen3, DeepSeek-R1-Distill-Llama, Gemini 2.5 a 5 MAS architekturami.

**Klíčový nález**: SAS ≥ MAS za rovných podmínek. MAS vítězí jen při těžkém kontextovém poškození (α ≥ 0.7).

**Teorie**: Data Processing Inequality — každý agent-handoff je mezičlánek, který nemůže zvýšit informaci, jen ji ztratit.

## Implikace pro STOPA

1. **Farm tier** (5–8 agentů) je zdůvodnitelný **paralelizací mechanických operací** (bulk edits, linter fixy), ne reasoning zlepšením.
2. **Pro reasoning-heavy tasky**: jeden silnější model s vyšším thinking budgetem > více agentů se stejným celkovým budgetem.
3. **Debate pattern** je nejsilnější MAS varianta — pokud MAS musíš použít, použij Debate (dva agenti s opačnými pozicemi).
4. **Benchmark srovnání MAS** musí kontrolovat celkový thinking budget (součet přes všechny agenty) — bez toho jsou výsledky zavádějící.

## Kdy MAS stále dává smysl

- Paralelizace nezávislých subtasků (každý agent řeší jinou část, žádný nepotřebuje kontext ostatních)
- Specializace (scout má jiné nástroje než worker)
- Fault isolation (agent selhání neprotéká do celého systému)
- Kontextový šum/korupce je těžký (α ≥ 0.7) — reálně: poškozené soubory, extrémně dlouhé noisy kontexty

## Prevence špatné aplikace

- NEZAKLÁDEJ MAS na tvrzení, že "více hlav = lepší reasoning" — to platí jen pro nekontrolované compute
- Při hodnocení výkonu orchestration: měř thinking tokeny celého tieru, ne jen jednoho agenta
