"""Building blocks: RMSNorm and SwiGLU FFN.

Papers:
- RMSNorm: "Root Mean Square Layer Normalization" (Zhang & Sennrich, 2019)
  Used in LLaMA instead of LayerNorm — simpler, no mean centering, no bias.
- SwiGLU: "GLU Variants Improve Transformer" (Shazeer, 2020)
  Used in LLaMA instead of ReLU FFN — gated activation with SiLU (Swish).
"""

import torch
import torch.nn as nn
import torch.nn.functional as F


class RMSNorm(nn.Module):
    """Root Mean Square Layer Normalization.

    Why RMSNorm over LayerNorm?
    - LayerNorm: y = (x - mean) / std * gamma + beta  (re-centering + re-scaling)
    - RMSNorm:   y = x / RMS(x) * gamma               (re-scaling only)

    Empirically, the re-centering (mean subtraction) in LayerNorm contributes
    little to performance, but adds compute. RMSNorm drops it, saving ~10-15%
    of the normalization cost with equivalent quality.

    LLaMA, Mistral, Qwen all use RMSNorm as the default.
    """

    def __init__(self, dim: int, eps: float = 1e-6):
        super().__init__()
        self.eps = eps
        self.weight = nn.Parameter(torch.ones(dim))  # gamma (learnable scale)
        # No bias (beta) — this is the key simplification

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        # RMS(x) = sqrt(mean(x^2))
        # We compute x * rsqrt(mean(x^2) + eps) for numerical stability
        rms = torch.rsqrt(x.pow(2).mean(dim=-1, keepdim=True) + self.eps)
        return x * rms * self.weight


class SwiGLU(nn.Module):
    """SwiGLU Feed-Forward Network.

    Why SwiGLU over standard ReLU FFN?

    Standard Transformer FFN:
        FFN(x) = ReLU(xW₁ + b₁)W₂ + b₂

    SwiGLU (what LLaMA uses):
        SwiGLU(x) = (SiLU(xW_gate) ⊙ xW_up) W_down

    The key difference is the GATING mechanism: instead of a single linear
    projection followed by ReLU, SwiGLU uses two parallel projections where
    one acts as a "gate" (through SiLU activation) that modulates the other.

    This gives the network more expressive control over information flow.
    Empirically, SwiGLU consistently outperforms ReLU and GELU FFNs at the
    same parameter count.

    Note: SwiGLU has 3 weight matrices instead of 2, so for the same hidden_dim,
    it has 50% more parameters. LLaMA compensates by using hidden_dim = 2/3 * 4d
    (≈ 2.67d) instead of the standard 4d, keeping total params roughly equal.

    Args:
        dim: Model dimension (input/output size)
        hidden_dim: Inner FFN dimension. If None, uses 2/3 * 4 * dim rounded
                     to nearest multiple of 256 (LLaMA convention).
    """

    def __init__(self, dim: int, hidden_dim: int | None = None):
        super().__init__()
        if hidden_dim is None:
            # LLaMA formula: 2/3 of the standard 4x expansion, rounded to multiple of 256
            hidden_dim = int(2 * (4 * dim) / 3)
            hidden_dim = 256 * ((hidden_dim + 255) // 256)

        self.w_gate = nn.Linear(dim, hidden_dim, bias=False)  # Gate projection
        self.w_up = nn.Linear(dim, hidden_dim, bias=False)    # Up projection
        self.w_down = nn.Linear(hidden_dim, dim, bias=False)  # Down projection

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        # SiLU(xW_gate) ⊙ xW_up — element-wise gating
        return self.w_down(F.silu(self.w_gate(x)) * self.w_up(x))
