"""Text generation with autoregressive decoding and KV-cache.

Implements:
- Greedy decoding (argmax)
- Top-k sampling: sample from top K most likely tokens
- Top-p (nucleus) sampling: sample from smallest set whose cumulative prob >= p
- Temperature: controls randomness (lower = more deterministic)
- KV-cache: efficient generation without recomputing previous tokens

Usage:
    python -m phase1_transformer.generate --checkpoint checkpoints/tiny_best.pt --prompt "To be or"
    python -m phase1_transformer.generate --checkpoint checkpoints/tiny_best.pt --interactive
"""

import argparse
import sys

import torch

from .config import CONFIGS
from .model import GPTModel
from .tokenizer import Tokenizer

sys.stdout.reconfigure(encoding="utf-8", errors="replace")


@torch.no_grad()
def generate(
    model: GPTModel,
    tokenizer: Tokenizer,
    prompt: str = "",
    max_new_tokens: int = 200,
    temperature: float = 0.8,
    top_k: int = 50,
    top_p: float = 0.9,
    device: torch.device | None = None,
) -> str:
    """Generate text autoregressively with KV-cache.

    Decoding strategy (applied in order):
    1. Temperature scaling: logits / temperature
       - T < 1: sharper distribution (more confident/repetitive)
       - T > 1: flatter distribution (more creative/chaotic)
       - T = 1: raw model distribution
    2. Top-k filtering: zero out all but top K logits
    3. Top-p (nucleus): zero out tokens outside the smallest set with cumprob >= p
    4. Sample from the filtered distribution

    KV-cache flow:
    - First step: process entire prompt, cache K/V for all layers
    - Subsequent steps: only feed the NEW token, append to cache
    - This makes generation O(n) per token instead of O(n^2)
    """
    model.eval()
    if device is None:
        device = next(model.parameters()).device

    # Encode prompt
    if prompt:
        tokens = tokenizer.encode(prompt)
    else:
        tokens = [tokenizer.eot_token]  # Start with <|endoftext|>

    tokens = torch.tensor([tokens], dtype=torch.long, device=device)

    # First pass: process entire prompt, build KV-cache
    logits, kv_caches = model(tokens, start_pos=0, kv_caches=None)

    generated = []
    next_pos = tokens.shape[1]

    for _ in range(max_new_tokens):
        # Get logits for the last position only
        next_logits = logits[:, -1, :]  # (1, vocab_size)

        # Apply temperature
        if temperature > 0:
            next_logits = next_logits / temperature

            # Top-k filtering
            if top_k > 0:
                top_k_vals, _ = torch.topk(next_logits, min(top_k, next_logits.size(-1)))
                threshold = top_k_vals[:, -1].unsqueeze(-1)
                next_logits[next_logits < threshold] = float("-inf")

            # Top-p (nucleus) filtering
            if top_p < 1.0:
                sorted_logits, sorted_indices = torch.sort(next_logits, descending=True)
                cumprob = torch.cumsum(torch.softmax(sorted_logits, dim=-1), dim=-1)
                # Remove tokens with cumulative prob above threshold
                mask = cumprob - torch.softmax(sorted_logits, dim=-1) >= top_p
                sorted_logits[mask] = float("-inf")
                # Scatter back to original positions
                next_logits = sorted_logits.scatter(1, sorted_indices, sorted_logits)

            # Sample
            probs = torch.softmax(next_logits, dim=-1)
            next_token = torch.multinomial(probs, num_samples=1)
        else:
            # Greedy decoding (temperature = 0)
            next_token = next_logits.argmax(dim=-1, keepdim=True)

        # Stop on <|endoftext|>
        if next_token.item() == tokenizer.eot_token:
            break

        generated.append(next_token.item())

        # Next step: feed only the new token, use KV-cache
        logits, kv_caches = model(next_token, start_pos=next_pos, kv_caches=kv_caches)
        next_pos += 1

    return prompt + tokenizer.decode(generated)


def load_model(checkpoint_path: str, device: str = "auto") -> tuple[GPTModel, Tokenizer, torch.device]:
    """Load model from checkpoint."""
    if device == "auto":
        device = "cuda" if torch.cuda.is_available() else "cpu"
    device = torch.device(device)

    checkpoint = torch.load(checkpoint_path, map_location=device, weights_only=False)
    config = CONFIGS[checkpoint["config_name"]]
    model = GPTModel(config).to(device)
    model.load_state_dict(checkpoint["model_state_dict"])
    model.eval()

    tokenizer = Tokenizer()
    print(f"Loaded {checkpoint['config_name']} model (step {checkpoint['step']}, loss {checkpoint['loss']:.4f})")
    return model, tokenizer, device


def main():
    parser = argparse.ArgumentParser(description="Generate text with trained GPT model")
    parser.add_argument("--checkpoint", required=True, help="Path to model checkpoint")
    parser.add_argument("--prompt", default="", help="Text prompt to continue from")
    parser.add_argument("--max-tokens", type=int, default=200)
    parser.add_argument("--temperature", type=float, default=0.8)
    parser.add_argument("--top-k", type=int, default=50)
    parser.add_argument("--top-p", type=float, default=0.9)
    parser.add_argument("--device", default="auto")
    parser.add_argument("--interactive", action="store_true", help="Interactive prompt loop")
    args = parser.parse_args()

    model, tokenizer, device = load_model(args.checkpoint, args.device)

    if args.interactive:
        print("\nInteractive mode. Type a prompt and press Enter. Ctrl+C to exit.\n")
        while True:
            try:
                prompt = input(">>> ")
                if not prompt.strip():
                    continue
                output = generate(model, tokenizer, prompt, args.max_tokens,
                                  args.temperature, args.top_k, args.top_p, device)
                print(output)
                print()
            except KeyboardInterrupt:
                print("\nBye!")
                break
    else:
        output = generate(model, tokenizer, args.prompt, args.max_tokens,
                          args.temperature, args.top_k, args.top_p, device)
        print(output)


if __name__ == "__main__":
    main()
