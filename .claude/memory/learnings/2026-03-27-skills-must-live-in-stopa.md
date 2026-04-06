---
date: 2026-03-27
type: architecture
severity: high
component: skill
tags: [source-of-truth, distribution, anti-pattern]
summary: "Skills must be developed in STOPA first, then distributed. Never create skills directly in target projects."
source: auto_pattern
verify_check: "Glob('.claude/skills/*/SKILL.md') → 1+ matches"
confidence: 0.7
uses: 0
successful_uses: 0
harmful_uses: 0
---

# Skills MUST be developed in STOPA first, then distributed

## Problem
7 skills (autoloop, budget, watch, harness, tdd, systematic-debugging, browse) were either:
- Developed in target projects (ADOBE-AUTOMAT, NG-ROBOT) instead of STOPA
- Only existed as runtime session improvements, never persisted to SKILL.md
- Referenced in skill-tiers.md but didn't exist anywhere

This caused:
- STOPA (source of truth) was missing its own core capabilities
- Session-level improvements to /watch (Tier 2b papers mode) were lost between sessions
- Budget tracking was unavailable in STOPA context
- No centralized place to evolve methodology skills (tdd, debugging)

## Root Cause
Skills were created ad-hoc where they were first needed (target projects), not where they should canonically live (STOPA). The sync script only goes STOPA → targets, so target-originated skills never flowed back.

## Fix Applied
1. Copied autoloop, budget, watch from ADOBE-AUTOMAT → STOPA
2. Created harness, tdd, systematic-debugging, browse fresh in STOPA
3. Added Tier 2b papers mode to /watch (was lost in session memory)
4. STOPA now has 25 skills (was 18)

## Rule
**Always create/edit skills in STOPA first.** Target projects receive skills via sync/plugin distribution. Never develop a skill "in the field" without backporting to STOPA in the same session.
