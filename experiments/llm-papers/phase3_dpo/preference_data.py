"""Preference dataset for DPO training.

In real-world DPO:
- Human annotators compare pairs of model responses
- They mark which response is "better" (chosen vs rejected)
- Examples: Anthropic HH-RLHF, OpenAI summarization preferences

For this learning implementation, we create SYNTHETIC preference data:
- Chosen: real Shakespeare text (coherent, original quality)
- Rejected: corrupted Shakespeare text (shuffled words, repeated tokens)

This teaches the model to prefer coherent text over corrupted text —
a simplified but valid demonstration of the DPO mechanism.
"""

import random
from dataclasses import dataclass
from pathlib import Path

import torch
from torch.utils.data import Dataset

from phase1_transformer.tokenizer import Tokenizer


@dataclass
class PreferencePair:
    """A single preference data point."""
    prompt_ids: list[int]     # Shared prefix (context)
    chosen_ids: list[int]     # Preferred continuation
    rejected_ids: list[int]   # Dispreferred continuation


def corrupt_text(text: str, corruption_type: str = "shuffle") -> str:
    """Create a corrupted version of text for rejection samples.

    Corruption strategies:
    - "shuffle": randomly shuffle words within each sentence
    - "repeat": repeat random words to create stuttering
    - "truncate": cut text short and pad with common words
    """
    words = text.split()
    if len(words) < 3:
        return text

    if corruption_type == "shuffle":
        # Shuffle words in groups of 5-8
        group_size = min(len(words), random.randint(5, 8))
        for i in range(0, len(words) - group_size, group_size):
            chunk = words[i:i + group_size]
            random.shuffle(chunk)
            words[i:i + group_size] = chunk
        return " ".join(words)

    elif corruption_type == "repeat":
        # Randomly repeat some words 2-3 times
        result = []
        for word in words:
            result.append(word)
            if random.random() < 0.2:
                result.extend([word] * random.randint(1, 2))
        return " ".join(result)

    elif corruption_type == "truncate":
        # Keep first half, then repeat a common word
        half = len(words) // 2
        filler = random.choice(["the", "and", "of", "to", "a"])
        return " ".join(words[:half] + [filler] * half)

    return text


class PreferenceDataset(Dataset):
    """Dataset of (prompt, chosen, rejected) pairs from Shakespeare text.

    For each sample:
    - prompt = first `prompt_len` tokens of a text chunk
    - chosen = next `response_len` tokens (original text)
    - rejected = same tokens but corrupted (shuffled/repeated)
    """

    def __init__(
        self,
        text_path: str | Path,
        tokenizer: Tokenizer,
        prompt_len: int = 64,
        response_len: int = 128,
        n_samples: int = 1000,
        seed: int = 42,
    ):
        self.tokenizer = tokenizer
        self.prompt_len = prompt_len
        self.response_len = response_len

        # Load and tokenize
        text = Path(text_path).read_text(encoding="utf-8")

        # Create pairs
        random.seed(seed)
        self.pairs: list[PreferencePair] = []

        total_len = prompt_len + response_len
        paragraphs = [p.strip() for p in text.split("\n\n") if len(p.strip()) > 100]

        for _ in range(n_samples):
            if not paragraphs:
                break

            # Pick a random paragraph
            para = random.choice(paragraphs)
            tokens = tokenizer.encode(para)

            if len(tokens) < total_len + 10:
                continue

            # Random start position
            start = random.randint(0, len(tokens) - total_len - 1)
            prompt_ids = tokens[start : start + prompt_len]
            chosen_ids = tokens[start + prompt_len : start + total_len]

            # Create rejected version by corrupting the text
            chosen_text = tokenizer.decode(chosen_ids)
            corruption = random.choice(["shuffle", "repeat", "truncate"])
            rejected_text = corrupt_text(chosen_text, corruption)
            rejected_ids = tokenizer.encode(rejected_text)[:response_len]

            # Pad rejected to same length
            if len(rejected_ids) < response_len:
                rejected_ids = rejected_ids + [tokenizer.eot_token] * (response_len - len(rejected_ids))

            self.pairs.append(PreferencePair(
                prompt_ids=prompt_ids,
                chosen_ids=chosen_ids,
                rejected_ids=rejected_ids[:response_len],
            ))

        print(f"PreferenceDataset: {len(self.pairs)} pairs "
              f"(prompt={prompt_len}, response={response_len} tokens)")

    def __len__(self) -> int:
        return len(self.pairs)

    def __getitem__(self, idx: int) -> dict[str, torch.Tensor]:
        pair = self.pairs[idx]

        # Concatenate prompt + response for both chosen and rejected
        chosen_full = pair.prompt_ids + pair.chosen_ids
        rejected_full = pair.prompt_ids + pair.rejected_ids

        # Create masks: 1 for response tokens, 0 for prompt tokens
        prompt_mask = [0] * len(pair.prompt_ids)
        response_mask = [1] * len(pair.chosen_ids)
        chosen_mask = prompt_mask + response_mask

        response_mask_r = [1] * len(pair.rejected_ids)
        rejected_mask = prompt_mask + response_mask_r

        return {
            "chosen_ids": torch.tensor(chosen_full, dtype=torch.long),
            "rejected_ids": torch.tensor(rejected_full, dtype=torch.long),
            "chosen_mask": torch.tensor(chosen_mask, dtype=torch.float),
            "rejected_mask": torch.tensor(rejected_mask, dtype=torch.float),
        }
