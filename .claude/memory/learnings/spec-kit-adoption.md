---
date: 2026-03-23
type: best_practice
severity: medium
component: orchestration
tags: [competitive-analysis, spec-kit, constitution, handoff]
summary: "spec-kit patterns worth adopting: constitution files, structured handoffs, role separation. Already partially in STOPA."
---

## Problém
Competitive analysis github/spec-kit (81k stars, 7 months). Spec-Driven Development toolkit.

## Root Cause
N/A — adoption analysis, not bug fix.

## Reseni
3 adopted patterns: (1) Constitution check — project governance doc as non-negotiable authority in /orchestrate and /brainstorm, (2) Handoff metadata — `handoffs:` field in skill frontmatter defines workflow graph, (3) Requirements-level checklist — "Are requirements defined for X?" + traceability tags [Spec], [Gap], [Ambiguity] in /critic --spec.

## Prevence
Hard question limits (max 3 open markers) force action over analysis paralysis. Spec-kit is document-generation tool, STOPA is execution system — complementary, not competing. Threat level LOW.
