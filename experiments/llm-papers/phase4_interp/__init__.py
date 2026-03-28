"""Phase 4B: Mechanistic Interpretability via Sparse Autoencoders.

Paper: "Scaling Monosemanticity: Extracting Interpretable Features from Claude 3 Sonnet"
       (Templeton et al., 2024)

Neural networks store information in "superposition" — each neuron encodes
multiple concepts simultaneously. Sparse Autoencoders (SAEs) decompose these
superposed representations into interpretable, monosemantic features.

SAE architecture:
    hidden_state → encoder → ReLU (sparse) → decoder → reconstructed_state

The encoder projects into a much LARGER space (e.g., 384 → 4096 latents),
but with L1 sparsity — most latents are zero for any given input.
Each active latent ideally corresponds to one interpretable concept.
"""
