---
date: 2026-03-30
type: architecture
severity: high
component: orchestration
tags: [multi-agent, reasoning, critic, diversity, alignment]
summary: "Kim et al. (2026) empiricky dokázali, že RL optimalizační tlak spontánně generuje interní multi-agentní debatu v reasoning modelech (DeepSeek-R1, QwQ-32B). Steering feature 30939 zdvojnásobil přesnost. Heterogenita perspektiv → výkon. Implikace: critic agent s odlišným system promptem není hack, je architektonicky opodstatněn. STOPA checkpoint/shared state potvrzena jako nutnost (bez temporal alignment se systémy rozpadají)."
source: external_research
uses: 1
harmful_uses: 0
verify_check: "manual"
confidence: 0.85
successful_uses: 0
---

## Nález

Paper Evans, Bratton & Agüera y Arcas (Science 2026, arXiv:2603.20639) je pozicový text opřený o Kim et al. (arXiv:2601.10825). Kim et al. testovali 8 262 úloh, 6 benchmarků, 4 vrstvy měření.

**Klíčové empirické výsledky:**
- RL fine-tuning na přesnost spontánně produkuje multi-perspektivní chování (bez explicitního tréninku)
- SAE Feature 30939 (65,7 % konverzační poměr): steering → 2× přesnost na aritmetice
- Kauzální vztah prokázán přes SEM (ne jen korelace)
- RL multi-agent: 38 % @ step 40 vs. 28 % monologue model
- Dialog features nejsilnější u GPQA/hard math, mizí u procedurálních úloh

**Intelektuální genealogie:**
- Tomasello: explicitně citován — „kulturní ráčna" jako analogie civilizačních intelligence explosions
- Minsky: implicitní — terminologie „societies of thought" echuje Society of Mind
- Dunbar: inferenční — De Marzo et al. 2024 prokázali LLM Dunbar number >1000

**Institutional alignment vs. RLHF:**
- RLHF je dyadic parent-child model → neškáluje na multi-agent systémy
- „A collective of safe agents is not a safe collective by default" (arXiv:2601.10599)
- Řešení: checks-and-balances, plurality aktérů, auditing přes systémy s odlišnými hodnotami

## Implikace pro STOPA

1. **Critic agent** s odlišným system promptem = nutnost, ne optional — empiricky validováno
2. **Heterogenita** system promptů per agent > kopie téhož modelu
3. **Orchestrátor ≠ single point of control** — „power must check power"
4. **Checkpoint/shared state** architektura = potvrzená nutnost (temporal alignment failure → instability ridge)
5. **High-stakes tasks**: orchestrátor + critic + human checkpoint jako minimální governance vrstva

## Limity paperu (pro kontextualizaci)

- Empirická základna úzká (aritmetika, malé modely)
- Formálně tenký — neobsahuje inženýrské instrukce
- Přímé kritiky zatím neexistují (paper 9 dní starý k 2026-03-30)
