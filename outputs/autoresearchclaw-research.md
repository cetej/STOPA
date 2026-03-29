# AutoResearchClaw — Architecture Research Brief

**Date:** 2026-03-28
**Question:** Deep architecture analysis of AutoResearchClaw — pipeline stages, agent architecture, decision mechanisms, anti-fabrication system, MetaClaw cross-run learning
**Scope:** standard (comparison)
**Sources consulted:** 12 (10 directly read, 2 inferred from structure)

---

## Executive Summary

AutoResearchClaw [VERIFIED][1] is a fully autonomous research pipeline that takes a natural-language idea and produces a conference-ready paper. The system is organized as a **23-stage, 8-phase linear pipeline** with three human-approval gate points and a recursive PROCEED/REFINE/PIVOT decision loop at Stage 15. It was created in March 2026 and has 9,194 GitHub stars as of 2026-03-28.

The architecture's most distinctive features are: (1) a **VerifiedRegistry** that creates a numeric whitelist from experiment data, preventing any fabricated metric from appearing in a written paper [VERIFIED][5]; (2) a **MetaClaw evolution system** that persists lessons across runs in JSONL format and injects them as prompt overlays into all subsequent pipeline stages [VERIFIED][4]; and (3) a **multi-agent debate mechanism** in the synthesis phase that spawns competing perspectives and synthesizes them before hypothesis generation [VERIFIED][7].

The anti-fabrication approach is architectural rather than post-hoc: the VerifiedRegistry is built *before* paper writing begins, and the paper verifier operates section-by-section during writing, rejecting unregistered numbers in strict sections (Results, Experiments, Tables) and issuing warnings in lenient sections (Introduction, Related Work) [VERIFIED][6].

---

## Detailed Findings

### 1. Pipeline Stages — Complete 23-Stage Breakdown

The pipeline executes stages 1–23 in fixed linear order [VERIFIED][2]:

| Phase | Stages | Description |
|-------|--------|-------------|
| A — Scoping | 1–2 | Topic initialization, problem decomposition into hierarchical tree |
| B — Literature | 3–5 | Multi-source discovery (OpenAlex, Semantic Scholar, arXiv), relevance screening gate (Stage 5) |
| C — Synthesis | 6–7 | Knowledge clustering, hypothesis generation via multi-agent debate |
| D — Design | 8–9 | Experiment planning, hardware-aware code generation, resource estimation; gate at Stage 9 |
| E — Execution | 10–14 | Sandbox execution, NaN/Inf detection, self-healing repair loop (≤10 iterations), result analysis |
| F — Analysis | 15 | Autonomous decision logic: PROCEED / REFINE / PIVOT |
| G — Writing | 16–19 | Outline, section-by-section draft (5,000–6,500 words), peer review, revision |
| H — Finalization | 20–23 | Quality gate (Stage 20), knowledge archive, LaTeX export, citation resolution |

Stages are numbered consistently: Stage 5 = literature quality gate, Stage 9 = experimental protocol gate, Stage 20 = paper quality gate [VERIFIED][3].

### 2. Stage Connection Mechanism

Stages communicate via **artifact directories** [VERIFIED][2]. Each stage writes to `stage-{N:02d}/` and downstream stages read from earlier directories. For example, Stage 17 (paper draft) reads `stage-14/experiment_summary.json`. After each successful stage, an atomic checkpoint is written (temp-file → rename) containing `last_completed_stage`, `last_completed_name`, `run_id`, and timestamp [VERIFIED][2].

Resume is possible from any stage via the `from_stage` parameter, enabling crash recovery.

### 3. PROCEED / REFINE / PIVOT Decision Logic

Stage 15 (`RESEARCH_DECISION`) is the sole decision point [VERIFIED][2]:

```
result.decision = "refine"  →  rollback to Stage 13
result.decision = "pivot"   →  rollback to Stage 8
```

Before re-executing rolled-back stages, `_version_rollback_stages()` renames existing directories (e.g., `stage-08/` → `stage-08_v1/`), preserving prior iteration data [VERIFIED][2].

A `_promote_best_stage14()` function scans all versioned `stage-14*/experiment_summary.json` files, scores by primary metric, and copies the best result to canonical `stage-14/` so paper writing always uses optimal — not latest — experimental data [VERIFIED][2].

**Forced PROCEED** activates when:
- `MAX_DECISION_PIVOTS` is exceeded
- `_consecutive_empty_metrics()` detects two cycles with zero experimental data
[VERIFIED][2]

