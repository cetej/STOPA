---
name: NG-ROBOT Media Expansion Plan
description: 6-phase plan for multi-file inbox, Groq Whisper transcription, subtitles, dubbing pipeline
type: project
---

NG-ROBOT rozšíření o multimédia — schváleno 2026-04-03.

**Why:** Uživatel potřebuje vkládat různé typy souborů (audio, video, obrázky) vedle textu, transkribovat audio/video, generovat titulky a předabovat.

## Implementační fáze

| Fáze | Co | Náklady | Status |
|------|----|---------|--------|
| 1 | Multi-file inbox (text + obrázky + audio + video upload, bundling) | $0 | TODO |
| 2 | Transkripce (Groq Whisper primary + faster-whisper fallback) | ~$0.11/hod | TODO |
| 3 | Audio extrakce z videa (ffmpeg → Whisper pipeline) | $0 | TODO |
| 4 | Generování titulků (SRT/VTT z transkripce) | $0 | TODO |
| 5 | Základní dubbing (transkripce → překlad → TTS → merge) | ~$0.15/hod | TODO |
| 6 | Lip sync (Wav2Lip, volitelné) | $0 (GPU) | TODO |

## Fáze 1 — Multi-file article bundle (DETAIL)

### Cíl
Rozšířit inbox tak, aby uživatel mohl nahrát více souborů najednou (text + obrázky + audio + video) a systém je seskupil do jednoho article directory.

### Co implementovat

1. **Rozšířit `allowed_file()` v ngrobot_web.py** o mediální formáty:
   - Obrázky: `.jpg`, `.jpeg`, `.png`, `.webp`, `.gif`
   - Audio: `.mp3`, `.wav`, `.m4a`, `.ogg`, `.flac`, `.wma`
   - Video: `.mp4`, `.avi`, `.mkv`, `.mov`, `.webm`

2. **Nový endpoint `/api/inbox/upload-bundle`** (nebo rozšířit upload-multiple):
   - Přijme N souborů + volitelný "bundle name"
   - Auto-klasifikuje typ (text/image/audio/video)
   - Textový soubor → hlavní dokument pro pipeline
   - Média → podsložky (images/, audio/, videos/)
   - Bez textu → placeholder s metadaty

3. **Rozšířit `document_processor.process_inbox()`**:
   - Rozpoznat bundle directory (ne jen flat files)
   - Předat média do article directory v `articles/`
   - Obrázky z bundlu → integrace do Phase 9

4. **UI rozšíření** (inbox stránka):
   - Drag & drop zóna pro více souborů
   - Vizuální indikace typu souboru (ikony)
   - Bundling interface

### Soubory k editaci
- `ngrobot_web.py` — allowed_file(), upload routes
- `blueprints/batch_bp.py` — inbox API endpoints
- `document_reader.py` — media type detection
- `document_processor.py` — bundle processing logic
- Templates/JS pro inbox UI

### Pravidla
- Zpětná kompatibilita stávajícího textového uploadu
- Pipeline fáze 0-9 se nemění — média se jen přikládají
- API klíče NIKDY do JSON — env vars

## Technická rozhodnutí

### Transkripce (Fáze 2)
- **Primární:** Groq Whisper Large V3 ($0.11/hod, čeština ✅)
- **Limity:** 25 MB upload / 100 MB via URL → ffmpeg auto-chunking
- **Fallback:** Lokální faster-whisper (zdarma, GPU 3-4 GB, bez limitu)
- **OpenAI Whisper:** $0.36/hod, 25 MB limit (záložní)

### Dubbing (Fáze 5)
- **Levný:** Groq transkripce + Claude překlad + Edge TTS (zdarma) + ffmpeg ≈ $0.15/hod
- **Premium:** ElevenLabs Dubbing Studio ($5-11/měs, 1 GB / 2.5 hod, čeština ✅)

### Co už existuje v NG-ROBOT
- ffmpeg (imageio-ffmpeg) ✅
- Edge TTS (cs-CZ-VlastaNeural, AntoninNeural) ✅
- Google TTS Chirp 3 HD (30 CZ hlasů) ✅
- Gemini TTS ✅
- Playwright pro video download ✅
- STT/Whisper ❌ (nové — Fáze 2)

### VibeVoice (Microsoft) — sledovat
- 60 min single pass, speaker diarization, MIT licence
- Čeština nepotvrzena, 12-24 GB VRAM
- Zatím nepoužívat, preferovat Whisper
