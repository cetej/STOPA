---
name: klip
description: Use when generating video via Kling on fal.ai. Trigger on 'generate video', 'klip', 'video clip'. Requires FAL_KEY env var. Do NOT use for images (/nano).
argument-hint: <prompt> [--image path/url] [--duration 5|10|15] [--aspect 16:9|9:16|1:1] [--tier standard|pro] [--output path]
tags: [generation, media]
phase: build
requires: [FAL_KEY]
user-invocable: true
allowed-tools:
  - Bash
  - Read
  - Write
  - Glob
model: sonnet
maxTurns: 12
effort: medium
---

# Kling — Video Generation via fal.ai

Generate high-quality video animations using Kling 3.0 through fal.ai API.

## Prerequisites

- `fal-client` Python package installed (`pip install fal-client`)
- `FAL_KEY` environment variable set (check `~/.claude/settings.json` env section)

<!-- CACHE_BOUNDARY -->

## Step 1: Parse Arguments

Extract from user input:
- **prompt**: Video description (required)
- **--image**: Input image for image-to-video. Can be:
  - Local file path (will be uploaded to fal.ai)
  - URL (used directly)
  - If omitted → text-to-video mode
- **--duration**: `5` (default), `10`, or `15` seconds
- **--aspect**: `16:9` (default), `9:16`, `1:1`
- **--tier**: `standard` (default) or `pro` (better quality, higher cost)
- **--output**: Output directory (default: `output/videos/` in current project)

## Step 2: Check FAL_KEY

```bash
python -c "import os; key = os.environ.get('FAL_KEY', ''); print('OK' if key else 'MISSING')"
```

Note: On this Windows system, use `python` not `python3` — fal-client is installed under `C:\Python313\python`.

If MISSING: tell user to add FAL_KEY to `~/.claude/settings.json` under `"env"` and restart Claude Code.

## Step 2b: Load prompt-library (if available)

Check if `prompt-library.yaml` exists in project root or STOPA root (`C:/Users/stock/Documents/000_NGM/STOPA/prompt-library.yaml`).

If found, load:
- `video.negative_prompt.template` → use as NEGATIVE_PROMPT value
- `video.patterns.*` → use matching pattern template when user describes a known effect (rotating, zoom, pan, etc.)

If not found, use hardcoded fallback: `"blur, distort, low quality, watermark, text overlay"`.

## Step 2c: Prompt Quality Gate

Before sending to the API, validate and enhance the prompt. This is a hard gate — fix issues before proceeding, do NOT call API with invalid prompts.

### Validation Rules (LLM-native — execute mentally, no Python)

| # | Rule | Severity | Check |
|---|------|----------|-------|
| ① | Prompt length 15–150 words | ❌ error if <15 or >200 | Too short = vague; too long = concept drift |
| ② | At least 1 camera/motion term | ⚠️ warning | Without motion direction, output looks like a slideshow. Add one: pan, zoom, tracking, dolly, rotate, drift, push-in, pull-back, orbit, tilt |
| ③ | No filler words | ❌ error | Hard-block: masterpiece, ultra-HD, 8K, best quality, hyper-realistic, extremely detailed, super resolution, ultra-clear. Use physical material/light words instead |
| ④ | Descriptive, not narrative | ⚠️ warning | Emotions → physical expressions. "She feels sad" → "tears streaming down her cheeks". Only describe what the renderer can SEE |
| ⑤ | No style conflicts | ❌ error | See conflict matrix below |
| ⑥ | I2V: changes only | ⚠️ warning | If `--image` provided: describe only motion/changes from the input image, not static content already visible. Prepend `preserve composition and colors` |

### Style Conflict Matrix (mutually exclusive — ❌ error if combined)

- Photorealistic + cartoon/anime style
- Film grain/vintage + ultra-sharp/crystal-clear
- Slow motion + speed ramp in same segment
- Wide-angle fisheye + shallow depth-of-field bokeh (physically impossible)
- Handheld shaky cam + perfect geometric symmetry

### Enhancement (auto-apply before API call)

- Convert emotional/narrative descriptions → observable physical actions
- Add motion intensity modifier if action verbs are vague (see Motion Intensity Scale below)
- Prefer semantic rhythm words (gentle, gradual, smooth) over technical params (24fps, f/2.8) — Kling parses semantics, not numbers

If any ❌ error after enhancement: inform user of the conflict and suggest fix. Do NOT proceed to API.

## Step 3: Determine Mode

| `--image` provided? | Mode | Endpoint |
|---------------------|------|----------|
| No | Text-to-Video | `fal-ai/kling-video/v3/{tier}/text-to-video` |
| Yes (URL) | Image-to-Video | `fal-ai/kling-video/v3/{tier}/image-to-video` |
| Yes (local file) | Image-to-Video | Upload file first, then use URL |

**I2V Golden Rule**: In image-to-video mode, the prompt must describe only **motion and changes** — never re-describe static content already visible in the input image (character appearance, scene layout, composition). Auto-prepend `preserve composition and colors,` to the prompt to lock visual consistency.

## Step 4: Upload Local Image (if needed)

If `--image` is a local file path:

```bash
python -c "
import fal_client
import sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

url = fal_client.upload_file('LOCAL_PATH')
print(url)
"
```

Use the returned URL as `start_image_url`.

## Step 5: Generate Video

Video generation takes 1-3 minutes. Use async queue pattern with progress tracking.

### Text-to-Video:

