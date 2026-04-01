---
name: fetch
description: Use when extracting clean readable text from one or more URLs for LLM analysis. Trigger on 'fetch URL', 'read page', 'načti stránku', 'obsah URL'. Do NOT use for Chrome automation (/browse) or YouTube (/youtube-transcript).
argument-hint: "<url> [url2...] [--analyze] [--raw] [--save path]"
tags: [research, osint, web]
user-invocable: true
allowed-tools: WebFetch, WebSearch, Read, Write, Bash
model: sonnet
effort: low
maxTurns: 10
---

# Fetch — Clean URL Reader (Jina Reader)

Extract clean, LLM-optimized text from any public URL using Jina Reader.
No API key required. No browser needed.

## How Jina Reader works

Prepend `https://r.jina.ai/` to any URL to get clean markdown:

```
https://r.jina.ai/https://example.com/article
```

Returns clean prose — no nav, no ads, no boilerplate. Ideal for LLM context windows.

<!-- CACHE_BOUNDARY -->

## Parse Arguments

From `$ARGUMENTS`:
- **URLs**: one or more public URLs (https://...)
- **--analyze**: after fetching, provide analysis + key takeaways
- **--raw**: skip Jina, use raw WebFetch (for JSON APIs, sitemaps, robots.txt)
- **--save <path>**: save extracted text to file

## Process

### Step 1: For each URL

**Default (Jina Reader):**
```
Fetch: https://r.jina.ai/{URL}
```

**Fallback** (if Jina returns error, empty, or HTTP 4xx):
```
Fetch: {URL} directly via WebFetch
```

**--raw flag**: skip Jina, fetch directly.

### Step 2: Validate content

Check the response:
- If `< 200 chars` → likely blocked or empty. Try raw WebFetch.
- If contains "Access denied" or "Cloudflare" → note limitation, try raw.
- If valid → proceed.

### Step 3: Report per URL

For each URL output:
```
## {title or URL}
Source: {url}
Method: jina | raw | failed
Length: {char count}

{content preview — first 500 chars}
```

### Step 4: Analyze (if --analyze)

Read full content and provide:
- **Shrnutí**: 2-3 věty o obsahu
- **Klíčové body**: max 5 bullet points
- **Relevance**: jak se to vztahuje k aktuálnímu projektu (zkontroluj context z conversation)

### Step 5: Save (if --save)

Write all fetched content to `{path}` in this format:
```markdown
# Fetched Content — {date}

## Source 1: {url}
{content}

## Source 2: {url}
{content}
```

## Decision Matrix — When to use which tool

| Situation | Tool |
|-----------|------|
| Public article, docs page | `/fetch` (Jina) |
| YouTube video | `/youtube-transcript` (yt-dlp) |
| Logged-in site (Gmail, dashboard) | `/browse` (Chrome) |
| Multiple research sources | `/deepresearch` |
| Need to interact with page | `/browse` |

## Limitations

- Jina Reader works on public pages only — no auth, no paywalls
- Some sites block Jina (Cloudflare, heavy JS SPAs) → fallback to raw WebFetch
- Raw WebFetch may include nav/boilerplate — note this in output
- For JavaScript-heavy pages where both fail → suggest `/browse`

## Rules

1. Always try Jina first — it's free, fast, and cleaner
2. If Jina fails, try raw WebFetch before giving up
3. If both fail, suggest `/browse` with explanation
4. Never fabricate content — if you can't read a page, say so
5. Multiple URLs = fetch in parallel (one WebFetch call per URL)
