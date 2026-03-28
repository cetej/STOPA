"""Smoke tests for the Transformer implementation.

Tests verify:
1. Tensor shapes are correct through the entire pipeline
2. RMSNorm produces unit-scale outputs
3. RoPE has correct rotational properties
4. Causal mask prevents attending to future tokens
5. KV-cache produces same results as full forward pass
6. Model can generate tokens (even if nonsense before training)
"""

import math

import torch
import torch.nn.functional as F

from phase1_transformer.attention import (
    CausalSelfAttention,
    apply_rope,
    precompute_rope_frequencies,
)
from phase1_transformer.config import TINY, TransformerConfig
from phase1_transformer.layers import RMSNorm, SwiGLU
from phase1_transformer.model import GPTModel
from phase1_transformer.tokenizer import Tokenizer


# Use tiny config for all tests
CFG = TINY


class TestRMSNorm:
    def test_output_shape(self):
        norm = RMSNorm(CFG.dim)
        x = torch.randn(2, 10, CFG.dim)
        out = norm(x)
        assert out.shape == x.shape

    def test_normalization_scale(self):
        """After RMSNorm, RMS of output should be approximately 1."""
        norm = RMSNorm(CFG.dim)
        x = torch.randn(2, 10, CFG.dim) * 5  # Scaled input
        out = norm(x)
        rms = out.pow(2).mean(dim=-1).sqrt()
        # Should be close to 1 (the learned weight is initialized to 1)
        assert torch.allclose(rms, torch.ones_like(rms), atol=0.1)


