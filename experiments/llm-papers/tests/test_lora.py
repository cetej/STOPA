"""Tests for LoRA implementation."""

import torch
import torch.nn as nn

from phase1_transformer.config import TINY, TransformerConfig
from phase1_transformer.model import GPTModel
from phase4_lora.lora import LoRALinear
from phase4_lora.apply_lora import apply_lora, merge_lora, get_lora_state_dict


SMALL_CFG = TransformerConfig(n_layers=2, n_heads=4, dim=128, max_seq_len=64, dropout=0.0)


class TestLoRALinear:
    def test_output_shape(self):
        original = nn.Linear(128, 256, bias=False)
        lora = LoRALinear(original, rank=8)
        x = torch.randn(2, 10, 128)
        out = lora(x)
        assert out.shape == (2, 10, 256)

    def test_zero_init(self):
        """At initialization, LoRA should not change the output (B=0)."""
        original = nn.Linear(128, 256, bias=False)
        lora = LoRALinear(original, rank=8)
        x = torch.randn(2, 10, 128)
        original_out = original(x)
        lora_out = lora(x)
        assert torch.allclose(original_out, lora_out, atol=1e-6), \
            "LoRA should start as identity (B initialized to zeros)"

    def test_trainable_params(self):
        original = nn.Linear(768, 768, bias=False)
        lora = LoRALinear(original, rank=8)
        assert lora.n_trainable == 8 * 768 * 2  # A + B
        assert lora.compression_ratio > 40  # 768*768 / (8*768*2) ≈ 48

    def test_merge_correctness(self):
        """Merged linear should produce same output as LoRA linear."""
        original = nn.Linear(64, 64, bias=False)
        lora = LoRALinear(original, rank=4)
        # Perturb B so LoRA has effect
        lora.lora_B.data.normal_(std=0.1)

        x = torch.randn(1, 5, 64)
        lora_out = lora(x)
        merged = lora.merge()
        merged_out = merged(x)
        assert torch.allclose(lora_out, merged_out, atol=1e-5)

    def test_gradient_only_on_lora(self):
        """Gradients should only flow to LoRA params, not original."""
        original = nn.Linear(64, 64, bias=False)
        lora = LoRALinear(original, rank=4)
        x = torch.randn(1, 5, 64)
        out = lora(x)
        out.sum().backward()
        assert lora.lora_A.grad is not None
        assert lora.lora_B.grad is not None
        assert original.weight.grad is None  # Frozen!


class TestApplyLoRA:
    def test_apply_and_count(self):
        model = GPTModel(SMALL_CFG)
        total_before = sum(p.numel() for p in model.parameters())
        model = apply_lora(model, rank=4)
        trainable = sum(p.numel() for p in model.parameters() if p.requires_grad)
        # Should be much less than total
        assert trainable < total_before * 0.1  # < 10% of total

    def test_forward_after_lora(self):
        model = GPTModel(SMALL_CFG)
        model = apply_lora(model, rank=4)
        tokens = torch.randint(0, SMALL_CFG.vocab_size, (1, 16))
        logits, _ = model(tokens)
        assert logits.shape == (1, 16, SMALL_CFG.vocab_size)

    def test_merge_and_compare(self):
        """After merge, model should produce same output without LoRA modules."""
        model = GPTModel(SMALL_CFG)
        tokens = torch.randint(0, SMALL_CFG.vocab_size, (1, 16))

        # Apply LoRA and get output
        model = apply_lora(model, rank=4)
        with torch.no_grad():
            lora_logits, _ = model(tokens)

        # Merge and get output
        model = merge_lora(model)
        with torch.no_grad():
            merged_logits, _ = model(tokens)

        assert torch.allclose(lora_logits, merged_logits, atol=1e-4)

    def test_lora_state_dict_small(self):
        model = GPTModel(SMALL_CFG)
        model = apply_lora(model, rank=4)
        state = get_lora_state_dict(model)
        # Should have entries for A and B per adapted layer
        assert len(state) > 0
        total_lora_params = sum(v.numel() for v in state.values())
        total_model_params = sum(p.numel() for p in model.parameters())
        assert total_lora_params < total_model_params * 0.05


if __name__ == "__main__":
    import traceback
    test_classes = [TestLoRALinear, TestApplyLoRA]
    passed = 0
    failed = 0
    for cls in test_classes:
        instance = cls()
        for method_name in sorted(dir(instance)):
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
