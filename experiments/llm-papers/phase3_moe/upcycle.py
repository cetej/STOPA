"""Sparse Upcycling — Convert a dense model to MoE.

Paper: "Sparse Upcycling: Training Mixture-of-Experts from Dense Checkpoints"
       (Komatsuzaki et al., 2022 / ICLR 2023)

Key insight: Instead of training MoE from random initialization, START from
a trained dense model:
1. Take a trained dense checkpoint (Phase 1 model)
2. Copy the dense FFN weights into EVERY expert (all N experts start identical)
3. Initialize the router with small random weights
4. Continue training → experts gradually specialize

Why this works:
- Dense model already learned good representations
- MoE training from scratch is unstable (router collapse, expert imbalance)
- Upcycling gives a "warm start" where every expert already performs well
- Router just needs to learn WHICH expert to specialize for WHICH tokens

Practical benefit:
- Reuse expensive dense training compute
- MoE model starts at same quality as dense, then improves
- Much faster convergence than MoE from scratch
"""

import copy

import torch

from phase1_transformer.config import TransformerConfig
from phase1_transformer.model import GPTModel

from .moe_model import GPTMoEModel


def upcycle_dense_to_moe(
    dense_model: GPTModel,
    n_experts: int = 8,
    n_active: int = 2,
    router_noise_std: float = 0.01,
) -> GPTMoEModel:
    """Convert a trained dense GPT model to a MoE model.

    Process:
    1. Create MoE config from dense config (add expert count)
    2. Build empty MoE model
    3. Copy shared weights (embeddings, attention, norms)
    4. Copy dense FFN → every expert (N identical copies)
    5. Initialize router with small random weights

    After upcycling, the MoE model should produce IDENTICAL outputs to
    the dense model (since all experts are the same and router doesn't
    matter when all experts give the same answer).

    Args:
        dense_model: Trained Phase 1 GPTModel
        n_experts: Number of experts per layer
        n_active: Number of active experts per token
        router_noise_std: Std for router weight initialization

    Returns:
        Initialized GPTMoEModel ready for continued training
    """
    dense_config = dense_model.config

    # 1. Create MoE config
    moe_config = TransformerConfig(
        n_layers=dense_config.n_layers,
        n_heads=dense_config.n_heads,
        dim=dense_config.dim,
        max_seq_len=dense_config.max_seq_len,
        vocab_size=dense_config.vocab_size,
        ffn_hidden_dim=dense_config.ffn_hidden_dim,
        dropout=dense_config.dropout,
        rope_theta=dense_config.rope_theta,
        n_experts=n_experts,
        n_active_experts=n_active,
    )

    # 2. Build MoE model
    moe_model = GPTMoEModel(moe_config)

    # 3. Copy shared weights
    # Embedding (shared with output via weight tying)
    moe_model.tok_emb.weight.data.copy_(dense_model.tok_emb.weight.data)

    # Final norm
    moe_model.norm.weight.data.copy_(dense_model.norm.weight.data)

    # 4. Per-layer: copy attention + norms, replicate FFN to all experts
    for i, (dense_layer, moe_layer) in enumerate(
        zip(dense_model.layers, moe_model.layers)
    ):
        # Attention weights (identical)
        moe_layer.attention.load_state_dict(dense_layer.attention.state_dict())

        # Norms (identical)
        moe_layer.norm1.weight.data.copy_(dense_layer.norm1.weight.data)
        moe_layer.norm2.weight.data.copy_(dense_layer.norm2.weight.data)

        # FFN → copy to EVERY expert
        dense_ffn_state = dense_layer.ffn.state_dict()
        for expert in moe_layer.moe.experts:
            expert.load_state_dict(copy.deepcopy(dense_ffn_state))

        # Router: small random initialization
        # Small weights → near-uniform routing initially → all experts contribute equally
        torch.nn.init.normal_(moe_layer.moe.router.gate.weight, std=router_noise_std)

    params = moe_model.count_parameters()
    dense_params = dense_model.count_parameters()
    print(f"Sparse Upcycling complete:")
    print(f"  Dense:  {dense_params:,} params")
    print(f"  MoE:    {params['total']:,} total, {params['active']:,} active")
    print(f"  Experts: {n_experts} total, {n_active} active per token")
    print(f"  Expansion: {params['total'] / dense_params:.1f}x total, "
          f"{params['active'] / dense_params:.2f}x active compute")

    return moe_model


def verify_upcycling(
    dense_model: GPTModel,
    moe_model: GPTMoEModel,
    test_tokens: torch.Tensor | None = None,
    atol: float = 0.1,
) -> bool:
    """Verify that upcycled MoE produces similar outputs to dense model.

    Since all experts are copies of the dense FFN, the MoE output should
    be close to the dense output (not exactly equal due to routing weights
    and normalization, but close).

    Returns True if outputs match within tolerance.
    """
    if test_tokens is None:
        test_tokens = torch.randint(0, dense_model.config.vocab_size, (1, 32))

    dense_model.eval()
    moe_model.eval()

    with torch.no_grad():
        dense_logits, _ = dense_model(test_tokens)
        moe_logits, _, aux_loss = moe_model(test_tokens)

    max_diff = (dense_logits - moe_logits).abs().max().item()
    mean_diff = (dense_logits - moe_logits).abs().mean().item()

    print(f"Upcycling verification:")
    print(f"  Max logit difference:  {max_diff:.6f}")
    print(f"  Mean logit difference: {mean_diff:.6f}")
    print(f"  Aux loss:              {aux_loss.item():.4f}")
    print(f"  Match (atol={atol}):   {'PASS' if max_diff < atol else 'FAIL'}")

    return max_diff < atol
