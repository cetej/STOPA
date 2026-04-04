"""MiPE — Minimal Positional Encoding from arXiv:2604.01178.

RoPE applied only to the first 2 coordinates of Q, K.
Activated only when the learned window w is below a threshold (smooth gate).
"""

import math

import torch
import torch.nn as nn


class MiPE(nn.Module):
    """Minimal Positional Encoding.

    When the screening unit's learned window is small (local attention),
    positional encoding is needed. When the window is large (global),
    positional encoding is unnecessary and potentially harmful.

    Uses a smooth sigmoid gate to transition between active/inactive.
    """

    def __init__(
        self,
        d_k: int,
        max_seq_len: int = 8192,
        base: float = 10000.0,
        activation_threshold: float = 50.0,
    ):
        super().__init__()
        self.d_k = d_k
        self.activation_threshold = activation_threshold

        # Precompute RoPE frequencies for first 2 coordinates only
        # theta_0 = base^(-0/d_k), theta_1 = base^(-2/d_k)
        freqs = 1.0 / (base ** (torch.arange(0, 2, 2).float() / d_k))
        positions = torch.arange(max_seq_len).float()
        # angles: (max_seq_len, 1)
        angles = torch.outer(positions, freqs)

        self.register_buffer("cos_cached", angles.cos())  # (max_seq_len, 1)
        self.register_buffer("sin_cached", angles.sin())  # (max_seq_len, 1)

    def _apply_rope_2d(
        self, x: torch.Tensor, seq_len: int
    ) -> torch.Tensor:
        """Apply RoPE rotation to first 2 coordinates of x.

        Args:
            x: (batch, seq, d_k)
            seq_len: actual sequence length

        Returns:
            x with first 2 coords rotated by position-dependent angle
        """
        cos = self.cos_cached[:seq_len]  # (seq, 1)
        sin = self.sin_cached[:seq_len]  # (seq, 1)

        # Extract first 2 coords
        x0 = x[..., 0:1]  # (B, T, 1)
        x1 = x[..., 1:2]  # (B, T, 1)

        # 2D rotation
        x0_rot = x0 * cos - x1 * sin
        x1_rot = x0 * sin + x1 * cos

        # Replace first 2 coords, keep rest unchanged
        if x.shape[-1] > 2:
            return torch.cat([x0_rot, x1_rot, x[..., 2:]], dim=-1)
        return torch.cat([x0_rot, x1_rot], dim=-1)

    def forward(
        self,
        q: torch.Tensor,
        k: torch.Tensor,
        s_w: torch.Tensor,
    ) -> tuple[torch.Tensor, torch.Tensor]:
        """Apply MiPE conditionally based on learned window width.

        Args:
            q: (batch, seq_q, d_k) — queries
            k: (batch, seq_k, d_k) — keys
            s_w: scalar — the ScreeningUnit's learned log-window parameter

        Returns:
            (q_out, k_out) with optional positional encoding applied
        """
        w = torch.exp(s_w) + 1.0

        # Smooth gate: active when window is small, inactive when large
        gate = torch.sigmoid(self.activation_threshold - w)

        if gate.item() < 0.01:
            # Nearly inactive — skip computation
            return q, k

        q_rot = self._apply_rope_2d(q, q.shape[1])
        k_rot = self._apply_rope_2d(k, k.shape[1])

        # Blend: gate * rotated + (1 - gate) * original
        q_out = gate * q_rot + (1.0 - gate) * q
        k_out = gate * k_rot + (1.0 - gate) * k

        return q_out, k_out
