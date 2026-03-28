"""Extract hidden state activations from a trained GPT model.

To train an SAE, we need a dataset of model activations (hidden states).
This module runs text through the model and collects the intermediate
representations from a specified layer.

Usage:
    model = GPTModel(config)
    activations = extract_activations(model, tokenizer, texts, layer_idx=3)
    # activations: (n_tokens, dim) tensor ready for SAE training
"""

import torch
from pathlib import Path

from phase1_transformer.model import GPTModel
from phase1_transformer.tokenizer import Tokenizer


@torch.no_grad()
def extract_activations(
    model: GPTModel,
    tokenizer: Tokenizer,
    texts: list[str] | str,
    layer_idx: int = -1,
    max_tokens: int = 50000,
    device: torch.device | None = None,
) -> torch.Tensor:
    """Extract hidden state activations from a specific layer.

    Args:
        model: Trained GPTModel
        tokenizer: Tokenizer
        texts: Text(s) to process
        layer_idx: Which layer to extract from (-1 = last before final norm)
        max_tokens: Maximum tokens to collect
        device: Device to run on

    Returns:
        Tensor of shape (n_tokens, dim) — one activation per token
    """
    model.eval()
    if device is None:
        device = next(model.parameters()).device

    if isinstance(texts, str):
        texts = [texts]

    # Hook to capture activations
    activations = []
    target_layer = model.layers[layer_idx]

    def hook_fn(module, input, output):
        # TransformerBlock returns (x, kv_cache)
        x = output[0] if isinstance(output, tuple) else output
        activations.append(x.detach().cpu())

    handle = target_layer.register_forward_hook(hook_fn)

    # Process texts
    total_tokens = 0
    for text in texts:
        tokens = tokenizer.encode(text)
        if total_tokens + len(tokens) > max_tokens:
            tokens = tokens[:max_tokens - total_tokens]

        if len(tokens) == 0:
            break

        input_ids = torch.tensor([tokens], device=device)
        model(input_ids)
        total_tokens += len(tokens)

        if total_tokens >= max_tokens:
            break

    handle.remove()

    # Concatenate: (n_chunks, seq_len, dim) → (n_tokens, dim)
    all_activations = torch.cat(activations, dim=1).squeeze(0)
    print(f"Extracted {all_activations.shape[0]:,} activation vectors from layer {layer_idx}")
    return all_activations


def extract_from_file(
    model: GPTModel,
    tokenizer: Tokenizer,
    file_path: str | Path,
    layer_idx: int = -1,
    max_tokens: int = 50000,
) -> torch.Tensor:
    """Extract activations from a text file."""
    text = Path(file_path).read_text(encoding="utf-8")
    return extract_activations(model, tokenizer, text, layer_idx, max_tokens)
