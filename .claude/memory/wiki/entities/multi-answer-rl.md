---
name: Multi-Answer RL (arXiv:2603.24844)
type: paper
first_seen: 2026-04-07
last_updated: 2026-04-07
sources: [beyond-mode-research]
tags: [rl, calibration, uncertainty, diverse-outputs, mit-csail]
---
# Multi-Answer RL (arXiv:2603.24844)

> MIT CSAIL paper by Puri et al. training LLMs via RLVR (GRPO) to generate K diverse answers in a single forward pass using structured `<answer1>…<answerK>` tags; 56% token savings vs best-of-K with improved calibration.

## Key Facts

- Single forward pass generates K candidates; reward = count of answers in ground-truth set; format reward enforces uniqueness (ref: sources/beyond-mode-research.md)
- 56% fewer tokens than best-of-K at same recall (ref: sources/beyond-mode-research.md)
- Prompt-only replication FAILS — fine-tuning required (4× A100, ~$50-150/run, Qwen3-8B only) (ref: sources/beyond-mode-research.md)
- Code: github.com/ishapuri/multi_answer_rl; no pre-trained weights published (ref: sources/beyond-mode-research.md)
- GRPO objective (no value model) trained with DeepSpeed + TRL (ref: sources/beyond-mode-research.md)
- Improves calibration: Brier score and ECE better than single-answer baseline (ref: sources/beyond-mode-research.md)

## Relevance to STOPA

Philosophy (outputs as distributions, not points) is directly applicable via prompt patterns to orchestrate skill: add confidence + key_uncertainties + alternative_if_wrong to plan output. Full fine-tuning only makes sense for ORAKULUM when labeled dataset of resolved predictions exists.

## Mentioned In

- [Reaching Beyond the Mode — Multi-Answer RL and Uncertainty Quantification](../sources/beyond-mode-research.md)
