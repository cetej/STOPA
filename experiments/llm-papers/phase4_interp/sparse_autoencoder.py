"""Sparse Autoencoder for mechanistic interpretability.

Paper: Templeton et al. (2024) — Scaling Monosemanticity

Architecture:
    x → (x - bias_d) → encoder(W_enc) → ReLU → latents → decoder(W_dec) → + bias_d → x_hat

Loss = reconstruction_loss + λ * sparsity_loss
     = MSE(x, x_hat) + λ * L1(latents)

Design choices:
- Expansion ratio: latent_dim / input_dim (typically 4-32×)
  Higher ratio = more features found, but harder to train
- L1 coefficient (λ): controls sparsity (higher = fewer active latents)
  Too high → dead latents; too low → dense, uninterpretable
- Decoder columns are normalized to unit norm (prevents scale collapse)
- Bias centered on the mean activation (removes the "default" direction)
"""

import torch
import torch.nn as nn
import torch.nn.functional as F


class SparseAutoencoder(nn.Module):
    """Sparse Autoencoder for decomposing neural network activations.

    Args:
        input_dim: Dimension of the input activations (model hidden_dim)
        latent_dim: Number of latent features (typically 4-32× input_dim)
        l1_coeff: L1 sparsity coefficient (controls how sparse latents are)
    """

    def __init__(
        self,
        input_dim: int,
        latent_dim: int = 4096,
        l1_coeff: float = 1e-3,
    ):
        super().__init__()
        self.input_dim = input_dim
        self.latent_dim = latent_dim
        self.l1_coeff = l1_coeff

        # Learnable bias (centered on mean activation)
        self.bias_d = nn.Parameter(torch.zeros(input_dim))

        # Encoder: input_dim → latent_dim
        self.encoder = nn.Linear(input_dim, latent_dim, bias=True)

        # Decoder: latent_dim → input_dim (no bias — bias_d handles it)
        self.decoder = nn.Linear(latent_dim, input_dim, bias=False)

        # Initialize decoder columns to unit norm
        with torch.no_grad():
            self.decoder.weight.data = F.normalize(self.decoder.weight.data, dim=0)

    def forward(self, x: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor, dict]:
        """Forward pass: encode → sparsify → decode.

        Args:
            x: (..., input_dim) — input activations

        Returns:
            x_hat: reconstructed activations
            latents: sparse latent activations
            metrics: loss components
        """
        # Center input
        x_centered = x - self.bias_d

        # Encode → ReLU (sparsity via non-linearity + L1)
        latents = F.relu(self.encoder(x_centered))

        # Decode
        x_hat = self.decoder(latents) + self.bias_d

        # Losses
        reconstruction_loss = F.mse_loss(x_hat, x)
        sparsity_loss = latents.abs().mean()  # L1 on latent activations
        total_loss = reconstruction_loss + self.l1_coeff * sparsity_loss

        # Metrics
        with torch.no_grad():
            n_active = (latents > 0).float().sum(dim=-1).mean().item()
            sparsity = 1.0 - n_active / self.latent_dim

        metrics = {
            "loss": total_loss.item(),
            "recon_loss": reconstruction_loss.item(),
            "sparsity_loss": sparsity_loss.item(),
            "n_active_latents": n_active,
            "sparsity": sparsity,
        }

        return x_hat, latents, metrics

    def get_loss(self, x: torch.Tensor) -> torch.Tensor:
        """Compute total loss for training."""
        x_centered = x - self.bias_d
        latents = F.relu(self.encoder(x_centered))
        x_hat = self.decoder(latents) + self.bias_d
        return F.mse_loss(x_hat, x) + self.l1_coeff * latents.abs().mean()

    @torch.no_grad()
    def normalize_decoder(self):
        """Normalize decoder columns to unit norm.

        Called periodically during training to prevent scale collapse
        (where encoder scales up and decoder scales down).
        """
        self.decoder.weight.data = F.normalize(self.decoder.weight.data, dim=0)

    @torch.no_grad()
    def get_feature_activations(
        self, x: torch.Tensor
    ) -> tuple[torch.Tensor, torch.Tensor]:
        """Get which features activate for given inputs.

        Returns:
            latents: (batch, latent_dim) — activation values
            top_features: (batch, k) — indices of top-k active features
        """
        x_centered = x - self.bias_d
        latents = F.relu(self.encoder(x_centered))
        k = min(10, self.latent_dim)
        _, top_features = latents.topk(k, dim=-1)
        return latents, top_features

    @torch.no_grad()
    def get_feature_direction(self, feature_idx: int) -> torch.Tensor:
        """Get the decoder direction for a specific feature.

        This is the "meaning" of a feature in the original activation space.
        """
        return self.decoder.weight[:, feature_idx]
