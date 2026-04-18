---
date: 2026-04-18
type: architecture
severity: high
component: orchestration
tags: [evaluation, synthesis, taxonomy, critic, double-critic, coverage, complexity, mechanism-design]
summary: "Simula (arXiv:2603.29791, TMLR 03/2026) formalizuje mechanism design jako samostatnou osu synthetic data generation ortogonální k 'quality/diversity/complexity'. 3-stage pipeline: (1) taxonomy construction via Best-of-N + critic refinement, (2) taxonomic sampling → meta-prompts → complexification, (3) double-critic filtering (independently assess correct + incorrect → mitigates sycophancy). Empirie: Novelty 0.94 vs 0-shot 0.32, full system dominuje všechny 5 datasetů (CTI, LEXam, GSM8k, Global MMLU). Local + Global diversity jsou aditivní, ne redundantní. Complexity help závisí na teacher-student gap. STOPA applicability: self-evolve (taxonomy-driven eval cases), critic (double-critic dekomponace), autoharness (failure class coverage), harness (N/V coverage ratio as planning metric)."
source: external_research
uses: 0
successful_uses: 0
harmful_uses: 0
confidence: 0.85
maturity: draft
valid_until: 2027-04-18
skill_scope: [self-evolve, critic, autoharness, harness]
related: [2026-04-18-mask-belief-vs-statement-pipeline.md, 2026-04-04-toolgenesis-cascade-evaluation.md, 2026-04-12-model-size-negatively-correlated-honesty.md]
verify_check: "manual"
impact_score: 0.0
task_context:
  task_class: research
  complexity: high
  tier: deep
---

## Paper core

**Title:** Reasoning-Driven Synthetic Data Generation and Evaluation (Simula)
**Authors:** Davidson (EPFL), Seguin, Bacis, Ilharco (DeepMind), Harkous (Google)
**ArXiv:** 2603.29791v1 (TMLR 03/2026)

### Contribution: Mechanism design as first-class axis

Traditional synthetic data research optimizes for "good data" desiderata (quality/diversity/complexity). Simula introduces **mechanism design** — *how* data is generated — as orthogonal research axis. Claim: the mechanism determines whether "good data" properties are even achievable at scale with audit trails.

## Three-stage pipeline

### Stage 1: Taxonomy construction
- Decompose target domain description `y` into factors of variation `f_i`
- Expand each `f_i` breadth-first into taxonomy `T_i` of depth `d_i`
- Per-level algorithm (critical detail):
  1. **Best-of-N proposal**: prompt M3 N times with node + ancestors + siblings → N candidate children sets
  2. **Critic refinement**: separate M3 call adds/removes/merges/edits nodes for completeness, soundness, specificity (generator-critic gap exploited)
  3. **Plan generation** (optional): before next level, M3 generates granularity plan → ensures parallel node expansions stay uniform

### Stage 2: Taxonomic sampling + agentic refinement
- **Sampling strategies**: weighted groups of taxonomies (e.g., "children's content" excludes mature themes) — prevents illogical combinations
- Node-sets → **meta-prompts** via M3: `M3(y, {house cat, poem, traveler}) = "haiku about cat adventure"`
- **Complexification**: prompt M3 to increase complexity of fraction `c` (default 0.5) while preserving requirements
- **Coverage ratio `N/V`**: `N` = target dataset size, `V` = unique node-sets. Ratio exposes local vs global diversity tradeoff — if `N < V`, not all node combinations get instantiated
- **Mode collapse mitigation** (large `N/V`): generate multiple meta-prompts simultaneously with previous attempts in context → reflection-based divergence

### Stage 3: Double-critic filtering
- **Point-wise**: M3 critiques generated sample against meta-prompt requirements (binary verdict + explanation)
- **Double-critic** (classification/MC tasks): independently assess "is correct?" AND "is incorrect?" — BOTH must agree for acceptance → mitigates sycophancy bias (Sharma 2024)
- Reject or auto-modify based on critic explanation, repeat

## Empirical findings

### Core reasoning components validated (Gemini 2.5 Flash, 6 expert taxonomies)

| Metric | Simula | 0-Shot |
|--------|--------|--------|
| Completeness (grounded) | 0.74 | 0.52 |
| Completeness (conceptual) | 0.78 | 0.50 |
| Soundness (grounded) | 0.75 | 0.70 |
| **Novelty** | **0.94** | **0.32** |
| **Coverage** | **1.72** | **0.83** |

