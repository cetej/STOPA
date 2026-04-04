"""Tests for ScreeningAttention — generic MHA replacement."""

import torch
import pytest

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from multiscreen.attention import ScreeningAttention


class TestScreeningAttention:
    def test_self_attention_shape(self):
        attn = ScreeningAttention(d_model=32, num_heads=4, d_k=8)
        x = torch.randn(2, 10, 32)
        out = attn(x, x, x)
        assert out.shape == (2, 10, 32)

    def test_cross_attention_shape(self):
        attn = ScreeningAttention(d_model=32, num_heads=4, d_k=8)
        q = torch.randn(2, 5, 32)
        kv = torch.randn(2, 15, 32)
        out = attn(q, kv, kv)
        assert out.shape == (2, 5, 32)

    def test_causal_mask(self):
        attn = ScreeningAttention(d_model=16, num_heads=2, d_k=8, use_distance_mask=False)
        x = torch.randn(1, 8, 16)
        out_causal = attn(x, x, x, is_causal=True)
        out_noncausal = attn(x, x, x, is_causal=False)
        assert not torch.allclose(out_causal, out_noncausal, atol=1e-4)

    def test_attn_mask_applied(self):
        """Additive -inf mask should block positions."""
        attn = ScreeningAttention(d_model=16, num_heads=2, d_k=8, use_distance_mask=False)
        x = torch.randn(1, 4, 16)
        # Mask out all positions except self
        mask = torch.full((4, 4), float("-inf"))
        mask.fill_diagonal_(0.0)
        out_masked = attn(x, x, x, attn_mask=mask)
        out_unmasked = attn(x, x, x)
        assert not torch.allclose(out_masked, out_unmasked, atol=1e-4)

    def test_no_gate_mode(self):
        attn = ScreeningAttention(d_model=16, num_heads=2, d_k=8, use_gate=False)
        x = torch.randn(2, 6, 16)
        out = attn(x, x, x)
        assert out.shape == (2, 6, 16)

    def test_with_mipe(self):
        attn = ScreeningAttention(d_model=16, num_heads=2, d_k=8, use_mipe=True)
        x = torch.randn(2, 6, 16)
        out = attn(x, x, x)
        assert out.shape == (2, 6, 16)

    def test_gradient_flows_all_params(self):
        attn = ScreeningAttention(d_model=16, num_heads=2, d_k=8)
        x = torch.randn(2, 5, 16, requires_grad=True)
        out = attn(x, x, x)
        out.sum().backward()
        assert x.grad is not None
        for name, p in attn.named_parameters():
            assert p.grad is not None, f"No gradient for {name}"
