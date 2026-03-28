"""Multi-Head Self-Attention with Rotary Position Embeddings (RoPE).

Papers:
- "Attention Is All You Need" (Vaswani et al., 2017)
  Core mechanism: Q·K^T / sqrt(d_k) → softmax → V
- "RoFormer: Enhanced Transformer with Rotary Position Embedding" (Su et al., 2021)
  Encodes position by ROTATING query and key vectors in 2D subspaces.

Why RoPE over learned/sinusoidal positional embeddings?
1. Relative position: attention between tokens depends on their DISTANCE,
   not absolute positions. RoPE naturally encodes this via rotation angles.
2. Extrapolation: RoPE generalizes better to longer sequences than trained on.
3. No extra parameters: position info is injected via rotation, not learned vectors.
4. Industry standard: LLaMA, Mistral, Qwen, DeepSeek all use RoPE.
"""

import math

import torch
import torch.nn as nn
import torch.nn.functional as F

from .config import TransformerConfig


def precompute_rope_frequencies(
    head_dim: int,
    max_seq_len: int,
    theta: float = 10000.0,
    device: torch.device | None = None,
) -> torch.Tensor:
    """Precompute complex-valued rotation frequencies for RoPE.

    RoPE works by pairing adjacent dimensions (2i, 2i+1) and rotating them
    by an angle that depends on position and frequency:

        freq_i = 1 / (theta^(2i/d))  for i = 0, 1, ..., d/2 - 1
        angle(pos, i) = pos * freq_i

    This gives each position a unique "fingerprint" of rotations across
    different frequency bands — low dimensions rotate slowly (capture
    long-range position), high dimensions rotate fast (capture local position).

    Returns: Complex tensor of shape (max_seq_len, head_dim // 2)
             where each value is exp(i * angle) = cos(angle) + i*sin(angle)
    """
    # Frequencies: 1/theta^(2i/d) for i in [0, d/2)
    freqs = 1.0 / (theta ** (torch.arange(0, head_dim, 2, device=device).float() / head_dim))
    # Positions: 0, 1, 2, ..., max_seq_len-1
    positions = torch.arange(max_seq_len, device=device).float()
    # Outer product: angles[pos, i] = pos * freq_i
    angles = torch.outer(positions, freqs)
    # Convert to complex: exp(i*angle) for efficient rotation
    return torch.polar(torch.ones_like(angles), angles)  # cos + i*sin


def apply_rope(
    x: torch.Tensor,
    freqs: torch.Tensor,
    start_pos: int = 0,
) -> torch.Tensor:
    """Apply rotary embeddings to query or key tensor.

    The rotation works by treating consecutive pairs of dimensions as
    2D vectors and rotating them:

        [x₂ᵢ, x₂ᵢ₊₁] → [x₂ᵢ·cos(θ) - x₂ᵢ₊₁·sin(θ),
                           x₂ᵢ·sin(θ) + x₂ᵢ₊₁·cos(θ)]

    Implementation trick: reshape to complex numbers, multiply by
    precomputed exp(iθ), then convert back to real. This is mathematically
    equivalent to the rotation above but much faster.

    Args:
        x: (batch, seq_len, n_heads, head_dim) — Q or K tensor
        freqs: precomputed complex frequencies (max_seq_len, head_dim // 2)
        start_pos: offset for KV-cache (during generation, position != 0)
    """
    seq_len = x.shape[1]
    # Slice frequencies for current positions
    freqs = freqs[start_pos : start_pos + seq_len]
    # Reshape x into pairs: (..., head_dim) → (..., head_dim/2, 2) → complex
    x_complex = torch.view_as_complex(x.float().reshape(*x.shape[:-1], -1, 2))
    # Broadcast freqs: (seq_len, head_dim/2) → (1, seq_len, 1, head_dim/2)
    freqs = freqs.unsqueeze(0).unsqueeze(2)
    # Rotate and convert back to real
    x_rotated = torch.view_as_real(x_complex * freqs).flatten(-2)
    return x_rotated.type_as(x)


