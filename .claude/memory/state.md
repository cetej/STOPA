---
task_id: ng-video-studio-phase2
goal: "ElevenLabs TTS integration: replace Edge TTS in studio/render.py with ElevenLabs for better voice quality, voice cloning, multi-language support"
type: feature
status: in_progress
branch: main
phase: 2-of-5
prev_task: ng-video-studio-phase1 (COMPLETED commit 229f22f)
subtasks:
  - {id: "st-2-1", description: "Integrate ElevenLabs API: update studio/render.py generate_tts() to use ElevenLabs client instead of edge_tts", criterion: "python -c 'from studio.render import generate_tts' passes AND render.py with ELEVENLABS_API_KEY env var works", done_when: "grep -q 'elevenlabs' studio/render.py AND python studio/render.py --dry-run test_scenario.json shows ElevenLabs TTS source", context_scope: ["ng-video/studio/render.py"], grounding_refs: [], depends_on: [], wave: 1, method: "Agent:general-purpose:sonnet", status: "pending", artifacts: []}
  - {id: "st-2-2", description: "Voice selection: expose voice_id in VoiceoverConfig (schema.py), default to 'Emma' (English) or 'Elena' (Czech)", criterion: "schema.py VoiceoverConfig has voice_id field AND scenario_generator.py respects it", done_when: "grep -q 'voice_id:' ng-video/studio/schema.py AND python -m studio.scenario_generator -a processed/2026-02-09... produces scenario with voice_id", context_scope: ["ng-video/studio/schema.py", "ng-video/studio/scenario_generator.py"], grounding_refs: [], depends_on: [], wave: 1, method: "direct", status: "pending", artifacts: []}
  - {id: "st-2-3", description: "Test with real article: E2E pipeline with ElevenLabs, dry-run render, verify audio quality via ffprobe", criterion: "Generated MP3s are valid AND durations match scenario timings ±0.5s", done_when: "python studio/render.py --from-article processed/2026-02-09... --dry-run succeeds AND ffprobe shows valid MP3 with correct duration", context_scope: ["ng-video/studio/"], grounding_refs: [], depends_on: ["st-2-1", "st-2-2"], wave: 2, method: "direct", status: "pending", artifacts: []}
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
