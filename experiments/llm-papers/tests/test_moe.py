"""Tests for Mixture of Experts implementation."""

import torch

from phase1_transformer.config import TransformerConfig
from phase1_transformer.model import GPTModel
from phase3_moe.router import TopKRouter
from phase3_moe.moe_layer import MoELayer
from phase3_moe.moe_model import GPTMoEModel
from phase3_moe.upcycle import upcycle_dense_to_moe, verify_upcycling


MOE_CFG = TransformerConfig(
    n_layers=2, n_heads=4, dim=128, max_seq_len=64, dropout=0.0,
    n_experts=4, n_active_experts=2,
)

DENSE_CFG = TransformerConfig(
    n_layers=2, n_heads=4, dim=128, max_seq_len=64, dropout=0.0,
)


class TestRouter:
    def test_output_shapes(self):
        router = TopKRouter(dim=128, n_experts=4, n_active=2)
        x = torch.randn(2, 8, 128)  # batch=2, seq=8
        indices, weights, aux_loss = router(x)
        assert indices.shape == (16, 2)  # 2*8 tokens, top-2
        assert weights.shape == (16, 2)
        assert aux_loss.ndim == 0  # scalar

    def test_weights_sum_to_one(self):
        router = TopKRouter(dim=128, n_experts=4, n_active=2)
        x = torch.randn(1, 4, 128)
        _, weights, _ = router(x)
        sums = weights.sum(dim=-1)
        assert torch.allclose(sums, torch.ones_like(sums), atol=1e-5)

    def test_indices_in_range(self):
        router = TopKRouter(dim=128, n_experts=8, n_active=2)
        x = torch.randn(2, 4, 128)
        indices, _, _ = router(x)
        assert indices.min() >= 0
        assert indices.max() < 8

    def test_aux_loss_positive(self):
        router = TopKRouter(dim=128, n_experts=4, n_active=2)
        x = torch.randn(2, 8, 128)
        _, _, aux_loss = router(x)
        assert aux_loss.item() > 0


class TestMoELayer:
    def test_output_shape(self):
        moe = MoELayer(dim=128, n_experts=4, n_active=2)
        x = torch.randn(2, 8, 128)
        out, aux_loss = moe(x)
        assert out.shape == x.shape

    def test_param_counts(self):
        moe = MoELayer(dim=128, n_experts=8, n_active=2)
        assert moe.total_params > moe.active_params
        # 8 experts total, 2 active → active ≈ 2/8 of expert params + router
        print(f"MoE Layer: {moe.total_params:,} total, {moe.active_params:,} active")


class TestMoEModel:
    def test_forward_pass(self):
        model = GPTMoEModel(MOE_CFG)
        tokens = torch.randint(0, MOE_CFG.vocab_size, (2, 16))
        logits, _, aux_loss = model(tokens)
        assert logits.shape == (2, 16, MOE_CFG.vocab_size)
        assert aux_loss.item() > 0

    def test_param_counts(self):
        model = GPTMoEModel(MOE_CFG)
        params = model.count_parameters()
        assert params["total"] > params["active"]
        print(f"MoE Model: {params['total']:,} total, {params['active']:,} active")


class TestUpcycling:
    def test_upcycle_produces_model(self):
        dense = GPTModel(DENSE_CFG)
        moe = upcycle_dense_to_moe(dense, n_experts=4, n_active=2)
        assert isinstance(moe, GPTMoEModel)

    def test_upcycle_preserves_behavior(self):
        """Upcycled MoE should produce similar outputs to dense model."""
        dense = GPTModel(DENSE_CFG)
        moe = upcycle_dense_to_moe(dense, n_experts=4, n_active=2)
        tokens = torch.randint(0, DENSE_CFG.vocab_size, (1, 16))
        matches = verify_upcycling(dense, moe, tokens, atol=0.5)
        # Tolerance is loose because router weights add some variance
        assert matches, "Upcycled MoE diverges too much from dense model"

    def test_moe_has_more_params(self):
        dense = GPTModel(DENSE_CFG)
        moe = upcycle_dense_to_moe(dense, n_experts=4, n_active=2)
        dense_params = dense.count_parameters()
        moe_params = moe.count_parameters()
        assert moe_params["total"] > dense_params


if __name__ == "__main__":
    import traceback
    test_classes = [TestRouter, TestMoELayer, TestMoEModel, TestUpcycling]
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
