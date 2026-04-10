---
name: prompt-evolve
description: "Use when optimizing generative prompts (image, video, infographic, TTS) through evolutionary self-play. Trigger on 'prompt-evolve', 'optimize prompts', 'evolve prompts', 'prompt quality'. Do NOT use for one-shot prompt writing or manual editing."
user-invocable: true
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
  - Agent
  - TodoWrite
  - WebFetch
tags:
  - orchestration
  - generation
  - media
phase: verify
requires:
  - FAL_KEY
effort: high
output-contract: "optimized prompt-library.yaml → YAML → prompt-library.yaml (updated entries with new version + score)"
---

# Prompt Evolve — GEPA-Inspired Prompt Self-Optimization

Evolutionary optimization of generative prompt templates in `prompt-library.yaml`.
Based on: "Self-Optimizing Multi-Agent Systems for Deep Research" (arXiv:2604.02988) — GEPA method.

## Core Loop

```
SEED → MUTATE → GENERATE → EVALUATE → SELECT → PERSIST
```

## Phase 1: Target Selection

1. Read `prompt-library.yaml` from project root
2. If `$ARGUMENTS` specifies a category (e.g., `image_styles`, `video`, `social`), optimize only that category
3. If no argument, select entries with `score: null` or `score < 0.7` (unoptimized or weak)
4. If all scores are >= 0.7, select the 3 oldest entries (by `optimized_at`)
5. Max 5 entries per run to control cost

## Phase 2: Mutation (GEPA-style)

For each selected entry:

1. Read the current `template` string (= baseline)
2. Generate N variants (N = `_meta.population_size`, default 5):
   - Variant 1: Baseline (unchanged)
   - Variant 2: Expansion — add detail/specificity
   - Variant 3: Compression — shorter, punchier
   - Variant 4: Style shift — different artistic vocabulary
   - Variant 5: Cross-pollination — borrow elements from high-scoring entries in other categories

Mutation prompt pattern:
```
You are optimizing a prompt template for {category}.
Current template: "{template}"
Goal: maximize {eval_criteria} while keeping the prompt under 200 characters.

Generate a variant that {mutation_strategy}.
Return ONLY the new template string, nothing else.
```

Mutation strategies rotate per variant:
- "adds more specific visual/technical detail"
- "is shorter and more direct while preserving intent"
- "uses different artistic vocabulary and composition terms"
- "combines the best elements from: {high_scoring_templates}"

### Low-Rank Mutation Principle (EGGROLL-inspired)

Instead of mutating the entire prompt (full-rank perturbation), each variant perturbs along ONE axis only (rank-1 perturbation). The final update is the weighted sum across the population — recovering full-rank expressivity.

| Variant | Perturbation axis | What changes | What stays fixed |
|---------|------------------|--------------|------------------|
| 2 (Expansion) | Detail specificity | Technical/visual terms | Structure, length, tone |
| 3 (Compression) | Length | Word count | Vocabulary, intent |
| 4 (Style shift) | Vocabulary | Artistic terms | Structure, length, specificity |
| 5 (Cross-pollination) | Structure | Composition pattern | Length, tone |

Why: EGGROLL proves that even rank-1 perturbations converge to the true ES gradient as dimension grows (Theorem 3). Translated to prompts: small, targeted mutations from many variants > large rewrites from few variants. The overall update is rank min(N×r, d) — not restricted to be low-rank.

## Phase 3: Generation & Evaluation

For each variant of each entry:

### Image prompts (`image_styles`, `image_types`, `image_suffixes`, `hero_image`, `social`)

1. Construct a test prompt: `"{variant_template}, a red fox in autumn forest"` (canonical test subject)
2. Generate image via fal.ai Nano Banana Pro:
```python
import fal_client, os, base64
result = fal_client.subscribe("fal-ai/nano-banana-pro", arguments={
    "prompt": TEST_PROMPT,
    "num_images": 1,
    "output_format": "png",
    "safe_mode": True,
    "image_size": {"width": 1024, "height": 1024}
})
```
3. Save image to `outputs/prompt-evolve/{category}_{variant_n}.png`
4. Evaluate with vision model rubric (use Gemini Flash via fal or Claude vision):

**Image Eval Rubric** (score 0-1 per criterion, average = final score):
- **Composition** (0.25): Is the subject well-placed? Rule of thirds? Visual balance?
- **Clarity** (0.25): Sharp details? No artifacts? No unwanted text/watermarks?
- **Relevance** (0.25): Does the image match the prompt intent?
- **Aesthetic** (0.25): Professional quality? Pleasing colors? Editorial feel?

### Video prompts (`video.patterns`, `video.negative_prompt`)

Video generation is expensive — use TEXT-ONLY evaluation:
1. Score each variant with LLM rubric:
   - Specificity (0-1): How precisely does it describe the desired motion?
   - Feasibility (0-1): Can current video models execute this?
   - Conciseness (0-1): No redundant words?
