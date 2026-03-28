"""Mixture of Experts Layer.

Replaces the single dense FFN in a Transformer block with N parallel
expert FFNs, where only top-k are activated per token.

Architecture:
    Dense:  x → FFN(x)                     # All params active
    MoE:    x → Σᵢ wᵢ · Expertᵢ(x)        # Only top-k experts active

Where wᵢ are the normalized routing weights and only k out of N experts
compute their output for each token.

Implementation notes:
- Naive approach: loop over experts (simple but slow on GPU)
- This implementation: batch tokens by expert assignment for efficiency
  (tokens going to same expert are processed together)
"""

import torch
import torch.nn as nn

from phase1_transformer.layers import SwiGLU

from .router import TopKRouter


class MoELayer(nn.Module):
    """Mixture of Experts FFN layer.

    Contains N expert FFN modules (each a SwiGLU network from Phase 1)
    and a router that selects top-k experts per token.

    Args:
        dim: Model hidden dimension
        n_experts: Number of expert FFNs
        n_active: Number of experts active per token
        ffn_hidden_dim: Hidden dimension of each expert FFN (None = auto)
    """

    def __init__(
        self,
        dim: int,
        n_experts: int = 8,
        n_active: int = 2,
        ffn_hidden_dim: int | None = None,
    ):
        super().__init__()
        self.n_experts = n_experts
        self.n_active = n_active
        self.dim = dim

        # Router: decides which experts handle each token
        self.router = TopKRouter(dim, n_experts, n_active)

        # N expert FFNs (each is an independent SwiGLU from Phase 1)
        self.experts = nn.ModuleList([
            SwiGLU(dim, ffn_hidden_dim) for _ in range(n_experts)
        ])

    def forward(self, x: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor]:
        """Process tokens through selected experts.

        Args:
            x: (batch, seq_len, dim) — input hidden states

        Returns:
            output: (batch, seq_len, dim) — MoE output
            aux_loss: scalar — load balancing loss from router

        Implementation:
        1. Router selects top-k experts and weights per token
        2. For each expert, gather the tokens assigned to it
        3. Process through expert FFN
        4. Scatter results back and weight by router scores
        """
        batch, seq_len, dim = x.shape
        x_flat = x.view(-1, dim)  # (n_tokens, dim)
        n_tokens = x_flat.shape[0]

        # Route: get expert assignments and weights
        top_k_indices, top_k_weights, aux_loss = self.router(x)
        # top_k_indices: (n_tokens, n_active) — which experts
        # top_k_weights: (n_tokens, n_active) — how much weight

        # Initialize output
        output = torch.zeros_like(x_flat)  # (n_tokens, dim)

        # Process each expert's assigned tokens
        # This loops over experts (not tokens) — more efficient when
        # n_experts << n_tokens, which is always the case
        for expert_idx in range(self.n_experts):
            # Find which (token, slot) pairs assigned to this expert
            # mask: (n_tokens, n_active) boolean
            mask = (top_k_indices == expert_idx)

            if not mask.any():
                continue  # No tokens for this expert

            # Get token indices assigned to this expert
            token_indices = mask.any(dim=-1).nonzero(as_tuple=True)[0]

            if len(token_indices) == 0:
                continue

            # Gather tokens for this expert
            expert_input = x_flat[token_indices]  # (n_assigned, dim)

            # Run through expert FFN
            expert_output = self.experts[expert_idx](expert_input)  # (n_assigned, dim)

            # Get weights for this expert's contribution
            # For each assigned token, get the weight from the slot where this expert was selected
            expert_weights = (mask[token_indices].float() * top_k_weights[token_indices]).sum(dim=-1)
            # expert_weights: (n_assigned,)

            # Weighted scatter back
            output[token_indices] += expert_output * expert_weights.unsqueeze(-1)

        return output.view(batch, seq_len, dim), aux_loss

    @property
    def total_params(self) -> int:
        """Total parameters (all experts)."""
        return sum(p.numel() for p in self.parameters())

    @property
    def active_params(self) -> int:
        """Parameters active per token (router + k experts)."""
        router_params = sum(p.numel() for p in self.router.parameters())
        expert_params = sum(p.numel() for p in self.experts[0].parameters())
        return router_params + self.n_active * expert_params
