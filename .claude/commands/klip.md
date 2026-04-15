---
name: klip
description: "Use when generating short video clips via Kling on fal.ai — product demos, social media clips, animated explainers. Supports text-to-video and image-to-video modes. Trigger on 'generate video', 'klip', 'video clip', 'udělej video', 'animace'. Requires FAL_KEY env var. Do NOT use for static images (/nano), video editing/montage (use external tools), or YouTube transcript extraction (/youtube-transcript)."
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
| ③ | No filler/degrading words | ❌ error | Hard-block: masterpiece, ultra-HD, 8K, best quality, hyper-realistic, extremely detailed, super resolution, ultra-clear, epic, amazing, beautiful, stunning. Soft-block (⚠️ warn + auto-fix): "fast" (unqualified), "cinematic" (alone without anchor), "lots of movement", "glow"/"glimmer"/"glints" (→ "steady intensity"/"diffuse"). Use physical material/light words instead |
| ④ | Descriptive, not narrative | ⚠️ warning | Emotions → physical expressions. "She feels sad" → "tears streaming down her cheeks". Only describe what the renderer can SEE |
| ⑤ | No style conflicts | ❌ error | See conflict matrix below |
| ⑥ | I2V: changes only | ⚠️ warning | If `--image` provided: describe only motion/changes from the input image, not static content already visible. Prepend `preserve composition and colors` |
| ⑦ | Has lighting descriptor | ⚠️ warning | Lighting has the BIGGEST impact on quality. If no lighting term present, auto-add at least one (golden hour as universal default). See Lighting Keywords in Prompt Architecture |
| ⑧ | 5-layer structure | ⚠️ warning | Prompt should follow Subject > Action > Camera > Style > Constraints order. Reorder if needed. Missing layers = lower quality |

### Style Conflict Matrix (mutually exclusive — ❌ error if combined)

- Photorealistic + cartoon/anime style
- Film grain/vintage + ultra-sharp/crystal-clear
- Slow motion + speed ramp in same segment
- Wide-angle fisheye + shallow depth-of-field bokeh (physically impossible)
- Handheld shaky cam + perfect geometric symmetry

### Enhancement (auto-apply before API call)

- **Restructure to 5-layer stack**: Subject > Action > Camera > Style > Constraints (see Prompt Architecture below)
- Convert emotional/narrative descriptions → observable physical actions
- Add motion intensity modifier if action verbs are vague (see Motion Intensity Scale below)
- Prefer semantic rhythm words (gentle, gradual, smooth) over technical params (24fps, f/2.8) — Kling parses semantics, not numbers
- **Lighting injection**: if no lighting descriptor present, add "golden hour" or contextually appropriate lighting keyword
- **Constraint suffix**: always append `sharp clarity, natural colors, stable picture, no blur, no ghosting, no flickering`
- **Character constraints**: if humans in scene, also append `avoid jitter, avoid bent limbs, maintain face consistency`
- **Degrading keyword replacement**: "fast" → specify which element; "cinematic" alone → add film ref + lighting; "glow"/"glimmer" → "steady intensity"/"diffuse"

If any ❌ error after enhancement: inform user of the conflict and suggest fix. Do NOT proceed to API.

## Step 2d: Provider Selection (scored)

Before choosing an endpoint, run the media provider selector for an auditable decision:

```bash
python C:/Users/stock/Documents/000_NGM/STOPA/scripts/media-provider-selector.py -c video -t "USER_TASK_DESCRIPTION" --json
```

Replace `USER_TASK_DESCRIPTION` with key terms from the user's prompt (e.g., "cinematic nature documentary trailer").

The selector ranks all available video providers across 7 dimensions (task_fit, quality, control, reliability, cost, latency, continuity) and returns the best match with a decision log entry.

**Use the selected provider's endpoint** unless:
- User explicitly requested a specific tier (`--tier pro/standard`) → override to Kling at that tier
- Selected provider doesn't support the required mode (e.g., Seedance has no text-to-video)

If the selector is unavailable (script missing), fall back to the hardcoded Kling endpoint below.

## Step 3: Determine Mode

| `--image` provided? | Mode | Endpoint |
|---------------------|------|----------|
| No | Text-to-Video | `{selected_endpoint}/text-to-video` (fallback: `fal-ai/kling-video/v3/{tier}/text-to-video`) |
| Yes (URL) | Image-to-Video | `{selected_endpoint}/image-to-video` (fallback: `fal-ai/kling-video/v3/{tier}/image-to-video`) |
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

