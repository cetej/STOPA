---
name: nano
description: Generate images via fal.ai Nano Banana Pro/2 API. Use when user wants to create images, product shots, 3D renders, or visual assets. Trigger on 'generate image', 'create visual', 'nano banana', 'nano', 'vygeneruj obrázek'. Use --for-video to optimize output as input for video animation (/klip). Do NOT use for infographics with precise element positioning (use /visual-data-architect). Do NOT use for editing existing images in bulk.
argument-hint: <prompt> [--model pro|2] [--aspect 16:9|1:1|9:16|4:3|3:4] [--resolution 1K|2K|4K] [--count 1-4] [--for-video] [--output path]
user-invocable: true
allowed-tools:
  - Bash
  - Read
  - Write
  - Glob
model: sonnet
maxTurns: 8
---

# Nano Banana — Image Generation via fal.ai

Generate high-quality images using Nano Banana Pro or Nano Banana 2 through fal.ai API.

## Prerequisites

- `fal-client` Python package installed (`pip install fal-client`)
- `FAL_KEY` environment variable set (check `~/.claude/settings.json` env section)

## Step 1: Parse Arguments

Extract from user input:
- **prompt**: The image description (required)
- **--model**: `pro` (default, reasoning-guided, better quality) or `2` (faster, latest gen)
- **--aspect**: Aspect ratio (default `1:1`). Options: `1:1`, `16:9`, `9:16`, `4:3`, `3:4`, `21:9`, `3:2`, `2:3`, `5:4`, `4:5`
- **--resolution**: `1K` (default), `2K`, `4K`
- **--count**: Number of images 1-4 (default `1`)
- **--for-video**: Optimize prompt for use as video animation input
- **--output**: Output directory (default: `output/images/` in current project)

## Step 2: Check FAL_KEY

```bash
python -c "import os; key = os.environ.get('FAL_KEY', ''); print('OK' if key else 'MISSING')"
```

Note: On this Windows system, use `python` not `python3` — fal-client is installed under `C:\Python313\python`.

If MISSING: tell user to add FAL_KEY to `~/.claude/settings.json` under `"env"` and restart Claude Code.

## Step 3: Optimize Prompt

If `--for-video` flag is set, append to the user's prompt:
- ", white background, centered subject, no text, no labels, clean edges, studio lighting, isolated object, suitable for video animation"

This ensures the generated image works well as input for Kling 3.0 image-to-video.

## Step 4: Generate Image

Select endpoint based on `--model`:
- `pro` → `fal-ai/nano-banana-pro`
- `2` → `fal-ai/nano-banana-2`

Run via Python:

```bash
python -c "
import fal_client
import urllib.request
import os
import json
import sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

result = fal_client.subscribe(
    'ENDPOINT_ID',
    arguments={
        'prompt': '''PROMPT_TEXT''',
        'aspect_ratio': 'ASPECT',
        'resolution': 'RESOLUTION',
        'num_images': COUNT,
        'output_format': 'png',
    }
)

# Print result for parsing
print(json.dumps({
    'images': [{'url': img['url'], 'width': img.get('width'), 'height': img.get('height')} for img in result['images']]
}))
"
```

Replace ENDPOINT_ID, PROMPT_TEXT, ASPECT, RESOLUTION, COUNT with actual values.

## Step 5: Download Images

For each image URL in the result:

```bash
python -c "
import urllib.request
import os
import sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

url = 'IMAGE_URL'
output_dir = 'OUTPUT_DIR'
os.makedirs(output_dir, exist_ok=True)

filename = 'FILENAME.png'
path = os.path.join(output_dir, filename)
urllib.request.urlretrieve(url, path)
print(f'Saved: {path}')
print(f'Size: {os.path.getsize(path)} bytes')
"
```

**Naming convention**: `nano_{model}_{timestamp}_{index}.png`
- Example: `nano_pro_20260322_143052_1.png`

## Step 6: Report

Output a summary:

```
Nano Banana Pro — Generation Complete

Model:      nano-banana-pro
Prompt:     [first 80 chars]...
Aspect:     16:9
Resolution: 2K
Images:     2

Files:
  1. output/images/nano_pro_20260322_143052_1.png (2.1 MB)
  2. output/images/nano_pro_20260322_143052_2.png (1.8 MB)

Cost estimate: ~$0.30 (2 × $0.15 at 1K) or ~$0.60 (2 × $0.30 at 4K)
```

## Error Handling

| Error | Cause | Fix |
|-------|-------|-----|
| `FAL_KEY not set` | Missing env var | Add to `~/.claude/settings.json` env, restart CC |
| `fal_client not found` | Package not installed | `pip install fal-client` |
| `401 Unauthorized` | Invalid or expired key | Check FAL_KEY, regenerate at fal.ai dashboard |
| `429 Rate Limited` | Too many requests | Wait 30s, retry |
| `500 Server Error` | fal.ai backend issue | Wait 1 min, retry once |
| Download fails | URL expired | Re-run generation (URLs are temporary) |

## Pricing Reference

| Resolution | Nano Banana Pro | Nano Banana 2 |
|------------|----------------|---------------|
| 1K | ~$0.15/image | ~$0.10/image |
| 2K | ~$0.20/image | ~$0.15/image |
| 4K | ~$0.30/image | ~$0.20/image |

## Rules

1. **Always check FAL_KEY** before calling API — fail fast with clear instructions
2. **Download immediately** — fal.ai URLs are temporary (expire in ~1 hour)
3. **Create output directory** if it doesn't exist
4. **Report cost estimate** in every output — user tracks budget
5. **--for-video prompt suffix** must NOT override user's creative intent — append, don't replace
6. **Filename includes timestamp** — prevents overwrites on repeated runs
7. **PNG format by default** — lossless, works best as Kling input
8. **Never log FAL_KEY** — don't print or include in error messages
