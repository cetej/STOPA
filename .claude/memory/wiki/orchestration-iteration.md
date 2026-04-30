---
generated: 2026-04-12
cluster: orchestration-iteration
sources: 22
last_updated: 2026-04-30
---

# Iterative Optimization Patterns

> **TL;DR**: Iterative refinement (autoloop, autoresearch, self-evolve) follows a "paradox" — early iterations are unreliable predictors of final quality, overfitting to eval metrics is the primary failure mode, and evolutionary approaches (EGGROLL) outperform gradient-based optimization for prompt tuning. Four 2026-04 additions sharpen the toolkit: **Best-of-N parallel candidates** replace linear try-fail-try sequences; **Parcae exponential decay** predicts iteration ceiling after 3-4 samples; **PRM step-verification** kills failing pipelines mid-flight instead of running to completion.

## Overview

STOPA's iterative skills (autoloop, autoresearch, self-evolve) share common optimization patterns distilled from research and practice. The iteration paradox reveals that performance at iterations 1-3 poorly predicts final outcome — patience through initial noise is essential (ref: 2026-04-11-iteration-paradox-meta-pattern.md). The primary risk is overfitting: agents optimize for the metric rather than the underlying goal, requiring explicit overfitting guards (ref: 2026-04-03-autoagent-overfitting-guard.md).

EGGROLL-style evolutionary optimization (low-rank ES with GRPO scoring) outperforms manual prompt engineering for prompt tuning tasks (ref: 2026-04-10-eggroll-evolutionary-optimization.md). The Claudini pattern shows that removing the human bottleneck from research loops (auto-hypothesis, auto-experiment, auto-analysis) dramatically increases throughput (ref: 2026-04-08-auto-research-removes-human-bottleneck.md).

### Three 2026-04 Sharpening Patterns

**Best-of-N with PRM scoring** (arXiv:2501.09686, ref: 2026-04-15-best-of-n-parallel-candidates.md) replaces linear iteration with parallel candidate generation: fork N=2-3 independent approaches, score each with a lightweight critic, expand the best. Explorational breadth beats depth-first retry — iterating on the best starting point converges faster than patching the first.

**Parcae exponential decay** (arXiv:2604.12946, ref: 2026-04-15-parcae-exponential-decay-stopping.md) models iterative compute as `L(T) = L∞ + Z·exp(-z·T)`. After 3-4 iterations the model fits with 0.85-1.3% prediction error — the predicted floor `L∞` tells you whether remaining iterations can possibly reach target, enabling early termination before burning compute. Plateau-detection ("3 iterations without improvement") is a lagging signal; fitted decay is leading.

**PRM step-verification** (ref: 2026-04-15-prm-step-verification-orchestrate.md) adds a haiku-level check after each subtask ("did this step satisfy the plan?") instead of running the full pipeline and critiquing at the end. Step-level rewards (Process Reward Models) dramatically outperform Outcome Reward Models for multi-step reasoning — identifies WHERE failure occurred, kills pipeline early on FAIL. Cost: ~200 tokens/subtask; ROI: skipped compute when step 2 of 6 fails.

### 2026-04-18 additions

**Autogenesis Protocol** (arXiv:2604.15034) formalizes self-evolving agents as two layers: RSPL (5 passive resource types: prompt/agent/tool/env/memory with explicit version+lifecycle) and SEPL (5 operators: Reflect ρ → Select σ → Improve ι → Evaluate ε → Commit κ). Key principle: decouple *what* evolves (resources) from *how* it evolves (operators). STOPA's self-evolve, autoloop, and autoresearch all implement ad-hoc versions of SEPL — formalizing them against Autogenesis enables trace-replay debugging and shared circuit breakers (ref: 2026-04-18-autogenesis-protocol.md). Already reflected in `rules/sepl-operators.md` and `rules/commit-invariants.md`.

