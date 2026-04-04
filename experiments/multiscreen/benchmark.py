"""
Benchmark: Multiscreen vs Standard Transformer
Compares parameter count, training loss, and inference speed.

Task: Next-token prediction on synthetic data (repeated patterns + noise)
"""

import sys
import time

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import torch
import torch.nn as nn

# Support both `python benchmark.py` (from within dir) and `python -m multiscreen.benchmark`
try:
    from multiscreen.lm import MultiScreenLM, TransformerLM
    from multiscreen.core import ScreeningUnit
except ImportError:
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    from multiscreen.lm import MultiScreenLM, TransformerLM
    from multiscreen.core import ScreeningUnit


def count_params(model: nn.Module) -> int:
    return sum(p.numel() for p in model.parameters())


def generate_synthetic_data(
    n_samples: int, seq_len: int, vocab_size: int
) -> tuple[torch.Tensor, torch.Tensor]:
    """Generate data with learnable patterns (not just random noise).

    Creates sequences with:
    - Repeated sub-patterns (e.g., A B C D A B C D)
    - Local correlations (next token depends on previous 2-3 tokens)
    """
    data = torch.zeros(n_samples, seq_len + 1, dtype=torch.long)

    for i in range(n_samples):
        # Mix of pattern types
        pattern_type = i % 3

        if pattern_type == 0:
            # Repeating pattern of length 4-8
            pat_len = 4 + (i % 5)
            pattern = torch.randint(0, vocab_size, (pat_len,))
            reps = (seq_len + 1 + pat_len - 1) // pat_len
            data[i] = pattern.repeat(reps)[: seq_len + 1]

        elif pattern_type == 1:
            # Arithmetic-like: each token = (prev + offset) % vocab
            offset = 1 + (i % 10)
            data[i, 0] = torch.randint(0, vocab_size, (1,))
            for j in range(1, seq_len + 1):
                data[i, j] = (data[i, j - 1] + offset) % vocab_size

        else:
            # Bigram pattern: next token depends on current
            bigram_table = torch.randint(0, vocab_size, (vocab_size,))
            data[i, 0] = torch.randint(0, vocab_size, (1,))
            for j in range(1, seq_len + 1):
                data[i, j] = bigram_table[data[i, j - 1]]

    inputs = data[:, :-1]
    targets = data[:, 1:]
    return inputs, targets


def train_epoch(
    model: nn.Module,
    inputs: torch.Tensor,
    targets: torch.Tensor,
    optimizer: torch.optim.Optimizer,
    batch_size: int = 32,
) -> float:
    """Train one epoch, return average loss."""
    model.train()
    total_loss = 0.0
    n_batches = 0

    for i in range(0, len(inputs), batch_size):
        batch_x = inputs[i : i + batch_size]
        batch_y = targets[i : i + batch_size]

        optimizer.zero_grad()
        _, loss = model(batch_x, batch_y)
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        optimizer.step()

        total_loss += loss.item()
        n_batches += 1

    return total_loss / n_batches


@torch.no_grad()
def measure_inference(
    model: nn.Module, inputs: torch.Tensor, n_runs: int = 5
) -> float:
    """Measure average inference time per batch."""
    model.eval()
    batch = inputs[:32]

    # Warmup
    for _ in range(2):
        model(batch)

    times = []
    for _ in range(n_runs):
        start = time.perf_counter()
        model(batch)
        elapsed = time.perf_counter() - start
        times.append(elapsed)

    return sum(times) / len(times)


def inspect_screening_params(model: MultiScreenLM):
    """Print learned screening parameters (r, w) for each tile."""
    print("\n=== Learned Screening Parameters ===")
    for i, layer in enumerate(model.layers):
        for j, tile in enumerate(layer.tiles):
            r = torch.exp(tile.screening.s_r).item() + 1.0
            w = torch.exp(tile.screening.s_w).item() + 1.0
            threshold = 1.0 - 1.0 / r
            print(
                f"  Layer {i}, Tile {j}: r={r:.2f} (threshold={threshold:.3f}), "
                f"w={w:.1f} (window)"
            )


def inspect_sparsity(model: MultiScreenLM, inputs: torch.Tensor):
    """Measure how sparse the screening attention actually is."""
    model.eval()
    batch = inputs[:8]
    x = model.embedding(batch)

    total_entries = 0
    total_zeros = 0

    with torch.no_grad():
        for layer in model.layers:
            h = layer.norm(x)
            for tile in layer.tiles:
                q = tile.W_q(h)
                k = tile.W_k(h)

                q_norm = torch.nn.functional.normalize(q, dim=-1)
                k_norm = torch.nn.functional.normalize(k, dim=-1)

                alpha = tile.screening._compute_relevance(q_norm, k_norm)

                total_entries += alpha.numel()
                total_zeros += (alpha == 0.0).sum().item()

            x = layer(x)

    sparsity = total_zeros / total_entries * 100
    print(f"\n=== Attention Sparsity: {sparsity:.1f}% zeros ===")
    print(f"  (Standard softmax attention: ~0% zeros)")


