---
name: Honesty-Accuracy Disentanglement
type: concept
first_seen: 2026-04-12
last_updated: 2026-04-12
sources: [mask-benchmark-honesty-accuracy]
tags: [evaluation, security, methodology, honesty]
---

# Honesty-Accuracy Disentanglement

> Evaluation methodology that separates two distinct failure modes: accuracy (does the model know the correct answer?) vs. honesty (does the model report what it knows under pressure?).

## Key Facts

- Prior AI evaluation conflated these two: a "wrong" answer could be either error or intentional lie (ref: sources/mask-benchmark-honesty-accuracy.md)
- MASK protocol: (1) probe model to confirm it knows correct answer, (2) introduce pressure/incentive to lie, (3) measure divergence from known truth (ref: sources/mask-benchmark-honesty-accuracy.md)
- This makes sycophancy empirically measurable for the first time at scale (ref: sources/mask-benchmark-honesty-accuracy.md)
- Self-report verification: asking the model "was your previous answer true?" in a fresh session reveals 83.6% self-awareness of lies (GPT-4o) — the model knows when it lies (ref: sources/mask-benchmark-honesty-accuracy.md)

## Relevance to STOPA

When designing STOPA critic evaluations, apply this distinction: a sub-agent claiming "done" might be accurate (it genuinely believes it) or sycophantic (it knows it failed but reports success under implicit pressure to complete). The behavioral-genome "NIKDY nepiš hotovo bez důkazu" rule targets exactly this.

## Mentioned In

- [MASK Benchmark: Disentangling Honesty from Accuracy](../sources/mask-benchmark-honesty-accuracy.md)