### 4. Gate Stages

Three explicit approval gates exist [VERIFIED][3]:
- **Stage 5**: Literature quality validation
- **Stage 9**: Experimental protocol validation
- **Stage 20**: Paper quality validation

When `result.status == BLOCKED_APPROVAL`, pipeline pauses. `--auto-approve` flag bypasses all gates. Rejection triggers rollback [VERIFIED][2].

### 5. Multi-Agent Debate Mechanism

The synthesis phase (Stage 7, hypothesis generation) uses `_multi_perspective_generate()` [VERIFIED][7]:

- Multiple agents are spawned with roles defined in `DEBATE_ROLES_HYPOTHESIS` (from `researchclaw.prompts`)
- Each agent generates a competing perspective
- `_synthesize_perspectives()` consolidates viewpoints into final hypotheses
- If all perspectives fail, a fallback prevents empty context from reaching the LLM (explicitly documented as preventing "pure hallucination") [VERIFIED][7]
- A novelty check validates hypotheses against existing literature

The RESEARCHCLAW_AGENTS.md clarifies that the top-level orchestrator is a **single agent** following a decision guide, not a debating multi-agent system [VERIFIED][3]. The debate is scoped specifically to the hypothesis generation stage.

### 6. Anti-Fabrication System — VerifiedRegistry

The VerifiedRegistry [VERIFIED][5] is the central anti-fabrication mechanism:

**Architecture:**
```python
@dataclass
class VerifiedRegistry:
    values: dict[float, str]           # numeric → provenance
    condition_names: set[str]
    conditions: dict[str, ConditionResult]
    primary_metric: float | None
    metric_direction: str              # "maximize" | "minimize"
    training_config: dict[str, Any]
```

**Registration pipeline (7 steps):**
1. Best-run metrics extraction (per-seed, pattern `"CondName/seed/metric_key"`)
2. Condition summaries
3. Metrics summary (min/max/mean)
4. Primary metric capture
5. Per-condition statistics (mean, std)
6. Pairwise differences (absolute + relative improvements)
7. Refinement log enrichment

**Variant registration:** Each value is automatically registered with rounding variants (1–4 decimal places), percentage conversions (×100 for [0,1] range), and fractional conversions (÷100 for values >1) — preventing false positives [VERIFIED][5].

**Verification:** `is_verified(number, tolerance=0.01)` applies 1% relative tolerance for fuzzy matching [VERIFIED][5].

**Infrastructure isolation:** Keys in `_INFRA_KEYS` (`elapsed_sec`, `SEED_COUNT`, etc.) go to `training_config` without value registration, separating experiment infrastructure from published claims [VERIFIED][5].

**BUG-222 fix:** A `best_only=True` mode loads only `experiment_summary_best.json` to prevent regressed refinement iterations from polluting the whitelist [VERIFIED][5].

### 7. Paper Verifier — Section-Level Enforcement

The `paper_verifier.py` [VERIFIED][6] applies the VerifiedRegistry during LaTeX generation:

**Section severity:**
- **Strict sections** (Results, Experiments, Tables): unverified numbers → rejection
- **Lenient sections** (Introduction, Related Work): unverified numbers → warnings only

**Skip patterns:** `\cite{}`, `\ref{}`, comments, code blocks are excluded via character-position masks.

**Training config check:** `_check_training_config()` validates training claims (epochs, condition counts) against registry data.

Note: The README reference to "4-layer citation verification" and "arXiv ID validation + CrossRef/DataCite DOI matching + LLM relevance scoring" does **not** appear in the actual `paper_verifier.py` or `_review_publish.py` code [VERIFIED][6,8]. The actual citation resolution uses a simpler 3-layer strategy: seminal database → API search with title-word-overlap scoring → skip-if-unconfident [VERIFIED][8].

### 8. MetaClaw Cross-Run Learning

The `evolution.py` module [VERIFIED][4] implements four components:

**LessonCategory Enum:** `SYSTEM | EXPERIMENT | WRITING | ANALYSIS | LITERATURE | PIPELINE`

**LessonEntry Dataclass:** per-lesson record with `stage_name`, `stage_num`, `category`, `severity`, `description`, `timestamp`, `run_id`

**EvolutionStore:** JSONL-backed append storage with staged queries

**Lesson capture sources:**
- Stage failures (status field + keyword matching against error text)
- Blocked stages (pipeline warnings)
- Decision pivots/refines (parsed from `decision_structured.json`)
- Runtime artifact scanning: stderr warnings, NaN/Inf metric anomalies