**Simula reasoning-first taxonomies** (arXiv:2603.29791, TMLR 03/2026) introduces mechanism design as a synthetic-data axis orthogonal to quality/diversity/complexity. 3-stage pipeline: taxonomy via Best-of-N + critic refinement, taxonomic sampling + meta-prompts + complexification, double-critic verification. Applied to STOPA evals: eval cases should cover taxonomic axes (agent type × failure mode × complexity tier) rather than random sampling. Double-critic (one for correctness, one for coverage) catches blind spots the single-critic setup misses (ref: 2026-04-18-simula-reasoning-first-taxonomies.md).

**MASK honesty measurement** (paper) separates belief B from statement S: neutral prompt elicits belief, pressure prompt elicits statement, compare S≠B (lying) independently from B≠T (accuracy). Measuring only accuracy conflates two orthogonal dimensions — a model can be accurate while lying when pressured. Implementation: `/critic` should run neutral-then-pressure for deception-sensitive tasks (research citations, cost estimates, uncertainty calibration) (ref: 2026-04-18-mask-belief-vs-statement-pipeline.md).

### 2026-04-23/26 sharpening: confirmation bias, plan-quality vs execution, human delegation cap

**LLM confirmation bias is empirically dominant in scientific agents** (25K runs, 8 domains, 11 LLMs): 68% of traces ignore evidence, only 26% revise beliefs in light of refutation, 7% draw on independent evidence lines. Base model variance explained 41.4% of outcome differences vs 1.5% from scaffold — model > framework. Counter-example prompting raised rule-discovery from 42% to 56%. STOPA `/autoresearch`, `/deepresearch`, `/critic`, `/self-evolve` need an explicit falsification gate: "What evidence would refute this hypothesis? Have you looked for it?" — current confirmatory loops will compound bias rather than correct it (ref: 2026-04-23-llm-confirmation-bias.md).

**Plan quality dominates execution quality**. When agents report 100% subtask completion but `/verify` FAILs, the root cause is a wrong plan executed perfectly — not a bad agent. Re-running scout (re-plan from current evidence) outperforms retrying the same agents on the same plan. The diagnostic is the gap between agent self-reports and verify outcomes: matching reports + failing verify = plan defect; non-matching reports = execution defect. STOPA `/orchestrate` should treat "verify FAIL after clean agent reports" as scout-rerun signal, not retry signal (ref: 2026-04-26-wrong-plan-executed-perfectly.md).

**Human delegation ceiling = 2.1 steps**. UCSD + Cornell field study (Huang et al., arXiv:2512.14012, N=13 observed + N=99 surveyed experienced devs, Aug-Oct 2025): experienced developers delegate at most 2.1 sequential steps to an agent before validating. All 13 observed sessions involved either reviewing the agent's plan or working from the dev's own. Agents are perceived positively — but as productivity boost, not autonomous implementer. This calibrates STOPA's existing budget tiers and per-2-rounds critic: the design matches observed expert behavior, validating the approach against external evidence (ref: 2026-04-23-ucsd-devs-dont-vibe.md).

**Linear orchestration beats naive tree search on noisy environments**. AgentOccam (linear pipeline, 45.7% on WebArena) outperforms all tree-search baselines on noisy web actions. Tree search only helps with typed I/O (tool planning where actions have clean preconditions/effects). Rule for STOPA: ramp linear pipeline to plateau first; only add search when you have high-quality state observations and plan-step typing. For web/UI domains, search is overhead. (ref: 2026-04-26-linear-beats-tree-search-webarena.md)

## Key Rules