2. Compare against known working prompts from Kling documentation

### Voice settings (`voice.*`)

TTS generation is cheap — generate short test clip:
1. Test text: "Vědci objevili nový druh hlubinné ryby v Mariánském příkopu."
2. Generate via ElevenLabs with each voice setting variant
3. Score naturalness (requires manual eval or user rating)
4. For automated runs: skip voice, flag for manual review

## Phase 4: Selection (EGGROLL Population Scoring + Pareto)

### Step 1: Population-Normalized Scoring (EGGROLL GRPO-style)

Raw eval scores are noisy across categories. Normalize each variant's score relative to the population:

```
For each entry with variants {v_1, ..., v_N} and raw scores {s_1, ..., s_N}:
  μ = mean(s_1, ..., s_N)
  σ_global = std(s_1, ..., s_N)   # global variance across ALL variants of this entry
  z_i = (s_i - μ) / max(σ_global, 0.01)   # z-score, floor σ to avoid division by zero
```

Why: EGGROLL (arXiv, Oxford/MILA 2026) shows that normalizing fitness scores by global population variance produces a more stable selection signal than raw scores — especially when eval rubrics differ across categories. This is the same scoring function used in GRPO for LLM reasoning.

**Population advantage signal**: When all variants score within ±0.05 of each other (σ < 0.05), the entry may be near a local optimum. Flag for cross-pollination in the next run.

### Step 2: Pareto Selection

1. Rank all variants by **z-score** (not raw score)
2. Apply Pareto selection: a variant is dominated if another variant has BOTH higher z-score AND shorter prompt length
3. Select the Pareto-optimal variant (highest z-score among non-dominated)
4. If Pareto-optimal variant **raw score** > baseline raw score: ADOPT
5. If Pareto-optimal variant raw score <= baseline: KEEP baseline, increment version anyway with note "no improvement found"

**Guard: no regression allowed.** A new template is adopted ONLY if its raw score is strictly higher than baseline. Z-scores are for ranking within the population, not for absolute thresholds.

## Phase 5: Persistence

1. Update `prompt-library.yaml`:
   - `template:` → new best template
   - `version:` → increment by 1
   - `score:` → eval score (0-1)
   - `optimized_at:` → today's date
   - `notes:` → what changed and why
2. Git diff the changes for user review
3. Log optimization run to `.claude/memory/learnings/` if score improved by > 0.1

## Output Format

```
## Prompt Evolution Report — {date}

### Optimized: {N} entries

| Category | Entry | Before | After | Delta | Method |
|----------|-------|--------|-------|-------|--------|
| image_styles | national_geographic | 0.62 | 0.78 | +0.16 | expansion |
| video | negative_prompt | null | 0.71 | new | cross-pollination |

### Unchanged: {M} entries (no improvement found)

### Next targets: {entries with lowest scores}
```

## Anti-Rationalization Defense

| Rationalization | Why Wrong | Do Instead |
|---|---|---|
| "I'll just manually rewrite the prompt, it's faster" | Manual edits bypass the eval loop — you don't know if it's actually better | Generate variants, evaluate each, let scores decide |
| "The baseline is already good enough, skip this category" | Paper shows GEPA improved even expert prompts by 5% | Run at least one mutation round — diminishing returns are still returns |
| "I'll skip image generation to save API calls" | Text-only eval for image prompts is unreliable — composition and clarity need visual check | Generate at least 1 image per variant for visual categories |
| "I'll evaluate based on how the prompt reads" | Prompt readability ≠ output quality — terse prompts often outperform verbose ones | Always evaluate the GENERATED OUTPUT, never the prompt text itself |

## Red Flags

STOP and re-evaluate if any of these occur:
- Generating more than 25 images in a single run (cost control)
- All variants scoring lower than baseline (mutation strategy is wrong)
- Eval model consistently giving 0.9+ scores (rubric is too lenient)
- Optimizing the same entry 3+ times without improvement (diminishing returns — move on)

## Verification Checklist

- [ ] `prompt-library.yaml` has updated `version` and `score` for all optimized entries
- [ ] At least one entry improved by > 0.05 score (otherwise the run was unproductive)
- [ ] No regression: no entry has lower score than before
- [ ] Generated images saved in `outputs/prompt-evolve/` for audit
- [ ] Git diff shows only the optimized entries changed (no accidental edits)

## Rules

- Max 5 entries per run
- Max 5 variants per entry (= max 25 image generations per run)
- Never modify `_meta` section without explicit user request
- Never delete old templates — only overwrite with higher-scoring variants
- If FAL_KEY is not set, fall back to text-only evaluation for all categories
- Report cost estimate before generating (approx $0.01 per Nano image)