```bash
python << 'PYEOF'
import fal_client
import json
import sys
import time

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

print("Submitting to Kling 3.0...", flush=True)

handler = fal_client.submit(
    "fal-ai/kling-video/v3/TIER/text-to-video",
    arguments={
        "prompt": """PROMPT_TEXT""",
        "duration": "DURATION",
        "aspect_ratio": "ASPECT",
        "generate_audio": False,
        "negative_prompt": "NEGATIVE_PROMPT",
        "cfg_scale": 0.5,
    }
)

print("Waiting for generation (1-3 min)...", flush=True)
start = time.time()

for event in handler.iter_events(with_logs=True):
    if isinstance(event, fal_client.InProgress):
        elapsed = int(time.time() - start)
        for log_entry in event.logs:
            print(f"  [{elapsed}s] {log_entry['message']}", flush=True)

result = handler.get()
elapsed = int(time.time() - start)
print(f"\nDone in {elapsed}s", flush=True)
print(json.dumps({"video_url": result["video"]["url"]}))
PYEOF
```

### Image-to-Video:

Same as above, but with endpoint `image-to-video` and additional argument:
```python
"start_image_url": "IMAGE_URL",
```

## Step 6: Download Video

```bash
python -c "
import urllib.request
import os
import sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

url = 'VIDEO_URL'
output_dir = 'OUTPUT_DIR'
os.makedirs(output_dir, exist_ok=True)

filename = 'FILENAME.mp4'
path = os.path.join(output_dir, filename)
urllib.request.urlretrieve(url, path)

size_mb = os.path.getsize(path) / (1024 * 1024)
print(f'Saved: {path}')
print(f'Size: {size_mb:.1f} MB')
"
```

**Naming convention**: `kling_{tier}_{duration}s_{timestamp}.mp4`
- Example: `kling_pro_5s_20260322_143052.mp4`

## Step 7: Report

```
Kling 3.0 — Generation Complete

Mode:       text-to-video
Tier:       pro
Prompt:     [first 80 chars]...
Duration:   5 seconds
Aspect:     16:9
Time:       87s

File: output/videos/kling_pro_5s_20260322_143052.mp4 (4.2 MB)

Cost estimate: ~$0.56 (5s × $0.112/s pro, no audio)
```

## Prompt Tips

### Effect Patterns (Kling 3.0)

| Effect | Prompt Pattern |
|--------|---------------|
| Rotating object | "smoothly rotating [object], center of mass stays fixed, rotating on its axis" |
| Exploding view | "exploding view diagram of [object], components separate in all directions, white background" |
| Camera pan | "cinematic slow pan across [scene], smooth camera movement" |
| Product shot | "product photography of [item], slowly rotating on pedestal, studio lighting" |
| Zoom in | "camera slowly zooming into [subject], shallow depth of field" |

### Descriptive Over Narrative

Only describe what the renderer can SEE — not emotions, intentions, or backstory:

| Don't write | Write instead |
|-------------|---------------|
| "She feels lonely" | "She sits motionless, staring at an empty chair across the table" |
| "An exciting chase" | "Man sprinting through rain-soaked alley, coat flapping violently behind him" |
| "Peaceful morning" | "Morning light through thin curtains, dust particles drifting slowly through beam" |
| "He is angry" | "Jaw clenched, fists tightening, veins visible on forearms" |

### Motion Intensity Scale

Use specific modifiers — avoid vague motion ("the camera moves", "object moves"):

| Intensity | Modifiers | Example |
|-----------|-----------|---------|
| Explosive | violent, sudden, snapping | "hair whipping violently in wind" |
| Dramatic | sweeping, surging, crashing | "waves crashing dramatically against cliff face" |
| Steady | smooth, flowing, continuous | "smooth tracking shot across landscape" |
| Gentle | gradual, drifting, easing | "petals gradually falling from branch" |
| Minimal | barely, subtly, faintly | "candle flame subtly flickering" |

Prefer rhythm words over technical params — `gentle gradual push-in` > `24fps f/2.8 slow dolly`.

## Error Handling

| Error | Cause | Fix |
|-------|-------|-----|
| `FAL_KEY not set` | Missing env var | Add to `~/.claude/settings.json` env, restart CC |
| `fal_client not found` | Package not installed | `pip install fal-client` |
| `401 Unauthorized` | Invalid or expired key | Check FAL_KEY at fal.ai dashboard |
| `429 Rate Limited` | Too many requests | Wait 60s, retry |
| `500 Server Error` | fal.ai backend issue | Wait 2 min, retry once |
| Timeout (>5 min) | Overloaded queue | Retry, consider standard tier |
| Upload fails | File too large or wrong format | Ensure image is PNG/JPG, <20MB |
| Download fails | URL expired | Re-run generation |
| `NSFW content detected` | Safety filter triggered | Rephrase prompt, avoid suggestive terms |

## Pricing Reference

| Tier | Per Second (no audio) | 5s | 10s | 15s |
|------|----------------------|-----|------|------|
| Standard | $0.084 | $0.42 | $0.84 | $1.26 |
| Pro | $0.112 | $0.56 | $1.12 | $1.68 |

Audio adds ~50% to cost. Not enabled by default.

## Rules

1. **Always check FAL_KEY** before calling API — fail fast with clear instructions
2. **Use async queue** (`submit` + `iter_events`) — never `subscribe` for video (too slow, may timeout)
3. **Download immediately** — fal.ai URLs are temporary (expire in ~1 hour)
4. **Report generation time** — user needs to know how long it took for budget planning
5. **Default to standard tier** — pro only when explicitly requested
6. **No audio by default** — audio doubles cost, most use cases don't need it
7. **Report cost estimate** in every output
8. **Filename includes tier + duration** — helps user identify outputs
9. **Never log FAL_KEY** — don't print or include in error messages
10. **If generation fails**: retry ONCE, then report error — don't loop
