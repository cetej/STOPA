---
name: Voxtral TTS (Mistral AI)
description: Open-weight multilingual TTS with voice cloning from 3s reference — 9 languages, NO Czech support. Candidate for future TTS pipeline if Czech added.
type: reference
---

## Voxtral TTS (arXiv:2603.25551, 2026-03-27)

**What:** Zero-shot multilingual TTS by Mistral AI, open weights (CC BY-NC).

**Architecture:**
- Voxtral Codec: 24kHz → 12.5Hz tokens (1 semantic VQ + 36 acoustic FSQ), 2.14 kbps
- Semantic token via ASR distillation from Whisper (not self-supervised — actually semantic)
- Decoder backbone: Ministral 3B, autoregressive on semantic tokens
- Flow-matching transformer: 3-layer, generates 36 acoustic tokens in 8 steps (vs 36 sequential for depth transformer)
- DPO adapted for hybrid discrete-continuous setting (semantic + flow-based preference)

**Results:**
- 68.4% win rate vs ElevenLabs Flash v2.5 (voice cloning, human eval)
- Voice cloning from 3 seconds of reference audio
- Streaming inference, sub-second latency, 30+ concurrent users on single H200

**Languages (9):** Arabic, Dutch, English, French, German, Hindi, Italian, Portuguese, Spanish
- **NO Czech, NO Slavic languages at all**
- Potential for future expansion — architecture is language-agnostic

**Serving:** vLLM-Omni, CUDA graph acceleration, chunked streaming

**How to apply:**
- Monitor for Czech language support in future versions
- Compare with alternatives that support Czech (e.g., Coqui XTTS, Microsoft Speech)
- Architecture patterns (semantic/acoustic factorization, flow-matching for parallel acoustic generation) are reusable insights for any TTS pipeline
