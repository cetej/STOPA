"""DPO Trainer — fine-tune a model with preference optimization.

Paper: "Direct Preference Optimization" (Rafailov et al., 2023)

Training loop:
1. Load a pre-trained model as BOTH policy (trainable) and reference (frozen)
2. For each batch of (prompt, chosen, rejected):
   a. Forward pass chosen through both policy and reference
   b. Forward pass rejected through both policy and reference
   c. Compute DPO loss
   d. Update policy only (reference stays frozen)
3. Monitor: reward margin, accuracy (chosen > rejected), loss

Usage:
    python -m phase3_dpo.dpo_trainer --checkpoint checkpoints/tiny_best.pt
"""

import argparse
import copy
import math
import sys
import time
from pathlib import Path

import torch
from torch.utils.data import DataLoader

from phase1_transformer.config import CONFIGS
from phase1_transformer.model import GPTModel
from phase1_transformer.tokenizer import Tokenizer

from .dpo_loss import dpo_loss
from .preference_data import PreferenceDataset

sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def train_dpo(
    checkpoint_path: str,
    data_path: str = "data/shakespeare.txt",
    n_epochs: int = 3,
    batch_size: int = 4,
    lr: float = 1e-5,
    beta: float = 0.1,
    n_samples: int = 500,
    device: str = "auto",
    log_interval: int = 10,
) -> None:
    if device == "auto":
        device = "cuda" if torch.cuda.is_available() else "cpu"
    device = torch.device(device)
    print(f"Device: {device}")

    # Load pre-trained model
    ckpt = torch.load(checkpoint_path, map_location=device, weights_only=False)
    config = CONFIGS[ckpt["config_name"]]

    # Policy model (will be trained)
    policy = GPTModel(config).to(device)
    policy.load_state_dict(ckpt["model_state_dict"])

    # Reference model (frozen copy)
    reference = copy.deepcopy(policy)
    reference.eval()
    for p in reference.parameters():
        p.requires_grad = False

    print(f"Model: {ckpt['config_name']} (step {ckpt['step']}, loss {ckpt['loss']:.4f})")
    print(f"DPO beta: {beta}")

    # Preference data
    tokenizer = Tokenizer()
    data_path = Path(__file__).parent.parent / data_path
    dataset = PreferenceDataset(
        data_path, tokenizer,
        prompt_len=64, response_len=128,
        n_samples=n_samples,
    )
    loader = DataLoader(dataset, batch_size=batch_size, shuffle=True, drop_last=True)

    # Optimizer — lower LR than pre-training (fine-tuning)
    optimizer = torch.optim.AdamW(policy.parameters(), lr=lr, weight_decay=0.01)

    # Training
    policy.train()
    t0 = time.time()

    for epoch in range(n_epochs):
        total_loss = 0
        total_acc = 0
        total_margin = 0
        n_batches = 0

        for batch in loader:
            chosen_ids = batch["chosen_ids"].to(device)
            rejected_ids = batch["rejected_ids"].to(device)
            chosen_mask = batch["chosen_mask"].to(device)
            rejected_mask = batch["rejected_mask"].to(device)

            # Labels are the input shifted by 1 (next-token prediction)
            chosen_labels = chosen_ids[:, 1:]
            rejected_labels = rejected_ids[:, 1:]
            chosen_mask = chosen_mask[:, 1:]
            rejected_mask = rejected_mask[:, 1:]

            # Forward pass through policy
            policy_chosen_logits, _ = policy(chosen_ids[:, :-1])
            policy_rejected_logits, _ = policy(rejected_ids[:, :-1])

            # Forward pass through reference (no gradient)
            with torch.no_grad():
                ref_chosen_logits, _ = reference(chosen_ids[:, :-1])
                ref_rejected_logits, _ = reference(rejected_ids[:, :-1])

            # DPO loss
            loss, metrics = dpo_loss(
                policy_chosen_logits, policy_rejected_logits,
                ref_chosen_logits, ref_rejected_logits,
                chosen_labels, rejected_labels,
                chosen_mask, rejected_mask,
                beta=beta,
            )

            # Backward + update
            optimizer.zero_grad()
            loss.backward()
            torch.nn.utils.clip_grad_norm_(policy.parameters(), 1.0)
            optimizer.step()

            total_loss += metrics["loss"]
            total_acc += metrics["accuracy"]
            total_margin += metrics["reward_margin"]
            n_batches += 1

            if n_batches % log_interval == 0:
                print(
                    f"  epoch {epoch+1} batch {n_batches:4d} | "
                    f"loss {metrics['loss']:.4f} | "
                    f"acc {metrics['accuracy']:.2f} | "
                    f"margin {metrics['reward_margin']:.3f}"
                )

        # Epoch summary
        avg_loss = total_loss / max(n_batches, 1)
        avg_acc = total_acc / max(n_batches, 1)
        avg_margin = total_margin / max(n_batches, 1)
        print(
            f"Epoch {epoch+1}/{n_epochs} | "
            f"loss {avg_loss:.4f} | "
            f"acc {avg_acc:.2f} | "
            f"margin {avg_margin:.3f} | "
            f"{time.time()-t0:.0f}s"
        )

    # Save aligned model
    save_path = Path(__file__).parent.parent / "checkpoints" / f"{ckpt['config_name']}_dpo.pt"
    save_path.parent.mkdir(parents=True, exist_ok=True)
    torch.save({
        "config_name": ckpt["config_name"],
        "step": ckpt["step"],
        "loss": avg_loss,
        "model_state_dict": policy.state_dict(),
        "dpo_beta": beta,
        "dpo_epochs": n_epochs,
    }, save_path)
    print(f"\nSaved DPO-aligned model to {save_path}")


def main():
    parser = argparse.ArgumentParser(description="DPO Training")
    parser.add_argument("--checkpoint", required=True)
    parser.add_argument("--epochs", type=int, default=3)
    parser.add_argument("--batch-size", type=int, default=4)
    parser.add_argument("--lr", type=float, default=1e-5)
    parser.add_argument("--beta", type=float, default=0.1)
    parser.add_argument("--device", default="auto")
    args = parser.parse_args()

    train_dpo(
        checkpoint_path=args.checkpoint,
        n_epochs=args.epochs,
        batch_size=args.batch_size,
        lr=args.lr,
        beta=args.beta,
        device=args.device,
    )


if __name__ == "__main__":
    main()
