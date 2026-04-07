---
name: NotebookLM Podcast API
type: tool
first_seen: 2026-04-07
last_updated: 2026-04-07
sources: [podcast-tts-research]
tags: [tts, podcast-generation, google, audio]
---
# NotebookLM Podcast API

> Google Cloud enterprise API for programmatic podcast/audio generation, GA-with-allowlist since August 28, 2025; standalone (no notebook required), input up to 100K tokens, outputs MP3.

## Key Facts

- GA-with-allowlist since August 28, 2025; access requires contacting Google Cloud sales (ref: sources/podcast-tts-research.md)
- Standalone API — does NOT require a NotebookLM notebook, Gemini Enterprise license, or data store (ref: sources/podcast-tts-research.md)
- Input: array of multimedia objects (text, images, audio, video); max 100,000 tokens; output: MP3 (ref: sources/podcast-tts-research.md)
- Length options: SHORT (4-5 min) or STANDARD (~10 min) (ref: sources/podcast-tts-research.md)
- Pricing: NOT disclosed — enterprise only, sales-rep engagement required (ref: sources/podcast-tts-research.md)
- IAM role: `roles/discoveryengine.podcastApiUser` (ref: sources/podcast-tts-research.md)

## Relevance to STOPA

Relevant for NG-ROBOT media expansion (audio content from articles) and any podcast-format output pipeline. Blocked by opaque enterprise pricing — AutoContent API is a cheaper alternative for non-enterprise.

## Mentioned In

- [AI Podcast Generation & TTS Ecosystem](../sources/podcast-tts-research.md)
