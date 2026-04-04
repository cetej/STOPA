---
date: 2026-03-25
type: architecture
severity: high
component: skill
tags: [critic, verify, evaluation, os-themis, apm]
summary: "Decomposed evaluation (per-dimension scoring) catches 3x more issues than holistic review. Use in /critic and /verify."
source: external_research
uses: 1
confidence: 0.7
---

# Decomposed evaluation beats holistic review

## Pattern
Single-pass holistic review suffers from **evidence dilution** — accumulated trivial successes mask critical failures. Decomposing evaluation into specialized phases (Selector → Verifier → Reviewer → Judge) catches more issues.

## Key insights from OS-Themis (arXiv:2603.19191)
- **Assignment goals** (Selector tells Verifier exactly what to check): +8.2% precision — largest single gain
- **Reviewer-as-Critic** (strict auditor, not collaborative advisor): +7.1% precision
- **Judge** is most critical component — without it, recall collapses to 5%
- **False positives worse than false negatives** in quality assessment — pipeline should favor precision

## Key insights from APM Manifesto (arXiv:2603.18916)
- **Process Frames** formalize agent constraints: normative (MUST/MUST NOT) vs operational (specific steps)
- **7 orchestration patterns**: Sequential, Parallel, Routing, Managerial, Adaptive, Mesh, Self-orchestration
- **Verification Pattern**: one performer systematically reviews output of another

## Applied to STOPA
- `/critic` redesigned as 4-phase pipeline (QUICK path unchanged)
- `/orchestrate` agent templates now include structured Process Frames (MUST/MUST NOT/AUTONOMY SCOPE)
- `/verify` now extracts milestones before verification plan
