---
name: Claude Code Auto Mode
type: concept
first_seen: 2026-04-07
last_updated: 2026-04-07
sources: [x-tip-analysis]
tags: [orchestration, security]
---
# Claude Code Auto Mode

> Bezpečný střed cesty mezi --dangerously-skip-permissions a constant prompting — classifier povoluje/blokuje akce bez expozice agent reasoning.

## Key Facts

- Classifier nevidí agent reasoning → nemůže craftnout argumenty pro safety bypass
- "Safer middle ground" — méně prompting než constant approval, bezpečnější než dangerously-skip
- Blog post: anthropic.com/engineering/claude-code-auto-mode
- Řeší approval fatigue (viz memory: feedback_approval_fatigue.md) (ref: sources/x-tip-analysis.md)
- Status: TODO přečíst celý blog post, evaluovat pro STOPA development

## Relevance to STOPA

Kandidát pro nahrazení současného permissions setup v settings.json. Srovnat s naším permission hook v3.0.

## Mentioned In

- [X-TIP Analýza: Claude Code tipy z X.com](../sources/x-tip-analysis.md)
