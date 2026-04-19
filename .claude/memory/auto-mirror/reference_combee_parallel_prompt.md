---
name: Combee parallel prompt learning
description: arXiv:2604.04247 — √n hierarchical aggregation, augmented shuffling, dynamic batch sizing for 17x speedup in prompt self-improvement
type: reference
---

## Combee: Scaling Prompt Learning for Self-Improving LM Agents

**Paper:** arXiv:2604.04247 (Li et al., Berkeley/Stanford, 2026-04-05)

### Core Problem
Naive parallel prompt learning causes "lossy compression" — aggregator LLM drops high-value task-specific insights when processing many reflections at once. Accuracy drops 87%→72.5% at batch 100 (Formula), context entries collapse 264→21.

### Three Components

1. **Parallel Scan Aggregation**: Tree-based, k=√n subgroups, 2-level merge. Each node processes √n items instead of n → prevents overload.

2. **Augmented Shuffling**: Duplicate each reflection p times (default p=2), shuffle before distribution. Self-consistency principle — increases survival chance of high-value insights.

3. **Dynamic Batch Size Controller**: Power-law delay profiling. `T_epoch(bs) = A · bs^(-α)`, plateau at `(αA/τ)^(1/(α+1))` with τ=1.6%.

### Results
| Benchmark | Speedup | Sequential acc | Combee acc | Cost |
|-----------|---------|---------------|------------|------|
| AppWorld | 12× (86→7 min) | 58.1% | 65.8% | ~$1.67 |
| Terminal-Bench | 17× (42→2.4 min) | 37.9% | 35.6% | ~$0.17 |
| Formula | 2.4× faster | comparable | best | - |
| FiNER | <50% time | best fixed | matched | - |

### STOPA Integration Opportunities

1. **self-evolve / autoloop**: Currently sequential refinement. Combee's √n partition applicable when running multiple eval variants in parallel.
2. **Outcome aggregation**: outcomes/ batch processing at /evolve could use hierarchical merge instead of flat read.
3. **Learning retrieval**: Augmented shuffling principle — when presenting learnings to aggregator, duplicate high-confidence ones to prevent loss.
4. **Budget-adaptive batching**: Dynamic batch controller maps to STOPA tier system — light=small batch, deep=large batch with Combee aggregation.

### Key Formulas
- Sequential: `C_{t+1} = Update(C_t, Reflect(τ_t))`
- Parallel naive: `C_{t+1} = Update(C_t, Agg(F_1...F_bs))` → degrades
- Combee: `C_{t+1} = Update(C_t, Reduce(Map(Shuffle(F_1...F_bs), √n)))` → stable

### Ablation Insights
- Without shuffling: quality fluctuates significantly across subgroup sizes
- √n subgroup size validated as optimal (peak performance)
- Cross-model transfer confirmed (GPT-OSS 120B = DeepSeek-V3.1 patterns)
