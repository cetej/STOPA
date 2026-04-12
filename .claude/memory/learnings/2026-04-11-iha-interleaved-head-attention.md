---
date: 2026-04-11
type: architecture
severity: medium
component: general
tags: [attention, inference, architecture, watch-item, long-context]
summary: "IHA (arXiv:2602.21371) umožňuje cross-head komunikaci přes pseudo-hlavy — P² attention patterns na hlavu místo 1. Multi-key retrieval +112% @16k, GSM8K +5.8%. Kompatibilní s FlashAttention. Watch item pro long-context a multi-hop reasoning."
source: external_research
confidence: 0.6
uses: 0
successful_uses: 0
harmful_uses: 0
related: [2026-04-11-calm-continuous-autoregressive.md]
verify_check: manual
---

## IHA — Interleaved Head Attention

**Paper:** arXiv:2602.21371 (Duvvuri, Ekbote, Bansal et al.)

**Technika:** Pseudo-hlavy jako lineární kombinace všech H hlav: Q̃_{h,j} = Σ α_{m,h,j} · Q_m. Až P² attention patterns na hlavu (vs 1 v MHA). Overhead jen 4H²P parametrů (~32K při H=P=20).

**Klíčová čísla:**
- Multi-Key Retrieval @16k (RULER): +112%
- GSM8K Maj@16 (po SFT): +5.8%
- MATH-500 Maj@16: +2.8%
- Teoreticky: Θ(√k) hlav místo Θ(k) pro k-hop reasoning
- Hybridní schedule (4 sliding-window + 1 global) = FLOP-parity s MHA

**Proč důležité:**
- Kompatibilní s FlashAttention (mixing PŘED attention, ne po)
- Striktní generalizace MHA (α = identity → standardní MHA)
- Biggest win v long-context multi-hop retrieval — přesně kde LLM pipeline trpí

**Limitace:** Jen from-scratch training (240B tokens), žádný retrofit. HumanEval bez zlepšení. Žádné wall-clock měření. Teoretické důkazy jen pro lineární attention.

**Pro STOPA:** Watch item. Pokud provideři adoptují IHA, automatický benefit pro long-context retrieval a multi-hop reasoning (deepresearch, pipeline zpracování dlouhých článků).
