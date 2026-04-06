# Design System: {PROJECT_NAME}

## 1. Visual Theme & Atmosphere

<!-- Overall mood, density, and design philosophy.
     Describe the visual identity in 2-3 paragraphs:
     - What feeling does the design evoke? (e.g., minimal, playful, premium, technical)
     - What makes it distinctive vs other sites in its category?
     - Core visual techniques (shadow style, border approach, color strategy)

     End with a **Key Characteristics** bullet list (6-10 items) summarizing
     the most important visual signatures an AI agent must replicate. -->

**Key Characteristics:**
- {characteristic_1}
- {characteristic_2}
- {characteristic_3}
- ...

## 2. Color Palette & Roles

<!-- Every color with: semantic name, hex value, CSS variable (if any), and functional role.
     Group into subsections by purpose. Include exact rgba/hsla values for shadows and overlays. -->

### Primary
- **{Name}** (`{#hex}`): {Where and why it is used.}

### Accent / Brand
- **{Name}** (`{#hex}`): {Functional role — when does this color appear?}

### Interactive
- **{Name}** (`{#hex}`): {Links, focus rings, hover states.}

### Neutral Scale
- **{Name}** (`{#hex}`): {Gray spectrum from darkest to lightest with roles.}

### Surface & Overlay
- **{Name}** (`{#hex}` or `{rgba/hsla}`): {Backgrounds, modals, selection highlights.}

### Shadows & Depth
- **{Name}** (`{shadow value}`): {Each shadow value used in the system with its purpose.}

## 3. Typography Rules

<!-- Full typography specification: font families, OpenType features, and a complete hierarchy table. -->

### Font Family
- **Primary**: `{font}`, fallbacks: `{fallback stack}`
- **Monospace** (if used): `{font}`, fallbacks: `{fallback stack}`
- **OpenType Features**: {e.g., "liga", "tnum" — where and why}

### Hierarchy

<!-- Complete table of every text role in the system. -->

| Role | Font | Size | Weight | Line Height | Letter Spacing | Notes |
|------|------|------|--------|-------------|----------------|-------|
| Display Hero | {font} | {px/rem} | {weight} | {value} | {value} | {usage context} |
| Section Heading | | | | | | |
| Sub-heading | | | | | | |
| Card Title | | | | | | |
| Body Large | | | | | | |
| Body | | | | | | |
| Body Small | | | | | | |
| Button / Link | | | | | | |
| Caption | | | | | | |
| Mono Body | | | | | | |
| {add rows as needed} | | | | | | |

### Principles
<!-- 3-5 bullet points on the typographic philosophy:
     weight usage rules, tracking behavior, font role separation, etc. -->

## 4. Component Stylings

<!-- Detailed specs for every reusable component. Include all states (default, hover, active, focus, disabled).
     Cover at minimum: Buttons, Cards, Inputs/Forms, Navigation, Image treatment.
     Add any distinctive/signature components unique to this design. -->

### Buttons

**Primary**
- Background: `{value}`
- Text: `{value}`
- Padding: {value}
- Radius: {value}
- Shadow/Border: {value}
- Hover: {state change}
- Focus: {focus ring spec}

**Secondary**
- ...

**{Other variants: Ghost, Pill, Icon, etc.}**
- ...

### Cards & Containers
- Background: `{value}`
- Border: {border or shadow-border technique}
- Radius: {value}
- Shadow: {full shadow stack}
- Hover: {state change}

### Inputs & Forms
- Border: {technique}
- Focus: {ring/outline spec}
- Placeholder: {color}
- Radius: {value}

### Navigation
<!-- Sticky? Position? Logo placement? Link style? CTA style? Mobile collapse? -->

### Image Treatment
<!-- Border, radius, aspect ratio, background treatment for product screenshots/images. -->

### Distinctive Components
<!-- Signature UI patterns unique to this brand (e.g., workflow pipelines, metric cards,
     trust bars, pricing tables). Describe each with full visual spec. -->

## 5. Layout Principles

### Spacing System
<!-- Base unit and full spacing scale used throughout the design. -->
- Base unit: {value}px
- Scale: {list of values}

### Grid & Container
- Max content width: {value}
- Column structure: {description}
- Section layout patterns: {hero, feature grids, full-width, etc.}

### Whitespace Philosophy
<!-- How whitespace is used as a design element — section padding, text density vs surrounding space. -->

### Border Radius Scale
<!-- Complete radius scale from smallest to largest with usage context. -->

| Size | Value | Use |
|------|-------|-----|
| Micro | {value} | {where} |
| Standard | {value} | {where} |
| Large | {value} | {where} |
| Pill | 9999px | {where} |

## 6. Depth & Elevation

<!-- Shadow/elevation system as a table from flat to highest elevation. -->

| Level | Treatment | Use |
|-------|-----------|-----|
| Flat (Level 0) | No shadow | {where} |
| Level 1 | {shadow value} | {where} |
| Level 2 | {shadow value} | {where} |
| Level 3 | {shadow value} | {where} |
| Focus | {outline/ring spec} | Keyboard focus on interactive elements |

<!-- Optional: paragraph explaining the shadow philosophy
     (e.g., shadow-as-border, Material-style elevation, glassmorphism). -->

## 7. Do's and Don'ts

<!-- Design guardrails and anti-patterns. 6-10 items per list.
     Be specific — reference exact values, not vague principles. -->

### Do
- {Specific positive rule with exact values where applicable}
- {e.g., "Use shadow-as-border (0px 0px 0px 1px rgba(0,0,0,0.08)) instead of CSS borders"}

### Don't
- {Specific anti-pattern with explanation why}
- {e.g., "Don't use weight 700 on body text — 600 is the maximum for headings only"}

## 8. Responsive Behavior

### Breakpoints

| Name | Width | Key Changes |
|------|-------|-------------|
| Mobile | {range} | {layout changes} |
| Tablet | {range} | {layout changes} |
| Desktop | {range} | {layout changes} |
| Large Desktop | {range} | {layout changes} |

### Touch Targets
<!-- Minimum sizes and padding for interactive elements on touch devices. -->

### Collapsing Strategy
<!-- How each major component adapts: navigation, grids, hero, images, footer.
     Describe the transformation, not just "it stacks". -->

### Image Behavior
<!-- How images scale, crop, or scroll across breakpoints. -->

## 9. Agent Prompt Guide

<!-- Ready-to-use reference for AI agents generating UI from this design system. -->

### Quick Color Reference
<!-- Flat list of the 6-8 most-used color assignments for fast lookup. -->
- Primary CTA: `{#hex}`
- Background: `{#hex}`
- Heading text: `{#hex}`
- Body text: `{#hex}`
- Border: `{shadow/border value}`
- Link: `{#hex}`
- Focus ring: `{value}`

### Example Component Prompts
<!-- 4-6 copy-paste-ready prompts an agent can use directly.
     Each prompt should produce one component with exact design system values.
     Cover: hero section, card, badge/pill, navigation, one distinctive component. -->

- "Create a hero section: {full spec with exact values from sections above}."
- "Design a card: {full spec}."
- "Build a badge/pill: {full spec}."
- "Create navigation: {full spec}."
- "Design a {distinctive component}: {full spec}."

### Iteration Guide
<!-- 4-6 numbered rules for the agent to follow when iterating on generated UI.
     These are the "if in doubt, do this" rules. -->
1. {Most important rule}
2. {Second rule}
3. ...
