---
task_id: ng-video-studio-phase3
goal: "FLUX image generation via FAL.ai: generate_images_fal() for scenes with visual_prompt"
type: feature
status: completed
branch: main
phase: 3-of-5
prev_task: ng-video-studio-phase2 (COMPLETED commit 63178d7)
next_task: ng-video-studio-phase4 (planned: LTX-2 video clip generation)
completed_commit: 385cb0b
subtasks:
  - {id: "st-3-1", description: "Populate visual_prompt in scenario_generator.py for intro/segment scenes", status: "completed", artifacts: ["commit 385cb0b"]}
  - {id: "st-3-2", description: "generate_images_fal() in render.py: FAL.ai FLUX image generation with fallback", status: "completed", artifacts: ["commit 385cb0b"]}
  - {id: "st-3-3", description: "Pipeline integration: --skip-images/--regenerate-images flags, image gen before TTS", status: "completed", artifacts: ["commit 385cb0b"]}
---

# Shared Memory — Task State

Current task state shared across all agents and skills.

## Active Task

**Goal**: New ng-video/studio/ module — scenario pipeline (article → scenario.json → Remotion render)
**Type**: feature
**Status**: done
**Tier**: standard (3 agents, 2 critic iterations)

### Subtasks

| # | Subtask | Criterion | Depends on | Wave | Method | Status |
|---|---------|-----------|-----------|------|--------|--------|
| 1 | ElevenLabs integration in render.py | Imports work, API calls functional | — | 1 | Agent:sonnet | pending |
| 2 | Voice selection in schema + generator | voice_id field exposed, defaults applied | — | 1 | direct | pending |
| 3 | E2E test with ElevenLabs | Real article pipeline with audio quality check | 1, 2 | 2 | direct | pending |

### Dependency Graph

```
1 ──→ 3 (output: schema + generator)
2 ──→ 3 (output: composition names + props interface)
3 ──→ 4 (output: full pipeline)

Wave 1: [1, 2]    ← independent (Python + TypeScript parallel)
Wave 2: [3]        ← needs schema + composition
Wave 3: [4]        ← E2E verification
```

## Task History

### 2026-04-09 — ng-video Studio Phase 1 (COMPLETED)
- **Goal**: Build scenario pipeline: article → scenario.json → TTS → Remotion render
- **Result**: Delivered commit 229f22f
  - `studio/schema.py` (87 lines): Pydantic v2 models (Scene, SceneType, Scenario, VoiceoverConfig, MusicConfig, BrandingConfig)
  - `studio/scenario_generator.py` (215 lines): Article extraction from 9_final.md, image finding, scene generation with auto-timing
  - `studio/render.py` (210 lines): TTS orchestration, Remotion CLI wrapper, --dry-run support
  - `NGVideoStudio.tsx` (269 lines): Scene-driven Remotion composition (Ken Burns, glass-morphism overlays, NG branding)
  - `Root.tsx` updated: Studio-Landscape/Portrait-Dynamic compositions registered
  - E2E verified: 30s video on real article (2026-02-09_meet-the-baronessthe-worlds-longest-wild-snake) with 5 scenes, 3 images, TTS sync working
- **Next**: Phase 2 (ElevenLabs TTS upgrade)

### 2026-04-05 — NLAH Implementation
- **Goal**: Implementace 3 aplikovatelných poznatků z arXiv:2603.25723
- **Result**: In progress — P1 (structured state/checkpoint), P2 (critic accuracy, acceptance gate), P3 (auto-checkpoint, self-evolve extensions)
- **Origin**: /deepresearch → implementation plan

### 2026-03-22 — skill-audit harness
- **Goal**: Run skill-audit harness on all 15 STOPA skills
- **Result**: Audit complete — overall health 3.9/5. Key gaps: verify/youtube-transcript missing memory writes; scout missing explicit disallow list; watch over-permissioned. Full report: `.harness/report.md`
- **Origin**: /harness skill-audit

### 2026-03-19 — Karpathy AutoResearch
- **Goal**: Research Karpathy AutoResearch + create /autoloop skill
- **Result**: M5 hybrid metric, /autoloop skill created, baseline scores for all skills
- **Origin**: STOPA orchestration

### 2026-03-18 — Initial System Build
- **Goal**: Vytvořit orchestrační systém (skills, sdílená paměť, budget, session continuity)
- **Result**: 9 skills, sdílená paměť, budget tiers, circuit breakers, /watch, /checkpoint
- **Origin**: Vyvinut v test1 (Pyramid Flow), přenesen do STOPA jako source of truth
