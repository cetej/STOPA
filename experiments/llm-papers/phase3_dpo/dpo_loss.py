"""DPO Loss Function.

Paper: "Direct Preference Optimization" (Rafailov et al., 2023)

The RLHF pipeline:
    1. Collect human preference data: (prompt, chosen, rejected)
    2. Train a reward model on preferences
    3. Use PPO to optimize the policy against the reward model
    → Complex, unstable, expensive

DPO insight: The optimal policy under RLHF has a closed-form relationship
with the reward function. So we can SKIP the reward model and optimize
preferences directly:

    L_DPO = -E[log σ(β · (log π_θ(y_w|x)/π_ref(y_w|x) - log π_θ(y_l|x)/π_ref(y_l|x)))]

Where:
    π_θ   = policy model (being trained)
    π_ref = reference model (frozen copy of π_θ before training)
    y_w   = chosen (winning) response
    y_l   = rejected (losing) response
    β     = temperature (higher = more conservative updates)
    σ     = sigmoid function

Intuition:
- Increase probability of chosen responses relative to reference
- Decrease probability of rejected responses relative to reference
- β controls how far the policy can drift from reference
"""

import torch
import torch.nn.functional as F


def compute_log_probs(
    logits: torch.Tensor,
    labels: torch.Tensor,
    mask: torch.Tensor | None = None,
) -> torch.Tensor:
    """Compute per-token log probabilities for given labels.

    Args:
        logits: (batch, seq_len, vocab_size) — model output
        labels: (batch, seq_len) — target token IDs
        mask: (batch, seq_len) — 1 for real tokens, 0 for padding

    Returns:
        (batch,) — sum of log probs per sequence
    """
    # Per-token log probs: log P(label_t | context)
    log_probs = F.log_softmax(logits, dim=-1)

    # Gather log probs for the actual tokens
    # labels.unsqueeze(-1) → (batch, seq_len, 1)
    per_token = log_probs.gather(-1, labels.unsqueeze(-1)).squeeze(-1)
    # per_token: (batch, seq_len)

    if mask is not None:
        per_token = per_token * mask

    # Sum over sequence → total log prob per sequence
    return per_token.sum(dim=-1)  # (batch,)


def dpo_loss(
    policy_chosen_logits: torch.Tensor,
    policy_rejected_logits: torch.Tensor,
    ref_chosen_logits: torch.Tensor,
    ref_rejected_logits: torch.Tensor,
    chosen_labels: torch.Tensor,
    rejected_labels: torch.Tensor,
    chosen_mask: torch.Tensor | None = None,
    rejected_mask: torch.Tensor | None = None,
    beta: float = 0.1,
) -> tuple[torch.Tensor, dict[str, float]]:
    """Compute DPO loss.

    The core formula:
        L = -log σ(β · (log_ratio_chosen - log_ratio_rejected))

    Where:
        log_ratio_chosen = log π_θ(y_w|x) - log π_ref(y_w|x)
        log_ratio_rejected = log π_θ(y_l|x) - log π_ref(y_l|x)

    Args:
        policy_chosen_logits: Policy model logits for chosen response
        policy_rejected_logits: Policy model logits for rejected response
        ref_chosen_logits: Reference model logits for chosen response
        ref_rejected_logits: Reference model logits for rejected response
        chosen_labels: Token IDs for chosen response
        rejected_labels: Token IDs for rejected response
        chosen_mask: Padding mask for chosen response
        rejected_mask: Padding mask for rejected response
        beta: Temperature parameter (higher = more conservative)

    Returns:
        loss: scalar DPO loss
        metrics: dict with debugging info
    """
    # Compute log probabilities under policy and reference
    pi_chosen = compute_log_probs(policy_chosen_logits, chosen_labels, chosen_mask)
    pi_rejected = compute_log_probs(policy_rejected_logits, rejected_labels, rejected_mask)
    ref_chosen = compute_log_probs(ref_chosen_logits, chosen_labels, chosen_mask)
    ref_rejected = compute_log_probs(ref_rejected_logits, rejected_labels, rejected_mask)

    # Log-ratios: how much the policy differs from reference
    log_ratio_chosen = pi_chosen - ref_chosen      # Should increase (prefer chosen)
    log_ratio_rejected = pi_rejected - ref_rejected  # Should decrease (avoid rejected)

    # DPO loss: -log σ(β * (log_ratio_chosen - log_ratio_rejected))
    logits_diff = beta * (log_ratio_chosen - log_ratio_rejected)
    loss = -F.logsigmoid(logits_diff).mean()

    # Metrics for monitoring
    with torch.no_grad():
        chosen_rewards = beta * log_ratio_chosen
        rejected_rewards = beta * log_ratio_rejected
        reward_margin = (chosen_rewards - rejected_rewards).mean().item()
        accuracy = (logits_diff > 0).float().mean().item()  # How often chosen > rejected

    metrics = {
        "loss": loss.item(),
        "reward_margin": reward_margin,
        "accuracy": accuracy,
        "chosen_reward": chosen_rewards.mean().item(),
        "rejected_reward": rejected_rewards.mean().item(),
    }

    return loss, metrics
