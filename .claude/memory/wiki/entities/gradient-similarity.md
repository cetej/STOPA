---
name: Gradient Similarity
type: concept
first_seen: 2026-04-13
last_updated: 2026-04-13
sources: [nexus-common-minima-generalization]
tags: [optimization, multi-task, gradient-alignment]
---

# Gradient Similarity

> CosSim(nabla L_i, nabla L_j) — cosine similarity mezi gradienty různých training tasks. Proxy pro "closeness" v loss landscape: vysoká similarity → task minima jsou blízko → lepší downstream generalizace.

## Key Facts

- Theorem 3.1: gradient similarity upper bounds parameter closeness — optimalizovatelný proxy bez nutnosti znát individual task minima (ref: sources/nexus-common-minima-generalization.md)
- Maximalizace gradient similarity je ekvivalentní minimalizaci second-order objektivu J_2nd (Theorem 3.2) (ref: sources/nexus-common-minima-generalization.md)
- Prakticky: Nexus inner loop (sequential NSGD) automaticky generuje Hessian-gradient product = gradient of gradient similarity (ref: sources/nexus-common-minima-generalization.md)
- Musí být vanilla SGD (bez momentu) — momentum inner loop nemaximalizuje gradient similarity (experimentálně ověřeno) (ref: sources/nexus-common-minima-generalization.md)

## Relevance to STOPA

Gradient similarity jako metrika konfliktu/alignment mezi úkoly je transferable: pokud dva sub-tasky v orchestraci "táhnou" řešení opačným směrem, jejich "gradient similarity" je nízká → signál pro decomposition nebo re-prioritization. Analogie pro multi-objective critic scoring.

## Mentioned In

- [Nexus: Common Minima Generalization](../sources/nexus-common-minima-generalization.md)
