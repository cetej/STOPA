"""Phase 3A: Mixture of Experts (MoE).

Papers:
- "Outrageously Large Neural Networks: Sparsely-Gated MoE" (Shazeer et al., 2017) — MoE ignition
- "Switch Transformers" (Fedus et al., 2021) — simplified single-expert routing
- "Mixtral of Experts" (Mistral AI, 2024) — open-weight MoE matching dense quality
- "Sparse Upcycling" (Komatsuzaki et al., 2022) — dense→MoE conversion

Core idea: Replace each FFN with N parallel "expert" FFNs. A learned router
selects the top-k experts per token. Total params grow N×, but active compute
stays constant (only k experts run per token).
"""
