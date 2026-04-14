---
date: 2026-04-13
type: best_practice
severity: medium
component: orchestration
tags: [rl-training, pairwise-comparison, evaluation, autoreason, skill-design]
summary: "Pairwise comparison (A vs B) je dostatečný verifiable reward signal pro iterativní zlepšování bez potřeby reward modelu. VMR-RLVR ukazuje, že binární choice zachovává stabilní gradient pro RL trénink — patternů využívá STOPA autoreason a self-evolve."
source: external_research
uses: 2
harmful_uses: 0
successful_uses: 0
confidence: 0.80
maturity: draft
related: [2026-04-08-direction-magnitude-decoupling-optimization.md]
verify_check: "manual"
skill_scope: [autoreason, self-evolve, autoloop]
---

# Pairwise Choice je Dostatečný Verifiable Signal

VMR-RLVR (arXiv:2511.02463) prokázal, že open-ended úlohy (kreativní psaní, subjektivní otázky) lze naučit iterativně zlepšovat pomocí binárního pairwise comparison bez potřeby reward modelu.

**Klíčový princip**: Místo "jak dobrá je tato odpověď?" (absolutní skóre) → "která z těchto dvou je lepší?" (relativní choice). Binární 0/1 feedback je verifiable a stabilní pro gradient-based learning.

**STOPA relevance**:
- autoreason skill explicitně používá A vs B comparison — tato práce dává tomuto patternu silné akademické zdůvodnění
- self-evolve používá "incumbent vs challenger" pattern — ekvivalent VMR-RLVR pairwise choice
- Implikace: reasoning-capable modely (Opus, Sonnet) profitují z iterativního pairwise feedbacku; haiku méně (scale reversal potvrzuje Tool-Genesis learning)

**Omezení**: Non-reasoning modely profitují minimálně. Metoda vyžaduje pre-existing reasoning schopnost.
