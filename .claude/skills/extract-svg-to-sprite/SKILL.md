---
name: extract-svg-to-sprite
description: "Use when extracting inline SVG icons from an HTML file into a single sprite sheet with <symbol> definitions. Do NOT use for generating new SVG artwork or converting between raster formats."
argument-hint: "<input HTML path> <output sprite path>"
tags: [media]
phase: build
version: "1.0.0"
maturity: validated
user-invocable: true
allowed-tools: Read, Write, Edit, Glob
disallowed-tools: Agent
max-depth: 1
model: sonnet
effort: low
maxTurns: 8
uses: 3
successful_uses: 2
harmful_uses: 0
---

# Extract SVG To Sprite

Gathers every inline `<svg>` element from an HTML file, wraps each one as a `<symbol id="...">` inside a single sprite SVG, and replaces the originals with `<svg><use href="#id"/></svg>` references.

## Preconditions

- Input HTML file exists and contains one or more inline `<svg>...</svg>` blocks.
- Each inline SVG either has a unique `id` attribute or can be assigned one from a nearby context (class, surrounding element id).

## Workflow

1. **Read input** — load the HTML file from the first argument path.
2. **Execute core operation** — parse out every inline `<svg>` element, assign or reuse an `id`, strip width/height attributes into a `viewBox`-only `<symbol>`, collect symbols into a single sprite `<svg xmlns="http://www.w3.org/2000/svg" style="display:none">...</svg>`. Write sprite to the second argument path. Replace each original inline SVG in the HTML with `<svg><use href="<sprite-path>#<id>"/></svg>`.
3. **Verify output** — confirm the sprite file is well-formed XML, every original SVG has a matching `<symbol>`, and the rewritten HTML references only ids that exist in the sprite.

## Anti-Rationalization Defense

| Rationalization | Why Wrong | Do Instead |
|---|---|---|
| "I already know this pattern, skip verification" | Draft skill — unvalidated assumptions likely wrong | Run the verification step |
| "Close enough, the output looks right" | Draft skills need pass/fail evidence, not vibes | Produce the artifact specified in Workflow step 3 |
| "This is a one-shot, skip structure" | /tool-synth drafts exist to be reused → structured output enables promotion | Follow all three Workflow steps |

## Red Flags

STOP and escalate if any of these occur:
- Input HTML has zero inline `<svg>` blocks — precondition unmet
- Duplicate `id` collisions across inline SVGs cannot be disambiguated
- Sprite target path lies outside the project directory

## Verification Checklist

- [ ] Preconditions checked before execution
- [ ] Every inline SVG in input HTML has a corresponding `<symbol>` in sprite output
- [ ] Rewritten HTML `<use href>` references only resolve to ids present in the sprite

## Notes

Sandbox skill synthesized by /tool-synth on 2026-04-18. Expires 2026-04-25. Promotion to top-level `.claude/skills/` requires `uses >= 3` AND successful critic gate via /evolve.
