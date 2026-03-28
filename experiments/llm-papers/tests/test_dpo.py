"""Tests for DPO implementation."""

import torch

from phase3_dpo.dpo_loss import compute_log_probs, dpo_loss


class TestLogProbs:
    def test_output_shape(self):
        logits = torch.randn(2, 10, 100)  # batch=2, seq=10, vocab=100
        labels = torch.randint(0, 100, (2, 10))
        log_probs = compute_log_probs(logits, labels)
        assert log_probs.shape == (2,)  # one value per sequence

    def test_log_probs_negative(self):
        """Log probabilities should be negative (probs < 1)."""
        logits = torch.randn(2, 10, 100)
        labels = torch.randint(0, 100, (2, 10))
        log_probs = compute_log_probs(logits, labels)
        assert (log_probs < 0).all()

    def test_mask_zeros_out_padding(self):
        """Masked positions should not contribute to log probs."""
        logits = torch.randn(1, 5, 100)
        labels = torch.randint(0, 100, (1, 5))
        mask_full = torch.ones(1, 5)
        mask_half = torch.tensor([[1.0, 1.0, 1.0, 0.0, 0.0]])

        lp_full = compute_log_probs(logits, labels, mask_full)
        lp_half = compute_log_probs(logits, labels, mask_half)
        # Half mask should give higher (less negative) log probs
        assert lp_half.item() > lp_full.item()


class TestDPOLoss:
    def test_loss_is_scalar(self):
        B, S, V = 2, 10, 100
        loss, metrics = dpo_loss(
            policy_chosen_logits=torch.randn(B, S, V),
            policy_rejected_logits=torch.randn(B, S, V),
            ref_chosen_logits=torch.randn(B, S, V),
            ref_rejected_logits=torch.randn(B, S, V),
            chosen_labels=torch.randint(0, V, (B, S)),
            rejected_labels=torch.randint(0, V, (B, S)),
        )
        assert loss.ndim == 0  # scalar
        assert loss.item() > 0  # DPO loss is always positive

    def test_metrics_keys(self):
        B, S, V = 2, 10, 100
        _, metrics = dpo_loss(
            policy_chosen_logits=torch.randn(B, S, V),
            policy_rejected_logits=torch.randn(B, S, V),
            ref_chosen_logits=torch.randn(B, S, V),
            ref_rejected_logits=torch.randn(B, S, V),
            chosen_labels=torch.randint(0, V, (B, S)),
            rejected_labels=torch.randint(0, V, (B, S)),
        )
        assert "loss" in metrics
        assert "reward_margin" in metrics
        assert "accuracy" in metrics

    def test_gradient_flows(self):
        """DPO loss should produce gradients for the policy model."""
        B, S, V = 2, 8, 50
        policy_chosen = torch.randn(B, S, V, requires_grad=True)
        policy_rejected = torch.randn(B, S, V, requires_grad=True)

        loss, _ = dpo_loss(
            policy_chosen_logits=policy_chosen,
            policy_rejected_logits=policy_rejected,
            ref_chosen_logits=torch.randn(B, S, V),
            ref_rejected_logits=torch.randn(B, S, V),
            chosen_labels=torch.randint(0, V, (B, S)),
            rejected_labels=torch.randint(0, V, (B, S)),
        )
        loss.backward()
        assert policy_chosen.grad is not None
        assert policy_rejected.grad is not None

    def test_perfect_separation(self):
        """When policy strongly prefers chosen, loss should be low."""
        B, S, V = 4, 10, 50
        labels = torch.randint(0, V, (B, S))

        # Policy: high logits for chosen labels
        chosen_logits = torch.zeros(B, S, V)
        chosen_logits.scatter_(2, labels.unsqueeze(-1), 10.0)  # High prob for correct tokens

        # Policy: low logits for rejected labels
        rejected_logits = torch.randn(B, S, V) * 0.1  # Near uniform

        # Reference: same for both (no preference)
        ref_logits = torch.randn(B, S, V) * 0.1

        loss, metrics = dpo_loss(
            chosen_logits, rejected_logits,
            ref_logits, ref_logits,
            labels, labels,
        )
        # When policy clearly prefers chosen, accuracy should be high
        assert metrics["accuracy"] > 0.5


if __name__ == "__main__":
    import traceback
    test_classes = [TestLogProbs, TestDPOLoss]
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
