---
date: 2026-04-15
source_type: text
source_url: https://arxiv.org/abs/2602.24281
---

# Memory Caching: RNNs with Growing Memory (arXiv:2602.24281)

Behrouz, Li, Deng, Zhong, Razaviyayn, Mirrokni (Google Research, 2026).

RNN s cachovanými checkpointy memory stavů — interpolace mezi fixní pamětí RNN O(L) a rostoucí pamětí Transformerů O(L²). Sekvence se segmentuje, na hranicích se cachuje memory state, při zpracování tokenu model přistupuje k aktuálnímu + cachovaným stavům.

4 varianty: Residual (součet, kolabuje u lineárních), Gated Residual Memory/GRM (context-aware gating, hlavní), Memory Soup (interpolace parametrů, pro non-lineární), Sparse Selective Caching/SSC (MoE top-k router, minimální overhead).

Komplexita: O(L) až O(L²) podle segment size. Log segmentace = O(L log L). Titans+GRM: +0.8% LM, 100% NIAH@16K. Blíží se Transformerům na recall. Funguje i post-training (inference-time). Hybrid modely (attention+RNN) = matematicky MC se segment=1.
