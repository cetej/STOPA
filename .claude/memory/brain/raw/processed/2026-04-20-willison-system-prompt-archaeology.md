---
source: https://simonwillison.net/2026/Apr/18/extract-system-prompts/
fetched: 2026-04-20
type: blog-post
author: Simon Willison
title: "Research: Claude system prompts as a git timeline"
---

# Raw: Willison — Claude System Prompts as Git Timeline

## Summary
Simon Willison's project converting Anthropic's published Claude system prompt documentation into a git-based exploration tool. Disaggregates monolithic markdown into individual files per model/revision with timestamped commits.

## Key Points
- Source: Anthropic publishes Claude system prompts as markdown docs
- Method: transformed into separate files per model + model family with fake git commit dates
- Enables: `git log`, `diff`, `blame` for tracing prompt evolution and attribution
- Applied to: analyze Opus 4.6 → 4.7 differences

## Repository
https://github.com/simonw/research/tree/main/extract-system-prompts

## Entities
- Simon Willison (author)
- Claude Opus 4.6, 4.7 (subjects of analysis)
- Anthropic (system prompt publisher)
