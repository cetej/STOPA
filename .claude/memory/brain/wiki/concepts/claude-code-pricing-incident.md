---
title: Claude Code Pricing Incident — Max Plan Test Rollback
category: concepts
tags: [anthropic, product-strategy, pricing, claude-code, trust]
sources: [simonwillison.net/2026/Apr/22/claude-code-confusion/]
updated: 2026-04-23
---

# Claude Code Pricing Incident — Max Plan Test Rollback

**Source**: Simon Willison, simonwillison.net, April 22, 2026  
**Organizations**: Anthropic, OpenAI  

## What Happened

Anthropic quietly updated pricing to restrict Claude Code to Max plans ($100–$200/month) instead of Pro ($20/month). The change was reversed within hours after public backlash.

| Tier | Price | Affected |
|------|-------|---------|
| Pro | $20/month | Was being removed from CC access |
| Max | $100–$200/month | New required tier during test |
| Cowork | Pro tier | Remained available (rebranded CC) |

Only ~2% of new prosumer signups were in the test group, but the **pricing page was publicly visible**, triggering a community reaction disproportionate to actual impact.

## Why It Matters

**Trust erosion pattern**: Opaque pricing changes without transparent communication damage community trust — even when the change affects few users. The visibility mismatch (public pricing page + limited rollout) is worse than either a full rollout or a fully hidden test.

**Competitive framing**: The incident coincided with OpenAI's Codex release, making the pricing narrative land in an adversarial context.

## Structural Lesson

| What Anthropic Did | Better Approach |
|-------------------|-----------------|
| Silent pricing page update | Explicit "testing new pricing" banner |
| Retroactive explanation | Proactive announcement before rollout |
| General rollout announcement | Feature flag with no public pricing page change |

## Person Reference: Simon Willison

105+ blog posts on Claude Code as of April 2026 — a high-signal community trust indicator. His ability to raise this publicly represents a distribution channel for user sentiment that Anthropic cannot ignore.

## STOPA Relevance

STOPA depends on Claude Code Pro/Max subscription. Any pricing tier changes directly affect operational costs and planned automation budgets. Monitor: Anthropic pricing pages for CC access tier changes.

## Related Concepts

→ [claude-opus-47.md](claude-opus-47.md)  
→ [agentic-engineering-patterns.md](agentic-engineering-patterns.md)  
→ [claude-code-design-space.md](claude-code-design-space.md)
