"""Tests for Speculative Decoding."""

import torch

from phase1_transformer.config import TransformerConfig
from phase1_transformer.model import GPTModel
from phase1_transformer.tokenizer import Tokenizer
from phase4_speculative.speculative import speculative_decode


# Small configs for testing
DRAFT_CFG = TransformerConfig(n_layers=2, n_heads=2, dim=64, max_seq_len=128, dropout=0.0)
TARGET_CFG = TransformerConfig(n_layers=4, n_heads=4, dim=128, max_seq_len=128, dropout=0.0)


class TestSpeculativeDecode:
    def test_produces_output(self):
        """Speculative decoding should generate tokens."""
        draft = GPTModel(DRAFT_CFG)
        target = GPTModel(TARGET_CFG)
        tokenizer = Tokenizer()

        text, stats = speculative_decode(
            target, draft, tokenizer,
            prompt="Hello",
            max_new_tokens=20,
            draft_k=3,
            temperature=1.0,
        )
        assert len(text) > len("Hello")
        assert stats["total_tokens"] > 0

    def test_acceptance_rate_recorded(self):
        """Stats should include acceptance metrics."""
        draft = GPTModel(DRAFT_CFG)
        target = GPTModel(TARGET_CFG)
        tokenizer = Tokenizer()

        _, stats = speculative_decode(
            target, draft, tokenizer,
            prompt="To be",
            max_new_tokens=10,
            draft_k=3,
        )
        assert "acceptance_rate" in stats
        assert "iterations" in stats
        assert stats["acceptance_rate"] >= 0
        assert stats["acceptance_rate"] <= 1

    def test_same_model_high_acceptance(self):
        """When draft = target (same model), acceptance should be ~100%."""
        model = GPTModel(DRAFT_CFG)
        tokenizer = Tokenizer()

        # Use same model as both draft and target
        _, stats = speculative_decode(
            model, model, tokenizer,
            prompt="The",
            max_new_tokens=15,
            draft_k=4,
            temperature=0.001,  # Near-greedy for determinism
        )
        # With near-zero temperature and same model, acceptance should be very high
        assert stats["acceptance_rate"] > 0.5, \
            f"Same model should have high acceptance, got {stats['acceptance_rate']:.2f}"


if __name__ == "__main__":
    import traceback
    test_classes = [TestSpeculativeDecode]
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
