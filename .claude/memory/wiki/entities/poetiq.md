---
name: Poetiq
type: company
first_seen: 2026-04-13
last_updated: 2026-04-13
sources: [harness-engineering-moat-poetiq]
tags: [ai-tools, orchestration, arc-agi, benchmark]
---

# Poetiq

> Startup založený ex-DeepMind výzkumníky. Dosáhl SOTA na ARC-AGI-2 (54%, $30.57/problém) bez vlastního modelu — jen recursive meta-system nad Gemini 3 Pro.

## Key Facts

- ARC-AGI-2: 54% accuracy, $30.57/problém — překonal Gemini 3 Deep Think (45%, $77.16) (ref: sources/harness-engineering-moat-poetiq.md)
- Gemini 3 Pro baseline: 31% za $0.81 → Poetiq orchestrace zvedla na 54% za 38× cenu — ROI z orchestrace (ref: sources/harness-engineering-moat-poetiq.md)
- Metoda: dekompozice puzzlů, generace Python programů, execution, failure analysis, self-auditing termination (ref: sources/harness-engineering-moat-poetiq.md)
- Žádný vlastní trénink — čistě inference-time orchestrace (ref: sources/harness-engineering-moat-poetiq.md)
- Založen ex-DeepMind výzkumníky (ref: sources/harness-engineering-moat-poetiq.md)

## Relevance to STOPA

Poetiq je živý důkaz STOPA teze: orchestrační vrstva nad commodity modelem vytváří víc hodnoty než samotný model. Jejich architektura (decompose → generate → execute → analyze failures → self-audit termination) odpovídá STOPA orchestrate patternu. Self-auditing termination = budget-aware circuit breaker.

## Mentioned In

- [Harness Engineering Moat + Poetiq](../sources/harness-engineering-moat-poetiq.md)