## Prompt Architecture — 5-Layer Stack

Structure every prompt in this order. The ordering carries weight — subject first pins the model's center of gravity, action second provides kinetic anchor, camera third locks framing, style adds flavor without hijacking motion, constraints close gaps.

```
[SUBJECT]: who/what — specific identity markers (age, hair, clothing, posture, accessories)
[ACTION]:  what happens — present tense, ONE primary movement, separate subject motion from camera motion
[CAMERA]:  ONE primary camera movement + rhythm modifier (slow/smooth/dynamic)
[STYLE]:   lighting FIRST (biggest quality impact), then color grade, then film reference
[CONSTRAINTS]: quality guardrails — always append the constraint suffix
```

### Layer 1: Subject — Specificity is load-bearing

Every identity marker you provide is one the model doesn't hallucinate. One subject per generation is safest, two work if spatially separated.

| Level | Example |
|-------|---------|
| Bad | "a woman" |
| Better | "a young woman with brown hair" |
| Best | "a woman in her late 20s, tight dark curls at ear length, small silver hoop in left ear, fitted black turtleneck, neutral expression" |

### Layer 2: Action — Directions, not states

Separate subject movement from camera movement ALWAYS. "Spinning camera around a dancing person" = ambiguous. "The dancer spins slowly, camera holds fixed framing" = two clear directives.

| Don't write | Write instead |
|-------------|---------------|
| "She feels lonely" | "She sits motionless, staring at an empty chair across the table" |
| "An exciting chase" | "Man sprinting through rain-soaked alley, coat flapping violently behind him" |
| "Peaceful morning" | "Morning light through thin curtains, dust particles drifting slowly through beam" |
| "He is angry" | "Jaw clenched, fists tightening, veins visible on forearms" |

### Layer 3: Camera — Keyword Library

ONE primary camera movement per generation. Describe rhythm (slow, smooth, gentle) rather than technical specs (f-stop, ISO, mm).

**Static shots:**

| Keyword | Effect |
|---------|--------|
| fixed / locked-off | Zero camera movement |
| static wide | Wide unmoving establishing shot |
| locked tripod | Eliminates ambient jitter |

**Movement keywords:**

| Keyword | Effect | Best for |
|---------|--------|----------|
| push-in / dolly in | Camera moves toward subject | Tension, emphasis, emotional close-ups |
| pull-out / dolly out | Camera moves away | Environmental reveals, context |
| pan left/right | Horizontal rotation in place | Scanning, following action |
| tracking shot / follow | Moves alongside subject | Action sequences |
| orbit / arc / 360 orbit | Circles subject | Product showcases, portraits, hero moments |
| aerial / drone shot | High altitude | Landscapes, establishing geography |
| handheld | Natural shake | Documentary feel, UGC authenticity |
| crane up/down | Vertical ascent/descent | Dramatic height reveals |
| steadicam walk | Smooth forward following | Polished cinematic walk-and-talk |
| whip pan | Rapid horizontal sweep | Urgency, scene transitions |
| rack focus | Shift focus foreground↔background | Redirecting attention |

**Speed modifiers:**

| Modifier | When to use |
|----------|-------------|
| imperceptible / barely | Extremely slow, almost unnoticeable |
| slow / gentle / gradual | Safest starting point (DEFAULT) |
| smooth / controlled | Natural rhythm |
| dynamic / swift | High impact — use with EXTREME caution |

For compound camera movement, sequence it: "start: slow dolly-in, then: gentle pan right for the final 2 seconds" — two temporal phases, not two competing instructions.

### Layer 4: Style — Lighting First

**Lighting has the single biggest impact on video quality** among all prompt elements — bigger than style adjectives, quality modifiers, or resolution requests. If you only add one element to a weak prompt, make it lighting.

**Lighting keywords that consistently produce:**

| Keyword | Effect |
|---------|--------|
| golden hour | Single highest quality-per-word improvement |
| rim light / dramatic rim light | Cinematic edge separation against dark bg |
| soft key from 45 degrees | Flattering talking-head lighting |
| overcast daylight / even overcast | Eliminates flicker in bright scenes |
| backlit silhouette at sunset | Dramatic mood |
| motivated lighting from practical source | Realism with visible light source |
| volumetric fog | Atmospheric depth, pairs with backlit |
| chiaroscuro | High-contrast Godfather-style |

**Color grading:**

