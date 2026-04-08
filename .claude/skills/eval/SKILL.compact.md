---
name: eval
variant: compact
description: Condensed eval for repeat invocations within session. Use full SKILL.md for first invocation.
---

# Eval — Compact (Session Re-invocation)

Grade harness traces, optimization runs, and failure patterns.

## Modes

| Mode | Trigger | What it does |
|------|---------|-------------|
| `--list` | no args | Scan .harness/traces/*.jsonl, show index |
| grade | trace file given | Structural validation + quality metrics + baseline comparison |
| `--diff t1 t2` | two traces | Phase-by-phase drift analysis, root cause classification |
| `--replay` | trace + harness | Re-run harness, auto-diff against original |
| `--baseline` | trace file | Lock as regression reference |
| `--optim [run]` | .traces/ dir | Grade optimization runs (proposal_quality, convergence_efficiency) |
| `--experiments` | list/top-k/pareto/diff | Unified query CLI over all optimization experiments |
| `--meta [target]` | .traces/ | Cross-run strategy effectiveness + target fragility |
| `--failures` | failures/ dir | HERA failure pattern analysis |

## Key Metrics

**Harness traces:** pass_rate, retry_rate, preflight_score, phase_coverage, harness_health (composite).
**Optimization runs:** proposal_quality, trace_utilization, convergence_efficiency, plateau_escape_rate, discard_to_keep_ratio.
**Meta-analysis:** strategy keep rates, target fragility (crash_rate + revert_rate), temporal improvement trends.

## Critical Rules

- Read-only — never modify trace files
- Isolate harness quality from model quality (note model changes)
- baseline.jsonl is sacred — never overwrite without explicit --baseline
- Missing JSONL fields → "n/a", never fail on incomplete traces
- Median reporting (Meta-Harness-inspired) — best-only hides typical improvement
