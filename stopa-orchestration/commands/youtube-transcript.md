---
name: youtube-transcript
description: Use when extracting transcripts from YouTube videos for analysis. Trigger on 'youtube transcript', 'video transcript', YouTube URL. Do NOT use for non-YouTube content.
argument-hint: <YouTube URL(s)> [--lang cs,en] [--analyze] [--output path]
tags: [research, media]
phase: meta
user-invocable: true
allowed-tools: Bash, Read, Write, Glob
model: sonnet
effort: medium
maxTurns: 15
disallowedTools: ""
---

# YouTube Transcript — Video-to-Text Pipeline

Download, clean, and optionally analyze YouTube video transcripts.

## Prerequisites

- `yt-dlp` installed (`pip install yt-dlp`)
- If yt-dlp fails with "Sign in to confirm you're not a bot" → update first: `pip install -U yt-dlp`
- MCP youtube-transcript server is BROKEN (2026-03) — do NOT use it, always use yt-dlp

<!-- CACHE_BOUNDARY -->

## Process

### Step 1: Parse arguments

Extract from `$ARGUMENTS`:
- **URLs**: one or more YouTube URLs (support youtube.com/watch, youtu.be, playlist links)
- **--lang**: subtitle languages to try (default: `en,cs` — English first, Czech fallback)
- **--analyze**: if present, provide analysis + key takeaways after download
- **--output**: directory to save transcripts (default: `input/` in current project)

### Step 2: Check yt-dlp

```bash
yt-dlp --version
```

If not found: `pip install yt-dlp`
If version is older than 3 months: suggest `pip install -U yt-dlp` (YouTube changes anti-bot frequently)

### Step 3: Download subtitles

For each URL:

```bash
yt-dlp --write-auto-sub --sub-lang "LANG" --skip-download -o "OUTPUT_NAME" "URL" 2>&1
```

**Language strategy** (try in order):
1. Manual subtitles in requested language (`--write-sub`)
2. Auto-generated subtitles (`--write-auto-sub`)
3. If neither exists, report to user — video may not have subtitles

**If blocked** ("Sign in to confirm you're not a bot"):
1. First try: update yt-dlp (`pip install -U yt-dlp`) and retry
2. Second try: use cookies from browser (`--cookies-from-browser brave` or `chrome`)
3. If DPAPI error on Windows: inform user they may need to export cookies manually

**Naming**: Use video title or ID as filename base. For multiple videos, prefix with number.

### Step 4: Clean VTT to plain text

VTT files contain duplicate lines, timing tags, and metadata. Clean with Python:

```python
import re

def clean_vtt(path):
    with open(path, 'r', encoding='utf-8') as f:
        text = f.read()
    # Remove VTT header
    text = re.sub(r'WEBVTT.*?\n\n', '', text, flags=re.DOTALL)
    # Remove timestamps
    text = re.sub(r'\d{2}:\d{2}:\d{2}\.\d{3} --> \d{2}:\d{2}:\d{2}\.\d{3}.*\n', '', text)
    # Remove inline timing tags
    text = re.sub(r'<[^>]+>', '', text)
    # Deduplicate lines (VTT repeats each line)
    lines = []
    seen = set()
    for line in text.split('\n'):
        line = line.strip()
        if line and line not in seen:
            seen.add(line)
            lines.append(line)
    return ' '.join(lines)
```

Save cleaned text as `{name}_transcript.txt` alongside the VTT file.

### Step 5: Report

For each video, output:
- Title (from yt-dlp output or filename)
- Language detected
- Character count
- File path saved
- First ~200 chars preview

### Step 6: Analyze (if --analyze)

If `--analyze` flag was set:
1. Read the cleaned transcript
2. Provide:
   - **Téma**: one-line summary
   - **Klíčové body**: 5-10 bullet points
   - **Možnosti využití**: how this relates to user's projects (check memory/checkpoint for context)
   - **Citace**: notable quotes (max 3, each under 15 words per copyright rules)

## Error Handling

| Error | Cause | Fix |
|-------|-------|-----|
| "Video unavailable" | yt-dlp outdated or geo-blocked | Update yt-dlp, try with VPN note |
| "Sign in to confirm" | YouTube anti-bot | Update yt-dlp → cookies → manual export |
| "DPAPI decrypt failed" | Windows cookie encryption | Can't auto-fix; suggest manual cookie export |
| 429 Too Many Requests | Rate limited | Wait 30s, retry one language at a time |
| No subtitles found | Video has no captions | Report to user, suggest alternative (manual transcription) |
| "nsig extraction failed" | Outdated yt-dlp JS parser | `pip install -U yt-dlp` |

## Output Structure

```
input/
├── video1.en.vtt              # Raw VTT (keep for reference)
├── video1_transcript.txt      # Cleaned plain text
├── video2.cs.vtt
└── video2_transcript.txt
```

## After Completion

1. If yt-dlp workarounds were used (update, cookies, etc.): write the working solution to `.claude/memory/learnings.md` under Patterns
2. If download failed permanently: write the failure pattern to `.claude/memory/learnings.md` under Anti-patterns
3. If `--analyze` was used: note key takeaways in `.claude/memory/state.md` under active task (if one exists)

## Rules

1. **Always use yt-dlp** — never use the MCP youtube-transcript server (broken since 2026-03)
2. **Keep both VTT and cleaned TXT** — VTT has timestamps if needed later
3. **Default output to `input/`** in current project directory
4. **Respect copyright** — in analysis, never quote more than 15 words verbatim
5. **Report file sizes** — user should know how much text they're getting
6. **Clean up temp files** — if downloading to /tmp, copy results to project dir
7. **Multiple videos = parallel downloads** — use separate Bash calls