| Keyword | Effect |
|---------|--------|
| teal and orange | Classic Hollywood |
| bleach bypass | Desaturated, gritty, high-contrast |
| warm tone / amber-tinted | Nostalgic |
| crushed blacks | Deep cinematic shadow loss |
| pastel | Soft anime or fashion aesthetic |

**Film reference anchors:**

| Reference | Result |
|-----------|--------|
| cinematic film tone, 35mm | Most reliable all-purpose anchor |
| 16mm film, handheld camera | Raw indie aesthetic |
| anamorphic lens flare | Widescreen cinematic |
| national geographic quality | Nature documentary |
| documentary-style handheld framing | Observational realism |

### Layer 5: Constraints — Quality Guardrails

**Standard constraint suffix** — append to EVERY generation:

```
sharp clarity, natural colors, stable picture, no blur, no ghosting, no flickering
```

**Character-specific constraints** — add when humans are in the shot:

```
avoid jitter, avoid bent limbs, avoid identity drift, maintain face consistency
```

### Degrading Keywords — NEVER Use

These look helpful and actively degrade output:

| Keyword | Problem | Fix |
|---------|---------|-----|
| "fast" (unqualified) | Accelerates everything simultaneously | Name which SINGLE element moves fast |
| "cinematic" (alone) | No visual meaning without anchors | Pair with texture + lighting + film ref |
| "epic" | No visual meaning to diffusion model | Describe the specific scale/grandeur |
| "amazing" / "beautiful" / "stunning" | Feelings, not instructions | Describe physical qualities |
| "lots of movement" | Triggers jitter across entire frame | Name ONE specific movement |
| "glow" / "glimmer" / "glints" | Specular flicker artifacts | Use "steady intensity" or "diffuse" |
| masterpiece / ultra-HD / 8K | Filler, no visual effect | Use physical material/light words |
| hyper-realistic / extremely detailed | Filler, concept drift | Describe specific textures |

**Principle**: if a word describes how the viewer should feel rather than what the camera should see, the model guesses what visual would produce that feeling — and guesses wrong.

### Motion Intensity Scale

| Intensity | Modifiers | Example |
|-----------|-----------|---------|
| Explosive | violent, sudden, snapping | "hair whipping violently in wind" |
| Dramatic | sweeping, surging, crashing | "waves crashing dramatically against cliff face" |
| Steady | smooth, flowing, continuous | "smooth tracking shot across landscape" |
| Gentle | gradual, drifting, easing | "petals gradually falling from branch" |
| Minimal | barely, subtly, faintly | "candle flame subtly flickering" |

If movement is too subtle, prepend "dynamic motion" or "vibrant energy" — acts as global intensity modifier without introducing new movement types.

### Effect Patterns

| Effect | Prompt Pattern |
|--------|---------------|
| Rotating object | "smoothly rotating [object], center of mass stays fixed, rotating on its axis" |
| Exploding view | "exploding view diagram of [object], components separate in all directions, white background" |
| Product hero | "[SUBJECT] on dark surface, [CAMERA] slow orbit, [STYLE] rim light catching edges, volumetric lighting, [CONSTRAINTS]" |
| Talking head UGC | "[SUBJECT] specific person details, [ACTION] holds product to camera, [CAMERA] handheld selfie angle, [STYLE] natural window lighting no ring light, [CONSTRAINTS]" |
| Cinematic scene | "[SUBJECT] detailed character, [ACTION] specific physical motion, [CAMERA] slow push-in, [STYLE] 35mm golden hour shallow DOF, [CONSTRAINTS]" |
| Nature documentary | "[SUBJECT] animal/landscape, [CAMERA] aerial drone or tracking, [STYLE] national geographic quality overcast daylight, [CONSTRAINTS]" |

### Iteration Rule

Generate 2-3 baseline options, then change ONE variable per iteration (camera, lighting, speed modifier — one thing). Score each for continuity and adherence, keep best, change one more variable. Never rewrite entire prompt after a failed generation — isolate what helped and what hurt.

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

## Step 8: Record Outcome

After generation (success or failure), record the outcome for UCB1 learning:

```bash
python C:/Users/stock/Documents/000_NGM/STOPA/scripts/media-provider-selector.py --record-outcome --provider "PROVIDER_NAME" --capability video --outcome success --task "TASK_DESCRIPTION"
```

Use `--outcome success` if video generated and looks correct, `--outcome failure` if generation failed or quality was poor. This feeds the UCB1 bandit that improves future provider selection.

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
11. **Run provider selector** before choosing endpoint — auditable decision trail
12. **Record outcome** after generation — enables UCB1 learning across sessions
