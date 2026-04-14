---
date: 2026-04-13
status: IMPLEMENTING
component: pipeline
tags: [video, orchestration, quality-gates, provider-selection]
---

# 0014 — OpenMontage Patterns Adoption

## Context

Analýza open-source video produkčního systému OpenMontage (github.com/calesthio/OpenMontage) odhalila několik přenositelných vzorů pro STOPA orchestraci a NG-ROBOT video pipeline. OpenMontage používá agent-first architekturu s YAML manifesty, 7D provider scoring a production governance gates.

## Decision

Adoptovat 7 vzorů z OpenMontage:

### Pro NG-ROBOT (implementováno)
1. **Post-render self-review** (`ng-video/studio/post_render_review.py`) — ffprobe validace, frame sampling, audio analýza po každém renderu
2. **Delivery promise classifier** (`ng-video/studio/delivery_promise.py`) — klasifikace produkčního záměru, oddělení "real motion" od "slide grammar"
3. **Slideshow risk scorer** (`ng-video/studio/slideshow_risk.py`) — 6D scoring před generováním assetů
4. **Clip composer** (`ng-video/studio/clip_composer.py`) — ffmpeg wrapper pro skládání klipů s crossfade, cut, background music
5. **Bug fix** — `generate_images_fal` → `generate_images` v render.py

### Pro STOPA (implementováno)
6. **Media provider selector** (`scripts/media-provider-selector.py`) — 7D scored výběr providera pro video/image/TTS s decision log
7. **Decision log pro automatická rozhodnutí** — structured JSON entries s `options_considered`, `confidence`, `reason`

## Alternatives Considered

1. **Plný OpenMontage fork** — příliš velký scope, AGPLv3 licence, jiný use case (obecná video produkce vs. NG article pipeline)
2. **Pouze scoring bez registru** — nemá smysl bez dat o providerech
3. **Pipeline manifest formát** — odloženo, STOPA recipes jsou dostatečné pro současný scope. Reconsider pokud přibude 5+ pipeline typů.

## Consequences

- NG-ROBOT Studio pipeline má 3 nové quality gates (pre-production, post-render, delivery promise)
- STOPA má reusable provider scoring pro /klip a /nano skills
- Follow-up: aktualizovat /klip a /nano skills aby volaly media-provider-selector místo hardcoded endpointů
- Follow-up: přidat outcome tracking do media-provider-selector (UCB1-style learning z výsledků)
- Revisit trigger: pokud NG-ROBOT přidá 3+ nové video providery, zvážit plný registry s auto-discovery