### Downstream (Gemma 3 4B student, Gemini 2.5 Flash teacher, LoRA SFT)

- **Full Simula = dominant strategy** across all 5 datasets (CTI-MCQ, CTI-RCM, LEXam, GSM8k, Global MMLU) at all data sizes
- **Local + Global diversity are additive**, isolated either is suboptimal
- **Critic impact is dataset-dependent** but NEVER hurts:
  - Global MMLU: 3% rejection → significant improvement
  - LEXam: 61% rejection (weak teacher at 57%) — high cost but maintained
  - Even when no accuracy gain: critic preserves coverage + correctness
- **Complexity impact depends on teacher-student gap**:
  - GSM8k: +10% from High vs Low Complexity split at 64k items
  - LEXam: only Low Complexity split improves with scale (weak teacher can't label hard cases)
- **Cost vs quality**: full Simula = up to 5× more inference than baseline per data point, but smaller high-quality datasets reduce training costs (dominant term)

## Design principles (extracted)

1. **Mechanism design is orthogonal to "good data"** — optimize both axes, not just data properties
2. **Seedless > seed-dependent** — reduces bias inheritance, enables novel domains
3. **Best-of-N + Critic ≫ 0-shot expansion** for structured generation (Novelty 0.94 vs 0.32)
4. **Per-level plan generation** ensures granularity consistency across parallel generations (coordination mechanism for agentic workflows)
5. **Batch-wise Elo scoring > per-sample scoring** — reduces noise from per-sample overconfidence (calibration pattern)
6. **Double-critic > single critic** — independent pos/neg judgments mitigate sycophancy
7. **Coverage ratio `N/V`** as capacity planning metric — exposes local vs global tradeoffs
8. **Complexity must match teacher capability** — "harder = better" is false for weak teachers (LEXam finding)
9. **Auditable mechanism > stochastic evolution** — explainability AND quality-control
10. **No silver bullets** — optimal data properties depend on domain × model × use case × scale → design for flexibility

## STOPA applicability map

| Simula concept | STOPA target | Gap |
|----------------|--------------|-----|
| Taxonomy-based eval case generation | `/self-evolve` curriculum agent | HIGH — currently ad-hoc case generation without coverage guarantees |
| Best-of-N + critic refinement for taxonomies | `/autoharness` failure mode generation | HIGH — systematic failure class coverage > single-pass pattern extraction |
| Double-critic independent correct/incorrect | `/critic` gate | HIGH — STOPA rules already flag sycophancy as concern |
| Calibrated Elo complexity ranking | `/eval` cross-run comparison | MEDIUM — replaces ad-hoc difficulty rating |
| `N/V` coverage ratio | `/harness` test case planning | MEDIUM — quantify blindspots |
| Per-level plan for parallel consistency | `/orchestrate` wave coordination | MEDIUM — same granularity across parallel agents |
| Taxonomy-path audit trace | `/eval` case provenance | MEDIUM — failure localization by node-set |

## Cross-reference to MASK (2026-04-18-mask-belief-vs-statement-pipeline.md)

- **MASK**: measures (honesty vs accuracy) via pressure prompt + belief elicitation
- **Simula**: generates synthetic datasets with auditable structure
- **Combined pattern**: MASK's 6 pressure archetypes → BE taxonomy factors in Simula instantiation to generate honesty-adversarial eval cases with taxonomic coverage guarantees
- Both share "reasoning-first" ethos: measurable, auditable, not opaque

## Cross-reference to Tool-Genesis (2026-04-04-toolgenesis-cascade-evaluation.md)

- Tool-Genesis: Schema-Utility Decoupling (format compliance ≠ functional correctness)
- Simula's double-critic is an anti-schema-trap mechanism: independent pos/neg prevents schema-valid-but-wrong acceptance
- Graduation path: if this learning gets `impact_score >= 0.7`, consider embedding double-critic as standard gate in `/critic`

## What NOT to adopt

- Embedding-based diversity metrics — requires NV embedding infrastructure not present in STOPA
- Full LoRA finetuning downstream — STOPA doesn't train models
- Gemini-specific implementation details — framework is model-agnostic, keep it that way

## Priority adoption signals (watch for)

Trigger `/self-evolve` or `/autoharness` refactor when:
- `/critic` sycophancy pattern recurs 3+ times in failure log
- `/self-evolve` eval coverage drops below heuristic threshold
- `/harness` false-positive rate shows schema-vs-utility mismatch

Otherwise: keep as `draft` learning, let `/evolve` graduate based on use count.
