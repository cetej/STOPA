"""Apply LoRA to an existing GPT model.

Injects LoRA adapters into attention layers (Q, K, V, O projections).
The original model weights are frozen; only LoRA matrices are trainable.

Which layers to adapt?
- Hu et al. (2021) found that adapting Q and V gives best results
- Common practice: adapt all of Q, K, V, O (more capacity, still very efficient)
- We adapt Q, K, V, O by default (configurable via target_modules)

Usage:
    model = GPTModel(config)
    model.load_state_dict(checkpoint)
    lora_model = apply_lora(model, rank=8)
    # Train lora_model — only LoRA params have gradients
"""

import torch.nn as nn

from phase1_transformer.model import GPTModel

from .lora import LoRALinear


def apply_lora(
    model: GPTModel,
    rank: int = 8,
    alpha: float | None = None,
    dropout: float = 0.0,
    target_modules: list[str] | None = None,
) -> GPTModel:
    """Inject LoRA adapters into a GPT model.

    Args:
        model: Pre-trained GPTModel
        rank: LoRA rank
        alpha: LoRA scaling (default: same as rank)
        dropout: Dropout on LoRA path
        target_modules: Which linear layers to adapt.
            Default: ["wq", "wk", "wv", "wo"] (all attention projections)

    Returns:
        Modified model with LoRA layers (original weights frozen)
    """
    if target_modules is None:
        target_modules = ["wq", "wk", "wv", "wo"]

    n_adapted = 0
    total_lora_params = 0
    total_original_params = sum(p.numel() for p in model.parameters())

    # Replace target linear layers with LoRA versions
    for layer in model.layers:
        attn = layer.attention
        for name in target_modules:
            if hasattr(attn, name):
                original = getattr(attn, name)
                if isinstance(original, nn.Linear):
                    lora_layer = LoRALinear(original, rank, alpha, dropout)
                    setattr(attn, name, lora_layer)
                    n_adapted += 1
                    total_lora_params += lora_layer.n_trainable

    # Freeze ALL parameters first
    for param in model.parameters():
        param.requires_grad = False

    # Unfreeze only LoRA parameters
    for module in model.modules():
        if isinstance(module, LoRALinear):
            module.lora_A.requires_grad = True
            module.lora_B.requires_grad = True

    trainable = sum(p.numel() for p in model.parameters() if p.requires_grad)

    print(f"LoRA applied:")
    print(f"  Rank: {rank}, Alpha: {alpha or rank}")
    print(f"  Adapted layers: {n_adapted} ({', '.join(target_modules)})")
    print(f"  Trainable params: {trainable:,} ({trainable/total_original_params*100:.2f}%)")
    print(f"  Frozen params: {total_original_params - trainable:,}")
    print(f"  Compression: {total_original_params / trainable:.0f}×")

    return model


def merge_lora(model: GPTModel) -> GPTModel:
    """Merge all LoRA adapters back into base weights.

    After merging, the model is a standard GPTModel with no LoRA overhead.
    This is irreversible — the LoRA matrices are absorbed into W.
    """
    n_merged = 0
    for layer in model.layers:
        attn = layer.attention
        for name in ["wq", "wk", "wv", "wo"]:
            module = getattr(attn, name, None)
            if isinstance(module, LoRALinear):
                merged = module.merge()
                setattr(attn, name, merged)
                n_merged += 1

    # Unfreeze all parameters (back to normal model)
    for param in model.parameters():
        param.requires_grad = True

    print(f"Merged {n_merged} LoRA layers back into base weights")
    return model


def get_lora_state_dict(model: GPTModel) -> dict:
    """Extract only LoRA parameters for saving.

    Returns a small state dict containing just the LoRA A and B matrices.
    This is what you'd distribute as an "adapter" — much smaller than full weights.
    """
    lora_state = {}
    for name, module in model.named_modules():
        if isinstance(module, LoRALinear):
            lora_state[f"{name}.lora_A"] = module.lora_A.data.clone()
            lora_state[f"{name}.lora_B"] = module.lora_B.data.clone()
    return lora_state
