---
date: 2026-04-09
type: architecture
severity: high
component: memory
tags: [aggregation, graduation, feedback-loop, bias, local-vs-global, skill-scope]
summary: "Globální agregátor (critical-patterns.md) nutně zhorší ≥1 dimenzi znalostí vs lokální skill-specifické agregátory (Acemoglu Theorem 3). Implementováno: skill_scope field pro lokální graduation, circular validation detection, inverse frequency graduation threshold."
source: external_research
uses: 1
harmful_uses: 0
successful_uses: 0
confidence: 0.8
verify_check: "Grep('skill_scope', path='.claude/rules/memory-files.md') → 1+ matches"
related: [2026-03-30-write-time-gating-salience.md]
---

## Pattern

Acemoglu et al. (arXiv:2604.04906, MIT, April 2026) formalizují endogenní feedback loop v AI agregaci:

1. **Theorem 3**: Jeden globální agregátor nutně zhorší učení alespoň v jedné dimenzi — lokální specializované agregátory zachovávají znalosti lépe
2. **Proposition 2**: Overrepresentace majority (často volaných skills) zesiluje bias — minority insights jsou potlačeny
3. **Theorem 2**: Rychlost updatů je kritická — pomalé updaty (vysoké ρ) umožňují nezávislému signálu se akumulovat

## Implementace v STOPA

Tři intervence adresující tři problémy:

- **Circular validation detection** v `learning-admission.py`: porovnává nový learning s titulky critical-patterns — flag `[circular-risk]` pokud >60% title keywords overlapuje
- **`skill_scope:`** nové YAML pole: learnings se scope graduují do `.claude/skills/<name>/learned-rules.md` místo globálního critical-patterns.md
- **Inverse frequency graduation**: `max(3, round(10 * (1 - 0.5 * frequency_factor)))` — rare-skill learnings potřebují méně uses pro graduation
