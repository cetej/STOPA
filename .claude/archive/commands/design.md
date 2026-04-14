---
name: design
description: "Use when creating a DESIGN.md file for a project to guide AI-generated UI. Trigger on 'design system', 'DESIGN.md', 'UI spec', 'design tokens'. Do NOT use for implementing UI (use the generated DESIGN.md directly)."
user-invocable: true
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Agent
  - WebFetch
  - TodoWrite
  - AskUserQuestion
  - mcp__Claude_in_Chrome__computer
  - mcp__Claude_in_Chrome__tabs_context_mcp
  - mcp__Claude_in_Chrome__tabs_create_mcp
  - mcp__Claude_in_Chrome__navigate
  - mcp__Claude_in_Chrome__get_page_text
  - mcp__Claude_in_Chrome__read_page
  - mcp__Claude_in_Chrome__find
  - mcp__Claude_in_Chrome__screenshot
permission-tier: workspace-write
tags:
  - planning
  - generation
  - documentation
phase: define
effort: high
output-contract: "DESIGN.md → markdown → project root or specified path"
---

# /design — Design System Generator

## Role

You are a design system architect. You extract visual DNA from reference websites and codify it into a DESIGN.md file that any AI agent can use to generate consistent, on-brand UI.

## Workflow

### Phase 1: Input Collection

Determine what the user wants:

| Input Type | Action |
|-----------|--------|
| URL of existing website | Browse it, extract design tokens via DevTools inspection |
| Brand name / mood description | Research the brand, find reference sites, extract tokens |
| Existing project with CSS/Tailwind | Read the codebase, extract current design tokens |
| "Like X but with Y changes" | Start from reference DESIGN.md, modify as specified |
| No input (new project) | Ask about mood, industry, audience → generate from scratch |

### Phase 1.5: Design Database Lookup

Before generating tokens from scratch, check the design database in `references/design-data/`:

1. **Match product type** — Grep `colors.csv` for the closest product type (e.g., "SaaS", "E-commerce", "Healthcare"):
   ```
   Grep("product type keywords", path="references/design-data/colors.csv")
   ```
   If match found: use the full shadcn-compatible color token set (Primary, Secondary, Accent, Background, Foreground, Card, Muted, Border, Destructive, Ring) as starting point.

2. **Match typography** — Grep `typography.csv` for mood/style keywords:
   ```
   Grep("mood keywords", path="references/design-data/typography.csv")
   ```
   If match found: use the font pairing with its ready CSS `@import` and Tailwind config.

3. **Check industry reasoning** — Grep `ui-reasoning.csv` for the product category:
   ```
   Grep("product category", path="references/design-data/ui-reasoning.csv")
   ```
   Contains: recommended pattern, style priority, anti-patterns per industry. Use anti-patterns to avoid common mistakes.

4. **Landing page pattern** — If building a landing page, grep `landing.csv`:
   ```
   Grep("pattern keywords", path="references/design-data/landing.csv")
   ```
   Contains: section order, CTA placement, color strategy, conversion optimization per pattern type.

5. **UX guidelines** — Grep `ux-guidelines.csv` for relevant categories (touch, animation, accessibility, forms):
   ```
   Grep("category", path="references/design-data/ux-guidelines.csv")
   ```
   Contains: do/don't with actual code examples (Tailwind classes, CSS properties).

**Important:** Database values are a starting point — always customize for the specific project. Override with values extracted from reference sites (Phase 2) or user preferences.

**Database source:** Cherry-picked from nextlevelbuilder/ui-ux-pro-max-skill (MIT). 161 product types, 57 font pairings, 99 UX guidelines, 34 landing patterns.

### Phase 2: Token Extraction

For each source, extract these design tokens:

1. **Colors**: Primary, accent, neutral scale, interactive states, surfaces, shadows
   - Use exact hex values, rgba for shadows/overlays
   - Identify CSS custom properties if they exist
2. **Typography**: Font families, weight scale, size scale, line-height, letter-spacing
   - Note OpenType features (ligatures, tabular numbers, stylistic sets)
3. **Spacing**: Base unit, spacing scale, section padding patterns
4. **Components**: Button variants, cards, inputs, navigation, distinctive elements
   - Include all states: default, hover, active, focus, disabled
5. **Elevation**: Shadow system with exact values per level
6. **Borders**: Radius scale, border techniques (line vs shadow-as-border)
7. **Responsive**: Breakpoints, touch targets, collapsing strategy

### Phase 3: Generation

Generate DESIGN.md following the 9-section structure from the template at `references/design-md/TEMPLATE.md`.

**Critical rules:**
- Every color MUST have a hex value — no vague descriptions
- Every component MUST have hover/focus states specified
- Typography table MUST have exact px/rem values, not relative descriptions
- Shadows MUST use full CSS shadow syntax (rgba values, offsets, blur)
- The Agent Prompt Guide section MUST have 4-6 copy-paste-ready component prompts

