---
name: NG-ROBOT Media Expansion Plan
description: Plan for multi-file inbox, audio/video transcription, subtitles, dubbing in NG-ROBOT
type: project
---

NG-ROBOT rozšíření o multimédia — schváleno 2026-04-03.

**Why:** Uživatel potřebuje vkládat různé typy souborů (audio, video, obrázky) vedle textu, transkribovat audio/video, generovat titulky a předabovat.

**How to apply:** Implementovat v 6 fázích, začít fází 1 (multi-file inbox).

## Implementační fáze

| Fáze | Co | Náklady | Effort | Status |
|------|----|---------|--------|--------|
| 1 | Multi-file inbox (text + obrázky + audio + video upload, bundling) | $0 | 2-3 dny | TODO |
| 2 | Transkripce (Groq Whisper primary + faster-whisper fallback) | ~$0.11/hod | 1-2 dny | TODO |
| 3 | Audio extrakce z videa (ffmpeg → Whisper pipeline) | $0 | půl dne | TODO |
| 4 | Generování titulků (SRT/VTT z transkripce) | $0 | půl dne | TODO |
| 5 | Základní dubbing (transkripce → překlad → TTS → merge) | ~$0.15/hod | 2-3 dny | TODO |
| 6 | Lip sync (Wav2Lip, volitelné) | $0 (GPU) | 3-5 dní | TODO |

## Technické rozhodnutí

### Transkripce
- **Primární:** Groq Whisper Large V3 ($0.11/hod, 100 MB via URL, čeština ✅)
- **Fallback:** Lokální faster-whisper (zdarma, bez limitu, potřebuje GPU 3-4 GB)
- **Omezení Groq:** 25 MB upload / 100 MB via URL → ffmpeg auto-chunking pro velké soubory
- **OpenAI Whisper:** $0.36/hod, 25 MB limit — dražší, ale spolehlivé (záložní option)

### Dubbing
- **Levný pipeline:** Groq transkripce + Claude překlad + Edge TTS (zdarma) + ffmpeg merge ≈ $0.15/hod
- **Premium:** ElevenLabs Dubbing Studio ($5-11/měs, 1 GB / 2.5 hod limit, čeština ✅, zero kód)
- **Lip sync:** Wav2Lip (open-source, GPU 4+ GB) — volitelná fáze 6

### Multi-file inbox
- Rozšíření stávajícího inbox API (`/api/inbox/upload-multiple`)
- Nový koncept "article bundle" — seskupení souborů do jednoho article directory
- Automatická detekce typu: text → zpracování pipeline, obrázky → images/, audio → audio/, video → videos/
- Obrázky přiložené k textu → integrace do Phase 9 (finální článek)

### Co už existuje v NG-ROBOT
- ffmpeg (imageio-ffmpeg) ✅
- Edge TTS (cs-CZ-VlastaNeural) ✅
- Google TTS Chirp 3 HD (30 CZ hlasů) ✅
- Gemini TTS ✅
- Playwright pro video download ✅
- NotebookLM audio/video ✅
- STT/Whisper ❌ (nové)

### VibeVoice (Microsoft)
- Sledovat pro budoucnost — 60 min single pass, speaker diarization
- Čeština nepotvrzena, vysoké VRAM nároky (12-24 GB)
- Zatím nepoužívat, preferovat Whisper