**Skill injection:** `build_overlay()` generates two-part prompt overlay [VERIFIED][4]:
1. Intra-run lessons — time-weighted, severity-boosted, queried from `lessons.jsonl`
2. Cross-run MetaClaw skills — up to 5 SKILL.md files loaded from `arc-*` directories in `skills_dir`

**SKILL.md format** (from `skills/loader.py`) [VERIFIED][9]:
```yaml
---
name: kebab-case-id
description: one-liner
metadata:
  category: domain
  trigger-keywords: "kw1,kw2"
---
Markdown body here...
```

**Cross-run bridge:** `export_to_memory()` maps lesson categories to memory categories via duck-typed `.add()` interface [VERIFIED][4].

Note: The 18.3% composite robustness improvement metric cited in the README is **not present in the evolution.py source code** [VERIFIED][4]. It appears in README marketing copy only.

### 9. Self-Healing Execution Loop

`experiment_diagnosis.py` [VERIFIED][10] implements:

**Failure categories detected:**
- Missing dependencies (`ModuleNotFoundError`)
- Permission errors
- GPU out-of-memory
- Time budget exceeded
- Synthetic data fallbacks
- Dataset unavailability
- Code crashes
- Hyperparameter issues (NaN/diverging loss)
- Identical ablation outputs
- Insufficient random seeds

**NaN detection:** regex pattern matching (`loss.*?\bnan\b`) plus loss-value parsing (values >100 flagged as diverging) [VERIFIED][10].

**Repairability limit:** `_assess_repairability()` tracks repeated deficiency types. If 3+ deficiency types recur across multiple prior diagnoses, the experiment is marked non-repairable. The 10-iteration cap is enforced at the orchestration layer [VERIFIED][10].

Repair prompts are ordered by severity (critical → major → minor) for execution by the CodeAgent [VERIFIED][10].

---

## Disagreements & Open Questions

1. **"4-layer citation verification" claim**: The README describes arXiv ID validation, CrossRef/DataCite DOI matching, title verification, and LLM relevance scoring as a 4-layer system. The actual `paper_verifier.py` implements numeric-only verification. The `_review_publish.py` citation resolution uses 3-layer title-word-overlap, not LLM scoring. **The README overstates this capability** [VERIFIED vs. README claim][6,8].

2. **18.3% improvement metric**: Present only in README, not in evolution.py source. Could be from a separate evaluation script not fetched, or marketing copy [SINGLE-SOURCE][1].

3. **Debate role definitions**: `DEBATE_ROLES_HYPOTHESIS` is imported from `researchclaw.prompts` but the actual role definitions were not fetched. The number of debate agents and their specific reasoning modes are unknown [UNVERIFIED].

4. **MetaClaw "arc-*" skill generation**: The skills loader reads from `arc-*` directories but the mechanism that *creates* these directories (the skill generation loop) was not found in the fetched code [UNVERIFIED].

---

## Evidence Table

