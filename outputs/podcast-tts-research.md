# AI Podcast Generation & TTS Ecosystem — Research Brief

**Date:** 2026-03-27
**Question:** Latest news 2025-2026 on NotebookLM, AI podcast generation, TTS breakthroughs, cost analysis, and NotebookLM podcast API
**Scope:** broad
**Sources consulted:** 20+

---

## Executive Summary

The AI audio/podcast generation landscape has shifted dramatically in 2025–2026. Three parallel developments have converged: (1) Google launched an official NotebookLM Podcast API (GA with allowlist, August 2025) for enterprise Google Cloud customers, removing the need for a notebook or data store; (2) a wave of open-source TTS models — Sesame CSM, Dia by Nari Labs, Fish Speech S2, Chatterbox — have closed the quality gap with proprietary APIs at a fraction of the cost; (3) costs for cloud TTS have become concrete enough to compare: self-hosted open-source wins on volume, ElevenLabs leads on quality for English, and OpenAI's gpt-4o-mini-tts hits ~$0.015/minute making it the cheapest cloud option.

The key uncertainty: Google's Podcast API has no public pricing and requires sales rep contact, making it opaque for independent developers. Public NotebookLM tiers (Free/Plus/Pro/Ultra) are usage-limited rather than API-based.

---

## Detailed Findings

### 1. NotebookLM — New Features (2025-2026)

**March 2025** — New Audio Overview interactive controls: Smart Pause, Section Jump, Instant Replay, Summary Mode. New format variants added: brief, critique, debate, deep-dive with customizable length and tone. [Source: workspaceupdates.googleblog.com]

**April 2025** — Audio Overviews expanded to 50+ languages (beta). [Source: workspaceupdates.googleblog.com]

**September 2025** — Biggest feature drop: custom ports (control structure/tone/language), dynamic templates, flashcards and quizzes.

**December 2025** — Gemini 2.5 Flash integration for NotebookLM Enterprise (Public Preview).

**Late 2025** — Google restructured consumer tiers into Free / Plus / Pro / Ultra:
- Free: 3 Audio Overviews/day
- Pro ($19.99/mo, bundled with Google AI Pro): 20/day
- Ultra ($249.99/mo): 200/day

**2026 roadmap** — "Lecture" format: single-host 30-minute monologue, expected 2026.

---

### 2. NotebookLM Podcast API — Enterprise Access

**August 28, 2025** — Podcast API reached GA-with-allowlist status.

Official docs: https://docs.cloud.google.com/gemini/enterprise/notebooklm-enterprise/docs/podcast-api

Key facts:
- **Standalone API** — does NOT require a NotebookLM notebook, Gemini Enterprise license, or data store
- **Input:** array of multimedia objects (text, images, audio, video); max 100,000 tokens
- **Output:** MP3 file
- **IAM role required:** `roles/discoveryengine.podcastApiUser`
- **Length options:** SHORT (4-5 min) or STANDARD (~10 min)
- **Languages:** BCP47 codes; defaults to English
- **Focus:** custom prompt to direct topic
- **Access:** "Select Google Cloud customers" — must contact Google Cloud sales rep
- **Pricing:** NOT disclosed in documentation
- **Separate API:** `notebooks.audioOverviews.create` for notebook-tied generation also exists

There is also an unofficial Playwright-based automator (github.com/israelbls/notebooklm-podcast-automator) for non-enterprise users.

---

### 3. TTS Breakthroughs (2025-2026)

#### Sesame CSM-1B
- **Released:** March 13, 2025 (Sesame AI Labs)
- **Architecture:** Llama backbone + Mimi audio decoder, RVQ tokens
- **License:** Apache 2.0
- **Key capability:** Conversational context-aware speech; multi-speaker support
- **Performance:** Blind listening tests — participants could not distinguish from real humans in short conversational excerpts
- **Hardware:** GPU and CPU compatible (low-latency real-time on both)
- **Roadmap:** 20+ language expansion planned
- **GitHub:** https://github.com/SesameAILabs/csm

