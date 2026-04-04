"""RetrievalScreener — query-vs-candidates relevance scoring using screening.

Unlike attention, retrieval doesn't need:
- Distance softmask (candidates are unordered)
- Causal mask (no temporal dependency)
- Value aggregation (we want scores, not weighted output)

The key insight: screening's exact-zero output for irrelevant items
is perfect for retrieval — it naturally separates relevant from irrelevant
without the softmax "always distribute some probability" problem.
"""

import torch
import torch.nn as nn
import torch.nn.functional as F


class RetrievalScreener(nn.Module):
    """Score query relevance against N candidates using screening mechanism.

    Multi-tile design: each tile has independent Q/K projections and
    learned threshold r. Final score = mean across tiles. This allows
    different tiles to capture different relevance aspects.
    """

    def __init__(self, d_embed: int, d_k: int = 16, n_tiles: int = 4):
        super().__init__()
        self.d_embed = d_embed
        self.d_k = d_k
        self.n_tiles = n_tiles

        # Per-tile projections
        self.W_q = nn.ModuleList(
            [nn.Linear(d_embed, d_k, bias=False) for _ in range(n_tiles)]
        )
        self.W_k = nn.ModuleList(
            [nn.Linear(d_embed, d_k, bias=False) for _ in range(n_tiles)]
        )

        # Per-tile learned thresholds
        self.s_r = nn.Parameter(torch.zeros(n_tiles))

    def _tile_scores(
        self,
        q: torch.Tensor,  # (B, d_k) — projected, L2-normed query
        k: torch.Tensor,  # (N, d_k) or (B, N, d_k) — projected, L2-normed candidates
        tile_idx: int,
    ) -> torch.Tensor:
        """Trim-and-Square relevance for one tile.

        Returns: (B, N) scores in [0, 1]
        """
        r = torch.exp(self.s_r[tile_idx]) + 1.0

        if k.dim() == 2:
            # Shared candidates: (B, d_k) @ (d_k, N) -> (B, N)
            s = torch.mm(q, k.t())
        else:
            # Per-batch candidates: (B, d_k) @ (B, d_k, N) -> (B, N)
            s = torch.bmm(q.unsqueeze(1), k.transpose(-2, -1)).squeeze(1)

        alpha = torch.clamp(1.0 - r * (1.0 - s), min=0.0)
        return alpha.square()

    def forward(
        self,
        query: torch.Tensor,
        candidates: torch.Tensor,
    ) -> torch.Tensor:
        """Score query against candidates.

        Args:
            query: (batch, d_embed) or (d_embed,) — query embedding
            candidates: (N, d_embed) or (batch, N, d_embed) — candidate embeddings

        Returns:
            scores: (batch, N) — relevance scores in [0, 1], many exactly 0
        """
        # Handle unbatched query
        if query.dim() == 1:
            query = query.unsqueeze(0)

        tile_scores = []
        for i in range(self.n_tiles):
            q_proj = F.normalize(self.W_q[i](query), dim=-1)

            if candidates.dim() == 2:
                k_proj = F.normalize(self.W_k[i](candidates), dim=-1)
            else:
                k_proj = F.normalize(self.W_k[i](candidates), dim=-1)

            tile_scores.append(self._tile_scores(q_proj, k_proj, i))

        # Average across tiles
        return torch.stack(tile_scores, dim=0).mean(dim=0)

    def score_and_select(
        self,
        query: torch.Tensor,
        candidates: torch.Tensor,
        top_k: int = 5,
    ) -> tuple[torch.Tensor, torch.Tensor]:
        """Score and return top-k non-zero results.

        Returns:
            scores: (batch, top_k) — top scores (descending)
            indices: (batch, top_k) — indices into candidates
        """
        all_scores = self.forward(query, candidates)

        # Select top-k
        k = min(top_k, all_scores.shape[-1])
        top_scores, top_indices = torch.topk(all_scores, k, dim=-1)

        return top_scores, top_indices

    @property
    def sparsity(self) -> str:
        """Describe current threshold settings."""
        thresholds = []
        for i in range(self.n_tiles):
            r = torch.exp(self.s_r[i]).item() + 1.0
            t = 1.0 - 1.0 / r
            thresholds.append(f"tile{i}: r={r:.2f} (threshold={t:.3f})")
        return ", ".join(thresholds)
