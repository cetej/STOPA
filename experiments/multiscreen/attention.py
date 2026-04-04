"""ScreeningAttention — generic drop-in replacement for nn.MultiheadAttention."""

import torch
import torch.nn as nn
import torch.nn.functional as F

from .core import ScreeningUnit, TanhNorm
from .mipe import MiPE


class ScreeningAttention(nn.Module):
    """Multi-head screening attention as a drop-in replacement for standard MHA.

    Each head is one screening tile with independent learned threshold (r)
    and window width (w). Supports self-attention, cross-attention,
    optional causal masking, RoPE, and attention masks.

    Unlike standard MHA, this module includes a gated output per head
    (subsuming the FFN role), matching the paper's architecture.
    """

    def __init__(
        self,
        d_model: int,
        num_heads: int,
        d_k: int = 16,
        d_v: int | None = None,
        use_gate: bool = True,
        use_distance_mask: bool = True,
        use_mipe: bool = False,
        max_seq_len: int = 8192,
    ):
        super().__init__()
        self.d_model = d_model
        self.num_heads = num_heads
        self.d_k = d_k
        self.d_v = d_v or (d_model // num_heads)
        self.use_gate = use_gate
        self.use_distance_mask = use_distance_mask

        # Per-head projections
        self.W_q = nn.Linear(d_model, num_heads * d_k, bias=False)
        self.W_k = nn.Linear(d_model, num_heads * d_k, bias=False)
        self.W_v = nn.Linear(d_model, num_heads * self.d_v, bias=False)
        if use_gate:
            self.W_g = nn.Linear(d_model, num_heads * self.d_v, bias=False)

        # Per-head screening parameters
        self.s_r = nn.Parameter(torch.zeros(num_heads))
        self.s_w = nn.Parameter(torch.full((num_heads,), 4.0))

        # Output projection
        self.W_o = nn.Linear(num_heads * self.d_v, d_model, bias=False)
        self.scale = nn.Parameter(torch.ones(num_heads))

        self.tanhnorm = TanhNorm()

        # Optional MiPE (per-head, shared frequencies)
        self.mipe = MiPE(d_k, max_seq_len) if use_mipe else None

    def _screening_per_head(
        self,
        q: torch.Tensor,  # (B, T_q, d_k)
        k: torch.Tensor,  # (B, T_k, d_k)
        v: torch.Tensor,  # (B, T_k, d_v)
        head_idx: int,
        is_cross: bool,
        is_causal: bool,
        attn_mask: torch.Tensor | None,
    ) -> torch.Tensor:
        """Run screening for one head."""
        # MiPE
        if self.mipe is not None:
            q, k = self.mipe(q, k, self.s_w[head_idx])

        # L2-normalize
        q_n = F.normalize(q, dim=-1)
        k_n = F.normalize(k, dim=-1)
        v_n = F.normalize(v, dim=-1)

        # Trim-and-Square relevance
        s = torch.bmm(q_n, k_n.transpose(-2, -1))
        r = torch.exp(self.s_r[head_idx]) + 1.0
        alpha = torch.clamp(1.0 - r * (1.0 - s), min=0.0).square()

        T_q, T_k = q.shape[1], k.shape[1]

        # Distance softmask (skip for cross-attention — positions are meaningless)
        if self.use_distance_mask and not is_cross:
            w = torch.exp(self.s_w[head_idx]) + 1.0
            q_pos = torch.arange(T_q, device=q.device).unsqueeze(1).float()
            k_pos = torch.arange(T_k, device=q.device).unsqueeze(0).float()
            softmask = torch.sigmoid(w - (q_pos - k_pos).abs()).unsqueeze(0)
            alpha = alpha * softmask

        # Causal mask
        if is_causal:
            causal = torch.tril(torch.ones(T_q, T_k, device=q.device)).unsqueeze(0)
            alpha = alpha * causal

        # External mask
        if attn_mask is not None:
            alpha = alpha * attn_mask

        h = torch.bmm(alpha, v_n)
        return self.tanhnorm(h)

    def forward(
        self,
        query: torch.Tensor,
        key: torch.Tensor,
        value: torch.Tensor,
        attn_mask: torch.Tensor | None = None,
        is_causal: bool = False,
    ) -> torch.Tensor:
        """
        Args:
            query: (batch, seq_q, d_model)
            key: (batch, seq_k, d_model) — same as query for self-attention
            value: (batch, seq_k, d_model)
            attn_mask: additive mask (converted to multiplicative internally)
            is_causal: apply causal (lower-triangular) mask

        Returns:
            output: (batch, seq_q, d_model)
        """
        B, T_q, _ = query.shape
        T_k = key.shape[1]
        is_cross = T_q != T_k or not torch.equal(query, key)

        # Project all heads at once
        q_all = self.W_q(query).reshape(B, T_q, self.num_heads, self.d_k)
        k_all = self.W_k(key).reshape(B, T_k, self.num_heads, self.d_k)
        v_all = self.W_v(value).reshape(B, T_k, self.num_heads, self.d_v)

        if self.use_gate:
            g_all = self.W_g(query).reshape(B, T_q, self.num_heads, self.d_v)

        # Convert additive mask to multiplicative
        mult_mask = None
        if attn_mask is not None:
            mult_mask = (attn_mask != float("-inf")).float()

        # Run each head
        head_outputs = []
        for h in range(self.num_heads):
            q_h = q_all[:, :, h, :]  # (B, T_q, d_k)
            k_h = k_all[:, :, h, :]  # (B, T_k, d_k)
            v_h = v_all[:, :, h, :]  # (B, T_k, d_v)

            u = self._screening_per_head(
                q_h, k_h, v_h, h, is_cross, is_causal, mult_mask
            )

            if self.use_gate:
                g_h = g_all[:, :, h, :]
                g_hat = torch.tanh(F.silu(g_h))
                u = u * g_hat

            head_outputs.append(u * self.scale[h])

        # Concatenate heads and project
        concat = torch.cat(head_outputs, dim=-1)  # (B, T_q, num_heads * d_v)
        return self.W_o(concat)