#### Dia 1.6B (Nari Labs)
- **Released:** April 21, 2025
- **Built by:** Two undergraduates, zero funding
- **Architecture:** Transformer-based, 1.6B parameters
- **License:** Apache 2.0
- **Key capability:** Native nonverbal cues from text tags: `(laughs)`, `(coughs)`, `(gasps)`; zero-shot voice cloning
- **Hardware:** GPU-only (~10GB VRAM); CPU support on roadmap
- **Inference:** 40 tokens/second on A4000; 86 tokens ≈ 1 second of audio
- **Language:** English only currently
- **Best for:** Podcasts, audiobooks, expressive emotional content
- **Site:** https://newsroom.stelia.ai/dia-text-to-speech-open-source-breakthrough/

#### Fish Speech S2
- **Released:** March 10, 2026 (Fish Audio)
- **Architecture:** Dual-AR: 4B Slow AR + 400M Fast AR; trained on 10M hours of audio
- **Languages:** 80+
- **Latency:** <150ms
- **Benchmarks:**
  - WER: 0.54% (Chinese), 0.99% (English)
  - Audio Turing Test: 0.515 (24% better than Seed-TTS)
  - EmergentTTS-Eval: 81.88% win rate vs GPT-4o-mini-tts
- **Emotion control:** 15,000+ natural language tags
- **License caveat:** Code is Apache-licensed; model weights use "Fish Audio Research License" — commercial use requires separate licensing
- **API cost:** ~$0.05/minute (Fish Audio API) vs ElevenLabs ~$0.18/minute
- **Fish Audio API tiers:** Free (7 min/month), Plus ($11/mo), Pro ($75/mo)
- **GitHub:** https://github.com/fishaudio/fish-speech

#### Chatterbox (Resemble AI)
- **Released:** 2025 (exact date not captured)
- **License:** MIT (truly permissive, including commercial)
- **Variants:** Chatterbox (base), Chatterbox Multilingual (23 languages), Chatterbox Turbo (<200ms latency)
- **Key capability:** Emotion exaggeration control (first open-source model), zero-shot voice cloning, PerTh imperceptible neural watermarking
- **Reception:** 1M+ Hugging Face downloads; 63.75% of evaluators preferred it over ElevenLabs
- **GitHub:** https://github.com/resemble-ai/chatterbox

#### F5-TTS
- **Status:** Active 2025; best known for voice cloning quality
- **Performance:** Inference at 3× real-time on RTX 4070 (~20s per minute of audio)
- **Recommendation:** Preferred for voice cloning tasks

#### Summary Table — Open-Source TTS

| Model | Params | Multi-speaker | Nonverbal | CPU | License | Best for |
|-------|--------|--------------|-----------|-----|---------|----------|
| Sesame CSM-1B | 1B | Yes | No | Yes | Apache 2.0 | Conversational AI |
| Dia 1.6B | 1.6B | Yes | Yes (tags) | No (GPU req.) | Apache 2.0 | Podcasts, audiobooks |
| Fish Speech S2 | 4.4B | Yes | Partial | No | Mixed* | Multi-lang production |
| Chatterbox | — | No (base) | Yes (Turbo) | No | MIT | General TTS, cloning |
| F5-TTS | — | No | No | No | Apache 2.0 | Voice cloning |

*Fish Audio Research License for weights

---

### 4. Cost Analysis — Podcast Audio Generation

#### Cloud APIs (per minute of generated audio)

| Provider | Model | Cost/min (approx) | Notes |
|----------|-------|------------------|-------|
| OpenAI | gpt-4o-mini-tts | ~$0.015/min | $0.60/M input tokens + $12/M output tokens |
| OpenAI | TTS standard | ~$0.10/min | $15/M characters |
| OpenAI | TTS HD | ~$0.20/min | $30/M characters |
| ElevenLabs | Standard | ~$0.18/min | Creator: $0.30/1000 chars; ~150 words/min = ~900 chars |
| ElevenLabs | Scale tier | ~$0.11/min | $0.18/1000 chars |
| Fish Audio API | S2 | ~$0.05/min | Dramatically cheaper for volume |
| Play.ht | Creator ($39/mo) | ~$0.065/min | 600K chars/yr included |
| Google NotebookLM | Podcast API | Undisclosed | Enterprise only, contact sales |
| Google NotebookLM | Consumer (Pro) | $19.99/mo flat | 20 Audio Overviews/day limit |

**Notes on ElevenLabs calculation:** At 150 words/minute average speech, ~900 chars/min. Creator-tier overage at $0.30/1000 chars = $0.27/min. Pro-tier ($99/mo, 500K credits) = ~$0.18/min effective.

