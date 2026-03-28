"""GPT Model — Decoder-only Transformer with LLaMA architecture.

Papers:
- "Attention Is All You Need" (Vaswani et al., 2017) — Transformer architecture
- "LLaMA: Open and Efficient Foundation LMs" (Touvron et al., 2023) — Modern defaults

Architecture decisions (LLaMA-style):
- Pre-norm: RMSNorm BEFORE attention/FFN (not after, like original Transformer)
  Why? Pre-norm is more stable during training, especially for deep models.
- No bias in linear layers: empirically equivalent quality, fewer parameters
- Weight tying: embedding matrix = output projection (saves ~vocab_size * dim params)
- SwiGLU activation: gated FFN outperforms ReLU at same parameter count
- RoPE: rotary position encoding instead of learned/sinusoidal embeddings
"""

import torch
import torch.nn as nn

from .attention import CausalSelfAttention, precompute_rope_frequencies
from .config import TransformerConfig
from .layers import RMSNorm, SwiGLU


class TransformerBlock(nn.Module):
    """Single Transformer decoder block.

    Data flow (pre-norm residual):
        x → RMSNorm → Attention → + residual
          → RMSNorm → SwiGLU FFN → + residual

    Pre-norm means we normalize BEFORE the sublayer, then add the residual.
    This is more stable than post-norm (original Transformer) because the
    residual stream stays "clean" — gradients flow through without being
    squeezed through normalization layers.
    """

    def __init__(self, config: TransformerConfig):
        super().__init__()
        self.attention = CausalSelfAttention(config)
        self.ffn = SwiGLU(config.dim, config.ffn_hidden_dim)
        self.norm1 = RMSNorm(config.dim)  # Pre-attention norm
        self.norm2 = RMSNorm(config.dim)  # Pre-FFN norm

    def forward(
        self,
        x: torch.Tensor,
        rope_freqs: torch.Tensor,
        start_pos: int = 0,
        kv_cache: tuple[torch.Tensor, torch.Tensor] | None = None,
        mask: torch.Tensor | None = None,
    ) -> tuple[torch.Tensor, tuple[torch.Tensor, torch.Tensor]]:
        # Attention with pre-norm and residual
        residual = x
        x = self.norm1(x)
        attn_out, new_kv_cache = self.attention(x, rope_freqs, start_pos, kv_cache, mask)
        x = residual + attn_out

        # FFN with pre-norm and residual
        residual = x
        x = residual + self.ffn(self.norm2(x))

        return x, new_kv_cache


class GPTModel(nn.Module):
    """Decoder-only GPT model with LLaMA architecture.

    Full architecture:
        Token IDs → Embedding (no positional embedding — RoPE handles position)
                  → Dropout
                  → N × TransformerBlock (each with attention + FFN)
                  → RMSNorm (final)
                  → Linear head → logits over vocabulary

    Weight tying: The embedding matrix and output projection share weights.
    This works because both map between the same spaces (token ↔ hidden state).
    Saves significant memory for large vocabularies.
    """

    def __init__(self, config: TransformerConfig):
        super().__init__()
        self.config = config

        # Token embedding (NO positional embedding — RoPE is applied in attention)
        self.tok_emb = nn.Embedding(config.vocab_size, config.dim)
        self.dropout = nn.Dropout(config.dropout)

        # Transformer blocks
        self.layers = nn.ModuleList([
            TransformerBlock(config) for _ in range(config.n_layers)
        ])

        # Final normalization before output projection
        self.norm = RMSNorm(config.dim)

        # Output head: hidden state → logits over vocabulary
        self.output = nn.Linear(config.dim, config.vocab_size, bias=False)

        # Weight tying: share embedding and output projection weights
        self.output.weight = self.tok_emb.weight

        # Precompute RoPE frequencies (stored as buffer — not a parameter)
        rope_freqs = precompute_rope_frequencies(
            config.head_dim, config.max_seq_len * 2, config.rope_theta
        )
        self.register_buffer("rope_freqs", rope_freqs, persistent=False)

        # Initialize weights
        self.apply(self._init_weights)

    def _init_weights(self, module: nn.Module) -> None:
        """Xavier/Kaiming-style initialization.

        Linear layers: normal(0, 0.02) — standard GPT initialization.
        Embeddings: normal(0, 0.02).
        Output projection gets scaled by 1/sqrt(2*n_layers) to prevent
        residual stream from growing too large in deep models.
        """
        if isinstance(module, nn.Linear):
            torch.nn.init.normal_(module.weight, mean=0.0, std=0.02)
            if module.bias is not None:
                torch.nn.init.zeros_(module.bias)
        elif isinstance(module, nn.Embedding):
            torch.nn.init.normal_(module.weight, mean=0.0, std=0.02)

    def forward(
        self,
        tokens: torch.Tensor,
        start_pos: int = 0,
        kv_caches: list[tuple[torch.Tensor, torch.Tensor]] | None = None,
    ) -> tuple[torch.Tensor, list[tuple[torch.Tensor, torch.Tensor]]]:
        """
        Args:
            tokens: (batch, seq_len) — token IDs
            start_pos: position offset for KV-cache during generation
            kv_caches: list of (k, v) caches per layer, or None for training

        Returns:
            logits: (batch, seq_len, vocab_size)
            new_kv_caches: updated KV-caches for generation
        """
        batch, seq_len = tokens.shape

        # Embed tokens (no positional encoding — RoPE handles it in attention)
        x = self.tok_emb(tokens)
        x = self.dropout(x)

        # Pass through transformer blocks
        new_kv_caches = []
        for i, layer in enumerate(self.layers):
            cache = kv_caches[i] if kv_caches is not None else None
            x, new_cache = layer(x, self.rope_freqs, start_pos, cache)
            new_kv_caches.append(new_cache)

        # Final norm + output projection
        x = self.norm(x)
        logits = self.output(x)

        return logits, new_kv_caches

    def count_parameters(self) -> int:
        """Count trainable parameters."""
        return sum(p.numel() for p in self.parameters() if p.requires_grad)

    @torch.no_grad()
    def estimate_memory_mb(self, batch_size: int = 1, seq_len: int | None = None) -> dict[str, float]:
        """Estimate GPU memory usage in MB."""
        seq_len = seq_len or self.config.max_seq_len
        param_mb = self.count_parameters() * 4 / 1024 / 1024  # fp32
        # Activations: rough estimate — ~2x params for forward, ~4x for backward
        act_mb = param_mb * 2 * batch_size * seq_len / self.config.max_seq_len
        return {
            "parameters_mb": round(param_mb, 1),
            "activations_est_mb": round(act_mb, 1),
            "total_est_mb": round(param_mb + act_mb, 1),
        }
