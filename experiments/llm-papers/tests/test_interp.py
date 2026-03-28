"""Tests for Sparse Autoencoder (mechanistic interpretability)."""

import torch

from phase4_interp.sparse_autoencoder import SparseAutoencoder


class TestSparseAutoencoder:
    def test_output_shape(self):
        sae = SparseAutoencoder(input_dim=128, latent_dim=512)
        x = torch.randn(32, 128)
        x_hat, latents, metrics = sae(x)
        assert x_hat.shape == x.shape
        assert latents.shape == (32, 512)

    def test_sparsity(self):
        """Latents should be sparse (most values zero due to ReLU + L1)."""
        sae = SparseAutoencoder(input_dim=128, latent_dim=512, l1_coeff=0.1)
        x = torch.randn(100, 128)
        _, latents, metrics = sae(x)
        # With high L1, should have significant sparsity
        assert metrics["sparsity"] > 0.5, f"Expected sparse latents, got sparsity={metrics['sparsity']:.2f}"

    def test_loss_positive(self):
        sae = SparseAutoencoder(input_dim=128, latent_dim=512)
        x = torch.randn(32, 128)
        _, _, metrics = sae(x)
        assert metrics["loss"] > 0
        assert metrics["recon_loss"] > 0

    def test_loss_decreases(self):
        """Loss should decrease after a few training steps."""
        sae = SparseAutoencoder(input_dim=64, latent_dim=256, l1_coeff=1e-4)
        optimizer = torch.optim.Adam(sae.parameters(), lr=1e-3)

        # Fixed data
        x = torch.randn(100, 64)

        # Get initial loss
        loss_before = sae.get_loss(x).item()

        # Train for a few steps
        for _ in range(50):
            optimizer.zero_grad()
            loss = sae.get_loss(x)
            loss.backward()
            optimizer.step()
            sae.normalize_decoder()

        loss_after = sae.get_loss(x).item()
        assert loss_after < loss_before, f"Loss didn't decrease: {loss_before:.4f} → {loss_after:.4f}"

    def test_feature_direction(self):
        sae = SparseAutoencoder(input_dim=128, latent_dim=512)
        direction = sae.get_feature_direction(0)
        assert direction.shape == (128,)

    def test_decoder_normalization(self):
        sae = SparseAutoencoder(input_dim=64, latent_dim=256)
        sae.normalize_decoder()
        # Each column of decoder should have unit norm
        norms = sae.decoder.weight.norm(dim=0)
        assert torch.allclose(norms, torch.ones_like(norms), atol=1e-5)


if __name__ == "__main__":
    import traceback
    test_classes = [TestSparseAutoencoder]
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
