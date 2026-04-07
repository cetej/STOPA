---
date: 2026-04-07
type: best_practice
severity: medium
component: skill
tags: [compact-variant, measurement, tokens, optimization]
summary: "Compact variants deliver 87-94% word reduction (measured across 6 skills). Claim of ~80% is conservative — actual savings are higher."
source: auto_pattern
uses: 1
harmful_uses: 0
successful_uses: 0
confidence: 0.90
supersedes: 2026-04-04-gap-compact-variant-measurement.md
verify_check: "Glob('.claude/skills/*/SKILL.compact.md') → 1+ matches"
---

## Compact Variant Measurement Baseline

### Measured Results (2026-04-07)

| Skill | Full (words/lines) | Compact (words/lines) | Reduction |
|-------|-------------------|----------------------|-----------|
| orchestrate | 5600w / 753L | 323w / 60L | **94%** |
| critic | 4540w / 518L | 293w / 57L | **93%** |
| autoresearch | 3633w / 547L | 288w / 55L | **92%** |
| autoloop | 2932w / 497L | 305w / 57L | **89%** |
| liveprompt | 2944w / 420L | 274w / 53L | **90%** |
| clean-writing | 1961w / 250L | 247w / 40L | **87%** |

**Average reduction: 91%** (word count as token proxy)

### Key Observations

1. Compact variants are remarkably consistent — all land between 247-323 words (~55 lines)
2. Larger skills benefit more (orchestrate 94% vs clean-writing 87%)
3. The ~80% claim in skill-files.md is conservative — actual is 87-94%
4. Word count correlates with token count at roughly 1.3 tokens/word for English markdown

### What Compact Variants Preserve

- Core purpose and role (1-2 sentences)
- Decision points and critical rules (condensed tables)
- Circuit breakers and anti-patterns (abbreviated)
- Output format expectations

### What Gets Cut

- Full phase descriptions and step-by-step workflows
- Detailed examples and reference file reads
- Extended tables, scoring rubrics, templates
- Anti-Rationalization Defense section (covered in first invocation)

### Recommendation

Current compact variants are well-calibrated. No changes needed. Consider creating compact variants for remaining high-use Tier 1 skills (scout, checkpoint, scribe) where full versions exceed 2000 words.
