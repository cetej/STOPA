---
name: AutoAgent — autonomous harness engineering
description: Open-source meta-agent that autonomously improves task-agent harnesses via trace-based iteration; first to beat hand-tuned entries on SpreadsheetBench/TerminalBench
type: reference
---

## AutoAgent (kevinrgu/autoagent)

- **Repo**: github.com/kevinrgu/autoagent (Python 3.12, no license yet, 2026-04-03)
- **Architecture**: meta-agent edits single-file harness (`agent.py`), Harbor adapter runs parallel Docker sandboxes for evaluation
- **Benchmarks**: SpreadsheetBench 96.5% (#1), TerminalBench 55.1% (#1) — all other entries hand-engineered

## Key Findings

1. **Same-model empathy**: Claude meta + Claude task > Claude meta + GPT task. Shared weights mean the meta-agent writes harnesses the inner model actually understands. Validates STOPA's same-model-family approach.

2. **Anti-overfitting guard**: "If this exact task disappeared, would this still be a worthwhile harness improvement?" Simple but effective check against metric gaming.

3. **Traces are everything**: Score-only feedback drops improvement rate hard. Understanding WHY something improved matters as much as knowing THAT it improved. Validates Meta-Harness paper (arXiv:2603.28052) already integrated in STOPA.

4. **Codex/weak models fail as meta-agents**: Ignore instructions to keep improving, give up early. Confirms STOPA's model tier choices (never use weak models for meta-reasoning).

5. **Splitting helps**: Being good at a domain and being good at improving at that domain are different capabilities. Meta/task split lets each specialize.

## Emergent Behaviors (not programmed)

- **Spot-checking**: ran isolated tasks for risky edits instead of full suite
- **Forced verification loops**: built deterministic self-checks, budgeted extra turns for self-correction
- **Writing tests**: steered task agent to build own unit tests per task
- **Progressive disclosure**: dumped long contexts to files when results overflowed
- **Orchestration logic**: built task-specific subagents when domain required it

## STOPA Relevance

- Validates existing: trace-based improvement, adversarial co-evolution, autoharness, warm-start
- Gap: no parallel candidate evaluation (sequential only)
- Gap: spot-checking is hardcoded (critic gates), not learned/adaptive
- Integrated: overfitting guard added to autoloop/autoresearch reward hacking detection
