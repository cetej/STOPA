---
name: Fish Speech S2
type: tool
first_seen: 2026-04-07
last_updated: 2026-04-07
sources: [podcast-tts-research]
tags: [tts, open-source, audio, multilingual]
---
# Fish Speech S2

> Dual-AR TTS model from Fish Audio (4.4B params: 4B Slow AR + 400M Fast AR), trained on 10M hours of audio; 80+ languages, <150ms latency.

## Key Facts

- Released March 10, 2026; code Apache-licensed, model weights use Fish Audio Research License (commercial requires separate agreement) (ref: sources/podcast-tts-research.md)
- WER: 0.54% (Chinese), 0.99% (English); EmergentTTS-Eval: 81.88% win rate vs GPT-4o-mini-tts (ref: sources/podcast-tts-research.md)
- API cost: ~$0.05/min vs ElevenLabs ~$0.18/min (ref: sources/podcast-tts-research.md)
- 15,000+ natural language emotion/style tags; 80+ languages (ref: sources/podcast-tts-research.md)
- GitHub: github.com/fishaudio/fish-speech (ref: sources/podcast-tts-research.md)
- Caveat: model weights license blocks drop-in commercial self-hosting without separate agreement (ref: sources/podcast-tts-research.md)

## Relevance to STOPA

Best cost/quality ratio for production multi-language TTS via API. For NG-ROBOT audio generation at volume, cheapest cloud option among quality providers. Self-hosted blocked by weight license for commercial.

## Mentioned In

- [AI Podcast Generation & TTS Ecosystem](../sources/podcast-tts-research.md)
