"""Core screening primitives: TanhNorm and ScreeningUnit."""

import torch
import torch.nn as nn
import torch.nn.functional as F


class TanhNorm(nn.Module):
    """TanhNorm: bounded normalization that preserves zero vectors.

    u = (tanh(||h||) / ||h||) * h

    Unlike LayerNorm, this keeps the direction and allows zero output
    (representing "no relevant context found").
    """

    def __init__(self, eps: float = 1e-8):
        super().__init__()
        self.eps = eps

    def forward(self, h: torch.Tensor) -> torch.Tensor:
        norm = h.norm(dim=-1, keepdim=True).clamp(min=self.eps)
        return (torch.tanh(norm) / norm) * h


class ScreeningUnit(nn.Module):
    """Core screening mechanism replacing softmax attention.

    For each query-key pair:
    1. Compute similarity s_ij = q_norm . k_norm^T  (in [-1, 1])
    2. Apply Trim-and-Square: alpha_ij = [max(1 - r*(1 - s_ij), 0)]^2
       where r = e^(s_r) + 1 is a learned inverse acceptance width
    3. Optionally apply distance softmask: alpha_ij * sigmoid(w - |i-j|)
    4. Optionally apply causal mask
    5. Aggregate: h_i = sum(alpha_ij * v_norm_j)
    6. Normalize: u_i = TanhNorm(h_i)
    """

    def __init__(self, d_k: int = 16, d_v: int = 64):
        super().__init__()
        self.d_k = d_k
        self.d_v = d_v

        # Learned screening parameters (per tile)
        self.s_r = nn.Parameter(torch.tensor(0.0))  # -> r = exp(s_r) + 1
        self.s_w = nn.Parameter(torch.tensor(4.0))  # -> w = exp(s_w) + 1

        self.tanhnorm = TanhNorm()

    @property
    def r(self) -> torch.Tensor:
        """Learned inverse acceptance width."""
        return torch.exp(self.s_r) + 1.0

    @property
    def w(self) -> torch.Tensor:
        """Learned window width."""
        return torch.exp(self.s_w) + 1.0

    def compute_relevance(
        self, q: torch.Tensor, k: torch.Tensor
    ) -> torch.Tensor:
        """Trim-and-Square transform for absolute relevance.

        Args:
            q: (batch, seq_q, d_k) — L2-normalized queries
            k: (batch, seq_k, d_k) — L2-normalized keys

        Returns:
            alpha: (batch, seq_q, seq_k) — relevance scores, many exactly 0
        """
        s = torch.bmm(q, k.transpose(-2, -1))
        r = self.r
        alpha = torch.clamp(1.0 - r * (1.0 - s), min=0.0)
        return alpha.square()

    def compute_softmask(
        self, seq_q: int, seq_k: int, device: torch.device
    ) -> torch.Tensor:
        """Distance-aware softmask: m_ij(w) = sigmoid(w - |i - j|)."""
        w = self.w
        q_pos = torch.arange(seq_q, device=device).unsqueeze(1).float()
        k_pos = torch.arange(seq_k, device=device).unsqueeze(0).float()
        dist = (q_pos - k_pos).abs()
        return torch.sigmoid(w - dist).unsqueeze(0)

    def forward(
        self,
        q: torch.Tensor,
        k: torch.Tensor,
        v: torch.Tensor,
        use_distance_mask: bool = True,
        use_causal_mask: bool = True,
        attn_mask: torch.Tensor | None = None,
    ) -> torch.Tensor:
        """
        Args:
            q: (batch, seq_q, d_k)
            k: (batch, seq_k, d_k)
            v: (batch, seq_k, d_v)
            use_distance_mask: apply positional softmask
            use_causal_mask: apply causal (lower-triangular) mask
            attn_mask: optional (seq_q, seq_k) or (batch, seq_q, seq_k) multiplicative mask

        Returns:
            u: (batch, seq_q, d_v)
        """
        T_q = q.shape[1]
        T_k = k.shape[1]

        q_norm = F.normalize(q, dim=-1)
        k_norm = F.normalize(k, dim=-1)
        v_norm = F.normalize(v, dim=-1)

        alpha = self.compute_relevance(q_norm, k_norm)

        if use_distance_mask:
            softmask = self.compute_softmask(T_q, T_k, q.device)
            alpha = alpha * softmask

        if use_causal_mask:
            causal = torch.tril(torch.ones(T_q, T_k, device=q.device)).unsqueeze(0)
            alpha = alpha * causal

        if attn_mask is not None:
            alpha = alpha * attn_mask

        h = torch.bmm(alpha, v_norm)
        return self.tanhnorm(h)