class CausalSelfAttention(nn.Module):
    """Multi-head self-attention with causal mask and KV-cache.

    Architecture (per head):
        1. Project input to Q, K, V via linear layers (no bias — LLaMA style)
        2. Apply RoPE to Q and K (position encoding via rotation)
        3. Compute attention: softmax(Q·K^T / sqrt(d_k)) · V
        4. Apply causal mask (prevent attending to future tokens)
        5. Project output back to model dimension

    KV-Cache (for efficient generation):
        During autoregressive generation, we only compute Q/K/V for the NEW
        token, but need K/V from ALL previous tokens for attention.
        The KV-cache stores previous K/V values so we don't recompute them.
        This reduces generation from O(n²) to O(n) per token.
    """

    def __init__(self, config: TransformerConfig):
        super().__init__()
        self.n_heads = config.n_heads
        self.head_dim = config.head_dim
        self.dim = config.dim
        self.dropout = config.dropout

        # Q, K, V projections (no bias — LLaMA convention)
        self.wq = nn.Linear(config.dim, config.dim, bias=False)
        self.wk = nn.Linear(config.dim, config.dim, bias=False)
        self.wv = nn.Linear(config.dim, config.dim, bias=False)
        # Output projection
        self.wo = nn.Linear(config.dim, config.dim, bias=False)

        self.attn_dropout = nn.Dropout(config.dropout)
        self.resid_dropout = nn.Dropout(config.dropout)

    def forward(
        self,
        x: torch.Tensor,
        rope_freqs: torch.Tensor,
        start_pos: int = 0,
        kv_cache: tuple[torch.Tensor, torch.Tensor] | None = None,
        mask: torch.Tensor | None = None,
    ) -> tuple[torch.Tensor, tuple[torch.Tensor, torch.Tensor]]:
        """
        Args:
            x: (batch, seq_len, dim)
            rope_freqs: precomputed RoPE frequencies
            start_pos: position offset for KV-cache
            kv_cache: (cached_k, cached_v) from previous steps, or None
            mask: optional attention mask (for causal masking during training)

        Returns:
            output: (batch, seq_len, dim)
            new_kv_cache: (k, v) to be cached for next step
        """
        batch, seq_len, _ = x.shape

        # 1. Linear projections → (batch, seq_len, n_heads, head_dim)
        q = self.wq(x).view(batch, seq_len, self.n_heads, self.head_dim)
        k = self.wk(x).view(batch, seq_len, self.n_heads, self.head_dim)
        v = self.wv(x).view(batch, seq_len, self.n_heads, self.head_dim)

        # 2. Apply RoPE to Q and K (NOT to V — values don't need position info)
        q = apply_rope(q, rope_freqs, start_pos)
        k = apply_rope(k, rope_freqs, start_pos)

        # 3. KV-cache: append new K, V to cached values
        if kv_cache is not None:
            cached_k, cached_v = kv_cache
            k = torch.cat([cached_k, k], dim=1)
            v = torch.cat([cached_v, v], dim=1)
        new_kv_cache = (k, v)

        # 4. Reshape for attention: (batch, n_heads, seq_len, head_dim)
        q = q.transpose(1, 2)
        k = k.transpose(1, 2)
        v = v.transpose(1, 2)

        # 5. Scaled dot-product attention
        # Using PyTorch's optimized SDPA when available (fuses the operation,
        # uses FlashAttention-like memory patterns under the hood)
        kv_len = k.shape[2]  # Total key/value length (may include cache)

        if mask is None and kv_cache is None and seq_len > 1:
            # Training path: use SDPA with is_causal=True (builds mask internally)
            out = F.scaled_dot_product_attention(
                q, k, v,
                dropout_p=self.dropout if self.training else 0.0,
                is_causal=True,
            )
        else:
            # Generation path or custom mask: manual attention
            scale = 1.0 / math.sqrt(self.head_dim)
            scores = torch.matmul(q, k.transpose(-2, -1)) * scale

            if mask is not None:
                scores = scores + mask
            elif seq_len > 1:
                # Build causal mask for multi-token generation with KV-cache
                # Query positions are [start_pos, start_pos+seq_len)
                # Key positions are [0, kv_len)
                # Each query at position i can attend to keys at positions <= i
                causal_mask = torch.full((seq_len, kv_len), float("-inf"), device=q.device)
                for i in range(seq_len):
                    causal_mask[i, : start_pos + i + 1] = 0.0
                scores = scores + causal_mask.unsqueeze(0).unsqueeze(0)

            attn = F.softmax(scores, dim=-1)
            attn = self.attn_dropout(attn)
            out = torch.matmul(attn, v)

        # 6. Reshape back: (batch, seq_len, dim) and project
        out = out.transpose(1, 2).contiguous().view(batch, seq_len, self.dim)
        out = self.wo(out)
        out = self.resid_dropout(out)

        return out, new_kv_cache
