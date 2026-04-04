"""Language models for benchmarking: MultiScreenLM and TransformerLM."""

import math

import torch
import torch.nn as nn
import torch.nn.functional as F

from .tile import MultiScreenLayer


class MultiScreenLM(nn.Module):
    """Multiscreen Language Model for comparison experiments.

    Architecture: Embedding -> N_L MultiScreen layers -> LM head
    Unified scaling: N_L = N_H = Psi, d_model = Psi^2
    """

    def __init__(
        self,
        vocab_size: int,
        psi: int = 4,
        d_k: int = 16,
        d_v: int = 64,
        max_seq_len: int = 512,
    ):
        super().__init__()
        self.d_model = psi * psi
        n_layers = psi
        n_tiles = psi

        self.embedding = nn.Embedding(vocab_size, self.d_model)
        self.layers = nn.ModuleList(
            [MultiScreenLayer(self.d_model, n_tiles, d_k, d_v) for _ in range(n_layers)]
        )
        self.norm_out = nn.LayerNorm(self.d_model)
        self.lm_head = nn.Linear(self.d_model, vocab_size, bias=False)
        self.lm_head.weight = self.embedding.weight

        self._init_weights()

    def _init_weights(self):
        for p in self.parameters():
            if p.dim() > 1:
                nn.init.normal_(p, std=0.02)

    def forward(
        self, input_ids: torch.Tensor, targets: torch.Tensor | None = None
    ) -> tuple[torch.Tensor, torch.Tensor | None]:
        x = self.embedding(input_ids)
        for layer in self.layers:
            x = layer(x)
        x = self.norm_out(x)
        logits = self.lm_head(x)

        loss = None
        if targets is not None:
            loss = F.cross_entropy(
                logits.reshape(-1, logits.size(-1)), targets.reshape(-1)
            )
        return logits, loss


# --- Standard Transformer baseline ---

class StandardAttention(nn.Module):
    """Standard multi-head causal self-attention for baseline."""

    def __init__(self, d_model: int, n_heads: int):
        super().__init__()
        self.n_heads = n_heads
        self.d_head = d_model // n_heads
        self.W_qkv = nn.Linear(d_model, 3 * d_model, bias=False)
        self.W_o = nn.Linear(d_model, d_model, bias=False)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        B, T, C = x.shape
        qkv = self.W_qkv(x).reshape(B, T, 3, self.n_heads, self.d_head)
        qkv = qkv.permute(2, 0, 3, 1, 4)
        q, k, v = qkv[0], qkv[1], qkv[2]

        scale = 1.0 / math.sqrt(self.d_head)
        attn = torch.matmul(q, k.transpose(-2, -1)) * scale
        causal_mask = torch.tril(torch.ones(T, T, device=x.device))
        attn = attn.masked_fill(causal_mask == 0, float("-inf"))
        attn = F.softmax(attn, dim=-1)
        out = torch.matmul(attn, v)

        out = out.transpose(1, 2).reshape(B, T, C)
        return self.W_o(out)


class TransformerBlock(nn.Module):
    """Standard Transformer block: attention + FFN."""

    def __init__(self, d_model: int, n_heads: int, ffn_mult: int = 4):
        super().__init__()
        self.norm1 = nn.LayerNorm(d_model)
        self.attn = StandardAttention(d_model, n_heads)
        self.norm2 = nn.LayerNorm(d_model)
        self.ffn = nn.Sequential(
            nn.Linear(d_model, d_model * ffn_mult, bias=False),
            nn.GELU(),
            nn.Linear(d_model * ffn_mult, d_model, bias=False),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = x + self.attn(self.norm1(x))
        x = x + self.ffn(self.norm2(x))
        return x


class TransformerLM(nn.Module):
    """Standard Transformer LM baseline."""

    def __init__(
        self,
        vocab_size: int,
        d_model: int = 64,
        n_layers: int = 4,
        n_heads: int = 4,
        max_seq_len: int = 512,
    ):
        super().__init__()
        self.d_model = d_model
        self.embedding = nn.Embedding(vocab_size, d_model)
        self.pos_emb = nn.Embedding(max_seq_len, d_model)
        self.layers = nn.ModuleList(
            [TransformerBlock(d_model, n_heads) for _ in range(n_layers)]
        )
        self.norm_out = nn.LayerNorm(d_model)
        self.lm_head = nn.Linear(d_model, vocab_size, bias=False)
        self.lm_head.weight = self.embedding.weight

        self._init_weights()

    def _init_weights(self):
        for p in self.parameters():
            if p.dim() > 1:
                nn.init.normal_(p, std=0.02)

    def forward(
        self, input_ids: torch.Tensor, targets: torch.Tensor | None = None
    ) -> tuple[torch.Tensor, torch.Tensor | None]:
        B, T = input_ids.shape
        pos = torch.arange(T, device=input_ids.device).unsqueeze(0)
        x = self.embedding(input_ids) + self.pos_emb(pos)

        for layer in self.layers:
            x = layer(x)

        x = self.norm_out(x)
        logits = self.lm_head(x)

        loss = None
        if targets is not None:
            loss = F.cross_entropy(
                logits.reshape(-1, logits.size(-1)), targets.reshape(-1)
            )
        return logits, loss
