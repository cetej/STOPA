---
title: "AI Podcast Generation & TTS Ecosystem"
slug: podcast-tts-research
source_type: research_output
date_ingested: 2026-04-07
entities_extracted: 7
claims_extracted: 4
---
# AI Podcast Generation & TTS Ecosystem

> **TL;DR**: NotebookLM Podcast API reached GA-with-allowlist in August 2025 (enterprise only, undisclosed pricing). Open-source TTS models (Sesame CSM-1B, Dia 1.6B, Fish Speech S2, Chatterbox) have closed the quality gap with proprietary APIs. For >1000 min/month, self-hosted wins decisively at $0.001-0.003/min vs ElevenLabs $0.18/min or OpenAI TTS $0.015-0.20/min.

## Key Claims

1. NotebookLM Podcast API is GA-with-allowlist since August 28, 2025 — standalone, no notebook required, input up to 100K tokens, outputs MP3 — pricing not disclosed — `[verified]`
2. Fish Speech S2 achieves 81.88% win rate vs GPT-4o-mini-tts on EmergentTTS-Eval with WER 0.99% (English), at $0.05/min API vs ElevenLabs $0.18/min — `[verified]`
3. Self-hosted open-source TTS on owned GPU costs $0.001-0.003/min vs cloud API $0.015-0.20/min; crossover point is ~1000 min/month — `[argued]`
4. Chatterbox (MIT license) is the only fully permissive commercial-use open-source TTS with emotion exaggeration control; 63.75% evaluators preferred it over ElevenLabs — `[argued]`

## Entities

| Entity | Type | Status |
|--------|------|--------|
| NotebookLM Podcast API | tool | new |
| Sesame CSM-1B | tool | new |
| Dia 1.6B (Nari Labs) | tool | new |
| Fish Speech S2 | tool | new |
| Chatterbox (Resemble AI) | tool | new |
| ElevenLabs | company | new |
| F5-TTS | tool | new |

## Relations

- Sesame CSM-1B `competes_with` Dia 1.6B
- Fish Speech S2 `outperforms` GPT-4o-mini-tts (EmergentTTS-Eval)
- Chatterbox `challenges` ElevenLabs
- NotebookLM Podcast API `produces` MP3 audio
- Dia 1.6B `enables` nonverbal cues via text tags
