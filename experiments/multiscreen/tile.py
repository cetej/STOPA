"""Gated screening tiles and multi-screen layers."""

import torch
import torch.nn as nn
import torch.nn.functional as F

from .core import ScreeningUnit


class GatedScreeningTile(nn.Module):
    """One screening tile = screening unit + gated output.

    Replaces one attention head + its share of FFN.
    """

    def __init__(
        self,
        d_model: int,
        d_k: int = 16,
        d_v: int = 64,
        use_gate: bool = True,
    ):
        super().__init__()
        self.d_model = d_model
        self.d_k = d_k
        self.d_v = d_v
        self.use_gate = use_gate

        self.W_q = nn.Linear(d_model, d_k, bias=False)
        self.W_k = nn.Linear(d_model, d_k, bias=False)
        self.W_v = nn.Linear(d_model, d_v, bias=False)
        if use_gate:
            self.W_g = nn.Linear(d_model, d_v, bias=False)

        self.screening = ScreeningUnit(d_k, d_v)
        self.W_o = nn.Linear(d_v, d_model, bias=False)
        self.scale = nn.Parameter(torch.tensor(1.0))

    def forward(
        self,
        x: torch.Tensor,
        kv: torch.Tensor | None = None,
        use_distance_mask: bool = True,
        use_causal_mask: bool = True,
        attn_mask: torch.Tensor | None = None,
    ) -> torch.Tensor:
        """
        Args:
            x: (batch, seq_q, d_model) — query source
            kv: (batch, seq_k, d_model) — key/value source (None = self-attention)
            use_distance_mask: positional softmask
            use_causal_mask: causal mask
            attn_mask: optional multiplicative attention mask
        """
        src = kv if kv is not None else x

        q = self.W_q(x)
        k = self.W_k(src)
        v = self.W_v(src)

        u = self.screening(q, k, v, use_distance_mask, use_causal_mask, attn_mask)

        if self.use_gate:
            g = self.W_g(x)
            g_hat = torch.tanh(F.silu(g))
            u = u * g_hat

        return self.W_o(u) * self.scale


class MultiScreenLayer(nn.Module):
    """One Multiscreen layer = N_H parallel screening tiles.

    No separate FFN block — the gated screening tiles subsume it.
    """

    def __init__(
        self,
        d_model: int,
        n_tiles: int,
        d_k: int = 16,
        d_v: int = 64,
        use_gate: bool = True,
    ):
        super().__init__()
        self.tiles = nn.ModuleList(
            [GatedScreeningTile(d_model, d_k, d_v, use_gate) for _ in range(n_tiles)]
        )
        self.norm = nn.LayerNorm(d_model)

    def forward(
        self,
        x: torch.Tensor,
        kv: torch.Tensor | None = None,
        use_distance_mask: bool = True,
        use_causal_mask: bool = True,
        attn_mask: torch.Tensor | None = None,
    ) -> torch.Tensor:
        """Residual connection over sum of all tile outputs."""
        h = self.norm(x)
        tile_sum = sum(
            tile(h, kv, use_distance_mask, use_causal_mask, attn_mask)
            for tile in self.tiles
        )
        return x + tile_sum
