---
name: p-alpha-sampling
type: concept
first_seen: 2026-04-08
last_updated: 2026-04-08
sources: [reasoning-with-sampling]
tags: [inference-time, sampling, reasoning, mcmc]
---

# p-alpha-sampling

> MCMC-based inference-time method that samples from sharpened model distributions (p^α) to elicit latent reasoning without training.

## Key Facts

- Algorithm: Metropolis-Hastings MCMC with sequential block processing (ref: sources/reasoning-with-sampling.md)
- p^α upweights tokens with fewer but higher-likelihood "future paths" — vs low-temperature greedy which is myopic (ref: sources/reasoning-with-sampling.md)
- Requires no verifier, no curated data, no fine-tuning — works on base models directly (ref: sources/reasoning-with-sampling.md)
- Token overhead: ~8.84× standard inference (ref: sources/reasoning-with-sampling.md)
- MATH500: 74.8% vs GRPO 78.5%; HumanEval: 57.3% vs GRPO 53.7% (ref: sources/reasoning-with-sampling.md)
- Maintains generation diversity — unlike RL post-training which causes diversity collapse (ref: sources/reasoning-with-sampling.md)

## Relevance to STOPA

Validates the Best-of-N strategy used in `/autoloop` and `/autoresearch`: sampling multiple variants from a model preserves diversity better than fine-tuned models. Direct API access to base models + raw logprobs not available, so full MCMC implementation is out of scope — but the diversity-preservation principle applies to all iterative skills.

## Mentioned In

- [Reasoning with Sampling (arXiv:2510.14901)](../sources/reasoning-with-sampling.md)
