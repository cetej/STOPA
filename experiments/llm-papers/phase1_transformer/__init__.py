"""Phase 1: Decoder-only Transformer from scratch.

Implements a modern GPT-style LLM with LLaMA-inspired architecture:
- Multi-head self-attention with RoPE (Paper #1, #8)
- RMSNorm instead of LayerNorm (Paper #7 — LLaMA)
- SwiGLU FFN instead of ReLU FFN (Paper #7 — LLaMA)
- KV-cache for efficient autoregressive generation
"""
