"""Training loop for the GPT model.

Implements:
- AdamW optimizer (Paper #7 — standard for Transformers)
- Cosine learning rate schedule with linear warmup
- Mixed precision training (fp16/bf16) via torch.amp
- Gradient accumulation for effective large batch sizes
- Periodic validation and checkpointing
- Logging: loss, learning rate, tokens/sec

Usage:
    python -m phase1_transformer.train --config tiny --data shakespeare
    python -m phase1_transformer.train --config small --data shakespeare --device cuda
"""

import argparse
import math
import sys
import time
from pathlib import Path

import torch
from torch.utils.data import DataLoader

from .config import CONFIGS
from .data import get_dataset
from .model import GPTModel
from .tokenizer import Tokenizer

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

CHECKPOINT_DIR = Path(__file__).parent.parent / "checkpoints"


def get_lr(step: int, warmup_steps: int, max_steps: int, max_lr: float, min_lr: float) -> float:
    """Cosine learning rate schedule with linear warmup.

    1. Linear warmup: 0 → max_lr over warmup_steps
    2. Cosine decay: max_lr → min_lr over remaining steps

    This schedule is standard across GPT-2, GPT-3, LLaMA, etc.
    Warmup prevents early instability from large gradient updates.
    Cosine decay gives a smooth landing as training converges.
    """
    if step < warmup_steps:
        return max_lr * step / warmup_steps
    if step >= max_steps:
        return min_lr
    # Cosine decay from max_lr to min_lr
    progress = (step - warmup_steps) / (max_steps - warmup_steps)
    return min_lr + 0.5 * (max_lr - min_lr) * (1 + math.cos(math.pi * progress))


def train(
    config_name: str = "tiny",
    data_name: str = "shakespeare",
    device: str = "auto",
    # Training hyperparameters
    max_steps: int = 5000,
    batch_size: int = 8,
    grad_accum_steps: int = 4,
    max_lr: float = 3e-4,
    min_lr: float = 3e-5,
    warmup_steps: int = 100,
    weight_decay: float = 0.1,
    grad_clip: float = 1.0,
    # Logging & checkpointing
    log_interval: int = 10,
    eval_interval: int = 250,
    eval_steps: int = 20,
    save_interval: int = 1000,
) -> None:
    # Device selection
    if device == "auto":
        device = "cuda" if torch.cuda.is_available() else "cpu"
    device = torch.device(device)
    use_amp = device.type == "cuda"
    dtype = torch.bfloat16 if torch.cuda.is_bf16_supported() else torch.float16

    print(f"Device: {device}" + (f" (AMP: {dtype})" if use_amp else ""))

    # Model
    config = CONFIGS[config_name]
    model = GPTModel(config).to(device)
    n_params = model.count_parameters()
    print(f"Model: {config_name} — {n_params:,} parameters ({n_params/1e6:.1f}M)")
    if device.type == "cuda":
        mem = model.estimate_memory_mb(batch_size, config.max_seq_len)
        print(f"Estimated memory: {mem['total_est_mb']:.0f} MB")

    # Data
    tokenizer = Tokenizer()
    train_ds, val_ds = get_dataset(data_name, tokenizer, config.max_seq_len)
    train_loader = DataLoader(train_ds, batch_size=batch_size, shuffle=True, drop_last=True)
    val_loader = DataLoader(val_ds, batch_size=batch_size, shuffle=False, drop_last=True)

    # Optimizer — AdamW with weight decay only on 2D parameters (not biases, norms)
    param_groups = [
        {"params": [p for p in model.parameters() if p.dim() >= 2], "weight_decay": weight_decay},
        {"params": [p for p in model.parameters() if p.dim() < 1], "weight_decay": 0.0},
    ]
    optimizer = torch.optim.AdamW(param_groups, lr=max_lr, betas=(0.9, 0.95))

    # Mixed precision scaler
    scaler = torch.amp.GradScaler(enabled=use_amp)

    # Training loop
    model.train()
    train_iter = iter(train_loader)
    tokens_processed = 0
    best_val_loss = float("inf")
    t0 = time.time()

    print(f"\nTraining for {max_steps} steps (batch={batch_size}, accum={grad_accum_steps})")
    print(f"Effective batch: {batch_size * grad_accum_steps} sequences")
    print("-" * 60)

    for step in range(max_steps):
        # Update learning rate
        lr = get_lr(step, warmup_steps, max_steps, max_lr, min_lr)
        for pg in optimizer.param_groups:
            pg["lr"] = lr

        # Gradient accumulation loop
        optimizer.zero_grad()
        accum_loss = 0.0

        for micro_step in range(grad_accum_steps):
            # Get next batch (cycle through dataset)
            try:
                x, y = next(train_iter)
            except StopIteration:
                train_iter = iter(train_loader)
                x, y = next(train_iter)

            x, y = x.to(device), y.to(device)

            # Forward pass with mixed precision
            with torch.amp.autocast(device_type=device.type, dtype=dtype, enabled=use_amp):
                logits, _ = model(x)
                loss = torch.nn.functional.cross_entropy(
                    logits.view(-1, logits.size(-1)), y.view(-1)
                )
                loss = loss / grad_accum_steps  # Scale for accumulation

            scaler.scale(loss).backward()
            accum_loss += loss.item()
            tokens_processed += x.numel()

        # Gradient clipping + optimizer step
        scaler.unscale_(optimizer)
        torch.nn.utils.clip_grad_norm_(model.parameters(), grad_clip)
        scaler.step(optimizer)
        scaler.update()

        # Logging
        if step % log_interval == 0:
            elapsed = time.time() - t0
            tok_per_sec = tokens_processed / elapsed if elapsed > 0 else 0
            print(
                f"step {step:5d} | loss {accum_loss:.4f} | lr {lr:.2e} | "
                f"{tok_per_sec:.0f} tok/s"
            )

        # Validation
        if step > 0 and step % eval_interval == 0:
            val_loss = evaluate(model, val_loader, device, eval_steps, use_amp, dtype)
            print(f"  >>> val loss: {val_loss:.4f} (perplexity: {math.exp(val_loss):.1f})")
            if val_loss < best_val_loss:
                best_val_loss = val_loss
                save_checkpoint(model, optimizer, step, val_loss, config_name)
                print(f"  >>> saved best checkpoint (val_loss={val_loss:.4f})")
            model.train()

        # Periodic save
        if step > 0 and step % save_interval == 0:
            save_checkpoint(model, optimizer, step, accum_loss, config_name, suffix=f"step{step}")

    # Final evaluation
    val_loss = evaluate(model, val_loader, device, eval_steps, use_amp, dtype)
    print(f"\nFinal val loss: {val_loss:.4f} (perplexity: {math.exp(val_loss):.1f})")
    save_checkpoint(model, optimizer, max_steps, val_loss, config_name, suffix="final")
    print(f"Training complete. Total tokens: {tokens_processed:,}")


