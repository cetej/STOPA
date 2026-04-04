"""Tests for core screening primitives: TanhNorm and ScreeningUnit."""

import torch
import pytest

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from multiscreen.core import TanhNorm, ScreeningUnit


class TestTanhNorm:
    def test_zero_input_gives_zero_output(self):
        norm = TanhNorm()
        h = torch.zeros(2, 4, 8)
        out = norm(h)
        assert torch.allclose(out, torch.zeros_like(out), atol=1e-6)

    def test_output_bounded(self):
        norm = TanhNorm()
        h = torch.randn(4, 10, 32) * 100  # large values
        out = norm(h)
        norms = out.norm(dim=-1)
        assert (norms <= 1.0 + 1e-5).all(), f"Max norm: {norms.max()}"

    def test_preserves_direction(self):
        norm = TanhNorm()
        h = torch.tensor([[3.0, 4.0]])  # norm=5
        out = norm(h)
        # Direction should be preserved: out / ||out|| == h / ||h||
        h_dir = h / h.norm(dim=-1, keepdim=True)
        out_dir = out / out.norm(dim=-1, keepdim=True)
        assert torch.allclose(h_dir, out_dir, atol=1e-5)

    def test_gradient_flows(self):
        norm = TanhNorm()
        h = torch.randn(2, 4, 8, requires_grad=True)
        out = norm(h)
        out.sum().backward()
        assert h.grad is not None
        assert not torch.all(h.grad == 0)


class TestScreeningUnit:
    def test_output_shape(self):
        unit = ScreeningUnit(d_k=16, d_v=32)
        q = torch.randn(2, 10, 16)
        k = torch.randn(2, 10, 16)
        v = torch.randn(2, 10, 32)
        out = unit(q, k, v)
        assert out.shape == (2, 10, 32)

    def test_cross_attention_shape(self):
        """Different seq lengths for q and k."""
        unit = ScreeningUnit(d_k=16, d_v=32)
        q = torch.randn(2, 5, 16)
        k = torch.randn(2, 10, 16)
        v = torch.randn(2, 10, 32)
        out = unit(q, k, v, use_distance_mask=False, use_causal_mask=False)
        assert out.shape == (2, 5, 32)

    def test_sparsity_exists(self):
        """Screening should produce some exact zeros."""
        unit = ScreeningUnit(d_k=16, d_v=32)
        q = torch.randn(4, 20, 16)
        k = torch.randn(4, 20, 16)
        q_n = torch.nn.functional.normalize(q, dim=-1)
        k_n = torch.nn.functional.normalize(k, dim=-1)
        alpha = unit.compute_relevance(q_n, k_n)
        zero_frac = (alpha == 0.0).float().mean().item()
        assert zero_frac > 0.0, "Expected some zero relevance scores"

    def test_causal_mask_enforced(self):
        """Position (i, j) where j > i should have zero contribution."""
        unit = ScreeningUnit(d_k=8, d_v=8)
        # Low threshold so many keys pass through — makes causal mask visible
        unit.s_r.data.fill_(-2.0)  # r ≈ 1.14, very permissive
        unit.s_w.data.fill_(0.0)  # w ≈ 2.0, small window
        x = torch.randn(1, 20, 8)  # longer sequence
        out_causal = unit(x, x, x, use_distance_mask=False, use_causal_mask=True)
        out_no_causal = unit(x, x, x, use_distance_mask=False, use_causal_mask=False)
        assert not torch.allclose(out_causal, out_no_causal, atol=1e-4)

    def test_distance_mask_optional(self):
        unit = ScreeningUnit(d_k=8, d_v=8)
        unit.s_r.data.fill_(-2.0)  # permissive threshold
        unit.s_w.data.fill_(-1.0)  # w ≈ 1.37, very small window
        x = torch.randn(1, 30, 8)  # long enough for window to matter
        out_with = unit(x, x, x, use_distance_mask=True, use_causal_mask=False)
        out_without = unit(x, x, x, use_distance_mask=False, use_causal_mask=False)
        assert not torch.allclose(out_with, out_without, atol=1e-4)

    def test_high_threshold_produces_high_sparsity(self):
        """With very high r, almost all similarities should be below threshold."""
        unit = ScreeningUnit(d_k=8, d_v=8)
        unit.s_r.data.fill_(5.0)  # r = exp(5) + 1 ≈ 149.4, threshold ≈ 0.993
        q = torch.randn(2, 10, 8)
        k = torch.randn(2, 10, 8)
        q_n = torch.nn.functional.normalize(q, dim=-1)
        k_n = torch.nn.functional.normalize(k, dim=-1)
        alpha = unit.compute_relevance(q_n, k_n)
        zero_frac = (alpha == 0.0).float().mean().item()
        assert zero_frac > 0.9, f"Expected >90% zeros with high threshold, got {zero_frac:.1%}"

    def test_gradient_flows(self):
        unit = ScreeningUnit(d_k=8, d_v=8)
        x = torch.randn(2, 5, 8, requires_grad=True)
        out = unit(x, x, x)
        out.sum().backward()
        assert x.grad is not None
        assert unit.s_r.grad is not None
        assert unit.s_w.grad is not None
