---
date: 2026-04-13
type: best_practice
severity: high
component: orchestration
tags: [autoloop, autoresearch, self-evolve, efficiency, budget-tiers, replay]
summary: "'Generate-then-discard' je suboptimální pattern pro iterativní skills. Před spuštěním nového agenta zkontroluj existující outcomes — přínos je analogický experience replay v RL (40% compute savings, stabilnější konvergence)."
source: external_research
uses: 0
successful_uses: 0
harmful_uses: 0
confidence: 0.65
maturity: draft
skill_scope: [autoloop, autoresearch, self-evolve, orchestrate]
verify_check: "manual"
task_context:
  task_class: research
  complexity: medium
  tier: standard
---

## Detail

arXiv:2604.08706: GRPO/PPO discards trajectories after single use — this wastes 80% of GPU hours.
Paper proves: moderate staleness (re-using 40-day-old trajectories) STABILIZES training and preserves output diversity (pass@k improves for k>1).

**STOPA behavioral rule:** Iterativní skills (autoloop, autoresearch, self-evolve) NESMÍ ignorovat `outcomes/`. Před generováním nového přístupu:
1. Zkontroluj jestli `outcomes/<skill>-*.md` existují
2. Přečti "What Worked" z posledních 3-5 runů
3. Použij jako výchozí bod místo generování od nuly

**Proč to není triviální:** Instinkt je "nový kontext = nový start". Ale paper dokazuje, že mírná staleness (použití 5-15 kroků starých trajektorií) snižuje overfitting a pomáhá zachovat diverzitu výstupu. Stejný efekt vidíme u skills: bez outcomes read se self-evolve opakuje v podobných cyklech místo convergence.

**Kdy NEaplikovat:** Pokud task_class změnila radikálně (jiný cílový soubor, jiný kontext) — pak jsou staré outcomes off-distribution a jejich čtení škodí (analogie: příliš velký buffer = příliš stará data → gradientní bias roste).

Ref: arXiv:2604.08706 Fig.1 — s bufferem N=84 a (W,T)=(5,3): 40% compute savings, 77% acc vs 76% baseline
