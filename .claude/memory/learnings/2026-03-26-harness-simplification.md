---
date: 2026-03-26
type: best_practice
severity: high
component: orchestration
tags: [harness, simplification, model-capability, architecture]
summary: "Modern Claude models handle multi-step reasoning natively. Simplify harnesses — remove unnecessary scaffolding, trust model capability."
source: external_research
related: [harness-engineering.md]
verify_check: "manual"
confidence: 0.7
uses: 0
successful_uses: 0
harmful_uses: 0
---

# Harness Simplification Principle

**Source:** Anthropic Engineering Blog — "Harness Design for Long-Running Application Development" (Prithvi Rajasekaran, 2026-03-24)

## Principle

Every component in an orchestration harness encodes an assumption about what the model can't do. As models improve, methodically remove components to identify what remains load-bearing. The design space for effective harnesses doesn't shrink — it moves toward more sophisticated orchestration.

## Key Findings

1. **Generator/Evaluator separation is load-bearing** — self-evaluation bias is persistent across model versions. Separate critic agents outperform self-critique consistently.

2. **Evaluator leniency is the #1 failure mode** — evaluators identify issues then talk themselves into dismissing them. Anti-leniency prompting is more tractable than making generators self-critical.

3. **Sprint contracts bridge spec-to-implementation gap** — explicit deliverables + testable success criteria before each phase prevents specification cascading errors.

4. **Cost reality: 22× for quality** — solo agent ($9/20min) vs. full harness ($200/6h) for same task, but harness produced functional result where solo failed. Budget tiers are justified.

5. **Opus 4.6 reduced need for context resets** — earlier versions needed full context clearing between agent swaps. Continuous sessions now work with 1M context.

## How to Apply in STOPA

- Periodically audit skills: which scaffolding assumptions still hold?
- /critic anti-leniency protocol (implemented 2026-03-26)
- /critic adaptive weight profiles per task type (implemented 2026-03-26)
- Don't add complexity unless evidence shows the model can't handle it without
- When adding a new skill component, document what model limitation it addresses