1. **Don't judge early iterations**: Performance at iter 1-3 is unreliable — commit to at least 5 iterations before evaluating (ref: 2026-04-08-early-iteration-performance-unreliable.md)
2. **Guard against overfitting**: Hold out test cases from the optimization loop — never optimize on full eval set (ref: 2026-04-03-autoagent-overfitting-guard.md)
3. **Regression gates**: After each improvement, verify previous gains are preserved (ref: 2026-04-05-regression-gate-pattern.md)
4. **Parallel candidates over linear iteration**: Fork N=2-3 candidates, score lightweight, expand best — not try-A-then-B (ref: 2026-04-15-best-of-n-parallel-candidates.md, 2026-04-03-autoagent-parallel-candidates.md)
5. **Direction-magnitude decoupling**: Separate "what to change" from "how much to change" (ref: 2026-04-08-direction-magnitude-decoupling-optimization.md)
6. **Fit exponential decay after 4+ iterations**: `L(T) = L∞ + Z·exp(-z·T)`; if `L∞ < target`, STOP — remaining iterations can't reach target (ref: 2026-04-15-parcae-exponential-decay-stopping.md)
7. **Training depth caps inference depth**: If skill self-evolved with max 5 iterations, deploying with 15 won't help — propagate `recommended_max_iterations` into optstate (ref: 2026-04-15-parcae-exponential-decay-stopping.md)
8. **Variable depth per-item in farm tier**: Classify item complexity before distribution — simple fix=1 iter, complex=3 — uniform effort wastes budget (ref: 2026-04-15-parcae-exponential-decay-stopping.md)
9. **PRM step-checks over ORM end-critic**: After each subtask, haiku verifies step satisfied plan — FAIL kills pipeline early (ref: 2026-04-15-prm-step-verification-orchestrate.md)
10. **Label iterative skill phases with SEPL operators (ρσιεκ)**: enables cross-skill trace replay and consistent circuit breakers (ref: 2026-04-18-autogenesis-protocol.md)
11. **Double-critic for eval coverage**: one critic for correctness, second for blind-spot coverage — single critic misses taxonomic gaps (ref: 2026-04-18-simula-reasoning-first-taxonomies.md)
12. **Neutral-then-pressure evaluation for honesty-sensitive tasks**: accuracy ≠ honesty; elicit belief separately from statement under pressure (ref: 2026-04-18-mask-belief-vs-statement-pipeline.md)

## Patterns

### Do
- Use evolutionary approaches (population-based) for prompt optimization (ref: 2026-04-10-eggroll-evolutionary-optimization.md)
- Share successful strategies across runs via optstate JSON (ref: 2026-04-05-self-improving-harness.md)
- Remove human from loop where possible — auto-research beats guided research (ref: 2026-04-08-auto-research-removes-human-bottleneck.md)
- Fork 2-3 parallel agent candidates for deep-tier orchestrate approaches (ref: 2026-04-15-best-of-n-parallel-candidates.md)
- Fit exponential decay to score trajectory for early-termination (ref: 2026-04-15-parcae-exponential-decay-stopping.md)
- Insert haiku step-checks after each orchestrate subtask (ref: 2026-04-15-prm-step-verification-orchestrate.md)

### Don't
- Don't stop at first improvement — explore alternatives even when score rises (ref: 2026-04-11-iteration-paradox-meta-pattern.md)
- Don't self-sharpen on own outputs without external validation (ref: 2026-04-06-osft-self-sharpening.md)
- Don't use Claudini loop without explicit termination criteria (ref: 2026-03-29-claudini-autoresearch-loop.md)
- Don't run Best-of-N with N>3 on Claude API — cost grows linearly with little benefit (ref: 2026-04-15-best-of-n-parallel-candidates.md)
- Don't apply Best-of-N to light tier — single-pass suffices; task must be decomposable into independent branches (ref: 2026-04-15-best-of-n-parallel-candidates.md)
- Don't rely on plateau-detection alone — it's a lagging signal vs fitted decay (ref: 2026-04-15-parcae-exponential-decay-stopping.md)

## Open Questions

- GAP: No empirical data yet on Best-of-N × PRM-scoring combined cost in STOPA — needs pilot run on deep-tier orchestrate task
- GAP: Parcae `L∞` fit requires `scripts/loop-state.py decay-predict`; current status unknown (implementation exists per related learnings but not confirmed active)

## Related Articles

- See also: [orchestration-multi-agent](orchestration-multi-agent.md) — parallel agent coordination
- See also: [skill-evaluation](skill-evaluation.md) — critic patterns, reward models

## Source Learnings

