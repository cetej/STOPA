"""Tokenizer wrapper using tiktoken (GPT-2 BPE).

We use an existing tokenizer rather than training our own because:
1. Tokenizer training is a separate discipline (BPE, SentencePiece, etc.)
2. GPT-2's BPE tokenizer works well for English text experiments
3. tiktoken is fast (Rust-based) and widely available

The GPT-2 tokenizer has 50,257 tokens (50,000 BPE merges + 256 byte tokens + 1 <|endoftext|>).
"""

import tiktoken


class Tokenizer:
    """Thin wrapper around tiktoken's GPT-2 BPE tokenizer."""

    def __init__(self):
        self.encoder = tiktoken.get_encoding("gpt2")
        self.eot_token = self.encoder.eot_token  # <|endoftext|> = 50256

    @property
    def vocab_size(self) -> int:
        return self.encoder.n_vocab  # 50257

    def encode(self, text: str) -> list[int]:
        """Encode text to token IDs."""
        return self.encoder.encode(text, allowed_special={"<|endoftext|>"})

    def decode(self, tokens: list[int]) -> str:
        """Decode token IDs back to text."""
        return self.encoder.decode(tokens)
