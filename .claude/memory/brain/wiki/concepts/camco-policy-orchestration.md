---
title: CAMCO — Constraint-Aware Multi-Agent Cognitive Orchestration
category: concepts
tags: [multi-agent, orchestration, enterprise, compliance, safety, policy]
sources: [arXiv:2604.17240]
updated: 2026-04-23
---

# CAMCO — Constraint-Aware Multi-Agent Cognitive Orchestration

**Paper**: arXiv:2604.17240  
**Authors**: Vinil Pasupuleti (IBM), Shyalendar Reddy Allala (Global Atlantic), Siva Bayyavarapu (DocuSign), Shrey Tyagi (Salesforce)

## Core Problem

Existing multi-agent frameworks "optimize expected reward while treating constraints implicitly." In regulated industries (SOX, HIPAA, GDPR), implicit constraints cause compliance violations that cannot be retroactively corrected.

## Solution: Constraint-Explicit Middleware

CAMCO operates as a deployment-time middleware layer (not training-time). Three core mechanisms:

| Mechanism | Function |
|-----------|----------|
| **Constraint Projection Engine** | Maps regulatory rules to per-action constraints |
| **Adaptive Risk-Weighted Lagrangian Utility Shaping** | Penalizes high-risk actions dynamically |
| **Iterative Negotiation Protocol** | Agents negotiate alternative actions when primary choice violates constraints |

**Integration**: Compatible with OPA (Open Policy Agent) for enterprise policy engines.

## Quantitative Results

| Metric | Value |
|--------|-------|
| Policy violations | 0 (across all test scenarios) |
| Risk exposure ratio | 0.71 mean (below threshold) |
| Utility retention | 92–97% |
| Convergence speed | 2.4 iterations mean |

**Key insight**: Constraint satisfaction with ~95% utility retention — compliance doesn't require abandoning performance.

## Architecture Position

```
Agent Pool → CAMCO Middleware → Policy Engine (OPA) → Execution
             ↑ constraint projection, negotiation, risk weighting
```

CAMCO sits between agents and execution, not between agents and the LLM. Agents don't change; the middleware enforces.

## STOPA Relevance

STOPA lacks explicit constraint enforcement — agents can take any action the LLM decides. Patterns applicable:
- **Constraint projection**: extend behavioral-genome.md rules into machine-checkable policy format
- **Iterative negotiation**: currently STOPA falls back (stop + ask); negotiation loop = find compliant alternative autonomously
- **Risk weighting**: budget-tier system is a primitive form of risk weighting (light → deep)

CAMCO = formalized version of STOPA's circuit-breaker + behavioral-genome combination.

## Related Concepts

→ [multi-agent-orchestration-protocols.md](multi-agent-orchestration-protocols.md)  
→ [context-kubernetes.md](context-kubernetes.md)  
→ [prompt-injection-defense.md](prompt-injection-defense.md)  
→ [adaptive-orchestration-dmoe.md](adaptive-orchestration-dmoe.md)
