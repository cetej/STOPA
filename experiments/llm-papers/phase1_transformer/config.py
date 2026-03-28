"""Model configurations — from tiny (CPU-trainable) to medium (8GB GPU).

Configs follow LLaMA conventions: pre-norm, no bias, SwiGLU hidden dim scaling.
"""

from dataclasses import dataclass


@dataclass
class TransformerConfig:
    # Architecture
    n_layers: int = 6
    n_heads: int = 6
    dim: int = 384
    max_seq_len: int = 512
    vocab_size: int = 50257  # GPT-2 BPE tokenizer

    # SwiGLU hidden dim (None = auto-compute using LLaMA 2/3 * 4d formula)
    ffn_hidden_dim: int | None = None

    # Regularization
    dropout: float = 0.1

    # RoPE
    rope_theta: float = 10000.0  # Base frequency for RoPE

    # MoE (Mixture of Experts) — Papers #17, #18, #19
    n_experts: int = 1           # 1 = dense model (no MoE). >1 = MoE
    n_active_experts: int = 1    # How many experts are active per token (top-k)
    moe_aux_loss_coeff: float = 0.01  # Load balancing loss weight

    @property
    def head_dim(self) -> int:
        assert self.dim % self.n_heads == 0
        return self.dim // self.n_heads

    @property
    def n_params(self) -> int:
        """Rough parameter count estimate."""
        # Embedding
        p = self.vocab_size * self.dim
        # Per layer: attention (Q, K, V, O) + FFN (gate, up, down)
        h = self.ffn_hidden_dim or int(2 * (4 * self.dim) / 3)
        h = 256 * ((h + 255) // 256)
        per_layer = 4 * self.dim * self.dim + 3 * self.dim * h
        p += self.n_layers * per_layer
        # Final norm + output head (shared with embedding → don't count twice)
        p += self.dim  # RMSNorm weight
        return p


# === Preset Configs ===

TINY = TransformerConfig(
    n_layers=6, n_heads=6, dim=384, max_seq_len=512, dropout=0.1,
)
# ~15M params — trains in minutes on CPU, seconds on GPU
# Good for: debugging, verifying architecture correctness

SMALL = TransformerConfig(
    n_layers=12, n_heads=12, dim=768, max_seq_len=1024, dropout=0.1,
)
# ~125M params — comparable to GPT-2 Small
# Good for: meaningful text generation, scaling law experiments

MEDIUM = TransformerConfig(
    n_layers=24, n_heads=16, dim=1024, max_seq_len=1024, dropout=0.1,
)
# ~350M params — comparable to GPT-2 Medium
# Good for: quality generation, tight fit on 8GB GPU with mixed precision


TINY_MOE = TransformerConfig(
    n_layers=6, n_heads=6, dim=384, max_seq_len=512, dropout=0.1,
    n_experts=8, n_active_experts=2,
)
# ~85M total params, ~25M active per token
# Same compute as tiny but with 8 expert capacity
# Good for: learning MoE mechanics, upcycling experiments

CONFIGS = {
    "tiny": TINY,
    "small": SMALL,
    "medium": MEDIUM,
    "tiny-moe": TINY_MOE,
}
