"""Phase 4A: LoRA — Low-Rank Adaptation.

Paper: "LoRA: Low-Rank Adaptation of Large Language Models" (Hu et al., 2021)

Instead of fine-tuning all model weights, LoRA freezes the original weights
and adds small trainable low-rank matrices (A, B) to selected layers:
    W' = W + BA    where B ∈ ℝ^(d×r), A ∈ ℝ^(r×d), r << d

Benefits:
- 10-100× fewer trainable parameters
- No inference overhead (merge A,B back into W)
- Multiple LoRA adapters can share the same base model
- The dominant fine-tuning method in practice (QLoRA, etc.)
"""
