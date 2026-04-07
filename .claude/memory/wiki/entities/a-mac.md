---
name: A-MAC
type: paper
first_seen: 2026-04-07
last_updated: 2026-04-07
sources: [agent-memory-problems]
tags: [memory, security, admission-control]
---

# A-MAC

> Guilin Dev et al. 2026 (arXiv:2603.04549) — write-time admission control pro LLM agentní paměť. Gate odmítne low-confidence entries před zápisem místo retroaktivní opravy.

## Key Facts

- 5-faktorové skórování: future utility, factual confidence, semantic novelty, temporal recency, content type priority (ref: sources/agent-memory-problems.md)
- F1 0.583 na LoCoMo benchmark, 31% snížení latence
- Klíčový insight: zabránit zápisu špatné paměti > retroaktivní oprava
- Inspirace pro STOPA `learning-admission.py` hook (soft gate s salience scoring)

## Relevance to STOPA

STOPA `learning-admission.py` hook (PreToolUse na zápis do learnings/) je přímá implementace A-MAC vzoru. Soft gate — neblokuje, ale varuje. `source:` weighting (user_correction 1.5× > agent_generated 0.8×) je analogie A-MAC factual confidence faktoru.

## Mentioned In

- [Agent Memory Problems Research](../sources/agent-memory-problems.md)