#### Self-Hosted Open Source (per minute of generated audio)

Cost = GPU compute only. No per-character fees.

| GPU | Model | RTF | Time to gen 1 min | Cloud GPU cost/hr (est.) | $/min audio |
|-----|-------|-----|-------------------|-------------------------|-------------|
| RTX 3060 | Fish Speech S2 | 0.07 | ~4s | N/A (owned) | ~$0.001 (electricity) |
| RTX 4070 | F5-TTS | 0.33 | ~20s | $0.30-0.50/hr | ~$0.003 |
| RTX 4090 | Fish Speech S2 | ~0.14 | ~8s | $1.20/hr | ~$0.003 |
| H200 (cloud) | Fish Speech S2 | 0.195 | ~12s | $4-6/hr | ~$0.015-0.020 |

**Takeaway:** Self-hosted on owned hardware ≈ $0.001-0.003/min. Even on rented cloud GPUs, self-hosted approaches $0.015-0.020/min — competitive with gpt-4o-mini-tts without any per-minute billing risk.

#### Crossover Point

For >1000 minutes/month: self-hosted wins decisively. For <100 minutes/month: cloud APIs more economical (no GPU overhead).

---

### 5. AI Podcast Generation Ecosystem — New Tools & Startups

**Dedicated podcast generation platforms (2025-2026):**
- **Podcastle** — 500+ AI voices, emotional modulation, voice cloning, royalty-free music library
- **Podsqueeze** — Post-production automation: transcripts, summaries, SEO blog posts from episodes
- **AutoContent API** — Third-party "NotebookLM alternative" API for programmatic podcast generation; processes URLs, YouTube, text; generates two-host conversational audio

**Key market data:**
- Global podcasting market: $30.72B in 2024 → projected $131.13B by 2030 (27% CAGR)
- ElevenLabs ARR: $25M (2023) → $200M (Q3 2025); valuation $6.6B after $180M Series C (Feb 2025)

---

## Disagreements & Open Questions

1. **NotebookLM Podcast API pricing:** Google has not published pricing. The API exists (confirmed via official docs, August 2025) but cost is opaque — requires sales engagement.

2. **Fish Speech S2 license ambiguity:** While marketed as open-source, the model weights require "Fish Audio Research License" — commercial use requires separate agreement. This is a meaningful caveat for production use.

3. **"Rivals ElevenLabs" claims for Dia:** Nari Labs' own claims of superiority over ElevenLabs lack independent benchmark backing. The model is impressive but independent MOS benchmarks are limited.

4. **OpenAI TTS billing complexity:** Community reports indicate actual billed costs sometimes exceed simplified estimates due to token counting methodology for audio output tokens.

---

## Evidence Table

| # | Source | URL | Key Claim | Type | Confidence |
|---|--------|-----|-----------|------|------------|
| 1 | Google Workspace Updates — March 2025 | https://workspaceupdates.googleblog.com/2025/03/new-features-available-in-notebooklm.html | Audio Overview interactive controls (Smart Pause etc.) | Primary | High |
| 2 | Google Cloud Docs — Podcast API | https://docs.cloud.google.com/gemini/enterprise/notebooklm-enterprise/docs/podcast-api | Standalone Podcast API, GA-with-allowlist, MP3 output | Primary | High |
| 3 | Google Cloud Release Notes | https://docs.cloud.google.com/gemini/enterprise/docs/release-notes | Podcast API launched Aug 28 2025; Gemini 2.5 Flash Dec 2025 | Primary | High |
| 4 | Stelia AI Newsroom — Dia | https://newsroom.stelia.ai/dia-text-to-speech-open-source-breakthrough/ | Dia 1.6B released Apr 21 2025, Apache 2.0, nonverbal tags | Secondary | High |
| 5 | Sesame AI — GitHub | https://github.com/SesameAILabs/csm | CSM-1B released Mar 13 2025, Apache 2.0, conversational | Primary | High |
| 6 | Fish Audio — Fish Speech S2 | https://fish.audio/s2/ | Released Mar 10 2026, 81.88% win vs GPT-4o-mini-tts | Primary | High |
| 7 | Emelia.io — Fish Speech S2 | https://emelia.io/hub/fish-speech-s2-tts | $0.05/min API cost vs ElevenLabs $0.18/min | Secondary | Medium |
| 8 | Resemble AI — Chatterbox | https://www.resemble.ai/chatterbox/ | MIT license, 63.75% preferred over ElevenLabs | Primary | High |
| 9 | Codersera — Dia vs CSM | https://codersera.com/blog/nari-dia-1-6b-vs-sesame-csm-1b-which-is-the-best-tts | Dia: podcast use; CSM: conversational/realtime use | Secondary | High |
| 10 | OpenAI Community | https://community.openai.com/t/new-tts-api-pricing-and-gotchas/1150616 | gpt-4o-mini-tts ~$0.015/min | Primary (community) | Medium |
| 11 | ElevenLabs Pricing | https://elevenlabs.io/pricing | Creator $11/mo, 100K credits; overages $0.30/1K chars | Primary | High |
| 12 | Google Workspace — 50 languages | https://workspaceupdates.googleblog.com/2025/04/language-expansion-audio-overviews-notebooklm.html | Audio Overviews in 50+ languages (April 2025) | Primary | High |

