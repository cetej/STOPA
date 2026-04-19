---
name: Voice cloning tools — Voicebox + VoxCPM2
description: Open-source voice cloning studios pro budoucí audio studio projekt; čeština není oficiálně podporována, VoxCPM2 má LoRA fine-tuning cestu
type: reference
---

## Voicebox (jamiepine/voicebox)
**Repo:** https://github.com/jamiepine/voicebox | **Licence:** MIT
**Web:** https://voicebox.sh

Lokální voice cloning studio — alternativa k ElevenLabs. 5 TTS engine, 23 jazyků, post-processing efekty, stories editor (multi-voice timeline), REST API.

**Stack:** Tauri (Rust), React/TS, Tailwind, Zustand, FastAPI (Python), SQLite, MLX/PyTorch, Pedalboard (Spotify)
**GPU:** Apple Silicon (MLX/Metal), NVIDIA (CUDA), AMD (ROCm), Intel Arc (IPEX), DirectML, CPU

**TTS enginy:**
- Qwen3-TTS (0.6B/1.7B) — 10 jazyků, delivery instructions
- LuxTTS — jen EN, lightweight (~1GB VRAM), 150x realtime CPU
- Chatterbox Multilingual — 23 jazyků (BEZ češtiny)
- Chatterbox Turbo — jen EN, paralinguistic tags ([laugh], [sigh]...)
- HumeAI TADA (1B/3B) — 10 jazyků, 700s+ koherentní audio

**Čeština: NENÍ.** Závisí na upstream modelech. Přidání do Voicebox = 4 soubory (regex + language map).

---

## VoxCPM2 (OpenBMB/VoxCPM)
**Repo:** https://github.com/OpenBMB/VoxCPM | **Licence:** Apache-2.0
**HF:** huggingface.co/openbmb/VoxCPM2 | **Docs:** voxcpm.readthedocs.io

2B parametrů, 2M+ hodin dat, tokenizer-free diffusion autoregressive (MiniCPM-4 backbone), 48kHz výstup.

**30 jazyků:** ar, my, zh, da, nl, en, fi, fr, de, el, he, hi, id, it, ja, km, ko, lo, ms, no, pl, pt, ru, es, sw, sv, tl, th, tr, vi — **BEZ češtiny oficiálně**, ale v benchmarku MiniMax-MLS čeština testována (WER 24.1% — špatný, ElevenLabs 2.1%).

**Klíčové funkce (navíc oproti Voicebox):**
- Voice Design — hlas z textového popisu, bez referenčního audia
- Controllable Cloning — klonuj + řiď emoci/tempo instrukcemi
- Ultimate Cloning — audio + transkript → věrná reprodukce nuancí
- LoRA fine-tuning — 5-10 min audia stačí pro adaptaci na jazyk/mluvčího
- Streaming API, CLI, WebUI, Nano-vLLM production serving
- ~8 GB VRAM, RTF ~0.3 (4090), 0.13 s Nano-vLLM

**Čeština:** Model ji částečně zvládá (testována v benchmarku), ale nekvalitně. **LoRA fine-tuning na českých datech = realistická cesta k české podpoře.**

**Ekosystém:** VoxCPM.cpp (GGUF/CPU), ONNX export, Apple Neural Engine, Rust reimpl, ComfyUI nodes

---

## Srovnání pro audio studio projekt

| | Voicebox | VoxCPM2 |
|---|---|---|
| Čeština | NE | Částečně (LoRA cesta) |
| Voice design | NE | ANO |
| Controllable clone | NE | ANO |
| Fine-tuning | NE | ANO (SFT + LoRA) |
| UI/UX | Nativní Tauri app, stories editor | WebUI, CLI |
| Post-processing | ANO (8 efektů, presety) | NE |
| Licence | MIT | Apache-2.0 |
| Kvalita audia | závisí na enginu | 48kHz studio |

**Doporučení:** VoxCPM2 jako TTS backend (voice design + LoRA čeština), Voicebox jako UI inspirace (stories editor, efekty). Případně oba — Voicebox může integrovat VoxCPM2 jako další engine.

**Why:** Uživatel uvažuje o vytvoření hlasů a audio studia.
**How to apply:** Při startu audio projektu začít s VoxCPM2 + LoRA fine-tuning na českém datasetu. Voicebox sledovat pro UI/UX inspiraci a potenciální integraci.
