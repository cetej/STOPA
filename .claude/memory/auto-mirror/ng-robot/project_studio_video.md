---
name: Studio Video — multi-agent video production
description: Studio Video pipeline — 3-fázový multi-agent systém (Critic, Grafik, Multi-clip) implementován 2026-04-10
type: project
---

# Studio Video — stav

**Stav:** Multi-agent pipeline implementován a testován na chimps článku. Pipeline funguje E2E, kreativní kvalita výrazně lepší, ale stále potřebuje iteraci — UI nenačítá nový scénář pokud pipeline běží (scenario.json se uloží až po renderu).
**Aktualizováno:** 2026-04-10

## Co funguje (implementováno tuto session)

### Scenario generator (Sonnet + Haiku)
- `ng-video/studio/scenario_generator.py` — dvou-callový přístup
- **Sonnet** = editorial plán (hlavní sdělení, pořadí scén, dramaturgická logika)
- **Haiku** = structured outputs (JSON scénář podle plánu)
- Detekce jazyka: `1_translated.md` existuje → CZ, fallback `0_analysis.json`

### Image generation (Nano Banana Pro = Gemini)
- `generate_images()` v `render.py` — nahradilo FLUX Pro
- Nano Banana zná reálnou technologii (Orion, Artemis II, NASA) — FLUX hallucintuje
- `image_generator.py` → `ImageGenerator.generate_from_prompt()`

### Video clip generation (Seedance 2.0 / Kling / Veo 2)
- `generate_clips_fal()` v `render.py` — image-to-video
- Dostupné modely: `seedance`, `seedance-fast`, `veo2`, `kling`
- Default: Seedance 2.0 (`bytedance/seedance-2.0/image-to-video`)
- `.env` override: `FAL_KEY` musí být aktuální (shell env může mít starou hodnotu → dotenv load v render.py)

### Pipeline (task_generate_studio_video v ngrobot_web.py)
Správné pořadí: scénář → **TTS** → přepočet scén podle audia → obrázky → klipy → render
- Audio řídí délku videa (ne naopak)
- `skip_clips=False` default (klipy ON)
- Staging dir pro Remotion (12 souborů místo 500MB)
- Remotion render: `--public-dir` + `--props` soubor + `src/index.ts` + absolutní output path

### Studio Editor UI
- Modální scene editor (klik na thumbnail → full-screen, obrázek vlevo, texty vpravo)
- Navigace Předchozí/Další, ESC
- Save → scenario.json, regenerate image (Nano Banana / FLUX), upload, z článku
- Audio přehrávač + TTS text textarea + přegenerovat

### API endpointy (blueprints/articles_bp.py)
- `POST /api/article/studio-video` — celý pipeline
- `POST /api/article/studio-video/save-scenario`
- `POST /api/article/studio-video/regenerate-image`
- `POST /api/article/studio-video/regenerate-tts`
- `POST /api/article/studio-video/upload-image`

## Známé bugy (opravit na začátku)

1. **Intro scéna brala infografiku z článku** → OPRAVENO (image=None, generuje se)
2. **Seedance content policy** — odmítá obrázky s realistickými tvářemi lidí (Mission Control). Řešení: visual prompt nesmí generovat rozpoznatelné obličeje, nebo fallback na Kling.
3. **Edge TTS příliš pomalé** — 85s audio pro 30s video. ElevenLabs není nainstalovaný (`pip install elevenlabs`). S ElevenLabs bude kratší.
4. **1 obrázek = 1 klip per scéna** — pro 20s scénu by měly být 2+ klipy nebo delší klip

## Multi-agent pipeline — IMPLEMENTOVÁNO (2026-04-10)

### Fáze 1: Critic Agent (HOTOVO)
- **`ng-video/studio/critic.py`** — Claude Sonnet Vision review obrázků
- Po `generate_images()`, před `generate_clips_fal()`
- Structured output: verdikty per scene (approve/reject + risk type + new_prompt)
- Max 1 iterace regenerace. `skip_critic` API param pro bypass.
- ~$1.20 za video (Sonnet Vision call)

### Fáze 2: Visual Prompt Specialist (HOTOVO)
- Tří-callový přístup v `scenario_generator.py`:
  - Call 1: Sonnet → editorial plán
  - Call 2: Haiku → texty (voiceover, overlay) — BEZ visual promptů
  - Call 3: Haiku → vizuální prompty (specializovaný grafik)
- `seedance_safe` hint v promptech → pre-screening pro content policy
- Fallback: pokud Call 3 selže, generuje se z voiceover textu

### Fáze 3: Multi-clip scény (HOTOVO)
- `SubClip` model v `schema.py` (backward compat: `sub_clips=[]`)
- Scény > 10s → 2 klipy, > 20s → 3 klipy
- Každý sub-clip má jiný camera motion (zoom, pan, drift, push, static, pull-back)
- `SubClipPlayer` v Remotion → `<Sequence>` per sub-clip
- Staging dir zpracovává sub-clip cesty

### Budoucí vylepšení
- **Režisér agent** (TeamCreate) — orchestruje celý process, iterativní vylepšování
- **Paralelní generování** — obrázky + klipy concurrent

### Sjednocení s Video poutáky (budoucnost)
- Jedno rozhraní pro oba typy videí
- Poutáky = krátký formát (15-30s), 3 callouty, Ken Burns
- Studio = obsahový formát (30-120s), video klipy, plný voiceover
- Sdílená infrastruktura: TTS, Remotion, obrázky, UI editor
- Video poutáky zatím NEMĚNIT — jen plánovat sjednocení

## Klíčové soubory

| Soubor | Účel |
|--------|------|
| `ng-video/studio/scenario_generator.py` | Sonnet+Haiku scénář |
| `ng-video/studio/render.py` | Pipeline orchestrátor (images, clips, TTS, music, render) |
| `ng-video/studio/schema.py` | Pydantic modely |
| `ng-video/src/compositions/NGVideoStudio.tsx` | Remotion kompozice |
| `ng-video/remotion.config.ts` | Remotion config (publicDir) |
| `static/js/article/studio-editor.js` | Editor UI JS |
| `blueprints/articles_bp.py` | API endpointy |
| `ngrobot_web.py` | Task funkce + registrace |
| `templates/article_detail.html` | Studio Video template sekce |
| `social_video_generator.py` | Video poutáky (NEMĚNIT, referenční) |

## Testovací článek
`processed/2026-04-08_space-weather-can-be-deadly-heres-how-nasa-protects-the-artemis-ii-crew/`
