# Reinforced Reasoning — Large Reasoning Models

**Type:** concept
**Tags:** ai, reasoning, rl, orchestration, test-time-compute
**Related:** [[rlvr]], [[process-reward-models]], [[tree-of-thoughts]], [[test-time-learning]]
**Updated:** 2026-04-15

---

Reinforced reasoning je paradigma kde LLM získávají reasoning schopnosti přes RL a strategické test-time compute. Survey arXiv:2501.09686 (Xu et al., Tsinghua/HKUST/Emory) identifikuje 3 pilíře.

## 3 pilíře

### 1. Data Construction — od lidí k MCTS

Posun od drahých ručních anotací k automatizované generaci reasoning trajektorií:
- MCTS simulace generují step-by-step reasoning data
- PRM trénink na syntetických procesních odměnách
- Dramaticky levnější, zachovává kvalitu

### 2. RL pro reasoning

Progrese: SFT → Outcome Reward Models (ORM) → Process Reward Models (PRM):
- **ORM** = odměna jen za finální výsledek (sparse signal)
- **PRM** = odměna za KAŽDÝ krok (dense signal) — klíčový průlom
- PRM umožňuje credit assignment: identifikuje KDE v řetězci reasoning selhal

### 3. Test-time scaling laws

Nové scaling zákony: víc compute při inferenci = lepší výsledky:
- PRM-guided search: hledej přes reasoning kroky, ne jen generuj
- Tree exploration: MCTS/ToT nad reasoning prostorem
- Self-consistency: generuj N řešení, hlasuj o výsledku
- Zásadní rozdíl od pretraining scaling (víc dat/parametrů)

## Klíčové metody

| Metoda | Princip | Compute cost |
|--------|---------|-------------|
| Best-of-N + ORM | Generuj N, vyber nejlepší podle outcome | N× inference |
| Best-of-N + PRM | Generuj N, vyber nejlepší podle procesu | N× inference + step scoring |
| Tree search (MCTS) | Expanduj slibné větve, prořezávej slabé | Variable, guided |
| Self-consistency | Majority voting přes N nezávislých řešení | N× inference |
| Beam search + PRM | Udržuj K nejlepších částečných řešení | K× per step |

## Open-source implementace

- **OpenR** — framework pro RL reasoning research
- **REST-MCTS*** — MCTS-guided reasoning s process rewards
- **Journey Learning** — učení z celé trajektorie (včetně chyb), ne jen finálního výsledku
- **LLaMA-Berry** — MCTS + self-refinement pro LLaMA modely

## Relevance pro STOPA

### Přímé mapování

| Paper koncept | STOPA ekvivalent | Gap |
|--------------|-----------------|-----|
| ORM (outcome-only) | Současný /critic — verdikt na konci | Funguje, ale pozdě detekuje chyby |
| PRM (step-wise) | **Chybí** — potřeba step-level checkpoints | Hlavní implementační příležitost |
| Best-of-N | Autoloop iterace (lineární) | Chybí paralelní kandidáti |
| MCTS/ToT | ToT zmíněn v wiki, neimplementován | Deep tier branching opportunity |
| Self-consistency | Neexistuje | Majority voting pro critic verdikty |
| Journey Learning | Outcomes/ tracking | Rozšířit o intermediate state capture |

### 3 konkrétní vylepšení

1. **Step-level verification v orchestrate** — po každém subtasku lightweight haiku check ("splnil krok co plán vyžadoval?"), kill early při selhání
2. **Best-of-N v autoloop/autoresearch** — paralelně 2-3 přístupy, PRM-score, expand nejlepší
3. **Adaptive test-time budget** — deep tier = self-consistency (3× critic, majority vote), light = single-pass

## Zdroj

Xu et al. (2025): "Towards Large Reasoning Models: A Survey of Reinforced Reasoning with Large Language Models" — arXiv:2501.09686