class TestSwiGLU:
    def test_output_shape(self):
        ffn = SwiGLU(CFG.dim)
        x = torch.randn(2, 10, CFG.dim)
        out = ffn(x)
        assert out.shape == x.shape

    def test_hidden_dim_formula(self):
        """LLaMA formula: 2/3 * 4d, rounded to 256."""
        ffn = SwiGLU(384)
        expected = 256 * ((int(2 * 4 * 384 / 3) + 255) // 256)
        assert ffn.w_gate.out_features == expected


class TestRoPE:
    def test_frequency_shape(self):
        freqs = precompute_rope_frequencies(CFG.head_dim, CFG.max_seq_len)
        assert freqs.shape == (CFG.max_seq_len, CFG.head_dim // 2)

    def test_rotation_preserves_norm(self):
        """RoPE should preserve the L2 norm of vectors (rotation = isometry)."""
        freqs = precompute_rope_frequencies(CFG.head_dim, 128)
        x = torch.randn(1, 32, CFG.n_heads, CFG.head_dim)
        x_rotated = apply_rope(x, freqs)
        # Norms should be preserved
        norm_before = x.norm(dim=-1)
        norm_after = x_rotated.norm(dim=-1)
        assert torch.allclose(norm_before, norm_after, atol=1e-4)

    def test_different_positions_different_rotations(self):
        """Different positions should produce different embeddings."""
        freqs = precompute_rope_frequencies(CFG.head_dim, 128)
        x = torch.ones(1, 2, 1, CFG.head_dim)  # Same vector at pos 0 and 1
        x_rotated = apply_rope(x, freqs)
        # Position 0 and position 1 should differ
        assert not torch.allclose(x_rotated[0, 0], x_rotated[0, 1])


class TestAttention:
    def test_output_shape(self):
        attn = CausalSelfAttention(CFG)
        freqs = precompute_rope_frequencies(CFG.head_dim, CFG.max_seq_len)
        x = torch.randn(2, 16, CFG.dim)
        out, kv_cache = attn(x, freqs)
        assert out.shape == x.shape

    def test_kv_cache_shape(self):
        attn = CausalSelfAttention(CFG)
        freqs = precompute_rope_frequencies(CFG.head_dim, CFG.max_seq_len)
        x = torch.randn(1, 16, CFG.dim)
        _, (k, v) = attn(x, freqs)
        assert k.shape == (1, 16, CFG.n_heads, CFG.head_dim)
        assert v.shape == (1, 16, CFG.n_heads, CFG.head_dim)


class TestGPTModel:
    def test_output_shape(self):
        model = GPTModel(CFG)
        tokens = torch.randint(0, CFG.vocab_size, (2, 32))
        logits, _ = model(tokens)
        assert logits.shape == (2, 32, CFG.vocab_size)

    def test_parameter_count(self):
        model = GPTModel(CFG)
        n_params = model.count_parameters()
        # Tiny model should be roughly 10-20M params
        assert 5_000_000 < n_params < 50_000_000, f"Got {n_params:,}"
        print(f"Tiny model: {n_params:,} parameters")

    def test_generation_without_training(self):
        """Model should generate tokens even without training (random output)."""
        model = GPTModel(CFG)
        model.eval()
        tokens = torch.tensor([[1, 2, 3]])  # Dummy prompt

        # Full forward pass
        logits, kv_caches = model(tokens)
        assert logits.shape == (1, 3, CFG.vocab_size)

        # Generate one more token using KV-cache
        next_token = logits[:, -1:, :].argmax(dim=-1)
        logits2, kv_caches2 = model(next_token, start_pos=3, kv_caches=kv_caches)
        assert logits2.shape == (1, 1, CFG.vocab_size)

    def test_kv_cache_consistency(self):
        """KV-cache generation should produce same logits as full forward pass."""
        model = GPTModel(CFG)
        model.eval()

        tokens = torch.tensor([[10, 20, 30, 40, 50]])

        # Full forward pass (no cache)
        full_logits, _ = model(tokens)

        # Incremental: process first 3 tokens, then 2 more via cache
        logits1, caches = model(tokens[:, :3])
        logits2, _ = model(tokens[:, 3:], start_pos=3, kv_caches=caches)

        # Logits for positions 3,4 should match between full and cached
        assert torch.allclose(full_logits[:, 3:, :], logits2, atol=1e-4), \
            f"Max diff: {(full_logits[:, 3:, :] - logits2).abs().max():.6f}"

    def test_causal_masking(self):
        """Changing a future token should NOT affect logits of earlier tokens."""
        model = GPTModel(CFG)
        model.eval()

        tokens1 = torch.tensor([[10, 20, 30, 40, 50]])
        tokens2 = torch.tensor([[10, 20, 30, 99, 99]])  # Changed last 2 tokens

        logits1, _ = model(tokens1)
        logits2, _ = model(tokens2)

        # Logits at positions 0, 1, 2 should be identical
        # (causal mask means they can't see position 3, 4)
        assert torch.allclose(logits1[:, :3, :], logits2[:, :3, :], atol=1e-5), \
            "Causal mask broken: future tokens affected past logits!"


class TestTokenizer:
    def test_roundtrip(self):
        tok = Tokenizer()
        text = "Hello, world! This is a test."
        encoded = tok.encode(text)
        decoded = tok.decode(encoded)
        assert decoded == text

    def test_vocab_size(self):
        tok = Tokenizer()
        assert tok.vocab_size == 50257  # GPT-2 BPE


if __name__ == "__main__":
    # Simple runner without pytest
    import traceback

    test_classes = [
        TestRMSNorm, TestSwiGLU, TestRoPE,
        TestAttention, TestGPTModel, TestTokenizer,
    ]

    passed = 0
    failed = 0

    for cls in test_classes:
        instance = cls()
        for method_name in dir(instance):
            if not method_name.startswith("test_"):
                continue
            try:
                getattr(instance, method_name)()
                print(f"  PASS  {cls.__name__}.{method_name}")
                passed += 1
            except Exception as e:
                print(f"  FAIL  {cls.__name__}.{method_name}: {e}")
                traceback.print_exc()
                failed += 1

    print(f"\n{'='*40}")
    print(f"Results: {passed} passed, {failed} failed")
