---
date: 2026-03-23
type: best_practice
severity: medium
component: general
tags: [fal-ai, python, windows, environment]
uses: 1
summary: "fal.ai on Windows: use fal-client not fal, handle async properly, set FAL_KEY env var, retry on timeouts."
source: auto_pattern
maturity: draft
confidence: 1.0
---

## Problém
fal.ai API integration on Windows has several gotchas.

## Root Cause
Platform-specific Python path issues and API behavior differences.

## Reseni
Use `python` (C:\Python313) not `python3` (WindowsApps stub). `fal_client.subscribe()` is blocking, OK for images. For video: use `submit()` + `iter_events()`. fal.ai result URLs expire ~1 hour — download immediately. FAL_KEY is in `~/.claude/settings.json` env section.

## Prevence
Pricing: Nano Banana Pro ~$0.15/image, Kling v3 standard ~$0.084/s, pro ~$0.112/s.
