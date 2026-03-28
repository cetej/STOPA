"""Speculative Decoding Algorithm.

Papers:
- "Fast Inference from Transformers via Speculative Decoding" (Leviathan et al., 2022)
- "Accelerating Large Language Model Decoding with Speculative Sampling" (Chen et al., 2023)

Algorithm:
1. Draft model generates K candidate tokens autoregressively (fast)
2. Target model scores all K tokens in one forward pass (parallel)
3. Accept tokens left-to-right where draft and target agree
4. At first rejection, sample from adjusted distribution
5. Repeat from step 1

Acceptance criterion (preserves target distribution exactly):
    For each position i, accept with probability:
        min(1, p_target(x_i) / p_draft(x_i))
    If rejected, sample from:
        norm(max(0, p_target - p_draft))

This guarantees the output distribution is IDENTICAL to the target model.
"""

import time

import torch
import torch.nn.functional as F

from phase1_transformer.model import GPTModel
from phase1_transformer.tokenizer import Tokenizer


@torch.no_grad()
def speculative_decode(
    target_model: GPTModel,
    draft_model: GPTModel,
    tokenizer: Tokenizer,
    prompt: str,
    max_new_tokens: int = 100,
    draft_k: int = 5,
    temperature: float = 1.0,
    device: torch.device | None = None,
) -> tuple[str, dict]:
    """Generate text using speculative decoding.

    Args:
        target_model: Large, high-quality model (slow but accurate)
        draft_model: Small, fast model (quick but less accurate)
        prompt: Input text
        max_new_tokens: Maximum tokens to generate
        draft_k: Number of draft tokens to propose per iteration
        temperature: Sampling temperature
        device: Device to run on

    Returns:
        generated_text: The complete generated text
        stats: Dictionary with acceptance rate, speedup, etc.
    """
    target_model.eval()
    draft_model.eval()
    if device is None:
        device = next(target_model.parameters()).device

    # Encode prompt
    tokens = tokenizer.encode(prompt)
    input_ids = torch.tensor(tokens, device=device)

    generated = list(tokens)
    total_draft = 0
    total_accepted = 0
    n_iterations = 0

    while len(generated) - len(tokens) < max_new_tokens:
        n_iterations += 1
        current = torch.tensor([generated], device=device)

        # Step 1: Draft model generates K candidate tokens
        draft_tokens = []
        draft_probs_list = []
        draft_input = current.clone()

        for _ in range(draft_k):
            draft_logits, _ = draft_model(draft_input)
            draft_logits = draft_logits[:, -1, :] / max(temperature, 1e-8)
            draft_probs = F.softmax(draft_logits, dim=-1)

            # Sample from draft distribution
            next_token = torch.multinomial(draft_probs, 1)
            draft_tokens.append(next_token.item())
            draft_probs_list.append(draft_probs.squeeze(0))

            # Extend draft input for next token
            draft_input = torch.cat([draft_input, next_token], dim=-1)

        total_draft += len(draft_tokens)

        # Step 2: Target model scores all candidates in ONE forward pass
        # Input: original context + all K draft tokens
        candidate = torch.tensor([generated + draft_tokens], device=device)
        target_logits, _ = target_model(candidate)

        # Get target probabilities for each draft position
        # Position i in target_logits corresponds to predicting token i+1
        n_ctx = len(generated)
        target_probs_list = []
        for i in range(len(draft_tokens)):
            pos = n_ctx - 1 + i  # Position that predicts draft_tokens[i]
            logits = target_logits[0, pos, :] / max(temperature, 1e-8)
            target_probs_list.append(F.softmax(logits, dim=-1))

        # Step 3: Accept/reject tokens left to right
        n_accepted = 0
        for i in range(len(draft_tokens)):
            draft_token = draft_tokens[i]
            p_target = target_probs_list[i][draft_token].item()
            p_draft = draft_probs_list[i][draft_token].item()

            # Acceptance probability
            accept_prob = min(1.0, p_target / max(p_draft, 1e-10))

            if torch.rand(1).item() < accept_prob:
                # Accept this token
                generated.append(draft_token)
                n_accepted += 1
            else:
                # Reject: sample from adjusted distribution
                # p_adjusted = norm(max(0, p_target - p_draft))
                adjusted = torch.clamp(
                    target_probs_list[i] - draft_probs_list[i], min=0
                )
                adjusted_sum = adjusted.sum()
                if adjusted_sum > 0:
                    adjusted = adjusted / adjusted_sum
                    new_token = torch.multinomial(adjusted, 1).item()
                else:
                    new_token = torch.multinomial(target_probs_list[i], 1).item()
                generated.append(new_token)
                break  # Stop accepting after first rejection

        total_accepted += n_accepted

        # If all K were accepted, sample one more from target
        if n_accepted == len(draft_tokens):
            last_pos = n_ctx - 1 + len(draft_tokens)
            if last_pos < target_logits.shape[1]:
                bonus_logits = target_logits[0, last_pos, :] / max(temperature, 1e-8)
                bonus_probs = F.softmax(bonus_logits, dim=-1)
                bonus_token = torch.multinomial(bonus_probs, 1).item()
                generated.append(bonus_token)

        # Stop on EOT
        if generated[-1] == tokenizer.eot_token:
            break

    # Decode
    new_tokens = generated[len(tokens):]
    text = prompt + tokenizer.decode(new_tokens)

    acceptance_rate = total_accepted / max(total_draft, 1)
    stats = {
        "total_tokens": len(new_tokens),
        "iterations": n_iterations,
        "total_draft": total_draft,
        "total_accepted": total_accepted,
        "acceptance_rate": acceptance_rate,
        "avg_accepted_per_iter": total_accepted / max(n_iterations, 1),
    }

    return text, stats


@torch.no_grad()
def standard_decode(
    model: GPTModel,
    tokenizer: Tokenizer,
    prompt: str,
    max_new_tokens: int = 100,
    temperature: float = 1.0,
    device: torch.device | None = None,
) -> tuple[str, float]:
    """Standard autoregressive decoding (for speed comparison)."""
    model.eval()
    if device is None:
        device = next(model.parameters()).device

    tokens = tokenizer.encode(prompt)
    generated = list(tokens)

    t0 = time.perf_counter()
    for _ in range(max_new_tokens):
        input_ids = torch.tensor([generated], device=device)
        logits, _ = model(input_ids)
        logits = logits[:, -1, :] / max(temperature, 1e-8)
        probs = F.softmax(logits, dim=-1)
        next_token = torch.multinomial(probs, 1).item()
        generated.append(next_token)
        if next_token == tokenizer.eot_token:
            break
    elapsed = time.perf_counter() - t0

    new_tokens = generated[len(tokens):]
    text = prompt + tokenizer.decode(new_tokens)
    return text, elapsed