---

## Sources

1. Google Workspace Updates, Mar 2025 — https://workspaceupdates.googleblog.com/2025/03/new-features-available-in-notebooklm.html
2. Google Cloud Docs — Podcast API — https://docs.cloud.google.com/gemini/enterprise/notebooklm-enterprise/docs/podcast-api
3. Google Cloud Docs — Audio Overview API — https://docs.cloud.google.com/gemini/enterprise/notebooklm-enterprise/docs/api-audio-overview
4. Google Cloud Release Notes — https://docs.cloud.google.com/gemini/enterprise/docs/release-notes
5. Google Workspace — 50+ language Audio Overviews — https://workspaceupdates.googleblog.com/2025/04/language-expansion-audio-overviews-notebooklm.html
6. Stelia AI — Dia TTS — https://newsroom.stelia.ai/dia-text-to-speech-open-source-breakthrough/
7. Sesame AI GitHub — https://github.com/SesameAILabs/csm
8. Sesame Hugging Face — https://huggingface.co/sesame/csm-1b
9. ComfyUI Wiki — Sesame CSM — https://comfyui-wiki.com/en/news/2025-03-03-sesame-csm
10. Fish Audio S2 — https://fish.audio/s2/
11. Fish Speech GitHub — https://github.com/fishaudio/fish-speech
12. Emelia.io Fish Speech S2 — https://emelia.io/hub/fish-speech-s2-tts
13. Resemble AI Chatterbox — https://www.resemble.ai/chatterbox/
14. Chatterbox GitHub — https://github.com/resemble-ai/chatterbox
15. Codersera — Dia vs CSM — https://codersera.com/blog/nari-dia-1-6b-vs-sesame-csm-1b-which-is-the-best-tts
16. DigitalOcean — Best TTS Models — https://www.digitalocean.com/community/tutorials/best-text-to-speech-models
17. ElevenLabs Pricing — https://elevenlabs.io/pricing
18. OpenAI TTS Community — https://community.openai.com/t/new-tts-api-pricing-and-gotchas/1150616
19. AutoContent API — NotebookLM alternative — https://autocontentapi.com/blog/does-notebooklm-have-an-api
20. NotebookLM Plans — https://notebooklm.google/plans

---

## Coverage Status

- **Directly verified (fetched and read):**
  - Google Podcast API docs (official, Aug 2025)
  - Google Cloud release notes (confirmed Aug 28 2025 date)
  - Dia release facts (Apr 21 2025)
  - Fish Speech S2 benchmark numbers (Mar 2026)
  - Sesame CSM release date and architecture

- **Inferred from multiple sources:**
  - ElevenLabs cost-per-minute calculation (multiple pricing pages)
  - Open-source GPU inference speed estimates (A2E.ai, BentoML, search results)
  - NotebookLM consumer tier restructuring (multiple review sites)

- **Unresolved:**
  - Google Podcast API pricing (not disclosed anywhere)
  - Chatterbox exact release date
  - Independent MOS benchmarks for Dia vs ElevenLabs (Nari Labs claims unverified)
  - OpenAI TTS exact per-minute billing for multi-host/conversational scenarios