| File | Date | Severity | Uses | Summary |
|------|------|----------|------|---------|
| iteration-paradox-meta-pattern | 2026-04-11 | high | 1 | Meta-pattern: early iters unreliable |
| eggroll-evolutionary-optimization | 2026-04-10 | high | 1 | Low-rank ES + GRPO scoring |
| auto-research-removes-human-bottleneck | 2026-04-08 | high | 1 | Autonomous research loops |
| autoagent-overfitting-guard | 2026-04-03 | high | 1 | Hold-out sets prevent metric gaming |
| regression-gate-pattern | 2026-04-05 | high | 1 | Verify previous gains preserved |
| direction-magnitude-decoupling | 2026-04-08 | medium | 1 | Separate direction from magnitude |
| early-iteration-performance-unreliable | 2026-04-08 | high | 1 | Don't judge early iterations |
| self-improving-harness | 2026-04-05 | high | 0 | Cross-run strategy persistence |
| osft-self-sharpening | 2026-04-06 | medium | 0 | Self-training risks without external data |
| autoagent-parallel-candidates | 2026-04-03 | medium | 0 | Run multiple candidates per iteration |
| claudini-autoresearch-loop | 2026-03-29 | high | 0 | Autonomous research pipeline |
| [2026-04-12-fresh-session-self-report-verification](../learnings/2026-04-12-fresh-session-self-report-verification.md) | 2026-04-12 | medium | — | Verify agent self-reports from fresh session |
| [2026-04-12-sycophancy-not-hallucination](../learnings/2026-04-12-sycophancy-not-hallucination.md) | 2026-04-12 | high | — | Sycophancy distinct from hallucination |
| [2026-04-15-best-of-n-parallel-candidates](../learnings/2026-04-15-best-of-n-parallel-candidates.md) | 2026-04-15 | medium | 3 | Best-of-N: fork 2-3 parallel, score, expand best — not linear retry |
| [2026-04-15-parcae-exponential-decay-stopping](../learnings/2026-04-15-parcae-exponential-decay-stopping.md) | 2026-04-15 | high | 2 | `L(T)=L∞+Z·exp(-z·T)` fits after 4 iters; training depth caps inference |
| [2026-04-15-prm-step-verification-orchestrate](../learnings/2026-04-15-prm-step-verification-orchestrate.md) | 2026-04-15 | high | 3 | PRM step-check after each subtask — early-kill on FAIL; ~200 tok/step |
| [2026-04-18-autogenesis-protocol](../learnings/2026-04-18-autogenesis-protocol.md) | 2026-04-18 | high | 0 | RSPL+SEPL protocol: resources × 5 operators (ρσιεκ) for self-evolving agents |
| [2026-04-18-simula-reasoning-first-taxonomies](../learnings/2026-04-18-simula-reasoning-first-taxonomies.md) | 2026-04-18 | high | 0 | Mechanism design as 4th axis; taxonomic sampling + double-critic |
| [2026-04-18-mask-belief-vs-statement-pipeline](../learnings/2026-04-18-mask-belief-vs-statement-pipeline.md) | 2026-04-18 | high | 0 | MASK: disentangle honesty (S≠B) from accuracy (B≠T) via neutral+pressure elicitation |
| [2026-04-23-llm-confirmation-bias](../learnings/2026-04-23-llm-confirmation-bias.md) | 2026-04-23 | critical | 4 | 68% ignore evidence, 26% revise beliefs — explicit falsification gate needed in autoresearch/critic |
| [2026-04-23-ucsd-devs-dont-vibe](../learnings/2026-04-23-ucsd-devs-dont-vibe.md) | 2026-04-23 | medium | 0 | Field study: experienced devs delegate ≤2.1 steps before validating — STOPA tier+critic design matches |
| [2026-04-26-wrong-plan-executed-perfectly](../learnings/2026-04-26-wrong-plan-executed-perfectly.md) | 2026-04-26 | high | 0 | When agents report 100% but verify FAILs → re-run scout (plan defect), not retry agents (execution defect) |
