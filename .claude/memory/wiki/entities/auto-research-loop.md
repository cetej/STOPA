---
name: Auto-Research Loop
type: concept
first_seen: 2026-04-08
last_updated: 2026-04-08
sources: [karpathy-nopriors-autoagent-loopy-era]
tags: [orchestration, research, pipeline, ai-tools]
---

# Auto-Research Loop

> Autonomous optimization loop: define objective + metric + boundaries → let agents iterate without human involvement; the human is the bottleneck by default and must be removed.

## Key Facts

- Core insight: anything with an objective metric that is cheap to verify but expensive to discover is a fit for auto-research (ref: sources/karpathy-nopriors-autoagent-loopy-era.md)
- Practical proof: overnight auto-research on Karpathy's "fairly well-tuned" GPT-2 repo found weight decay on value embeddings + untuned adam betas — things 20 years of manual tuning missed (ref: sources/karpathy-nopriors-autoagent-loopy-era.md)
- Anti-fits: anything without a verifiable objective — nuance, intent, when to ask clarifying questions — will "meander" (ref: sources/karpathy-nopriors-autoagent-loopy-era.md)
- Parallelization: the interesting next step is not a single loop but N loops collaborating (ref: sources/karpathy-nopriors-autoagent-loopy-era.md)
- Distributed variant: untrusted pool of internet workers; verification is cheap (just run the candidate); similar to folding@home / blockchain structure with commits as blocks (ref: sources/karpathy-nopriors-autoagent-loopy-era.md)
- Meta-optimization: "program.md" = research org as markdown files; run auto-research on the org itself to improve its methodology (ref: sources/karpathy-nopriors-autoagent-loopy-era.md)

## Relevance to STOPA

This is the conceptual foundation for `/autoresearch` and `/autoloop` skills. The "cheap to verify, expensive to discover" principle should be the first check before triggering either skill. The distributed variant is the future direction for STOPA farm-tier orchestration.

## Mentioned In

- [No Priors: Code Agents, AutoResearch, and the Loopy Era](../sources/karpathy-nopriors-autoagent-loopy-era.md)
