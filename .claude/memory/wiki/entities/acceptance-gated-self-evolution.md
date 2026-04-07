---
name: Acceptance-Gated Self-Evolution
type: concept
first_seen: 2026-04-07
last_updated: 2026-04-07
sources: [nlah-implementation-plan]
tags: [orchestration, code-quality, self-improvement]
---

# Acceptance-Gated Self-Evolution

> Paradigma iterativního zlepšování artefaktů s přísným accept/revert filtrem — ne víc pokusů, ale přísnější kritéria přijetí. Klíčový modul NLAH systému (+4.8% SWE-bench).

## Key Facts

- Nejsilnější jednotlivý modul v NLAH: +4.8% na SWE-bench Verified (ref: sources/nlah-implementation-plan.md)
- Princip: "disciplined acceptance-gated attempts rather than expanding search trees" — filtr přísnosti, ne search šíře (ref: sources/nlah-implementation-plan.md)
- STOPA `/self-evolve` již implementuje: Curriculum Critic Gate (≥3/5), Critic Gate každé 2 kola, Keep/Revert po každém editu, 3 consecutive reverts → STOP (ref: sources/nlah-implementation-plan.md)
- Mezera: STOPA aplikuje pattern jen na skills — NLAH naznačuje aplikaci na libovolný artefakt (hook, config, pipeline) (ref: sources/nlah-implementation-plan.md)
- Navržený generalizovaný hook `acceptance-gate.py` (PostToolUse na Write/Edit): detekuje typ artefaktu → spustí odpovídající validaci → FAIL → auto-revert + log (ref: sources/nlah-implementation-plan.md)

## Relevance to STOPA

P2 priorita (4h effort). Rozšíří self-evolution disciplínu z SKILL.md na celý systém. Validates current /self-evolve design — gap je pouze v rozsahu aplikace.

## Mentioned In

- [NLAH Implementation Plan](../sources/nlah-implementation-plan.md)
