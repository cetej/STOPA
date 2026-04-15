---
date: 2026-04-08
type: best_practice
severity: high
component: orchestration
tags: [orchestration, research, pipeline, autoloop, autoresearch]
summary: "The human is always the bottleneck in iterative optimization. For any task with a cheap-to-verify objective metric, remove yourself from the loop: define objective + metric + boundaries, let agents iterate autonomously. Karpathy's overnight auto-research found issues 20 years of manual tuning missed."
source: external_research
uses: 1
successful_uses: 0
harmful_uses: 0
confidence: 0.95
failure_class:
verify_check: "manual"
---

## Detail

Karpathy framing (No Priors, 2026-03-20): "The name of the game is to increase your leverage — put in very few tokens just once in a while and a huge amount of stuff happens on your behalf."

The unlock condition: anything where **verification is cheap but discovery is expensive** fits auto-research:
- Hyperparameter optimization → train and measure loss (cheap verify)
- Code efficiency → run benchmark (cheap verify)
- NOT: nuance, intent, when to ask clarifying questions → no verifiable metric

Proof: overnight auto-research on a "fairly well-tuned" repo found untuned weight decay on value embeddings + suboptimal adam betas — things 2 decades of manual tuning had missed.

**How to apply in STOPA:**
- Before launching `/autoresearch` or `/autoloop`: confirm task has an objective metric that agents can verify autonomously
- If no such metric exists: auto-research is the wrong skill — use `/orchestrate` instead
- On multi-step research: your job is to define the metric and boundaries, then step away
