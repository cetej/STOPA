---
date: 2026-04-01
type: best_practice
severity: medium
component: general
tags: [cost-optimization, caching, browse, chrome-automation]
summary: Adding or removing images anywhere in a Claude API prompt invalidates the entire prompt cache. Browse/screenshot workflows consistently miss cache, paying full input price every turn.
source: external_research
confidence: 0.8
uses: 0
harmful_uses: 0
verify_check: "manual"
---

## Image Presence Breaks Prompt Cache

Anthropic docs confirm: adding or removing an image **anywhere** in the prompt
invalidates the cache prefix match. This applies to Claude Code too — same API underneath.

### Impact on STOPA workflows

| Workflow | Impact | Why |
|----------|--------|-----|
| `/browse` + Claude in Chrome | **HIGH** | Each screenshot is a different image block → cache miss every turn |
| Preview tools (screenshot verification) | **HIGH** | Same as browse |
| `/nano`, `/klip` | **NONE** | Return URLs as text, not inline image blocks |

### What to do

- **Cannot fix** — this is an API-level limitation
- **Be aware** — browse-heavy sessions consume more tokens than text-only sessions
- **Minimize screenshots** — use `read_page`/`get_page_text` where possible instead of `computer(action="screenshot")`; prefer accessibility snapshots over visual screenshots when verifying page state
- Cache write costs 1.25× base input; cache read costs 0.1× — a miss means paying 12.5× more than a hit

### Pricing math (Sonnet 4.6)

- Cache hit: $0.30/MTok
- Cache miss: $3.00/MTok (or $3.75 if write overhead counted)
- A 10-turn browse session with screenshots on every turn: zero cache benefit on message blocks
