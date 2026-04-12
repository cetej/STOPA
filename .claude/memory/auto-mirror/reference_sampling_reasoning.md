---
name: Inference-Time Sampling for Reasoning (arXiv:2510.14901)
description: Base models have untapped reasoning potential via MCMC sampling from power distributions — no RL training needed
type: reference
---

# Reasoning with Sampling (arXiv:2510.14901)

**Authors**: Aayush Karan, Yilun Du (Harvard)

## Core Claim

Base models already contain substantial latent reasoning capability. Inference-time sampling from **p^α** (power distributions) can nearly match or outperform RL post-training (GRPO) — **without any training, verifiers, or curated datasets**.

## Method

- **Algorithm**: Metropolis-Hastings MCMC with sequential block processing
- **Target distribution**: p^α — upweights high-likelihood tokens with fewer but higher-likelihood "future paths" (vs low-temperature sampling which is greedy)
- **No verifier needed** — unlike most inference-time compute methods
- **Cost**: ~8.84× standard inference tokens overhead

## Results vs GRPO (RL baseline)

| Benchmark | Method | GRPO |
|-----------|--------|------|
| MATH500 | 74.8% | 78.5% |
| HumanEval | **57.3%** | 53.7% |
| GPQA | substantial gains | — |

Tested on: Qwen2.5-Math-7B, Qwen2.5-7B, Phi-3.5-mini-instruct

**Key advantage**: maintains generation diversity — RL post-training causes diversity collapse.

## Relevance to STOPA

1. **Model tier selection**: base models (not instruction-tuned) may be worth considering for iterative reasoning tasks — their p^α is richer
2. **Inference-time scaling**: this validates the "thinking budget" pattern — more inference compute > fine-tuning for reasoning
3. **Pass@k diversity**: for `/autoresearch` and `/autoloop` — sampling approaches maintain diversity better than deterministic RL-trained models
4. **Training-free**: aligns with STOPA's preference for skill-level orchestration over fine-tuning

## How to Apply

- When choosing models for iterative reasoning loops (autoloop, autoresearch): consider that a base model with sampling strategy may outperform a fine-tuned smaller model
- High temperature + iterative sampling > greedy decoding for reasoning tasks
- The 8.84× token overhead means this approach costs ~9× more inference — factor into budget tier decisions
