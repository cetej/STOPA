---
title: "Gradient Descent Optimization Algorithms — Ruder Survey + Post-2017 Landscape"
slug: gradient-descent-research
source_type: research_output
date_ingested: 2026-04-07
entities_extracted: 10
claims_extracted: 4
---

# Gradient Descent Optimization Algorithms — Ruder Survey + Post-2017 Landscape

> **TL;DR**: Ruder's 2016/2017 survey (arXiv:1609.04747) is the most-cited GD overview (~6,700 citations) covering 9 algorithms from Momentum to AMSGrad, recommending Adam as best overall. Since the last revision (June 2017), 20+ significant optimizers have been published; the most critical gap is AdamW (decoupled weight decay, now the transformer de facto standard). Learning-rate-free methods (Prodigy, Schedule-Free) and second-order approaches (SOAP, Sophia) represent the 2024 frontier.

## Key Claims

1. Adam is recommended as best overall optimizer in the survey; AMSGrad added in blog update 2018 — `[verified]`
2. AdamW (arXiv:1711.05101) is now the de facto standard for transformer training; the original paper doesn't cover it — `[verified]`
3. Schedule-Free optimizer (arXiv:2405.15682) eliminates LR schedule entirely and won MLCommons AlgoPerf 2024 — `[verified]`
4. SOAP (arXiv:2409.11321) runs Adam in Shampoo's eigenbasis, achieving 40% fewer iterations than Adam — `[verified]`

## Entities

| Entity | Type | Status |
|--------|------|--------|
| Sebastian Ruder | person | new |
| AdamW | concept | new |
| Schedule-Free Optimizer | concept | new |
| SAM (Sharpness-Aware Minimization) | concept | new |
| SOAP Optimizer | concept | new |
| Prodigy Optimizer | concept | new |
| Lion Optimizer | concept | new |
| Sophia Optimizer | concept | new |
| arXiv:1609.04747 (Ruder) | paper | new |
| D-Adaptation | concept | new |

## Relations

- Sebastian Ruder `authored` arXiv:1609.04747 (Ruder)
- AdamW `supersedes` Adam (for transformer training, weight decay correctness)
- Schedule-Free Optimizer `supersedes` D-Adaptation (improved version by same authors)
- Prodigy Optimizer `extends` D-Adaptation (LR-free learning)
- SOAP Optimizer `combines` Adam (in Shampoo eigenbasis)
