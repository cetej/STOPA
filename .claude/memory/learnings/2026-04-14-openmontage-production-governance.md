---
date: 2026-04-14
type: architecture
severity: high
component: pipeline
tags: [video, orchestration, quality-gates, provider-selection, openmontage]
summary: "OpenMontage production governance patterns: 7D provider scoring, delivery promise classifier, slideshow risk scorer, post-render self-review — adopted into STOPA/NG-ROBOT."
source: external_research
uses: 1
successful_uses: 0
harmful_uses: 0
confidence: 0.8
maturity: draft
verify_check: "Glob('scripts/media-provider-selector.py') → 1+ matches"
---

# OpenMontage Production Governance Patterns

Source: github.com/calesthio/OpenMontage (AGPLv3, 1589 stars, April 2026)

## Key Patterns Adopted

### 1. 7-Dimension Provider Scoring
Weighted scoring: task_fit (30%), output_quality (20%), control (15%), reliability (15%), cost_efficiency (10%), latency (5%), continuity (5%). Continuity penalizuje přechody mezi providery — konzistence stylu v multi-clip videu.

Implementace: `scripts/media-provider-selector.py`

### 2. Delivery Promise Classifier
Klasifikuje produkční záměr (MOTION_LED, SOURCE_LED, IMAGE_EXPLAINER, DATA_EXPLAINER, HYBRID). Klíčové rozlišení: "slide grammar" (Remotion-animated still images) ≠ "real motion" (actual video clips). Zabraňuje silent downgrade.

Implementace: `NG-ROBOT/ng-video/studio/delivery_promise.py`

### 3. Slideshow Risk Scorer
6-dimenzionální scoring (repetition, decorative_visuals, weak_motion, typography_overreliance, generic_prompts, consecutive_sameness). Spouštět PO scene_plan, PŘED asset generation — kdy je oprava levná.

Implementace: `NG-ROBOT/ng-video/studio/slideshow_risk.py`

### 4. Post-Render Self-Review
Povinná 4-složková kontrola: ffprobe validace, frame sampling (4 pozice), audio level analýza, subtitle check. Video neprezentovat pokud review selže.

Implementace: `NG-ROBOT/ng-video/studio/post_render_review.py`

### 5. Decision Log Pattern
Každé automatické rozhodnutí musí mít: `options_considered` (min 2 alternativy), `reason` (ne "best option"), `confidence` (0-1). Reviewer odmítá confidence 1.0 jako nerealistickou.

### 6. Clip Composer
FFmpeg wrapper: trim → scale → concat (crossfade/cut) → background music overlay. Fallback z xfade na concat demuxer.

Implementace: `NG-ROBOT/ng-video/studio/clip_composer.py`

## Patterns NOT Adopted (and why)

- **Pipeline manifest format**: STOPA recipes dostatečné pro současný scope
- **Full tool registry with auto-discovery**: premature — máme 4 video + 4 image providery
- **Remotion composition engine**: NG-ROBOT už Remotion používá
- **3-layer knowledge architecture**: STOPA má 2 vrstvy (skills + learnings), 3. vrstva (external tech knowledge) je overkill

## ADR

docs/decisions/0014-openmontage-patterns-adoption.md
