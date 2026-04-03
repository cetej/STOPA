---
date: 2026-04-01
status: DONE
component: skill
tags: [council, review, karpathy]
---

# 0002 — Council pattern adopted from Karpathy

## Context
Needed structured multi-perspective decision-making for architecture choices and technology selection.

## Decision
New `/council` skill + `--council` flag in `/critic` and `/pr-review`. Anonymized cross-review with aggregate ranking.

## Consequences
- Council available for any decision needing 3+ perspectives
- Integrated into existing review workflows via flag
