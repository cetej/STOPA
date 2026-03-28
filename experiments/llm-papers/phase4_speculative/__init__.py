"""Phase 4C: Speculative Decoding.

Paper: "Fast Inference from Transformers via Speculative Decoding"
       (Leviathan et al., 2022 / Chen et al., 2023)

Key idea: Use a small fast "draft" model to propose K tokens, then verify
them all at once with the large "target" model in a single forward pass.

Why it works:
- Autoregressive generation is sequential (1 token = 1 forward pass)
- But VERIFICATION is parallel (check K tokens = 1 forward pass)
- If the draft model is good, most proposals are accepted
- Expected speedup: ~2-3× with a well-matched draft model

Mathematically, this produces EXACTLY the same distribution as the
target model alone — no quality degradation, just speed.
"""
