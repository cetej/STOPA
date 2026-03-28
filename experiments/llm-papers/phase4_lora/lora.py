"""LoRA Linear Layer — the core building block.

Paper: "LoRA: Low-Rank Adaptation of Large Language Models" (Hu et al., 2021)

Standard linear layer:     y = Wx
LoRA-adapted linear layer: y = Wx + (BA)x = Wx + B(Ax)

Where:
- W ∈ ℝ^(out×in) — original frozen weights
- A ∈ ℝ^(r×in)   — down-projection (trainable), init: Kaiming uniform
- B ∈ ℝ^(out×r)   — up-projection (trainable), init: zeros
- r              — rank (typically 4-64, controls capacity vs efficiency)
- α              — scaling factor (α/r scales the LoRA contribution)

Key design choices:
1. B initialized to ZEROS → at start, LoRA contribution is 0 → model unchanged
2. α/r scaling → allows changing r without retuning learning rate
3. Only applied to attention projections (Q, K, V, O) — FFN left alone
   (empirically, attention adapters capture most task-specific behavior)

Training: freeze W, train only A and B
Inference: merge W' = W + (α/r)BA → single matrix, no overhead
"""

import math

import torch
import torch.nn as nn
import torch.nn.functional as F


class LoRALinear(nn.Module):
    """Linear layer with LoRA adaptation.

    Wraps an existing nn.Linear and adds low-rank trainable matrices.
    The original weight is frozen; only A and B are trained.

    Args:
        original: The original nn.Linear layer to adapt
        rank: LoRA rank (lower = fewer params, higher = more capacity)
        alpha: Scaling factor (default: same as rank)
        dropout: Dropout on LoRA path (regularization)
    """

    def __init__(
        self,
        original: nn.Linear,
        rank: int = 8,
        alpha: float | None = None,
        dropout: float = 0.0,
    ):
        super().__init__()
        self.original = original
        self.rank = rank
        self.alpha = alpha if alpha is not None else float(rank)
        self.scaling = self.alpha / self.rank

        in_features = original.in_features
        out_features = original.out_features

        # Freeze original weights
        self.original.weight.requires_grad = False
        if self.original.bias is not None:
            self.original.bias.requires_grad = False

        # LoRA matrices
        # A: down-projection — Kaiming uniform init (like a normal linear layer)
        self.lora_A = nn.Parameter(torch.empty(rank, in_features))
        nn.init.kaiming_uniform_(self.lora_A, a=math.sqrt(5))

        # B: up-projection — ZERO init (crucial: LoRA starts as identity)
        self.lora_B = nn.Parameter(torch.zeros(out_features, rank))

        # Optional dropout on LoRA path
        self.lora_dropout = nn.Dropout(dropout) if dropout > 0 else nn.Identity()

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """y = Wx + scaling * B(A(dropout(x)))"""
        # Original path (frozen)
        result = self.original(x)

        # LoRA path (trainable)
        lora_out = self.lora_dropout(x)
        lora_out = F.linear(lora_out, self.lora_A)  # x @ A^T → (*, rank)
        lora_out = F.linear(lora_out, self.lora_B)  # → (*, out_features)

        return result + self.scaling * lora_out

    def merge(self) -> nn.Linear:
        """Merge LoRA weights back into the original linear layer.

        W' = W + (α/r) * B @ A

        After merging, the layer is a standard nn.Linear with no overhead.
        This is done for inference — no need for separate A, B matrices.
        """
        merged = nn.Linear(
            self.original.in_features,
            self.original.out_features,
            bias=self.original.bias is not None,
        )
        # W' = W + scaling * B @ A
        delta_w = self.scaling * (self.lora_B @ self.lora_A)
        merged.weight.data = self.original.weight.data + delta_w

        if self.original.bias is not None:
            merged.bias.data = self.original.bias.data.clone()

        return merged

    @property
    def n_trainable(self) -> int:
        """Number of trainable LoRA parameters."""
        return self.lora_A.numel() + self.lora_B.numel()

    @property
    def n_original(self) -> int:
        """Number of original (frozen) parameters."""
        return self.original.weight.numel()

    @property
    def compression_ratio(self) -> float:
        """How much smaller LoRA is vs full fine-tuning."""
        return self.n_original / self.n_trainable