def main():
    print("=" * 60)
    print("  Multiscreen vs Transformer — Benchmark")
    print("  Based on arXiv:2604.01178")
    print("=" * 60)

    # Hyperparameters
    VOCAB_SIZE = 256
    SEQ_LEN = 128
    N_SAMPLES = 512
    N_EPOCHS = 20
    BATCH_SIZE = 32
    PSI = 4  # -> d_model=16, 4 layers, 4 tiles (tiny for CPU)

    # For fair comparison, match d_model
    d_model_ms = PSI * PSI  # = 16

    print(f"\nConfig: vocab={VOCAB_SIZE}, seq_len={SEQ_LEN}, "
          f"samples={N_SAMPLES}, epochs={N_EPOCHS}")
    print(f"Multiscreen: Ψ={PSI}, d_model={d_model_ms}, "
          f"layers={PSI}, tiles={PSI}")

    # Generate data
    print("\nGenerating synthetic data...")
    inputs, targets = generate_synthetic_data(N_SAMPLES, SEQ_LEN, VOCAB_SIZE)

    # --- Multiscreen model ---
    print("\n--- Multiscreen ---")
    ms_model = MultiScreenLM(
        vocab_size=VOCAB_SIZE, psi=PSI, d_k=16, d_v=32, max_seq_len=SEQ_LEN
    )
    ms_params = count_params(ms_model)
    print(f"Parameters: {ms_params:,}")

    # Paper claims stable training with LR=2^-4=0.0625 (much higher than typical)
    ms_opt = torch.optim.AdamW(ms_model.parameters(), lr=0.0625, betas=(0.9, 0.95))

    ms_losses = []
    for epoch in range(N_EPOCHS):
        loss = train_epoch(ms_model, inputs, targets, ms_opt, BATCH_SIZE)
        ms_losses.append(loss)
        if (epoch + 1) % 5 == 0:
            print(f"  Epoch {epoch+1:2d}: loss = {loss:.4f}")

    ms_time = measure_inference(ms_model, inputs)

    # --- Transformer baseline (matched d_model) ---
    print("\n--- Transformer Baseline ---")
    tf_model = TransformerLM(
        vocab_size=VOCAB_SIZE,
        d_model=d_model_ms,
        n_layers=PSI,
        n_heads=PSI,
        max_seq_len=SEQ_LEN,
    )
    tf_params = count_params(tf_model)
    print(f"Parameters: {tf_params:,}")

    tf_opt = torch.optim.AdamW(tf_model.parameters(), lr=0.001, betas=(0.9, 0.95))

    tf_losses = []
    for epoch in range(N_EPOCHS):
        loss = train_epoch(tf_model, inputs, targets, tf_opt, BATCH_SIZE)
        tf_losses.append(loss)
        if (epoch + 1) % 5 == 0:
            print(f"  Epoch {epoch+1:2d}: loss = {loss:.4f}")

    tf_time = measure_inference(tf_model, inputs)

    # --- Larger Transformer (matched loss target) ---
    # Paper claims ~40% fewer params at same loss. Let's also try a bigger Transformer.
    print("\n--- Transformer Larger (d_model=24, for loss matching) ---")
    tf_large = TransformerLM(
        vocab_size=VOCAB_SIZE,
        d_model=24,
        n_layers=PSI,
        n_heads=4,  # 24/4 = 6 dim per head
        max_seq_len=SEQ_LEN,
    )
    tf_large_params = count_params(tf_large)
    print(f"Parameters: {tf_large_params:,}")

    tf_large_opt = torch.optim.AdamW(tf_large.parameters(), lr=0.001, betas=(0.9, 0.95))

    tf_large_losses = []
    for epoch in range(N_EPOCHS):
        loss = train_epoch(tf_large, inputs, targets, tf_large_opt, BATCH_SIZE)
        tf_large_losses.append(loss)
        if (epoch + 1) % 5 == 0:
            print(f"  Epoch {epoch+1:2d}: loss = {loss:.4f}")

    tf_large_time = measure_inference(tf_large, inputs)

    # --- Results ---
    print("\n" + "=" * 60)
    print("  RESULTS")
    print("=" * 60)

    print(f"\n{'Model':<25} {'Params':>10} {'Final Loss':>12} {'Inf. Time':>12}")
    print("-" * 60)
    print(f"{'Multiscreen (Ψ=4)':<25} {ms_params:>10,} {ms_losses[-1]:>12.4f} {ms_time*1000:>10.1f}ms")
    print(f"{'Transformer (d=16)':<25} {tf_params:>10,} {tf_losses[-1]:>12.4f} {tf_time*1000:>10.1f}ms")
    print(f"{'Transformer (d=24)':<25} {tf_large_params:>10,} {tf_large_losses[-1]:>12.4f} {tf_large_time*1000:>10.1f}ms")

    param_ratio = ms_params / tf_params
    speed_ratio = tf_time / ms_time

    print(f"\nMultiscreen vs Transformer (d=16):")
    print(f"  Parameter ratio: {param_ratio:.2f}x ({'+' if param_ratio > 1 else ''}{(param_ratio-1)*100:.0f}%)")
    print(f"  Speed ratio:     {speed_ratio:.2f}x {'faster' if speed_ratio > 1 else 'slower'}")
    print(f"  Loss delta:      {ms_losses[-1] - tf_losses[-1]:+.4f}")

    # Screening-specific analysis
    inspect_screening_params(ms_model)
    inspect_sparsity(ms_model, inputs)

    # Training dynamics: loss curve comparison
    print("\n=== Training Curves (every 2 epochs) ===")
    print(f"{'Epoch':>5} {'Multiscreen':>12} {'TF (d=16)':>12} {'TF (d=24)':>12}")
    for i in range(0, N_EPOCHS, 2):
        print(f"{i+1:>5} {ms_losses[i]:>12.4f} {tf_losses[i]:>12.4f} {tf_large_losses[i]:>12.4f}")

    print("\nDone.")


if __name__ == "__main__":
    main()
