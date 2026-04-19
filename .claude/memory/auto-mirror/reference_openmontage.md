---
name: reference_openmontage
description: OpenMontage — open-source agentic video production system; 7D provider scoring, delivery promise, slideshow risk scorer, post-render review adopted into STOPA/NG-ROBOT
type: reference
---

OpenMontage (github.com/calesthio/OpenMontage) — first open-source agent-first video production system.

**Architecture:** Agent reads YAML pipeline manifests + markdown skills at runtime. Python provides tools + persistence only, no code orchestrator.

**Adopted patterns (ADR 0014):**
1. 7D provider scoring → `scripts/media-provider-selector.py`
2. Delivery promise classifier → `NG-ROBOT/ng-video/studio/delivery_promise.py`
3. Slideshow risk scorer → `NG-ROBOT/ng-video/studio/slideshow_risk.py`
4. Post-render self-review → `NG-ROBOT/ng-video/studio/post_render_review.py`
5. Clip composer → `NG-ROBOT/ng-video/studio/clip_composer.py`
6. Decision log structured format (options_considered, confidence, reason)

**Not adopted:** Pipeline manifest format (recipes sufficient), full auto-discovery registry (premature), 3-layer knowledge architecture (overkill).

**Key insight:** Slide grammar (Ken Burns over stills) ≠ real motion (video clips). Without this distinction, systems silently downgrade from motion-led to slideshow.
