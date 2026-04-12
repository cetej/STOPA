---
date: 2026-04-12
type: architecture
severity: high
component: skill
tags: [deterministic, latent-space, skill-design, optimization, scripts]
summary: "Audit 10 skills identifikoval 91 kroků kde model dělá deterministickou práci (aritmetika, thresholds, set operace, YAML parsing). 65 z nich (71%) je easy k extrakci do Pythonu. Implementovány 3 skripty: deterministic-gates.py (orchestrate), loop-state.py (autoloop/self-evolve), scribe-maintenance.py (scribe) — celkem 24 subcommands."
source: auto_pattern
uses: 0
successful_uses: 0
harmful_uses: 0
confidence: 0.8
impact_score: 0.0
skill_scope: [orchestrate, autoloop, self-evolve, scribe]
verify_check: "Glob('scripts/deterministic-gates.py') → 1+ matches"
related: [2026-04-12-latent-deterministic-boundary.md, 2026-04-12-purpose-built-tools-75x-faster.md]
---

## Detail

Audit top 10 skills (orchestrate, critic, evolve, scribe, checkpoint, autoloop, self-evolve, deepresearch, scout, sweep) identifikoval 5 kategorií deterministické práce:

1. **Aritmetika a vzorce** (28 instancí): weighted averages, confidence decay, UCB1, budget alokace
2. **Counting/Filtering/Thresholds** (24 instancí): řádky v TSV, failures v JSONL, porovnání s prahem
3. **YAML/JSON/JSONL parsing** (18 instancí): frontmatter čtení, counter inkrement, FIFO trim
4. **Set operace a dedup** (12 instancí): file list disjointness, regression detection, tag overlap
5. **Template rendering** (9 instancí): TSV rows, JSON soubory, checkpoint markdown

Implementační vzor: `Skill instrukce → python scripts/X.py subcommand --args → stdout JSON → model čte JSON a pokračuje latentním krokem`.

Zbývá: aktualizace skill bodies aby odkazovaly na skripty místo inline instrukcí.
