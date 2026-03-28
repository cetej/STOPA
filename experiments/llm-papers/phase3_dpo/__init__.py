"""Phase 3B: Direct Preference Optimization (DPO).

Paper: "Direct Preference Optimization: Your Language Model is Secretly a Reward Model"
       (Rafailov et al., 2023)

DPO simplifies RLHF by eliminating the reward model and PPO loop.
Instead, it directly optimizes the policy using human preference pairs:
    (prompt, chosen_response, rejected_response)

The DPO loss implicitly defines a reward function from the language model
itself, making alignment much simpler to implement and more stable to train.
"""
