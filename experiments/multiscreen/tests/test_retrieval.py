"""Tests for RetrievalScreener — query vs candidates scorer."""

import torch
import pytest

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from multiscreen.retrieval import RetrievalScreener


class TestRetrievalScreener:
    def test_output_shape(self):
        screener = RetrievalScreener(d_embed=32, d_k=8, n_tiles=4)
        query = torch.randn(2, 32)
        candidates = torch.randn(10, 32)
        scores = screener(query, candidates)
        assert scores.shape == (2, 10)

    def test_scores_in_range(self):
        screener = RetrievalScreener(d_embed=32, d_k=8, n_tiles=4)
        query = torch.randn(3, 32)
        candidates = torch.randn(20, 32)
        scores = screener(query, candidates)
        assert (scores >= 0.0).all()
        assert (scores <= 1.0).all()

    def test_identical_query_candidate_positive_score(self):
        """A candidate identical to the query should score > 0 when projections match."""
        screener = RetrievalScreener(d_embed=16, d_k=8, n_tiles=2)
        screener.s_r.data.fill_(-2.0)  # permissive threshold
        # Share W_q and W_k so identical input → identical projected vectors
        with torch.no_grad():
            for i in range(2):
                screener.W_k[i].weight.copy_(screener.W_q[i].weight)
        query = torch.randn(1, 16)
        candidates = torch.cat([query, torch.randn(5, 16)], dim=0)
        scores = screener(query, candidates)
        assert scores[0, 0].item() > 0.0

    def test_sparsity_with_high_threshold(self):
        """High threshold should produce many exact zeros."""
        screener = RetrievalScreener(d_embed=16, d_k=8, n_tiles=2)
        screener.s_r.data.fill_(4.0)  # very selective
        query = torch.randn(2, 16)
        candidates = torch.randn(50, 16)
        scores = screener(query, candidates)
        zero_frac = (scores == 0.0).float().mean().item()
        assert zero_frac > 0.5, f"Expected >50% zeros, got {zero_frac:.1%}"

    def test_score_and_select(self):
        screener = RetrievalScreener(d_embed=32, d_k=8, n_tiles=4)
        query = torch.randn(1, 32)
        candidates = torch.randn(20, 32)
        top_scores, top_indices = screener.score_and_select(query, candidates, top_k=5)
        assert top_scores.shape == (1, 5)
        assert top_indices.shape == (1, 5)
        # Should be sorted descending
        assert (top_scores[0, :-1] >= top_scores[0, 1:]).all()

    def test_unbatched_query(self):
        screener = RetrievalScreener(d_embed=16, d_k=8, n_tiles=2)
        query = torch.randn(16)  # no batch dim
        candidates = torch.randn(10, 16)
        scores = screener(query, candidates)
        assert scores.shape == (1, 10)

    def test_batched_candidates(self):
        screener = RetrievalScreener(d_embed=16, d_k=8, n_tiles=2)
        query = torch.randn(3, 16)
        candidates = torch.randn(3, 10, 16)  # per-batch candidates
        scores = screener(query, candidates)
        assert scores.shape == (3, 10)

    def test_gradient_flows(self):
        screener = RetrievalScreener(d_embed=16, d_k=8, n_tiles=2)
        query = torch.randn(2, 16, requires_grad=True)
        candidates = torch.randn(10, 16)
        scores = screener(query, candidates)
        scores.sum().backward()
        assert query.grad is not None
        assert screener.s_r.grad is not None