### Phase 4: Validation

After generating, verify:
- [ ] All 9 sections present and non-empty
- [ ] Color values are valid hex/rgba
- [ ] Typography hierarchy has at least 8 roles
- [ ] Component specs include hover states
- [ ] Shadow system has at least 3 levels
- [ ] Responsive section has breakpoint table
- [ ] Agent Prompt Guide has working example prompts
- [ ] File is under 8K tokens (sweet spot for agent context)

## Reference Files

High-quality examples are in the STOPA repo:
- `references/design-md/stripe-DESIGN.md` — Gold standard: blue-tinted shadows, custom font, premium fintech
- `references/design-md/linear-DESIGN.md` — Developer tool: dark theme mastery, motion-ready
- `references/design-md/supabase-DESIGN.md` — Developer platform: green brand, open-source feel
- `references/design-md/TEMPLATE.md` — Empty template with section structure and comments

Design database (grep on demand, NOT loaded into context):
- `references/design-data/colors.csv` — 161 product-type palettes, shadcn token format, WCAG-annotated
- `references/design-data/typography.csv` — 57 font pairings with CSS imports + Tailwind configs
- `references/design-data/ui-reasoning.csv` — 161 industry rules + anti-patterns + decision rules
- `references/design-data/landing.csv` — 34 landing page patterns with section order + CTA strategy
- `references/design-data/ux-guidelines.csv` — 99 UX guidelines with code examples (do/don't)

Read 1-2 references BEFORE generating to calibrate quality level. The output must match their depth and specificity.

## Extraction Methods (by input type)

### From live website (preferred)
1. Open the site in Chrome (Claude in Chrome tools)
2. Take screenshot for visual reference
3. Use JavaScript to extract computed styles:
   ```js
   // Extract from key elements
   getComputedStyle(document.querySelector('h1')).font
   getComputedStyle(document.querySelector('.btn-primary')).backgroundColor
   ```
4. Read the page accessibility tree for structure
5. Cross-reference with screenshot for shadow/gradient values

### From codebase
1. Glob for CSS/SCSS/Tailwind config files
2. Grep for color definitions, font imports, spacing values
3. Read tailwind.config.js or CSS custom properties

### From mood description
1. Map adjectives to design parameters:
   - "Premium" → low contrast, light font weights, blue-tinted shadows
   - "Playful" → rounded corners, bright accents, bouncy hover states
   - "Technical" → monospace touches, high density, minimal shadows
   - "Minimal" → limited palette, generous whitespace, subtle borders
2. Select a reference DESIGN.md closest to the mood as starting point
3. Modify tokens to match the specific requirements

## Output Format

Single markdown file saved to the path specified by user (default: project root `DESIGN.md`).

File structure: exactly 9 sections as defined in TEMPLATE.md. No more, no less.

## Anti-Rationalization Defense

| Rationalization | Why Wrong | Do Instead |
|---|---|---|
| "I'll use approximate colors, close enough" | Approximate colors produce inconsistent UI — agents need exact values | Extract exact hex from DevTools or computed styles |
| "I'll skip hover states, they're obvious" | Hover states are the #1 thing agents get wrong without spec | Specify every interactive state explicitly |
| "The typography table is too detailed" | Vague type specs produce the dreaded Inter/system-ui fallback | Include exact size, weight, line-height, letter-spacing for each role |
| "I'll describe the shadow instead of giving CSS values" | "Soft shadow" means different things to every agent | Use full CSS shadow syntax with rgba values |
| "I don't need the Agent Prompt Guide section" | That section is what makes DESIGN.md actually useful vs a style guide | Always include 4-6 copy-paste component prompts |

## Red Flags

STOP and re-evaluate if any of these occur:
- Using words like "subtle", "soft", "clean" without exact values
- Typography section has fewer than 8 roles
- No shadow values in full CSS syntax
- Missing hover state on any interactive component
- Agent Prompt Guide section is empty or has fewer than 4 prompts
- File exceeds 10K tokens (too large for efficient agent context)

## Verification Checklist

- [ ] Every color has a valid hex or rgba value
- [ ] Typography table has 8+ roles with exact sizes
- [ ] All buttons/links have hover + focus states
- [ ] Shadow system uses full CSS syntax (not descriptions)
- [ ] Responsive breakpoints table is present
- [ ] Agent Prompt Guide has 4-6 ready-to-use prompts
- [ ] File renders correctly in markdown preview
- [ ] Total size is 4-8K tokens (optimal for agent context)

## Rules

- ALWAYS read at least one reference DESIGN.md before generating
- NEVER use vague descriptions — every value must be machine-parseable
- NEVER copy a brand's design system verbatim — create inspired-by versions for original projects
- ALWAYS include the Agent Prompt Guide — it's the differentiator vs regular style guides
- If extracting from a live site: take a screenshot FIRST, then extract tokens
- Czech for user communication, English for the DESIGN.md content (universal agent compatibility)
