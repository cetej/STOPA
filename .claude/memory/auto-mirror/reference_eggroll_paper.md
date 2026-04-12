---
name: reference_eggroll_paper
description: "EGGROLL (Oxford/MILA 2026): low-rank ES for billion-param models, 3 principles adopted into STOPA skills (rank-1 mutations, GRPO scoring, adaptive sigma)"
type: reference
---

EGGROLL paper (Sarkar, Fellows et al., Oxford FLAIR + MILA, 2026): Evolution Strategies at the Hyperscale.
URL: https://eshyperscale.github.io/

3 principy adoptovane do STOPA:
1. Rank-1 perturbace staci (Theorem 3) — kazda varianta mutuje jednu osu → prompt-evolve, autoloop
2. GRPO-style z-score normalizace pres populaci → prompt-evolve Phase 4
3. Tri rezimy sigma (linearizace/kriticka/divergence) → self-evolve Adaptive Mutation Strength

Dalsi relevance: RWKV-7 jako efektivni inference model (NG-ROBOT, MONITOR), int8 pretraining bez gradientu.
