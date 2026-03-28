"""MoE GPT Model — Transformer with Mixture of Experts layers.

Extends the Phase 1 GPT model by replacing dense FFN layers with MoE layers.
Shares all other components (attention, embeddings, norms) with the dense model.

Key differences from dense model:
1. FFN → MoE FFN (N experts, top-k routing)
2. Additional auxiliary loss for load balancing
3. Total params >> active params (sparse computation)

Can be initialized from scratch or via Sparse Upcycling (see upcycle.py).
"""

import torch
import torch.nn as nn

from phase1_transformer.attention import CausalSelfAttention, precompute_rope_frequencies
from phase1_transformer.config import TransformerConfig
from phase1_transformer.layers import RMSNorm

from .moe_layer import MoELayer


class MoETransformerBlock(nn.Module):
    """Transformer block with MoE FFN.

    Data flow:
        x → RMSNorm → Attention → + residual
          → RMSNorm → MoE FFN   → + residual + aux_loss
    """

    def __init__(self, config: TransformerConfig):
        super().__init__()
        self.attention = CausalSelfAttention(config)
        self.moe = MoELayer(
            dim=config.dim,
            n_experts=config.n_experts,
            n_active=config.n_active_experts,
            ffn_hidden_dim=config.ffn_hidden_dim,
        )
        self.norm1 = RMSNorm(config.dim)
        self.norm2 = RMSNorm(config.dim)

    def forward(
        self,
        x: torch.Tensor,
        rope_freqs: torch.Tensor,
        start_pos: int = 0,
        kv_cache: tuple[torch.Tensor, torch.Tensor] | None = None,
        mask: torch.Tensor | None = None,
    ) -> tuple[torch.Tensor, tuple[torch.Tensor, torch.Tensor], torch.Tensor]:
        """Returns (output, kv_cache, aux_loss)."""
        # Attention
        residual = x
        x = self.norm1(x)
        attn_out, new_kv_cache = self.attention(x, rope_freqs, start_pos, kv_cache, mask)
        x = residual + attn_out

        # MoE FFN
        residual = x
        moe_out, aux_loss = self.moe(self.norm2(x))
        x = residual + moe_out

        return x, new_kv_cache, aux_loss


class GPTMoEModel(nn.Module):
    """GPT model with Mixture of Experts layers.

    Architecture identical to Phase 1 GPTModel except:
    - TransformerBlock → MoETransformerBlock (MoE FFN instead of dense)
    - Forward pass returns auxiliary loss alongside logits
    - Parameter counting distinguishes total vs active params

    Comparison (tiny config):
        Dense:  ~30M total, ~30M active
        MoE-8:  ~85M total, ~25M active (8 experts, 2 active)
        → MoE has 3x capacity but same compute cost!
    """

    def __init__(self, config: TransformerConfig):
        super().__init__()
        self.config = config

        # Token embedding (same as dense)
        self.tok_emb = nn.Embedding(config.vocab_size, config.dim)
        self.dropout = nn.Dropout(config.dropout)

        # MoE Transformer blocks
        self.layers = nn.ModuleList([
            MoETransformerBlock(config) for _ in range(config.n_layers)
        ])

        # Final norm + output head (same as dense)
        self.norm = RMSNorm(config.dim)
        self.output = nn.Linear(config.vocab_size, config.dim, bias=False)
        # Fix: output should be (dim → vocab_size), not the reverse
        self.output = nn.Linear(config.dim, config.vocab_size, bias=False)
        self.output.weight = self.tok_emb.weight  # Weight tying

        # Precompute RoPE
        rope_freqs = precompute_rope_frequencies(
            config.head_dim, config.max_seq_len * 2, config.rope_theta
        )
        self.register_buffer("rope_freqs", rope_freqs, persistent=False)

        self.apply(self._init_weights)

    def _init_weights(self, module: nn.Module) -> None:
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
    ) -> tuple[torch.Tensor, list[tuple[torch.Tensor, torch.Tensor]], torch.Tensor]:
        """
        Returns:
            logits: (batch, seq_len, vocab_size)
            kv_caches: updated KV caches
            total_aux_loss: sum of all layer auxiliary losses
        """
        batch, seq_len = tokens.shape

        x = self.tok_emb(tokens)
        x = self.dropout(x)

        new_kv_caches = []
        total_aux_loss = torch.tensor(0.0, device=tokens.device)

        for i, layer in enumerate(self.layers):
            cache = kv_caches[i] if kv_caches is not None else None
            x, new_cache, aux_loss = layer(x, self.rope_freqs, start_pos, cache)
            new_kv_caches.append(new_cache)
            total_aux_loss = total_aux_loss + aux_loss

        x = self.norm(x)
        logits = self.output(x)

        return logits, new_kv_caches, total_aux_loss

    def count_parameters(self) -> dict[str, int]:
        """Count total and active parameters."""
        total = sum(p.numel() for p in self.parameters() if p.requires_grad)

        # Active params: embedding + attention + norms + k/N of expert params + router
        expert_total = sum(
            sum(p.numel() for p in layer.moe.experts.parameters())
            for layer in self.layers
        )
        # Each expert has expert_total / (n_layers * n_experts) params
        # Active: n_active experts per layer
        expert_per_one = expert_total / (self.config.n_layers * self.config.n_experts)
        active_expert = expert_per_one * self.config.n_active_experts * self.config.n_layers

        non_expert = total - expert_total
        active = int(non_expert + active_expert)

        return {"total": total, "active": active}