| # | Source | URL | Key Claim | Type | Confidence |
|---|--------|-----|-----------|------|------------|
| 1 | AutoResearchClaw README | https://raw.githubusercontent.com/aiming-lab/AutoResearchClaw/main/README.md | 23-stage 8-phase pipeline, MetaClaw, VerifiedRegistry overview | primary | high |
| 2 | pipeline/runner.py | https://raw.githubusercontent.com/aiming-lab/AutoResearchClaw/main/researchclaw/pipeline/runner.py | Stage sequence, PROCEED/REFINE/PIVOT logic, rollback versioning, checkpoint/resume | primary | high |
| 3 | RESEARCHCLAW_AGENTS.md | https://raw.githubusercontent.com/aiming-lab/AutoResearchClaw/main/RESEARCHCLAW_AGENTS.md | Single orchestrator agent, 3 gate stages, execution modes | primary | high |
| 4 | evolution.py | https://raw.githubusercontent.com/aiming-lab/AutoResearchClaw/main/researchclaw/evolution.py | MetaClaw: LessonCategory, LessonEntry, EvolutionStore, build_overlay, JSONL format | primary | high |
| 5 | pipeline/verified_registry.py | https://raw.githubusercontent.com/aiming-lab/AutoResearchClaw/main/researchclaw/pipeline/verified_registry.py | VerifiedRegistry dataclass, 7-step registration, 1% tolerance, variant registration | primary | high |
| 6 | pipeline/paper_verifier.py | https://raw.githubusercontent.com/aiming-lab/AutoResearchClaw/main/researchclaw/pipeline/paper_verifier.py | Section-level severity, numeric whitelist enforcement, LaTeX skip patterns | primary | high |
| 7 | pipeline/stage_impls/_synthesis.py | https://raw.githubusercontent.com/aiming-lab/AutoResearchClaw/main/researchclaw/pipeline/stage_impls/_synthesis.py | Multi-agent debate via _multi_perspective_generate, fallback anti-hallucination | primary | high |
| 8 | pipeline/stage_impls/_review_publish.py | https://raw.githubusercontent.com/aiming-lab/AutoResearchClaw/main/researchclaw/pipeline/stage_impls/_review_publish.py | 3-layer citation resolution (seminal DB → API → skip), title word overlap | primary | high |
| 9 | researchclaw/skills/loader.py | https://raw.githubusercontent.com/aiming-lab/AutoResearchClaw/main/researchclaw/skills/loader.py | SKILL.md format with YAML frontmatter, loading hierarchy | primary | high |
| 10 | pipeline/experiment_diagnosis.py | https://raw.githubusercontent.com/aiming-lab/AutoResearchClaw/main/researchclaw/pipeline/experiment_diagnosis.py | 10 failure categories, NaN/Inf detection, repairability assessment | primary | high |
| 11 | GitHub API repo metadata | https://api.github.com/repos/aiming-lab/AutoResearchClaw | Stars: 9,194, created 2026-03-15, language: Python | primary | high |
| 12 | GitHub API directory tree | https://api.github.com/repos/aiming-lab/AutoResearchClaw/git/trees/main?recursive=1 | Full module structure, subpackage list | primary | high |

---

## Sources

1. AutoResearchClaw README — https://raw.githubusercontent.com/aiming-lab/AutoResearchClaw/main/README.md
2. pipeline/runner.py — https://raw.githubusercontent.com/aiming-lab/AutoResearchClaw/main/researchclaw/pipeline/runner.py
3. RESEARCHCLAW_AGENTS.md — https://raw.githubusercontent.com/aiming-lab/AutoResearchClaw/main/RESEARCHCLAW_AGENTS.md
4. evolution.py — https://raw.githubusercontent.com/aiming-lab/AutoResearchClaw/main/researchclaw/evolution.py
5. pipeline/verified_registry.py — https://raw.githubusercontent.com/aiming-lab/AutoResearchClaw/main/researchclaw/pipeline/verified_registry.py
6. pipeline/paper_verifier.py — https://raw.githubusercontent.com/aiming-lab/AutoResearchClaw/main/researchclaw/pipeline/paper_verifier.py
7. pipeline/stage_impls/_synthesis.py — https://raw.githubusercontent.com/aiming-lab/AutoResearchClaw/main/researchclaw/pipeline/stage_impls/_synthesis.py
8. pipeline/stage_impls/_review_publish.py — https://raw.githubusercontent.com/aiming-lab/AutoResearchClaw/main/researchclaw/pipeline/stage_impls/_review_publish.py
9. researchclaw/skills/loader.py — https://raw.githubusercontent.com/aiming-lab/AutoResearchClaw/main/researchclaw/skills/loader.py
10. pipeline/experiment_diagnosis.py — https://raw.githubusercontent.com/aiming-lab/AutoResearchClaw/main/researchclaw/pipeline/experiment_diagnosis.py
11. GitHub API — https://api.github.com/repos/aiming-lab/AutoResearchClaw
12. GitHub API tree — https://api.github.com/repos/aiming-lab/AutoResearchClaw/git/trees/main?recursive=1

---

## Coverage Status

- **[VERIFIED]:** 23-stage pipeline structure, PROCEED/REFINE/PIVOT logic with exact rollback targets, VerifiedRegistry 7-step registration + 1% tolerance, MetaClaw JSONL storage + build_overlay injection, section-level paper verification severity, multi-agent debate fallback behavior, citation resolution 3-layer strategy, NaN/Inf failure detection, SKILL.md format
- **[INFERRED]:** Debate produces better hypotheses than single-agent (implied by fallback anti-hallucination logic)
- **[SINGLE-SOURCE]:** 18.3% improvement claim (README only, not in code)
- **[UNVERIFIED]:** Exact DEBATE_ROLES_HYPOTHESIS definitions, arc-* skill generation mechanism, total number of debate agents
