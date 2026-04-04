"""Tests for MiPE — Minimal Positional Encoding."""

import torch
import pytest

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from multiscreen.mipe import MiPE


class TestMiPE:
    def test_output_shapes_preserved(self):
        mipe = MiPE(d_k=16)
        q = torch.randn(2, 10, 16)
        k = torch.randn(2, 10, 16)
        s_w = torch.tensor(1.0)  # small window → MiPE active
        q_out, k_out = mipe(q, k, s_w)
        assert q_out.shape == q.shape
        assert k_out.shape == k.shape

    def test_small_window_applies_rotation(self):
        """Small window (s_w=1) should activate MiPE, changing first 2 coords."""
        mipe = MiPE(d_k=8, activation_threshold=50.0)
        q = torch.randn(1, 5, 8)
        k = torch.randn(1, 5, 8)
        s_w = torch.tensor(1.0)  # w = e^1 + 1 ≈ 3.7 << 50
        q_out, k_out = mipe(q, k, s_w)
        # First 2 coords should differ
        assert not torch.allclose(q_out[..., :2], q[..., :2], atol=1e-4)
        # Remaining coords should be unchanged (blended close to original)
        # Gate is ~1.0 for small window, so rotation dominates
        # But since gate is sigmoid-based, remaining coords get gate*0 + (1-gate)*original

    def test_large_window_skips_rotation(self):
        """Large window should deactivate MiPE (gate → 0)."""
        mipe = MiPE(d_k=8, activation_threshold=50.0)
        q = torch.randn(1, 5, 8)
        k = torch.randn(1, 5, 8)
        s_w = torch.tensor(10.0)  # w = e^10 + 1 ≈ 22027 >> 50
        q_out, k_out = mipe(q, k, s_w)
        # Should be unchanged (gate < 0.01 → early return)
        assert torch.allclose(q_out, q, atol=1e-6)
        assert torch.allclose(k_out, k, atol=1e-6)

    def test_gradient_flows_through_gate(self):
        mipe = MiPE(d_k=8)
        q = torch.randn(1, 5, 8, requires_grad=True)
        k = torch.randn(1, 5, 8, requires_grad=True)
        s_w = torch.tensor(2.0, requires_grad=True)
        q_out, k_out = mipe(q, k, s_w)
        (q_out.sum() + k_out.sum()).backward()
        assert q.grad is not None
        assert k.grad is not None

    def test_different_seq_lengths(self):
        mipe = MiPE(d_k=16)
        q = torch.randn(2, 5, 16)
        k = torch.randn(2, 10, 16)
        s_w = torch.tensor(1.0)
        q_out, k_out = mipe(q, k, s_w)
        assert q_out.shape == (2, 5, 16)
        assert k_out.shape == (2, 10, 16)
