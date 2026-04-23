---
date: 2026-04-23
type: anti_pattern
severity: critical
component: skill
tags: [autoresearch, deepresearch, critic, falsification, evidence, bias]
summary: "LLM scientific agents ignore evidence in 68% of traces, revise beliefs only 26%, use independent evidence lines only 7% (25K runs, 8 domains). Counter-example prompting boosts rule discovery 42→56%. STOPA /autoresearch + /critic need explicit falsification gate."
source: external_research
uses: 0
harmful_uses: 0
successful_uses: 0
confidence: 0.85
maturity: draft
skill_scope: [autoresearch, deepresearch, critic, self-evolve]
verify_check: "manual"
related: []
---

## Context

Empirical study (identified via semantic search, ~25 000 agent runs napříč 8 doménami, 11 LLMs) zjistila, že LLM-based scientific agents:
- **68% tras ignoruje evidence** (executes workflows ✓, scientific reasoning ✗)
- **26% refutation-driven belief revision** (zbytek confirmatory)
- **7% independent evidence lines** (rare convergent multi-test evidence)
- Base model = **41.4% variance**, scaffold = **1.5% variance** → model > framework efekt
- **Counter-example prompting: 42% → 56%** rule discovery improvement

## Implication for STOPA

3 skills mají přímý expozici:
- `/autoresearch` (hypothesis-driven iteration) — může akumulovat confirmatory bias, nenutí falsifikaci
- `/deepresearch` (evidence synthesis) — risk zapamatování první pozitivní evidence
- `/critic` (should falsify, not confirm) — momentálně "review" bez explicit "refute" prompt
- `/self-evolve` — iterativní skill úpravy bez falsification gate mohou driftovat k broadly misaligned patterns (viz learning 2026-04-23-emergent-misalignment.md pokud existuje)

## Action

Edit `.claude/skills/autoresearch/SKILL.md`:
1. Přidat mandatory **Phase 2.5: Falsification Step** PŘED každou další iterací
2. Explicit zápis v trace: *"What evidence would refute current hypothesis?"* + *"Did I seek it?"*
3. Pokud agent skipne → `/critic` FAIL, ne graduate
4. Counter-example prompting jako support pattern (42→56%) v ρ Reflect phase

Sekundární: přidat do `/critic` SKILL.md instrukci *"Prefer refutation over confirmation"*.

## Rationale

Empirie 25K runs + cross-domain consistency = vysoká confidence. Counter-example prompting má concrete mechanism (paper-backed 14pp improvement). Falsification gate je levné opatření s vysokým expected value pro `/autoresearch` quality.
