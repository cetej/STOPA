"""Dataset loading and preparation.

Supports:
- TinyShakespeare (~1MB): classic benchmark for small language models
- Custom text files: any .txt file for experimentation

Data pipeline:
1. Load raw text
2. Tokenize with GPT-2 BPE
3. Create fixed-length chunks for training
4. Each chunk: input = tokens[:-1], target = tokens[1:] (next-token prediction)
"""

import os
import urllib.request
from pathlib import Path

import torch
from torch.utils.data import Dataset

from .tokenizer import Tokenizer

DATA_DIR = Path(__file__).parent.parent / "data"

SHAKESPEARE_URL = "https://raw.githubusercontent.com/karpathy/char-rnn/master/data/tinyshakespeare/input.txt"


def download_shakespeare() -> Path:
    """Download TinyShakespeare dataset (~1MB)."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    filepath = DATA_DIR / "shakespeare.txt"
    if not filepath.exists():
        print(f"Downloading TinyShakespeare to {filepath}...")
        urllib.request.urlretrieve(SHAKESPEARE_URL, filepath)
        print(f"Done. Size: {filepath.stat().st_size / 1024:.0f} KB")
    return filepath


class TextDataset(Dataset):
    """Fixed-length token chunks from a text file.

    Each item is a (input, target) pair where:
    - input:  tokens[i : i + seq_len]
    - target: tokens[i+1 : i + seq_len + 1]

    This is the standard causal LM training setup: predict the next token
    at every position simultaneously (teacher forcing).
    """

    def __init__(
        self,
        text_path: str | Path,
        tokenizer: Tokenizer,
        seq_len: int = 512,
        stride: int | None = None,
    ):
        """
        Args:
            text_path: path to .txt file
            tokenizer: tokenizer instance
            seq_len: context window size
            stride: step between consecutive chunks. None = seq_len (no overlap).
                    Using stride < seq_len creates overlapping chunks (more data).
        """
        self.seq_len = seq_len
        self.stride = stride or seq_len

        # Load and tokenize
        text = Path(text_path).read_text(encoding="utf-8")
        self.tokens = torch.tensor(tokenizer.encode(text), dtype=torch.long)

        # Calculate number of chunks
        self.n_chunks = max(0, (len(self.tokens) - seq_len - 1) // self.stride + 1)

    def __len__(self) -> int:
        return self.n_chunks

    def __getitem__(self, idx: int) -> tuple[torch.Tensor, torch.Tensor]:
        start = idx * self.stride
        chunk = self.tokens[start : start + self.seq_len + 1]
        x = chunk[:-1]   # Input: first seq_len tokens
        y = chunk[1:]     # Target: shifted by 1 (next-token prediction)
        return x, y


def get_dataset(
    name: str = "shakespeare",
    tokenizer: Tokenizer | None = None,
    seq_len: int = 512,
    train_split: float = 0.9,
) -> tuple[TextDataset, TextDataset]:
    """Get train/val split of a dataset.

    Returns:
        (train_dataset, val_dataset)
    """
    if tokenizer is None:
        tokenizer = Tokenizer()

    if name == "shakespeare":
        text_path = download_shakespeare()
    elif os.path.isfile(name):
        text_path = Path(name)
    else:
        raise ValueError(f"Unknown dataset: {name}. Pass 'shakespeare' or a file path.")

    # Load full text and split by character position (not token — simpler)
    text = Path(text_path).read_text(encoding="utf-8")
    split_idx = int(len(text) * train_split)

    # Write train/val splits to temp files
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    train_path = DATA_DIR / f"{Path(text_path).stem}_train.txt"
    val_path = DATA_DIR / f"{Path(text_path).stem}_val.txt"

    train_path.write_text(text[:split_idx], encoding="utf-8")
    val_path.write_text(text[split_idx:], encoding="utf-8")

    train_ds = TextDataset(train_path, tokenizer, seq_len)
    val_ds = TextDataset(val_path, tokenizer, seq_len)

    print(f"Dataset: {name}")
    print(f"  Train: {len(train_ds)} chunks of {seq_len} tokens")
    print(f"  Val:   {len(val_ds)} chunks of {seq_len} tokens")
    print(f"  Total tokens: {len(tokenizer.encode(text)):,}")

    return train_ds, val_ds