@torch.no_grad()
def evaluate(
    model: GPTModel,
    val_loader: DataLoader,
    device: torch.device,
    max_steps: int = 20,
    use_amp: bool = False,
    dtype: torch.dtype = torch.float16,
) -> float:
    """Run validation and return average loss."""
    model.eval()
    total_loss = 0.0
    n_steps = 0

    for x, y in val_loader:
        if n_steps >= max_steps:
            break
        x, y = x.to(device), y.to(device)
        with torch.amp.autocast(device_type=device.type, dtype=dtype, enabled=use_amp):
            logits, _ = model(x)
            loss = torch.nn.functional.cross_entropy(
                logits.view(-1, logits.size(-1)), y.view(-1)
            )
        total_loss += loss.item()
        n_steps += 1

    return total_loss / max(n_steps, 1)


def save_checkpoint(
    model: GPTModel,
    optimizer: torch.optim.Optimizer,
    step: int,
    loss: float,
    config_name: str,
    suffix: str = "best",
) -> None:
    """Save model checkpoint."""
    CHECKPOINT_DIR.mkdir(parents=True, exist_ok=True)
    path = CHECKPOINT_DIR / f"{config_name}_{suffix}.pt"
    torch.save({
        "step": step,
        "loss": loss,
        "config_name": config_name,
        "model_state_dict": model.state_dict(),
        "optimizer_state_dict": optimizer.state_dict(),
    }, path)


def main():
    parser = argparse.ArgumentParser(description="Train GPT model")
    parser.add_argument("--config", default="tiny", choices=list(CONFIGS.keys()))
    parser.add_argument("--data", default="shakespeare")
    parser.add_argument("--device", default="auto")
    parser.add_argument("--max-steps", type=int, default=5000)
    parser.add_argument("--batch-size", type=int, default=8)
    parser.add_argument("--grad-accum", type=int, default=4)
    parser.add_argument("--lr", type=float, default=3e-4)
    parser.add_argument("--eval-interval", type=int, default=250)
    args = parser.parse_args()

    train(
        config_name=args.config,
        data_name=args.data,
        device=args.device,
        max_steps=args.max_steps,
        batch_size=args.batch_size,
        grad_accum_steps=args.grad_accum,
        max_lr=args.lr,
        eval_interval=args.eval_interval,
    )


if __name__ == "__main__":
    main()
