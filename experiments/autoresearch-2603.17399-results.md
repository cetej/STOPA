# Autoresearch Experiment: arXiv:2603.17399 Validation

**Date**: 2026-03-31
**Paper**: Bootstrapping Coding Agents (arXiv:2603.17399)
**Hypothesis**: Agent can re-implement a skill from description-only spec

## Setup

- **Target skill**: `/status` (81 lines, system dashboard)
- **Input to agent**: description field (1 sentence) + YAML metadata (tools, model, tags)
- **Agent model**: Sonnet
- **No access to**: original implementation, other skills, project conventions

## Results

| Metric | Value |
|--------|-------|
| Core functions captured | 4/5 (80%) |
| Data sources discovered | 4/7 (57%) |
| Missing features | eval_trend, perf_trend, context_budget |
| Novel additions by agent | Quick Actions section, detailed news parsing |
| Output format | Divergent (box-drawing vs plaintext) |
| Functional coverage estimate | ~60-70% |

## Analysis

### What the spec captured
- Task status from state.md
- Budget info from budget.md
- Checkpoint state from checkpoint.md
- News scan date from news.md
- Memory health check (line count warnings)

### What the spec missed
- eval-baseline.tsv health score trending
- performance/*.json run history
- session-stats.json context window budget
- Specific output format (key: value plaintext)
- Date math for "N days ago"

### Key insight
Description-only re-implementation captures the INTENT (~80%) but misses ACCUMULATED DESIGN DECISIONS (~40% of features). The missing features (eval trending, perf tracking, context budget) were added over multiple iterations and aren't implied by the description.

This validates the paper's core claim that "specification is the program" for initial implementation, but challenges it for mature skills where iterative refinement has added domain-specific features.

## Implications for STOPA

1. Skill descriptions should be enriched if we want bootstrapping to work better
2. Consider adding a `key-features:` frontmatter field listing non-obvious capabilities
3. The re-implementation's visual format (box-drawing dashboard) was arguably better than the original plaintext — worth considering as an upgrade

## Files

- Original: `.claude/commands/status.md` (restored from git)
- Re-implementation: `experiments/autoresearch-status-reimpl.md`
