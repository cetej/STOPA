---
date: 2026-04-11
type: architecture
severity: medium
component: hook
tags: [security, prompt-injection, tradeoff, defense-design]
summary: "No current prompt injection defense achieves both high utility AND low ASR. Best security (SecAlign++, 21% ASR) requires accepting 45-84% utility loss. Best utility (PISanitizer, 99%) is defeated by adaptive attacks at 86% ASR. Layered architecture is the correct response."
source: external_research
uses: 0
harmful_uses: 0
successful_uses: 0
confidence: 0.7
verify_check: "manual"
---

# No Defense Achieves Security and Utility Simultaneously

## Finding

PIArena (arXiv:2604.08499) benchmarks across 9 defenses reveal fundamental tradeoff — no defense escapes it:

| Defense | Utility | ASR (adaptive) |
|---------|---------|----------------|
| PISanitizer | 99% | 86% |
| PIGuard | 72% | 79% |
| SecAlign++ | 45-84% | 21% |
| None | 100% | 99% |

Robustness training (GPT-4o-mini) worsens both dimensions: 76% ASR with likely utility degradation.

## Impact on STOPA

Single-layer defense design is doomed to either accept high ASR or accept utility loss. STOPA's current approach (regex + PromptGuard + user confirmation) is implicitly layered — this is validated.

## Correct Architecture

Each layer should sacrifice the MINIMUM utility for MAXIMUM security given its position:
1. **Structural constraints** (CaMeL `[UNTRUSTED]` tagging) — zero utility cost, catches privilege escalation
2. **Static classifiers** (PromptGuard) — minimal utility cost, catches opportunistic attacks
3. **User confirmation** — highest utility cost, use only for high-stakes tool calls
4. **Content verification** — applied post-response for RAG/summarization (no pre-execution cost)

**Why:** The tradeoff is fundamental, not implementation gap. Layering is the only way to distribute the security/utility cost across cases rather than applying maximum cost to all.
**How to apply:** When designing STOPA hook layers, assign each layer a failure class it handles — don't expect any single layer to solve all injection types.
