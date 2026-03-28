"""Top-K Router for Mixture of Experts.

Papers:
- Shazeer et al. (2017): Sparsely-gated MoE — introduced noisy top-k gating
- Fedus et al. (2021): Switch Transformers — simplified to top-1 routing
- Mixtral (2024): Uses top-2 routing as the sweet spot

The router is a simple linear layer that maps each token's hidden state
to a score per expert. Top-k experts are selected, and their outputs are
weighted by the (normalized) router scores.

Load Balancing:
Without balancing, the router often collapses to always picking the same
1-2 experts ("expert collapse"). The auxiliary loss encourages uniform
expert utilization by penalizing imbalance between:
- fraction of tokens routed to each expert (f_i)
- average router probability for each expert (P_i)
"""

import torch
import torch.nn as nn
import torch.nn.functional as F


class TopKRouter(nn.Module):
    """Learned top-k routing network.

    For each token, produces:
    1. Router logits: one score per expert
    2. Top-k selection: indices and weights of chosen experts
    3. Auxiliary loss: load-balancing penalty

    The routing decision:
        logits = x @ W_router          (batch*seq, n_experts)
        probs = softmax(logits)
        top_k_indices, top_k_weights = top_k(probs)
        top_k_weights = normalize(top_k_weights)  # sum to 1 within selected

    Args:
        dim: Model hidden dimension
        n_experts: Total number of experts
        n_active: Number of experts to activate per token (top-k)
        noise_std: Standard deviation of noise added during training
                   (encourages exploration of different experts)
    """

    def __init__(
        self,
        dim: int,
        n_experts: int,
        n_active: int = 2,
        noise_std: float = 0.1,
    ):
        super().__init__()
        self.n_experts = n_experts
        self.n_active = n_active
        self.noise_std = noise_std

        # Linear projection: token → expert scores
        self.gate = nn.Linear(dim, n_experts, bias=False)

    def forward(
        self, x: torch.Tensor
    ) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
        """Route tokens to experts.

        Args:
            x: (batch, seq_len, dim) — token hidden states

        Returns:
            top_k_indices: (batch*seq, n_active) — selected expert indices
            top_k_weights: (batch*seq, n_active) — normalized routing weights
            aux_loss: scalar — load balancing auxiliary loss
        """
        batch, seq_len, dim = x.shape
        # Flatten to (batch*seq, dim) for routing
        x_flat = x.view(-1, dim)
        n_tokens = x_flat.shape[0]

        # Compute router logits
        logits = self.gate(x_flat)  # (n_tokens, n_experts)

        # Add noise during training for exploration (Shazeer et al., 2017)
        if self.training and self.noise_std > 0:
            noise = torch.randn_like(logits) * self.noise_std
            logits = logits + noise

        # Softmax to get routing probabilities
        router_probs = F.softmax(logits, dim=-1)  # (n_tokens, n_experts)

        # Select top-k experts per token
        top_k_weights, top_k_indices = torch.topk(
            router_probs, self.n_active, dim=-1
        )  # both (n_tokens, n_active)

        # Normalize weights of selected experts to sum to 1
        top_k_weights = top_k_weights / (top_k_weights.sum(dim=-1, keepdim=True) + 1e-8)

        # Compute load-balancing auxiliary loss
        aux_loss = self._load_balance_loss(router_probs, top_k_indices, n_tokens)

        return top_k_indices, top_k_weights, aux_loss

    def _load_balance_loss(
        self,
        router_probs: torch.Tensor,
        top_k_indices: torch.Tensor,
        n_tokens: int,
    ) -> torch.Tensor:
        """Compute load balancing auxiliary loss.

        From Switch Transformers (Fedus et al., 2021):
            L_aux = n_experts * Σᵢ (fᵢ * Pᵢ)

        Where:
        - fᵢ = fraction of tokens routed to expert i
        - Pᵢ = average routing probability for expert i

        Minimizing this product encourages:
        - Even distribution of tokens across experts (uniform fᵢ)
        - Even router probabilities (uniform Pᵢ)

        Perfect balance: fᵢ = Pᵢ = 1/n_experts → L = 1.0
        Worst case (all to one expert): L ≈ n_experts
        """
        # fᵢ: fraction of tokens assigned to each expert
        # Count how many times each expert appears in top-k selections
        one_hot = F.one_hot(top_k_indices, self.n_experts).float()  # (n_tokens, n_active, n_experts)
        tokens_per_expert = one_hot.sum(dim=1).sum(dim=0)  # (n_experts,)
        f = tokens_per_expert / (n_tokens * self.n_active)  # Normalize

        # Pᵢ: average routing probability per expert
        P = router_probs.mean(dim=0)  # (n_experts,)

        # Auxiliary loss
        aux_loss = self.n_experts * (f * P).sum()

        return aux_loss
