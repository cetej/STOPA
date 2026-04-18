---
date: 2026-04-11
type: architecture
severity: medium
component: hook
tags: [security, prompt-injection, adaptive, static-defense, llamafirewall]
summary: "Strategy-based adaptive attacks (10 strategies + feedback refinement) achieve 86% ASR vs best static defense (PISanitizer), 2-8× higher than static attacks. PromptGuard ADOPT recommendation remains valid for static injection but needs adaptive complement."
source: external_research
maturity: draft
uses: 1
harmful_uses: 0
successful_uses: 0
confidence: 1.0
verify_check: "manual"
related: [2026-04-05-agent-defense-frameworks.md]
---

# Adaptive Attacks Defeat Static Defenses

## Finding

PIArena (arXiv:2604.08499) shows strategy-based adaptive attacks (attacker LLM uses feedback to adapt) achieve 86% ASR vs PISanitizer vs 11% for direct static attacks. Existing PromptGuard evaluation (AUC 0.98) used static attack types — not adaptive.

## Mechanism

Two-phase attack:
1. Generate N candidates using 10 strategies (Author's Note, System Update, etc.)
2. Refine based on defense feedback: stealth optimization (if detected) / imperativeness boost (if ignored) / general analysis

## Impact on STOPA

STOPA's content-sanitizer.py uses regex + PromptGuard (static BERT classifier). Both are static — they match known patterns, not adaptive adversaries. Against an actual adversary using strategy-based mutation, static defense will be probed until bypass is found.

## Mitigation

Short-term: PromptGuard ADOPT recommendation stands for opportunistic/script-kiddie attacks (no feedback loop). Long-term: behavioral constraints (CaMeL `[UNTRUSTED]` tagging + blocking privileged tool calls) reduce attack surface regardless of injection bypass.

**Why:** Static classifiers have fixed decision boundaries — an adaptive attacker with feedback will find the boundary and step just past it. Behavioral constraints (limiting what untrusted data can trigger) don't have this failure mode.
**How to apply:** Treat PromptGuard as opportunistic filter, not security guarantee. Pair with structural constraints: untrusted data sources cannot directly trigger state.md writes or tool calls to external APIs.
